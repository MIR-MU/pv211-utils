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
    pkg-config \ # Added pkg-config
    tzdata \
    vim \
    wget \
"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Prague

# Install system dependencies
RUN apt-get -qy update \
 && apt-get -qy install --no-install-recommends ${DEPENDENCIES} \
 # Ensure python3.8 is the default python3 if multiple are installed
 && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 \
 && update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1 \
 # Install Rust and Cargo
 && curl https://sh.rustup.rs -sSf | sh -s -- -y \
 && apt-get -qy autoclean \
 && apt-get -qy clean \
 && apt-get -qy autoremove --purge \
 && rm -rf ${AUXILIARY_FILES}

# Add Cargo to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Install python and python packages
COPY . /pv211-utils
WORKDIR /pv211-utils
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.8 \
 && python3.8 -m pip install --upgrade pip setuptools wheel \ # Upgrade pip and build tools
 && python3.8 -m pip install .[notebooks] \ # Explicitly use python3.8 -m pip
 && python3.8 -m script.download_datasets # all
# Rewrite "# all" to "all" in order to create a fat Docker image with all dataset formats

# Create home directory
RUN useradd -u 1000 --create-home jovyan
WORKDIR /home/jovyan
USER 1000
ADD notebooks .
RUN ln -s /media/persistent-storage