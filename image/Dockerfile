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
    bash

RUN wget https://github.com/gohugoio/hugo/releases/download/v0.89.4/hugo_0.89.4_Linux-64bit.deb \
    && apt install ./hugo_0.89.4_Linux-64bit.deb

RUN curl -fsSL https://deb.nodesource.com/setup_19.x | bash - && \
    apt-get install -y nodejs

RUN npm install -g firebase-tools    

ENV PATH="$PATH:$PWD/node/bin"

RUN git clone https://github.com/jcgregorio/blog.git \
    && cd blog \
    && git submodule update --init --recursive

COPY . /

ENTRYPOINT [ "/entrypoint.sh" ]
