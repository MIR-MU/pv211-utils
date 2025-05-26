FROM nvidia/cuda:11.3.1-runtime-ubuntu20.04

ARG AUXILIARY_FILES="\
    /tmp/* \
    # ... (rest of auxiliary files)
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
    # Change Python version to 3.9
    python3.9 \
    python3.9-dev \
    python3.9-distutils \
    pkg-config \
    tzdata \
    vim \
    wget \
"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Prague

# Install system dependencies
RUN apt-get -qy update \
 && apt-get -qy install --no-install-recommends ${DEPENDENCIES} \
 # Ensure python3.9 is the default python3
 && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1 \
 && update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1 \
 # Install Rust and Cargo
 && curl https://sh.rustup.rs -sSf | sh -s -- -y \
 && apt-get -qy autoclean \
 && apt-get -qy clean \
 && apt-get -qy autoremove --purge \
 && rm -rf ${AUXILIARY_FILES}

ENV PATH="/root/.cargo/bin:${PATH}"

# Install python and python packages
COPY . /pv211-utils
WORKDIR /pv211-utils
# Use python3.9 for pip and package installation
# Inside your Dockerfile, where Python packages are installed:
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.9 \
 && python3.9 -m pip install --upgrade pip setuptools wheel \
 && python3.9 -m pip install --upgrade Cython numpy \ # Install/upgrade Cython and NumPy first
 && python3.9 -m pip install .[notebooks] \
 && python3.9 -m script.download_datasets # all

# Create home directory
RUN useradd -u 1000 --create-home jovyan
WORKDIR /home/jovyan
USER 1000
ADD notebooks .
RUN ln -s /media/persistent-storage