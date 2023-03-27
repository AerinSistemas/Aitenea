module.exports = function (RED) {
    "use strict";
  
    function SQLConf(n) {
      RED.nodes.createNode(this, n);
      
      this.name = n.name;
      this.host = n.host;
      this.database = n.database;
      this.port = n.port;
      this.user = n.user;
      this.password = n.password;
    }
    RED.nodes.registerType("sqldb-conf", SQLConf);
  };