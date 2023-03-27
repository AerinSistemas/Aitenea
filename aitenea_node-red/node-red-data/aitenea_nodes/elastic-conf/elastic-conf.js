module.exports = function (RED) {
  "use strict";

  function ElasticConf(n) {
    RED.nodes.createNode(this, n);
    
    this.name = n.name;
    this.host = n.host;
    this.port = n.port;
    this.user = n.user;
    this.password = n.password;
  }
  RED.nodes.registerType("elastic-conf", ElasticConf);
};