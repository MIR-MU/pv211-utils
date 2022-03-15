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
    python3.8 \
    python3.8-dev \
    python3.8-distutils \
    tzdata \
    vim \
    wget \
"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Prague

# Install system dependencies
RUN apt-get -qy update \
 && apt-get -qy install --no-install-recommends ${DEPENDENCIES} \
 && apt-get -qy autoclean \
 && apt-get -qy clean \
 && apt-get -qy autoremove --purge \
 && rm -rf ${AUXILIARY_FILES}

# Install python and python packages
COPY . /pv211-utils
WORKDIR /pv211-utils
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.8 \
 && pip install .[notebooks] \
 && python3.8 -m script.download_datasets

# Create home directory
RUN useradd -u 1000 --create-home jovyan
WORKDIR /home/jovyan
USER 1000
ADD notebooks .
RUN ln -s /media/persistent-storage
