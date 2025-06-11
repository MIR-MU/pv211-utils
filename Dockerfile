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

# Changed: Switched from python3.8 to python3.9 and added python3-pip
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

# Changed: Added deadsnakes PPA to install Python 3.9
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

# Changed: Use python3.9 and system pip, removed get-pip.py, added --no-cache-dir
# Install python and python packages
COPY . /pv211-utils
WORKDIR /pv211-utils
RUN python3.9 -m pip install --no-cache-dir .[notebooks] \
 && python3.9 -m script.download_datasets # all
# Rewrite "# all" to "all" in order to create a fat Docker image with all dataset formats

# Create home directory
RUN useradd -u 1000 --create-home jovyan
WORKDIR /home/jovyan
USER 1000
ADD notebooks .
RUN ln -s /media/persistent-storage