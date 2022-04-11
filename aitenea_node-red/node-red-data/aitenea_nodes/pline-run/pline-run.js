module.exports = function (TDATA) {
  function PlineRun(config) {
    TDATA.nodes.createNode(this, config);

    this.auth = TDATA.nodes.getNode(config.auth);
    this.run_type = config.runselect;
    //this.output = config.output;
    this.trainSize = config.trainSize;
    this.runAsGA = config.runAsGA;
    this.generations = config.generations;
    this.population = config.population;
    this.timeout = config.timeout;

    let node = this;
    let URL = "";
    node.status({fill:"",shape:"",text:""});
    if (this.runAsGA) {
      URL = process.env.AITENEA_URL_BACKEND + `/api/pline/genetic/`;
    }
    else { URL = process.env.AITENEA_URL_BACKEND + `/api/pline/${this.run_type}/`; }

    node.on('input', function (msg) {
      msg.payload["run_type"] = this.run_type;
      //msg.payload["output"] = this.output;
      msg.payload["origin"]["options"]["run_as_ga"] = this.runAsGA;

      if (this.run_type.includes("fit")) {
        msg.payload["origin"]["options"]["train_size"] = parseInt(this.trainSize) / Math.pow(10, 2);
      }
      if (this.runAsGA) {
        msg.payload["origin"]["options"]["generations"] = Math.floor(this.generations);
        msg.payload["origin"]["options"]["population"] = Math.floor(this.population);
      }

      const isWorkflowValid = validateWorkflow(msg, node);
      executePline(msg, node, isWorkflowValid, this.auth, URL);

    });
  }
  TDATA.nodes.registerType("Pline-run", PlineRun);

  function validateWorkflow(msg, node) {
    let isWorkflowValid = true;
    let error_msg = "";
    try {
      const run_type = msg.payload.run_type;
      const steps = msg.payload.pline.steps;

      if (steps != undefined) {
        if (steps.length > 0) {
          let ai_count = 0;
          let ai_found = false;
          for (let step of steps) {
            if (step.step_type.includes("_ai")) {
              ai_found = true;
              ai_count++;
            }
            // Error AI class antes de TRANSFORM class
            if (step.step_type.includes("_transform") && ai_found) {
              isWorkflowValid = false;
              error_msg = "You can't use a Pline-step TRANSFORM class after a Pline-step AI class.";
              node.error("Error: " + error_msg, msg);
            }
          }

          // Error multiple AI classes
          if (ai_count > 1) {
            isWorkflowValid = false;
            error_msg = "You can't use more than 1 Pline-step AI class in the same workflow.";
            node.error("Error: " + error_msg, msg);
          }

          // Error AI class
          if (steps[steps.length - 1].step_type.includes("_ai") && run_type != "fit" && run_type != "fit_predict") {
            isWorkflowValid = false;
            error_msg = "You can only use 'fit' or 'fit_predict' run types if the workflow ends with a Pline-step AI class.";
            node.error("Error: " + error_msg, msg);
          }

          // Error TRANSFORM class
          if (steps[steps.length - 1].step_type.includes("_transform") && run_type != "fit" && run_type != "fit_transform") {
            isWorkflowValid = false;
            error_msg = "You can only use 'fit' or 'fit_transform' run types if the workflow ends with a Pline-step TRANSFORM class.";
            node.error("Error: " + error_msg, msg);
          }
        }
      }

      // Error model-get solo predict permitido
      if (msg.payload.pline.id != undefined) {
        if (run_type != "predict") {
          isWorkflowValid = false;
          error_msg = "You can only use 'predict' run type if the workflow contains a Model-get node.";
          node.error("Error: " + error_msg, msg);
        }
      }
    }
    catch (error) {
      isWorkflowValid = false;
      console.log(error);
    }

    return isWorkflowValid;
  }

  function login(username, password) {
    const request = require("request");

    let AUTH_TOKEN = "";

    let URL = process.env.AITENEA_URL_BACKEND + "/api/auth/login/";
    const data = {
      username: username,
      password: password,
    };

    let opts = {
      method: 'POST',
      url: URL,
      timeout: 5000,
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data),
    };
    return new Promise(function (resolve, reject) {
      request.post(opts, function (error, response, body) {
        if (error != null) {
          console.error('error:', error); // Print the error if one occurred
          return reject('Error in authentication.');
        }
        else {
          let body_json = JSON.parse(body)
          AUTH_TOKEN = body_json["token"];
          return resolve(AUTH_TOKEN);
        }
      });
    });
  }

  async function executePline(msg, node, isWorkflowValid, auth, URL, RED) {
    const request = require("request");

    let AUTH_TOKEN = "";
    try {
      AUTH_TOKEN = await login(auth.user, auth.password);
    } catch (e) {
      console.log(e);
    }

    if (isWorkflowValid && AUTH_TOKEN != "") {
      let opts = {
        method: 'POST',
        url: URL,
        timeout: parseInt(node.timeout),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${AUTH_TOKEN}`
        },
        body: JSON.stringify(msg.payload),
      };
      request.post(opts, function (error, response, body) {
        if (error != null) {
          if (error == 'Error: ESOCKETTIMEDOUT'){
            let error_timeout = "Timeout error. Execution time is too long, increase the timeout in pline-run";
            error_timeout += ". Actual value " + node.timeout + " ms"
            node.status({fill:"red",shape:"ring",text:"Timeout"});
            node.error(error_timeout);
            msg.payload["error"] = error_timeout;
          }
        }
        else{
        body = JSON.parse(body);
        try{
          let body_out = JSON.parse(body.out);
          body.out = body_out;
        } catch (err)
        {
          body["out"] = null;
        }
        msg.payload["result"] = body;
        node.status({fill:"green",shape:"ring",text:"done"});
      }
        node.send(msg);
      });
    }
    else {
      if (AUTH_TOKEN == "") {
        let error_msg = "Login credentials not valid."
        node.error("Error: " + error_msg);
      }
    }
  }

}

