FROM nvidia/cuda:11.3.1-runtime-ubuntu20.04

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
    netcat \
    nodejs \
    npm \
    python3.9 \
    python3.9-dev \
    python3.9-distutils \
    python3-pip \
    tzdata \
    vim \
    wget \
"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Prague

# Install system dependencies
RUN apt-get -qy update \
 && apt-get -qy install --no-install-recommends software-properties-common \
 && add-apt-repository ppa:deadsnakes/ppa \
 && apt-get -qy update \
 && apt-get -qy install --no-install-recommends ${DEPENDENCIES} \
 && apt-get -qy autoclean \
 && apt-get -qy clean \
 && apt-get -qy autoremove --purge \
 && rm -rf ${AUXILIARY_FILES}

# Install python and python packages
COPY . /pv211-utils
WORKDIR /pv211-utils
# CHANGED: Added "numpy<2" to prevent compilation errors with gensim.
RUN python3.9 -m pip install --upgrade pip setuptools wheel \
 && python3.9 -m pip install --no-cache-dir "numpy<2" .[notebooks] \
 && python3.9 -m script.download_datasets # all
# Rewrite "# all" to "all" in order to create a fat Docker image with all dataset formats

# Create home directory
RUN useradd -u 1000 --create-home jovyan
WORKDIR /home/jovyan
USER 1000
ADD notebooks .
RUN ln -s /media/persistent-storage