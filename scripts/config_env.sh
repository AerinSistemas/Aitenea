#!/bin/bash

ENV_PATH="./.env"

# Propiedades a rellenar en .env
SEARCH_AITENEA_URL="AITENEA_URL="
SEARCH_AITENEA_URL_BACKEND="AITENEA_URL_BACKEND="
SEARCH_BACKEND_IP="BACKEND_IP="
SEARCH_BACKEND_PORT="BACKEND_PORT="
SEARCH_NODERED_IP="NODERED_IP"
SEARCH_NODERED_PORT="NODERED_PORT="
SEARCH_REDIS_IP="REDIS_IP="
SEARCH_REDIS_PORT="REDIS_PORT="
SEARCH_DB_IP="DB_IP="
SEARCH_DB_PORT="DB_PORT="

# IPs
ip_backend="172.61.0.6"
ip_nodered="172.61.0.10"
ip_redis="172.61.0.8"
ip_db="172.61.0.4"

# Puertos
port_backend="7000"
port_nodered="1880"
port_redis="6379"
port_db="5432"

# Asignar IPs y puertos (sin docker) si el despliegue es en producción
if [ $1 = "production" ] || [ $1 = "production-backend" ] || [ $1 = "production-nodered" ]
then
    ip_backend="0.0.0.0"
    ip_redis="0.0.0.0"
    ip_nodered="0.0.0.0"
    ip_db="0.0.0.0"

    if [ $1 = "production-nodered" ]
    then
        read -p "Introduce la dirección IP donde estará desplegado (Django y Redis), por defecto (0.0.0.0)" READ_BACKEND_IP
        if [ ! -z $READ_BACKEND_IP ]
        then
            ip_backend=$READ_BACKEND_IP
            ip_redis=$READ_BACKEND_IP
            ip_db=$READ_BACKEND_IP
        fi
    fi

    if [ $1 = "production-backend" ]
    then
        read -p "Introduce la dirección IP donde estará desplegado (Node-RED), por defecto (0.0.0.0)" READ_NODERED_IP
        if [ ! -z $READ_NODERED_IP ]
        then
            ip_nodered=$READ_NODERED_IP
        fi
    fi

    read -p "Introduce el puerto externo disponible para (Django), por defecto (7000)" READ_BACKEND_PORT
    if [ ! -z $READ_BACKEND_PORT ]
    then
        port_backend=$READ_BACKEND_PORT
    fi

    read -p "Introduce el puerto externo disponible para (Node-RED), por defecto (1880)" READ_NODERED_PORT
    if [ ! -z $READ_NODERED_PORT ]
    then
        port_nodered=$READ_NODERED_PORT
    fi

    read -p "Introduce el puerto externo disponible para (Redis), por defecto (6379)" READ_REDIS_PORT
    if [ ! -z $READ_REDIS_PORT ]
    then
        port_redis=$READ_REDIS_PORT
    fi
fi

# Construir strings con IPs y puertos
REPLACED_AITENEA_URL="AITENEA_URL=http://${ip_backend}:${port_backend}"
REPLACED_AITENEA_URL_BACKEND="AITENEA_URL_BACKEND=http://${ip_backend}:${port_backend}"
REPLACED_BACKEND_IP="BACKEND_IP=${ip_backend}"
REPLACED_BACKEND_PORT="BACKEND_PORT=${port_backend}"
REPLACED_NODERED_IP="NODERED_IP=${ip_nodered}"
REPLACED_NODERED_PORT="NODERED_PORT=${port_nodered}"
REPLACED_REDIS_IP="REDIS_IP=${ip_redis}"
REPLACED_REDIS_PORT="REDIS_PORT=${port_redis}"
REPLACED_DB_IP="DB_IP=${ip_db}"
REPLACED_DB_PORT="DB_PORT=${port_db}"


# Buscar y reemplazar líneas en el archivo .env
sed -i "s@^$SEARCH_AITENEA_URL[^ ]*@$REPLACED_AITENEA_URL@" "$ENV_PATH"
sed -i "s@^$SEARCH_AITENEA_URL_BACKEND[^ ]*@$REPLACED_AITENEA_URL_BACKEND@" "$ENV_PATH"
sed -i "s@^$SEARCH_BACKEND_IP[^ ]*@$REPLACED_BACKEND_IP@" "$ENV_PATH"
sed -i "s@^$SEARCH_BACKEND_PORT[^ ]*@$REPLACED_BACKEND_PORT@" "$ENV_PATH"
sed -i "s@^$SEARCH_NODERED_IP[^ ]*@$REPLACED_NODERED_IP@" "$ENV_PATH"
sed -i "s@^$SEARCH_NODERED_PORT[^ ]*@$REPLACED_NODERED_PORT@" "$ENV_PATH"
sed -i "s@^$SEARCH_REDIS_IP[^ ]*@$REPLACED_REDIS_IP@" "$ENV_PATH"
sed -i "s@^$SEARCH_REDIS_PORT[^ ]*@$REPLACED_REDIS_PORT@" "$ENV_PATH"
sed -i "s@^$SEARCH_DB_IP[^ ]*@$REPLACED_DB_IP@" "$ENV_PATH"
sed -i "s@^$SEARCH_DB_PORT[^ ]*@$REPLACED_DB_PORT@" "$ENV_PATH"


# ################################### CONFIGURAR PUERTO REDIS 

REDIS_CONF_PATH="./redis.conf"

# Construir string con su puerto
SEARCH_REDIS_CONF_PORT="port "
REPLACED_REDIS_CONF_PORT="port ${port_redis}"

# Buscar y reemplazar líneas en el archivo redis.conf
sed -i "s@^$SEARCH_REDIS_CONF_PORT[^ ]*@$REPLACED_REDIS_CONF_PORT@" "$REDIS_CONF_PATH"

# Modificar mode y bind para permitir o denegar conexiones externas
SEARCH_REDIS_CONF_MODE="protected-mode "
if [ $1 = "production" ] || [ $1 = "production-backend" ]
then
    REPLACED_REDIS_CONF_MODE="protected-mode no"
    sed -i "s@^$SEARCH_REDIS_CONF_MODE[^ ]*@$REPLACED_REDIS_CONF_MODE@" "$REDIS_CONF_PATH"

    SEARCH_REDIS_CONF_BIND="bind 127.0.0.1 ::1"
    REPLACED_REDIS_CONF_BIND="#bind 127.0.0.1 ::1"
    sed -i "s@^$SEARCH_REDIS_CONF_BIND[^ ]*@$REPLACED_REDIS_CONF_BIND@" "$REDIS_CONF_PATH"
fi

if [ $1 = "devel" ]
then
    REPLACED_REDIS_CONF_MODE="protected-mode yes"
    sed -i "s@^$SEARCH_REDIS_CONF_MODE[^ ]*@$REPLACED_REDIS_CONF_MODE@" "$REDIS_CONF_PATH"

    SEARCH_REDIS_CONF_BIND="#bind 127.0.0.1 ::1"
    REPLACED_REDIS_CONF_BIND="bind 127.0.0.1 ::1"
    sed -i "s@^$SEARCH_REDIS_CONF_BIND[^ ]*@$REPLACED_REDIS_CONF_BIND@" "$REDIS_CONF_PATH"
fi


# ################################### CONFIGURAR CORS DJANGO (settings.py)

if [ $1 = "production" ] || [ $1 = "production-backend" ]
then
    # Definir PATH
    DJANGO_SETTINGS_PATH="./aitenea_api/aitenea_api/settings.py"
    SEARCH_CONF="'http:\/\/172.61.0.8:6379',"

    # Construir strings con IPs y puertos
    CORS_BACKEND="'http:\/\/${ip_backend}:${port_backend}',"
    CORS_NODERED="'http:\/\/${ip_nodered}:${port_nodered}',"
    CORS_REDIS="'http:\/\/${ip_redis}:${port_redis}',"

    REPLACED_CORS="    ${CORS_BACKEND}\n    ${CORS_NODERED}\n    ${CORS_REDIS}"

    # Buscar IP en el array CORS_ORIGIN_WHITELIST de settings.py y borrar las siguientes.
    sed -i "/$SEARCH_CONF/,/\]/{//!d}" "$DJANGO_SETTINGS_PATH"
    sleep .5
    # Añadir nuevas IPs al CORS_ORIGIN_WHITELIST array de settings.py
    sed -i "/$SEARCH_CONF/a\\$REPLACED_CORS" "$DJANGO_SETTINGS_PATH"
fi
