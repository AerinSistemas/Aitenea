#!/bin/bash
echo "\e[32mInstalando Node-RED AITenea\e[0m"

sudo cp -r ../aitenea /opt

# Instalar dependencias de Ubuntu
sudo apt-get clean && apt-get update && apt-get install -y python3.8-dev \
python3-pip \
fping \
libcurl4-openssl-dev \
curl \
git \
vim \
cron \
curl \
libssl-dev

# Instalar node, node-red
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
nvm install 16.10.0
nvm use 16.10.0
npm install -g npm@6.14.8
npm install -g --ignore-scripts --unsafe-perm node-red@1.3.5

# Configurar node-red
mkdir -p ~/.node-red
sudo mkdir -p /data/aitenea_nodes
cd /opt/aitenea
sudo cp -r aitenea_node-red/node-red-data/aitenea_nodes /data

sudo cp .env ~/.node-red/.env
sudo cp aitenea_node-red/node-red-data/settings.js ~/.node-red/settings.js
sudo cp aitenea_node-red/node-red-data/user-authentication.js ~/.node-red/user-authentication.js
sudo cp aitenea_node-red/node-red-data/flows.json ~/.node-red/flows.json
sudo cp aitenea_node-red/package.json ~/.node-red/package.json 
sudo cp aitenea_node-red/nodemon.json ~/.node-red/nodemon.json

# Instalar nodos de node-red
cd ~/.node-red/
npm install --ignore-scripts
