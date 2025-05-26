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

# Updated DEPENDENCIES to list Python 3.11 packages
# software-properties-common will be installed separately to enable add-apt-repository
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
    python3.11-venv \ # Good practice to include venv
    tzdata \
    vim \
    wget \
"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Prague

# Install system dependencies, including Python 3.11 from PPA
RUN apt-get -qy update \
 && apt-get -qy install --no-install-recommends software-properties-common \ # Needed for add-apt-repository
 && add-apt-repository -y ppa:deadsnakes/ppa \ # PPA for newer Python versions
 && apt-get -qy update \ # Update package list again after adding PPA
 # Set timezone
 && ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \
 && apt-get -qy install --no-install-recommends tzdata \
 && dpkg-reconfigure --frontend noninteractive tzdata \
 # Install listed dependencies, now including Python 3.11 from the PPA
 && apt-get -qy install --no-install-recommends ${DEPENDENCIES} \
 # Set python3.11 as the default python and python3
 && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
 && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 \
 # Clean up
 && apt-get -qy autoclean \
 && apt-get -qy clean \
 && apt-get -qy autoremove --purge \
 && rm -rf ${AUXILIARY_FILES} \
 && rm -rf /var/lib/apt/lists/*

# Install python and python packages using Python 3.11
COPY . /pv211-utils
WORKDIR /pv211-utils

RUN curl https://bootstrap.pypa.io/get-pip.py | python3.11 \
 && python3.11 -m pip install --no-cache-dir --upgrade pip setuptools wheel \
 && python3.11 -m pip install --no-cache-dir .[notebooks] \
 && python3.11 -m script.download_datasets # all
# Rewrite "# all" to "all" in order to create a fat Docker image with all dataset formats

# Create home directory and user
RUN useradd -u 1000 --create-home jovyan
WORKDIR /home/jovyan
USER 1000
ADD notebooks .
RUN ln -s /media/persistent-storage persistent-storage-link # Clarified link name for symlink