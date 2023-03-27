module.exports = function(RED){
    function NaNValuesCleaning(config){
      //Initialization of all the features that the node shares
        RED.nodes.createNode(this, config);
        //All the options built in the html file has been defined below:
        var node = this
        this.timeout = config.timeout;
        this.run_type = config.runselect;
        this.axis = config.axis;
        this.how = config.how;
        this.subset = config.subset;
        this.method = config.method;
        //the process in nodered can be folowed by node.status
        node.status({fill:"", shape:"", text:""});
        //Send the input to process all the messages through the flow
        node.on('input', function(msg){
          if (msg.payload['origin'] == undefined){
            node.status({fill:"red", shape:"ring", text:"No data to use"})
            var msg1 = { payload:"There is no available data to use. Please, upload data with the nodes such as 'From-CSV', 'From-ElasticSearch', or 'Manual-data'" };
            node.send(msg1)            
          }
          else {
            node.status({fill:"yellow", shape:"ring", text:"In execution"})
            //Updating the msg.payload with the options that previosuly were defined
            msg.payload['origin']['options']['type_nan'] = node.run_type;
            msg.payload['origin']['options']['subset'] = this.subset;
            msg.payload['origin']['options']['how'] = this.how;
            msg.payload['origin']['options']['axis'] = this.axis;
            msg.payload['origin']['options']['method'] = this.method;            
            //Calling NanValues
            NaNValues(msg, node)
          }
            
        });        
    }
    //The settings of the node are registered
    RED.nodes.registerType("NAN Values", NaNValuesCleaning);

    function NaNValues(msg, node) {
        //Define the request (the connection between nodered and backend is established)
        const request = require("request");
        //Setting URL (This was defined in aitenea_api/pline/api/urls.py)
        let URL = process.env.AITENEA_URL_BACKEND + `/api/nan_values/`;                       
        //options for request process
        let opts = {
          method: 'POST',
          url: URL,
          timeout: Number(node.timeout),
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(msg.payload),
        };
        //send post request to the url that was specified previously
        request.post(opts, function (error, response, body) {         
          //manage errors if there is any
          if (body == undefined || error != null){   
            if (error == 'Error: ESOCKETTIMEDOUT'){
              let error_nan = 'Timeout Error. Increase the value of timeout'            
              node.status({fill:"red", shape:"ring", text:"Timeout: increase value"})
              msg.payload['error'] = error_nan
              node.send(msg);
            }            
          }
          else if (JSON.parse(body)['error'] == 'KeyError'){
            let error_nan = 'Check the correct name and format of columns in subset. Avoid spaces between column names.'            
            node.status({fill:"red", shape:"ring", text:"Error in subset"})
            msg.payload['error'] = error_nan
            node.send(msg);
          } 
          //completing msg.payload with the anwswer after request and if the nan values process was applied
          else {
            //parsing the body after request
            body = JSON.parse(body);
            //use of try and finally in order to extract the elastic type if a destination node is
            //present before the nan values node
            try{
              toward_elastic = msg.payload.target
              if (toward_elastic == undefined){
                toward_elastic = null
              }
              else{
                toward_elastic = toward_elastic.type                
              }
            }
            finally{
              if ((toward_elastic == 'elastic') && (body['To elastic'] != undefined)){
                msg.payload['To elastic'] = body['To elastic']
              }
            }             
            msg.payload['NaN Values'] = body['output'];                
            node.status({fill:"green",shape:"ring",text:"done"});        
            node.send(msg);                                                
          }          
        });        
      }
}


