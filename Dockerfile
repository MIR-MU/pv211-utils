FROM nvidia/cuda:11.3.1-runtime-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Prague
RUN apt-get update && apt-get install -y tzdata python3.8 python3.8-distutils python3.8-dev \
    bash less netcat vim curl wget build-essential git nodejs npm \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl https://bootstrap.pypa.io/get-pip.py | python3.8
RUN pip install jupyterhub jupyterlab git+https://gitlab.fi.muni.cz/xstefan3/pv211-utils.git
RUN useradd -u 1000 --create-home jovyan
WORKDIR /home/jovyan
USER 1000