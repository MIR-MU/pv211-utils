FROM nvidia/cuda:11.3.1-runtime-ubuntu20.04

# Define arguments for cleanup and dependencies
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

# Updated to Python 3.9 and added pkg-config
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
    pkg-config \
    tzdata \
    vim \
    wget \
"

# Non-interactive frontend for apt to avoid prompts
ARG DEBIAN_FRONTEND=noninteractive
# Set Timezone (using Europe/Prague as per original ENV)
ENV TZ=Europe/Prague

# Install system dependencies, Python 3.9, Rust, and set up Python alternatives
RUN apt-get -qy update \
 # Set timezone correctly
 && ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \
 && apt-get -qy install --no-install-recommends tzdata \
 && dpkg-reconfigure --frontend noninteractive tzdata \
 # Install main dependencies including Python 3.9
 && apt-get -qy install --no-install-recommends ${DEPENDENCIES} \
 # Set python3.9 as the default python and python3
 && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1 \
 && update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1 \
 # Install Rust and Cargo
 && curl https://sh.rustup.rs -sSf | sh -s -- -y \
 # Clean up apt caches and downloaded files
 && apt-get -qy autoclean \
 && apt-get -qy clean \
 && apt-get -qy autoremove --purge \
 && rm -rf ${AUXILIARY_FILES} \
 && rm -rf /var/lib/apt/lists/*

# Add Cargo to PATH (for root user during build and jovyan later if not overridden)
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy application code into the image
COPY . /pv211-utils
WORKDIR /pv211-utils

# Install Python packages using Python 3.9
# This includes upgrading pip/setuptools/wheel and pre-installing Cython/numpy
# Using --no-cache-dir to prevent caching issues and reduce layer size
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.9 \
 && python3.9 -m pip install --no-cache-dir --upgrade pip setuptools wheel \
 && python3.9 -m pip install --no-cache-dir --upgrade Cython numpy \
 && python3.9 -m pip install --no-cache-dir .[notebooks] \
 && python3.9 -m script.download_datasets # all
# Rewrite "# all" to "all" in order to create a fat Docker image with all dataset formats

# Create a non-root user 'jovyan' and switch to it
RUN useradd -u 1000 --create-home jovyan
# WORKDIR /home/jovyan # Original WORKDIR was here, but ADD notebooks . implies it should be done from /home/jovyan context
# USER 1000 # Switching user before ADD might be an issue if ADD needs root, let's test original way first for jovyan part

# The following section for user 'jovyan' setup:
# Switch to home directory of jovyan for subsequent commands if needed as jovyan
WORKDIR /home/jovyan
# ADD notebooks . # This copies 'notebooks' from build context to /home/jovyan/
# The line below looks like it intended to copy files *as* jovyan or at least into its home.
# Let's ensure the WORKDIR and USER are set correctly for these operations.

USER 1000
ADD notebooks . # This will add 'notebooks' from your project root to /home/jovyan/
RUN ln -s /media/persistent-storage persistent-storage-link # Renamed link for clarity

# Example: Expose a port if your application (e.g., Jupyter) needs it
# EXPOSE 8888

# Example: Define a default command to run when the container starts
# CMD ["python3.9", "-m", "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]