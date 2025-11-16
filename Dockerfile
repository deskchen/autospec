# AutoSpec Dockerfile with Frama-C

# Use official Frama-C Docker image as base
FROM framac/frama-c:31.0

# Switch to root to install additional packages
USER root

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy Python requirements
COPY requirements.txt /workspace/requirements.txt

# Install Python dependencies
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Set up environment to use OPAM packages
ENV PATH="/home/opam/.opam/default/bin:${PATH}"
ENV OPAM_SWITCH_PREFIX="/home/opam/.opam/default"

# Verify Frama-C is available
RUN eval $(opam env) && frama-c -version