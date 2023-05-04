module.exports = function (TDATA) {
  function tDataSettingNode(config) {
    TDATA.nodes.createNode(this, config);

    this.server = TDATA.nodes.getNode(config.server);
    this.nodeName = config.nodeName;
    this.index = config.index;
    this.xAttr = config.xAttr;
    this.yAttr = config.yAttr;
    this.query = config.query;

    let node = this;

    node.on("input", function (msg) {
      const source = {
        type: "elastic",
        options: {
          connection: {
            host: this.server.host,
            port: this.server.port,
            user: this.server.user,
            password: this.server.password
          },
          index: this.index,
          q: {
            _source: this.xAttr.concat(this.yAttr),
            query: this.query,
          },
          X: this.xAttr,
          y: this.yAttr,
        },
      }

      msg.payload = {};
      msg.payload.origin = source;
      node.send(msg);
    });
  }
  TDATA.nodes.registerType("From-Elasticsearch", tDataSettingNode);

  TDATA.httpAdmin.get("/getAiteneaUrl", TDATA.auth.needsPermission('tDataSettingNode.read'), function (req, res) {
    res.json(process.env.AITENEA_URL);
  });
};