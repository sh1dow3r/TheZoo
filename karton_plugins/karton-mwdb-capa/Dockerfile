# FROM python:3.9

# WORKDIR /app/service
# COPY ./requirements.txt ./requirements.txt
# RUN git clone https://github.com/mandiant/capa.git /app/service/capa 
# RUN cd /app/service/capa; git submodule update --init rules
# RUN pip install -e /app/service/capa 
# RUN pip install --no-cache-dir -r requirements.txt
# RUN cp /usr/local/bin/capa /usr/bin/capa
# COPY ./karton-mwdb-flare-capa.py ./karton-mwdb-flare-capa.py
# CMD [ "python" , "karton-mwdb-flare-capa.py" ]


FROM python:3.12-alpine

LABEL maintainer="0xalamri@layer0.xyz"

# Install required Alpine packages
RUN apk add --no-cache \
    git \
    build-base \
    libffi-dev \
    musl-dev \
    openssl-dev \
    python3-dev \
    py3-cffi

WORKDIR /app

# Copy and install requirements
COPY requirements.txt /app

# Clone capa and initialize submodules
RUN git clone https://github.com/mandiant/capa.git /app/capa && \
    cd /app/capa && \
    git submodule update --init rules

# Set up virtualenv and install capa
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir -e /app/capa && \
    /app/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

ENV PATH="/app/venv/bin:$PATH"

# Copy your Karton module
COPY ./karton-mwdb-flare-capa.py /app/karton-mwdb-flare-capa.py

CMD ["/app/venv/bin/python", "/app/karton-mwdb-flare-capa.py"]
