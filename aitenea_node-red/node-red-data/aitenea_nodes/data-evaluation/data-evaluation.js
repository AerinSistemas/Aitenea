module.exports = function (RED) {
  function DataEvaluation(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    this.timeout = config.timeout;
    node.status({fill:"", shape:"", text:""});
    node.on('input', function(msg) {
      if (msg.payload['origin'] == undefined){
        node.status({fill:"red", shape:"ring", text:"No data tu use"})
        var msg1 = { payload:"There is no available data to use. Please, upload data with the nodes such as 'From-CSV', 'From-ElasticSearch', 'From-SQL', or 'Manual-data'" };
        node.send(msg1)
      }else {
        node.status({fill:"yellow", shape:"ring", text:"In execution"})
        evaluate(msg, node);
      }      
  });


  }
  
  RED.nodes.registerType("Data-evaluation", DataEvaluation);

  function evaluate(msg, node) {
    const request = require("request");
    let URL = process.env.AITENEA_URL_BACKEND + `/api/data_evaluation/`;
    const origin_type = msg.payload.origin.type;
    const options = msg.payload.origin.options;
    const data = {
      origin_type: origin_type,
      options: options
    };
    let opts = {
      method: 'POST',
      url: URL,
      timeout: Number(node.timeout),
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data),
    };
    request.post(opts, function (error, response, body) {
      if (error != null) {
        console.error('error:', error); // Print the error if one occurred
        node.status({fill:"red", shape:"ring", text:"Timeout"})
        msg.payload["evaluation"] = error;
        node.send(msg);
        return null;
      }
      else {
        body = JSON.parse(body);
        if (body["error"] != undefined)
        {
          check_error = body['error'].startsWith('The table')
          console.log(check_error)
          if (check_error){
            let msg_error = body["error"]
            node.status({fill:"red", shape:"ring", text:"Table not accesible"})
            msg.payload["evaluation"] = msg_error;
          }else if(body['error'].startsWith('Problem')){
            let msg_error = body["error"]
            node.status({fill:"red", shape:"ring", text:"Error in Query"})
            msg.payload["evaluation"] = msg_error;
          }else{
            let msg_error = "Error, probably wrong syntax in search. " + body["error"]
            console.error('error:', msg_error); 
            node.status({fill:"red", shape:"ring", text:"Keyerror"})
            msg.payload["evaluation"] = msg_error;
          }
          
          node.send(msg);
          return null;
        }
        if (body["evaluation"]['Header of values of x'] == undefined)
        {
          body["evaluation"]['Header of values of x'] = null;
        }
        else
        {
          body["evaluation"]['Header of values of x'] = JSON.parse(body["evaluation"]['Header of values of x']);
        }
        if (body["evaluation"]['Header of values of y'] == undefined)
        {
          body["evaluation"]['Header of values of y'] = null;
        }
        else
        {
          body["evaluation"]['Header of values of y'] = JSON.parse(body["evaluation"]['Header of values of y']);
        }
        if (body["evaluation"]["data describe X"] == undefined)
        {
          body["evaluation"]["data describe X"] = null;
        }
        else
        {
          body["evaluation"]["data describe X"] = JSON.parse(body["evaluation"]["data describe X"]);
        }
        if (body["evaluation"]["data describe y"] == undefined)
        {
          body["evaluation"]["data describe y"] = null;
        }
        else
        {
          body["evaluation"]["data describe y"] = JSON.parse(body["evaluation"]["data describe y"]);
        }
        if (body["evaluation"]["correlation"] == undefined)
        {
          body["evaluation"]["correlation"] = null;
        }
        else
        {
          body["evaluation"]["correlation"] = JSON.parse(body["evaluation"]["correlation"]);
        }
        if (body["evaluation"]['NaN Values of x'] == undefined)
        {
          body["evaluation"]['NaN Values of x'] = null;
        }
        else
        {
          body["evaluation"]['NaN Values of x'] = JSON.parse(body["evaluation"]['NaN Values of x']);
        }
        if (body["evaluation"]['NaN Values of y'] == undefined)
        {
          body["evaluation"]['NaN Values of y'] = null;
        }
        else
        {
          body["evaluation"]['NaN Values of y'] = JSON.parse(body["evaluation"]['NaN Values of y']);
        }
        msg.payload["evaluation"] = body["evaluation"];
        node.status({fill:"green",shape:"ring",text:"done"});
        node.send(msg);
      }
    });

    
    }
}
