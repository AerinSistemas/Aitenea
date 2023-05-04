FROM ubuntu:20.04

ENV PYTHONUNBUFFERED 1

WORKDIR /opt/aitenea/aitenea_api/

ENV PYTHONPATH "${PYTHONPATH}:/opt"

# Instalar dependencias Ubuntu
RUN apt-get clean && apt-get update && apt-get install -y python3.8-dev \
python3-pip \
fping \
libcurl4-openssl-dev \
curl \
git \
vim \
cron \
libssl-dev \
libpq-dev \
unixodbc \
unixodbc-dev

# Instalar requirements Python
RUN mkdir /opt/aitenea/aitenea-config/
ADD docker/backend/config /opt/aitenea/aitenea-config/
RUN mkdir /opt/aitenea/data
RUN mkdir /opt/aitenea/data/csv/
ADD data/csv /opt/aitenea/data/csv/
RUN cd /opt/aitenea/aitenea-config/ && pip3 install -r requirements.txt

#Instalar driver MSSQL
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y --allow-unauthenticated msodbcsql18

ENV DEBIAN_FRONTEND noninteractive


RUN apt-get -y install sudo \
wget \
lsb-core
RUN apt-get update

#Instalar driver PostgreSQL
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt focal-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
RUN apt-get update
RUN apt-get -y install postgresql
RUN apt-get install odbc-postgresql

