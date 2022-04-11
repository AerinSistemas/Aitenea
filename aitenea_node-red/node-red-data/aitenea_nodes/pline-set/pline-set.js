module.exports = function (transformation) {
  function transformationNode(config) {
    transformation.nodes.createNode(this, config);
    
    this.auth = transformation.nodes.getNode(config.auth);
    this.plineName = config.plineName;
    this.plineDescription = config.plineDescription;
    this.overwrite = config.overwrite;
    this.exists = config.exists;
    this.owner = config.owner;

    let node = this;

    node.on("input", function (msg) {

      if (this.exists == true && this.overwrite == false){
        node.error("El pline existe, por favor seleccione sobreescribir en el nodo de destino");
        return false;
      }
      let update_index = false;
      if (this.overwrite == true){
        update_index = true;
      }

      const source = {
        name: this.plineName,
        description: this.plineDescription,
        owner: this.owner,
        steps: [],
        update_index: update_index
      }
      if (!(typeof msg.payload === 'object')){
        msg.payload = {}
      }
      msg.payload.pline = {};
      msg.payload.pline = source;

      node.send(msg);
    });
  }

  transformation.nodes.registerType("Pline-set", transformationNode);
};