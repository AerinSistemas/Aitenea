module.exports = function (transformation) {
  function transformationNode(config) {
    const crypto = require("crypto");
    transformation.nodes.createNode(this, config);

    this.auth = transformation.nodes.getNode(config.auth);
    this.plineId = config.plineId;

    let node = this;
    
    node.on("input", function (msg) {
      msg.payload["redis_topic"] = "pline_run_" + crypto.randomBytes(8).toString('hex');
      const source = {
        id: parseInt(this.plineId),
      }
      if (!(typeof msg.payload === 'object')){
        msg.payload = {}
      }

      if (msg.payload.pline == undefined) {
        msg.payload.pline = {};
        msg.payload.pline = source;
  
        node.send(msg);
      }
      else {
        let error_msg = "Model-get and Pline-step nodes can't be used in the same workflow.";
        node.error("Error: " + error_msg, msg);
      }
    });
  }

  transformation.nodes.registerType("Model-get", transformationNode);

};