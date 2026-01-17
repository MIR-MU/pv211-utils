FROM docker.io/nvidia/cuda:11.3.1-runtime-ubuntu20.04

ARG AUXILIARY_FILES="\
    /tmp/* \
    /var/tmp/* \
    /var/log/* \
    /var/lib/apt/lists/* \
    /var/lib/{apt,dpkg,cache,log}/* \
    /usr/share/man/* \
    /usr/share/locale/* \
    /var/cache/apt/* \
"

ARG DEPENDENCIES="\
    bash \
    build-essential \
    curl \
    git \
    htop \
    less \
    libpython3.11-dev \
    netcat \
    nodejs \
    npm \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    tzdata \
    vim \
    wget \
"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Prague

RUN apt-get -qy update \
 && apt-get -qy install --no-install-recommends \
    software-properties-common

RUN add-apt-repository ppa:deadsnakes/ppa -y \
 && apt-get -qy update
 
# Install system dependencies
RUN apt-get -qy install --no-install-recommends ${DEPENDENCIES}

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11 \
 && apt-get -qy autoclean \
 && apt-get -qy clean \
 && apt-get -qy autoremove --purge \
 && rm -rf ${AUXILIARY_FILES}

# Install python and python packages
COPY . /pv211-utils
WORKDIR /pv211-utils

RUN python3.11 -m pip install --upgrade pip setuptools wheel \
 && python3.11 -m pip install cython \
 && python3.11 -m pip install .[notebooks] \
 && python3.11 -m script.download_datasets # all
 # Rewrite "# all" to "all" in order to create a fat Docker image with all dataset formats

# Create home directory
RUN useradd -u 1000 --create-home jovyan
WORKDIR /home/jovyan
USER 1000
ADD notebooks .
RUN ln -s /media/persistent-storage
