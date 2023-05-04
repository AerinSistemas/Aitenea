#!/bin/bash
echo "\e[32mInstalando Backend AITenea\e[0m"

sudo cp -r ../aitenea /opt
sudo chown -R $USER:$USER /opt/aitenea

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
libssl-dev \
unixodbc-dev

# Crear carpeta para almacenar CSVs
sudo mkdir -p /opt/aitenea/data/csv

# Instalar redis
sudo apt-get install -y redis

# Instalar requirements
cd /opt/aitenea
pip3 install --user -r docker/backend/config/requirements.txt

# Configurar Redis
sudo cp redis.conf /etc/redis/redis.conf

# Reiniciar Redis para aplicar cambios en la configuración
sudo /etc/init.d/redis-server restart

# Correr migraciones
echo 'Clean=> ... start'
sudo rm -rf */*/migrations/*
cd /opt/aitenea/aitenea_api
sudo python3 manage.py makemigrations accounts
sudo python3 manage.py makemigrations pline
sudo python3 manage.py makemigrations reports
sudo python3 manage.py migrate
sudo python3 manage.py loaddata pline/fixtures/initial_data.json

# Instalar node
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
nvm install 16.10.0
nvm use 16.10.0
npm install -g npm@6.14.8

# Instalar frontend React + Gogo-React UI
cd /opt/aitenea
npm install --legacy-peer-deps --ignore-scripts

# Compilar React
npm run build

# Instalar drivers para MSSQL
if ! [[ "18.04 20.04 21.04" == *"$(lsb_release -rs)"* ]];
then
    echo "Ubuntu $(lsb_release -rs) is not currently supported.";
    exit;
fi

sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list

exit
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
