module.exports = function(RED) {
  function toCSV(config) {
    const crypto = require("crypto");
    RED.nodes.createNode(this, config);

    this.indexName = config.indexName;
    this.separator = config.separator;
    this.singleOutputFile = config.singleOutputFile;
    //this.overwrite = config.overwrite;
    this.exists = config.exists;

    let node = this;

    node.on("input", function(msg) {
      
      let source = {
        type: "CSV",
        options: {
          index: this.indexName.toLowerCase(),
          separator: this.separator,
          singleOutputFile: this.singleOutputFile
        }
      }
      if (!(typeof msg.payload === 'object')){
        msg.payload = {};
      }

      msg.payload.target = source;
      node.send(msg);
     
    });
  }
  RED.nodes.registerType("To-CSV", toCSV);

};



