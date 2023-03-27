module.exports = function(SQLDATA){
    function SQLDBSettings(config){
        SQLDATA.nodes.createNode(this, config);
        this.dbmanager = config.dbmanager;
        this.server = SQLDATA.nodes.getNode(config.server);
        this.index = config.index;
        this.xAttr = config.xAttr;
        this.yAttr = config.yAttr;
        this.query = config.query;
        this.advanced = config.advanced;
        this.search = config.search;
        var node = this;

        node.on("input", function(msg){
            node.status({fill:"yellow", shape:"ring", text:"In execution"})
            const source = {
                type: "sql",
                options: {
                    connection: {
                        dbmanager: this.dbmanager,
                        host: this.server.host,
                        port: this.server.port,
                        database: this.server.database,
                        user: this.server.user,
                        password: this.server.password
                    },
                    index: this.index,
                    q: {
                        _source: this.xAttr.concat(this.yAttr),
                        advanced: this.advanced,
                        query: this.query,
                        search: this.search,
                    },
                    X: this.xAttr,
                    y: this.yAttr,
                }
            }
            msg.payload = {}
            msg.payload.origin = source;
            if (msg.payload['origin']['options']['q']['advanced']=="yes" &&
            msg.payload['origin']['options']['q']['query']==""){
             node.status({fill:"red", shape:"ring", text:"Query has not been defined"})
             var msg1 = { payload:"There is no available data to use. Please, define a query" };
             node.send(msg1)
            }else{                
                node.status({fill:"green", shape:"ring", text:"Done"})
                node.send(msg);
            }            
        });
    }
    SQLDATA.nodes.registerType("From-SQL", SQLDBSettings);
    SQLDATA.httpAdmin.get("/getAiteneaUrl", SQLDATA.auth.needsPermission('SQLDBSettings.read'), function (req, res) {
        res.json(process.env.AITENEA_URL);
    });
};