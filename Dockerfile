FROM docker.io/nvidia/cuda:12.0.1-runtime-ubuntu22.04

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
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
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
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11 \
 && python3.11 -m pip install --upgrade pip "setuptools<81" wheel \
 && python3.11 -m pip install --no-build-isolation --no-cache-dir "numpy<2" .[notebooks] \
 && python3.11 -m script.download_datasets # all

# Create home directory
RUN useradd -u 1000 --create-home jovyan
WORKDIR /home/jovyan
USER 1000
ADD notebooks .
RUN ln -s /media/persistent-storage

