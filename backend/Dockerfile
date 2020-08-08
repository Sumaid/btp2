FROM ubuntu:18.04
RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update --fix-missing\
    && apt-get install -yq --no-install-recommends \
    python3 \
    python3-pip
RUN pip3 install --upgrade pip\
    && pip3 install setuptools

# Install dependencies
RUN apt-get -qq update; \
    apt-get install -qqy --no-install-recommends \
        ca-certificates \
        autoconf automake cmake dpkg-dev file git make patch \
        libc-dev libc++-dev libgcc-7-dev libstdc++-7-dev  \
        dirmngr gnupg2 lbzip2 wget xz-utils libtinfo5; \
    rm -rf /var/lib/apt/lists/*

# # Signing keys
# ENV GPG_KEYS 09C4E7007CB2EFFB A2C794A986419D8A B4468DF4E95C63DC D23DD2C20DD88BA2 8F0871F202119294 0FC3042E345AD05D

# # Retrieve keysi
# #RUN apt install -y gnupg2
# RUN gpg --batch --keyserver ipv4.pool.sks-keyservers.net --recv-keys $GPG_KEYS

# Version info
# ENV LLVM_RELEASE 7
# ENV LLVM_VERSION 7.0.1

# # Install Clang and LLVM
# COPY install.sh .
# RUN ./install.sh

# for open cv
RUN apt-get update --fix-missing
RUN apt-get install -y libgtk2.0-dev 
# for flask web server
EXPOSE 8081

# set working directory
ADD . /app
WORKDIR /app
RUN apt-get install -y ipython3 build-essential python-dev python3-dev
# install required libraries
RUN pip3 install -r requirements.txt

# This is the runtime command for the container
CMD python3 app.py 8081
