# FROM python:3.7

# WORKDIR /app/service
# COPY ./requirements.txt ./requirements.txt
# COPY ./karton-mwdb-peparser.py ./karton-mwdb-peparser.py
# COPY ./PEParser.py ./PEParser.py
# RUN pip install --no-cache-dir -r requirements.txt
# CMD [ "python" , "karton-mwdb-peparser.py" ]


FROM python:3.12-alpine
LABEL maintainer="0xalamri@layer0.xyz"

# Install system dependencies
RUN apk add --no-cache git

WORKDIR /app

# Copy application files
COPY requirements.txt /app
COPY ./PEParser.py /app/PEParser.py

# Create virtual environment and install dependencies
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip --no-cache-dir install -r /app/requirements.txt

# Ensure virtual environment is in PATH
ENV PATH="/app/venv/bin:$PATH"

# Run the application
CMD [ "/app/venv/bin/python", "/app/PEParser.py" ]

