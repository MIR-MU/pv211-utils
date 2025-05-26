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

# Using Python 3.9
ARG PYTHON_VERSION_MAJOR_MINOR=3.9
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
    # Python 3.9 packages from main Ubuntu 20.04 repos
    python${PYTHON_VERSION_MAJOR_MINOR} \
    python${PYTHON_VERSION_MAJOR_MINOR}-dev \
    python${PYTHON_VERSION_MAJOR_MINOR}-distutils \
    python${PYTHON_VERSION_MAJOR_MINOR}-venv \
    # For Rust/Cargo
    cargo \
    tzdata \
    vim \
    wget \
"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Prague

# Install system dependencies, including Python 3.9
RUN apt-get -qy update \
 && ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \
 && apt-get -qy install --no-install-recommends tzdata \
 && dpkg-reconfigure --frontend noninteractive tzdata \
 && apt-get -qy install --no-install-recommends ${DEPENDENCIES} \
 && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION_MAJOR_MINOR} 1 \
 && update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_VERSION_MAJOR_MINOR} 1 \
 && apt-get -qy autoclean \
 && apt-get -qy clean \
 && apt-get -qy autoremove --purge \
 && rm -rf ${AUXILIARY_FILES} \
 && rm -rf /var/lib/apt/lists/*

# Copy your project code (including setup.py and requirements.txt)
COPY . /pv211-utils
WORKDIR /pv211-utils

# Install python and python packages using Python 3.9
RUN curl https://bootstrap.pypa.io/get-pip.py | python${PYTHON_VERSION_MAJOR_MINOR} \
 && python${PYTHON_VERSION_MAJOR_MINOR} -m pip install --no-cache-dir --upgrade pip setuptools wheel \
 # ADD THIS LINE: Try to pre-install a known compatible version of puccinialin
 && python${PYTHON_VERSION_MAJOR_MINOR} -m pip install --no-cache-dir puccinialin==0.1.4 \
 && python${PYTHON_VERSION_MAJOR_MINOR} -m pip install --no-cache-dir .[notebooks] \
 && python${PYTHON_VERSION_MAJOR_MINOR} -m script.download_datasets all
# Rewrite "# all" to "all" in order to create a fat Docker image with all dataset formats

# Create home directory and user
RUN useradd -u 1000 --create-home jovyan
WORKDIR /home/jovyan
USER 1000
ADD notebooks . # This adds your 'notebooks' folder to /home/jovyan/notebooks
RUN ln -s /media/persistent-storage persistent-storage-link