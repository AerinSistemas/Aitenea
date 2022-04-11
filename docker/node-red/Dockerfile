FROM nodered/node-red:1.3.5

ADD aitenea_node-red/node-red-data /data

ADD aitenea_node-red/package.json .
ADD aitenea_node-red/nodemon.json .

USER root
RUN npm install -g nodemon@2.0.9
RUN npm install --ignore-scripts --unsafe-perm --no-update-notifier --no-fund --only=production