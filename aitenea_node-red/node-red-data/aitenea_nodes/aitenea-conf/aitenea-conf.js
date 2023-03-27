module.exports = function (RED) {
  "use strict";

  function AITeneaConf(n) {
    RED.nodes.createNode(this, n);
    this.user = n.user;
    this.password = n.password;
  }
  RED.nodes.registerType("aitenea-conf", AITeneaConf);
};