module.exports = function (transformation) {
  function transformationNode(config) {
    const crypto = require("crypto");
    transformation.nodes.createNode(this, config);
    this.server = transformation.nodes.getNode(config.server);

    this.classType = config.classType;
    this.className = config.className;
    this.moduleName = config.moduleName;
    this.optionsvals = config.optionsvals;
    this.geneticparametersvals = config.geneticparametersvals;

    const test = {
      "name": "",
      "description": "description",
      //"owner": 1,
      "steps": [
      ]
    }

    let node = this;
    
    node.on("input", function (msg) {
      msg.payload["redis_topic"] = "pline_run_" + crypto.randomBytes(8).toString('hex');
      let source = msg.payload
      if (!source.hasOwnProperty('pline')) {
        source = test
        source.name = msg.topic
        source.steps = []
        msg.payload.pline = {};

      } else {
        source = msg.payload.pline
      }

      if (source.steps != undefined) {
        const step = {
          step_number: source.steps.length + 1,
          step_type: this.classType,
          step_name: this.className,
          module_name: this.moduleName.replace(/["']/g, ""),
          step_options: JSON.parse(this.optionsvals),
          step_genetic_parameters: JSON.parse(this.geneticparametersvals)
        }
        source.steps.push(step)
        msg.payload.pline = source
        node.send(msg);
      }
      else {
        let error_msg = "Model-get and Pline-step nodes can't be used in the same workflow.";
        node.error("Error: " + error_msg, msg);
      }

    });
  }

  transformation.nodes.registerType("Pline-step", transformationNode);

};