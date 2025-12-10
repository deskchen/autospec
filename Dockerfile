# AutoSpec Dockerfile with Frama-C

# Use official Frama-C Docker image as base
FROM framac/frama-c:31.0

# Switch to root to install additional packages
USER root

# Install Python, LLVM/clang, and other dependencies
# Try to install LLVM 18, fallback to available version if needed
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    wget \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Add LLVM 18 repository (for Ubuntu 22.04/Jammy)
RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | gpg --dearmor -o /usr/share/keyrings/llvm-snapshot.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/llvm-snapshot.gpg] http://apt.llvm.org/$(lsb_release -cs)/ llvm-toolchain-$(lsb_release -cs)-18 main" >> /etc/apt/sources.list.d/llvm.list && \
    apt-get update && \
    apt-get install -y \
    llvm-18 \
    libclang-18-dev \
    clang-18 \
    || (echo "LLVM 18 not available, trying default..." && \
        apt-get install -y libclang-dev clang llvm) && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy Python requirements
COPY requirements.txt /workspace/requirements.txt

# Install Python dependencies
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Install clang Python bindings for example.py
# Use libclang-py3 which is more compatible with newer libclang versions
RUN pip3 install --no-cache-dir --break-system-packages libclang-py3

# Set up environment variables for libclang
ENV LLVM_CONFIG=/usr/bin/llvm-config-18
ENV LD_LIBRARY_PATH=/usr/lib/llvm-18/lib
# Set LIBCLANG_PATH as fallback (will be found dynamically via llvm-config, but this helps)
ENV LIBCLANG_PATH=/usr/lib/x86_64-linux-gnu/libclang-18.so.18

# Set up environment to use OPAM packages
ENV PATH="/home/opam/.opam/default/bin:${PATH}"
ENV OPAM_SWITCH_PREFIX="/home/opam/.opam/default"

# Verify Frama-C is available
RUN eval $(opam env) && frama-c -version

# Verify libclang is available for example.py
RUN python3 -c "import clang.cindex; print('libclang found:', clang.cindex.Config.library_path or 'default')" || \
    (echo "Warning: libclang not found, but continuing..." && true)