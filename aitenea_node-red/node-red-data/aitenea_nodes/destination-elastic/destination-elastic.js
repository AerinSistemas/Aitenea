module.exports = function(RED) {
  function destinationElastic(config) {
    const crypto = require("crypto");
    RED.nodes.createNode(this, config);

    this.server = RED.nodes.getNode(config.server);
    this.indexName = config.indexName;
    this.overwrite = config.overwrite;
    this.exists = config.exists;
    //this.useOrigin = config.useOrigin;

    let node = this;

    node.on("input", function(msg) {
      msg.payload["redis_topic"] = "pline_run_" + crypto.randomBytes(8).toString('hex');
      if (this.exists == true && this.overwrite == false){
        node.error("El índice existe, por favor seleccione sobreescribir en el nodo de destino");
        return false;
      }
      let update_index = false;
      if (this.overwrite == true){
        update_index = true;
      }
      let source = {
        type: "elastic",
        options: {
          connection:{
            host: this.server.host,
            port: this.server.port,
            user: this.server.user,
            password: this.server.password
          },
          update_index: update_index,
          index: this.indexName.toLowerCase()
        }
      }

      if (!(typeof msg.payload === 'object')){
        msg.payload = {};
      }

      msg.payload.target = source;
      node.send(msg);
    });
  }

  RED.nodes.registerType("Destination-Elastic", destinationElastic);
};
