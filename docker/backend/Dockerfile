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
libpq-dev

# Instalar requirements Python
RUN mkdir /opt/aitenea/aitenea-config/
ADD docker/backend/config /opt/aitenea/aitenea-config/
RUN mkdir /opt/aitenea/data/csv/
ADD data/csv /opt/aitenea/data/csv/
RUN cd /opt/aitenea/aitenea-config/ && pip3 install -r requirements.txt