FROM debian:11.5-slim

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt update \
    && apt upgrade -y \
    && apt install -y \
    git \
    curl \
    wget \
    psutils \
    make \
    hugo \
    xmlstarlet \
    bash

RUN curl -fsSL https://deb.nodesource.com/setup_19.x | bash - && \
    apt-get install -y nodejs

RUN npm install -g firebase-tools    

ENV PATH="$PATH:$PWD/node/bin"
