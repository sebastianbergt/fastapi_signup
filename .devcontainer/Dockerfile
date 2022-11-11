FROM ubuntu:20.04

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends vim python3 python3-pip git
RUN pip3 install black

RUN pip3 install "fastapi[all]"
RUN pip3 install "uvicorn[standard]"
