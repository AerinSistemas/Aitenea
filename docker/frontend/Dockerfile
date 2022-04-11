FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Madrid

RUN mkdir -p /opt/aitenea/aitenea_api/
ADD aitenea_api/ /opt/aitenea/aitenea_api/
ADD package.json /opt/aitenea/package.json
ADD webpack.config.js /opt/aitenea/webpack.config.js
ADD babel.config.json /opt/aitenea/babel.config.json
ADD .env /opt/aitenea/.env

WORKDIR /opt/aitenea

RUN apt-get clean && apt-get update
RUN apt-get install -y fping \
python3.8-dev \
python3-pip \
libcurl4-openssl-dev \
curl \
vim \
cron

RUN apt -y install curl dirmngr apt-transport-https lsb-release ca-certificates
RUN apt -y install gcc g++ make

# https://gist.github.com/remarkablemark/aacf14c29b3f01d6900d13137b21db3a#gistcomment-3935756
RUN mkdir /usr/local/nvm
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
# nvm environment variables
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 16.10.0
ENV NVM_INSTALL_PATH $NVM_DIR/versions/node/v$NODE_VERSION
# install nvm
RUN curl --silent -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
# install node and npm
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default
# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_INSTALL_PATH/lib/node_modules
ENV PATH $NVM_INSTALL_PATH/bin:$PATH
# confirm installation
RUN node -v
RUN npm -v

# Install dependencies
RUN cd /opt/aitenea/ && npm install --legacy-peer-deps --ignore-scripts
