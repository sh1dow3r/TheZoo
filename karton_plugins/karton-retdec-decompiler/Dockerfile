# Stage 1: Build RetDec
FROM ubuntu:focal AS builder

# Install dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential cmake git python3 doxygen graphviz upx \
    openssl libssl-dev zlib1g-dev autoconf automake \
    pkg-config m4 libtool python3-pip python3-venv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up RetDec build
WORKDIR /home/retdec
RUN git clone https://github.com/avast/retdec.git && \
    cd retdec && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=/home/retdec/retdec-install \
             -DCMAKE_LIBRARY_PATH=/usr/lib/gcc/x86_64-linux-gnu/7/ && \
    make -j2 && make install

# Stage 2: Final lightweight runtime
FROM ubuntu:focal
LABEL maintainer="0xalamri@layer0.xyz"

# Install only necessary runtime dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 python3-venv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Add non-root user
RUN useradd -m retdec
USER retdec
WORKDIR /home/retdec

# Copy RetDec from the build stage
COPY --from=builder /home/retdec/retdec-install /home/retdec/retdec-install

# Set up RetDec in the environment
ENV PATH="/home/retdec/retdec-install/bin:$PATH"

# Copy application files
COPY --chown=retdec ./requirements.txt /home/retdec/requirements.txt
COPY --chown=retdec ./karton-retdec-decompiler.py /home/retdec/karton-retdec-decompiler.py

# Set up Python environment
RUN python3 -m venv /home/retdec/venv && \
    /home/retdec/venv/bin/pip --no-cache-dir install -r /home/retdec/requirements.txt

# Ensure virtual environment is in the PATH
ENV PATH="/home/retdec/venv/bin:$PATH"

# Run the script
CMD [ "/home/retdec/venv/bin/python", "karton-retdec-decompiler.py" ]
