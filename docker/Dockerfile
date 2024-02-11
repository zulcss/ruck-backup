FROM debian:testing

RUN apt-get update && \
    apt-get install -y git-core \
                       python3-dev \
                       python3-pip \
                       python3-click \
                       python3-pbr \
                       python3-rich 

ADD assets/pip.conf /etc/pip.conf

RUN mkdir -p /usr/src/ruck

WORKDIR /usr/src/ruck