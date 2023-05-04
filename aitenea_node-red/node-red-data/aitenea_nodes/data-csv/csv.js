module.exports = function (TDATA) {
  function tDataSettingNode(config) {
    TDATA.nodes.createNode(this, config);

    this.auth = TDATA.nodes.getNode(config.auth);
    this.fileName = config.fileName;
    this.index = config.index;
    this.xAttr = config.xAttr;
    this.yAttr = config.yAttr;

    let node = this;

    node.on("input", function (msg) {
      const source = {
        type: "csv",
        options: {
          index: this.index,
          X: this.xAttr,
          y: this.yAttr,
        },
      }

      msg.payload = {};
      msg.payload.origin = source;
      node.send(msg);
    });
  }
  TDATA.nodes.registerType("From-CSV", tDataSettingNode);

  TDATA.httpAdmin.post("/inject/:id", TDATA.auth.needsPermission("inject.write"), function (req, res) {
    let node_origin = TDATA.nodes.getNode(req.params.id);
  });

  TDATA.httpAdmin.get("/getAiteneaUrl", TDATA.auth.needsPermission('tDataSettingNode.read'), function (req, res) {
    res.json(process.env.AITENEA_URL);
  });
};