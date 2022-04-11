module.exports = function (RED) {
  function ManualData(config) {
    RED.nodes.createNode(this, config);
    let node = this;
    this.data = config.data;

    node.on('input', function () {
      let data = {
        "origin": {"type": "manual data", "options": JSON.parse(this.data)},
      };
      let msg =  {"payload": data};
      node.send(msg);
    });

  }
  RED.nodes.registerType("Manual-data", ManualData);

  RED.httpAdmin.post("/inject/:id", RED.auth.needsPermission("inject.write"), function (req, res) {
    let node_origin = RED.nodes.getNode(req.params.id);
  });
}