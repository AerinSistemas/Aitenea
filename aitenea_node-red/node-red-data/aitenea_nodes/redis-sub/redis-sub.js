module.exports = function (RED) {
  "use strict";
  const Redis = require("ioredis");
  let connections = {};
  let usedConn = {};

  function RedisConf(n) {
    RED.nodes.createNode(this, n);

    this.name = n.name;
    this.cluster = n.cluster;
    
    if (this.optionsType === "") {
      this.options = n.options;
    } else {
      this.options = RED.util.evaluateNodeProperty(
        n.options,
        n.optionsType,
        this
      );
    }
  }
  RED.nodes.registerType("redis-conf", RedisConf);

  function RedisSub(n) {
    RED.nodes.createNode(this, n);

    this.server = RED.nodes.getNode(n.server);
    this.name = n.name;
    this.topic = "";
    this.obj = n.obj;
    this.timeout = n.timeout;
    let node = this;
    let client = getConn(this.server, n.id);

    node.on("close", async (undeploy, done) => {
      node.status({});
      disconnect(node.id);
      client = null;
      done();
    });

    node.on('input', function (msg) {
      this.topic = msg.payload["redis_topic"];

      client['subscribe'](node.topic, (err, count) => {
        node.status({
          fill: "green",
          shape: "ring",
          text: "connected",
        });
      });
    });

    client.on("message", function (channel, message) {
      let payload = null;
      try {
        if (node.obj) {
          payload = JSON.parse(message);

          // Pline running
          if (!payload.completed && !payload.error) {
            node.status({
              fill: "yellow",
              shape: "dot",
              text: "running",
            });
          }

          // Pline completed
          if (payload.completed && !payload.error) {
            node.status({
              fill: "green",
              shape: "dot",
              text: "completed",
            });
          }

          // Pline error
          if (!payload.completed && payload.error) {
            node.status({
              fill: "red",
              shape: "dot",
              text: "error",
            });
          }

        } else {
          payload = message;
        }
      } catch (err) {
        payload = message;
      } finally {
        node.send({
          topic: channel,
          payload: payload,
        });
      }
    });
  }

  RED.nodes.registerType("redis-sub", RedisSub);

  function getConn(config, id) {
    if (connections[id]) {
      usedConn[id]++;
      return connections[id];
    }

    let options = config.options;

    if (!options) {
      return config.error(
        "Missing options in the redis config - Are you upgrading from old version?",
        null
      );
    }
    try {
      if (config.cluster) {
        connections[id] = new Redis.Cluster(options);
      } else {
        connections[id] = new Redis(options);
      }

      connections[id].on("error", (e) => {
        config.error(e, null);
      });

      if (usedConn[id] === undefined) {
        usedConn[id] = 1;
      }
      return connections[id];
    } catch (e) {
      config.error(e.message, null);
    }
  }

  function disconnect(id) {
    if (usedConn[id] !== undefined) {
      usedConn[id]--;
    }
    if (connections[id] && usedConn[id] <= 0) {
      connections[id].disconnect();
      delete connections[id];
    }
  }
};