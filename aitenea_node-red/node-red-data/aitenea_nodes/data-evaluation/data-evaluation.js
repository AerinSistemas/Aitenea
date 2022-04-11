module.exports = function (RED) {
  function DataEvaluation(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    this.timeout = config.timeout;
    node.status({fill:"", shape:"", text:""});
    node.on('input', function(msg) {
      evaluate(msg, node);
  });


  }
  
  RED.nodes.registerType("Data-evaluation", DataEvaluation);

  function evaluate(msg, node) {
    const request = require("request");
    let URL = process.env.AITENEA_URL_BACKEND + `/api/data_evaluation/`;
    const origin_type = msg.payload.origin.type;
    const options = msg.payload.origin.options;
    const data = {
      origin_type: origin_type,
      options: options
    };
    let opts = {
      method: 'POST',
      url: URL,
      timeout: Number(node.timeout),
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data),
    };
    request.post(opts, function (error, response, body) {
      if (error != null) {
        console.error('error:', error); // Print the error if one occurred
        node.status({fill:"red", shape:"ring", text:"Timeout"})
        msg.payload["evaluation"] = error;
        node.send(msg);
        return null;
      }
      else {
        body = JSON.parse(body);
        if (body["error"] != undefined)
        {
          let msg_error = "Error, probably wrong syntax in search. " + body["error"]
          console.error('error:', msg_error); 
          msg.payload["evaluation"] = msg_error;
          node.send(msg);
          return null;
        }
        if (body["evaluation"]["data describe X"] == undefined)
        {
          body["evaluation"]["data describe X"] = null;
        }
        else
        {
          body["evaluation"]["data describe X"] = JSON.parse(body["evaluation"]["data describe X"]);
        }
        if (body["evaluation"]["data describe y"] == undefined)
        {
          body["evaluation"]["data describe y"] = null;
        }
        else
        {
          body["evaluation"]["data describe y"] = JSON.parse(body["evaluation"]["data describe y"]);
        }
        if (body["evaluation"]["correlation"] == undefined)
        {
          body["evaluation"]["correlation"] = null;
        }
        else
        {
          body["evaluation"]["correlation"] = JSON.parse(body["evaluation"]["correlation"]);
        }
        msg.payload["evaluation"] = body["evaluation"];
        node.status({fill:"green",shape:"ring",text:"done"});
        node.send(msg);
      }
    });

    
    }
}
