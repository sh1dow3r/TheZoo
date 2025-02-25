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

# Install necessary dependencies
RUN apk add --no-cache git

WORKDIR /app

# Copy and install requirements
COPY requirements.txt /app

# Clone capa repository and initialize submodules
RUN git clone https://github.com/mandiant/capa.git /app/capa && \
    cd /app/capa && \
    git submodule update --init rules

# Create virtual environment and install dependencies
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip --no-cache-dir install -e /app/capa && \
    /app/venv/bin/pip --no-cache-dir install -r /app/requirements.txt

# Ensure capa is available in the PATH
ENV PATH="/app/venv/bin:$PATH"

# Copy the script
COPY ./karton-mwdb-flare-capa.py /app/karton-mwdb-flare-capa.py

# Run the script
CMD [ "/app/venv/bin/python", "/app/karton-mwdb-flare-capa.py" ]
