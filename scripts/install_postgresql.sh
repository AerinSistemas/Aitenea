#!/bin/bash
echo "\e[32mInstalando PostgreSQL\e[0m"

# Añadir repositorio de PostgreSQL
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
 sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ focal-pgdg main" > /etc/apt/sources.list.d/postgresql.list'

# Instalar dependencias de Ubuntu
sudo apt-get update
sudo apt-get install -y libpq-dev
sudo apt-get install -y postgresql-14

# Inicilizar postgresql
sudo /etc/init.d/postgresql start

# Configure postgresql
sudo -u postgres psql -c "CREATE DATABASE aitenea;"
sudo -u postgres psql -c "CREATE USER root WITH PASSWORD 'maLe2K21';"
sudo -u postgres psql -c "ALTER DATABASE aitenea OWNER TO root;"
