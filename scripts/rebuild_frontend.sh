#!/bin/bash
echo "\e[32mRebuildeando Frontend AITenea\e[0m"

cd /opt/aitenea
sudo rm -rf /opt/aitenea/aitenea_api/frontend/build
npm run build