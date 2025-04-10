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
RUN apk add --no-cache git build-base libffi-dev

WORKDIR /app

COPY requirements.txt /app
COPY peparser_lib.py /app/peparser_lib.py
COPY karton-mwdb-peparser.py /app/karton-mwdb-peparser.py

RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r /app/requirements.txt

ENV PATH="/app/venv/bin:$PATH"

CMD ["/app/venv/bin/python", "/app/karton-mwdb-peparser.py"]
