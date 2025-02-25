# FROM python:3.7

# WORKDIR /app/service
# COPY ./requirements.txt ./requirements.txt
# COPY ./karton-mwdb-strings.py ./karton-mwdb-strings.py
# RUN pip install --no-cache-dir -r requirements.txt
# CMD [ "python" , "karton-mwdb-strings.py" ]

FROM python:3.12-alpine
LABEL maintainer="0xalamri@layer0.xyz"

WORKDIR /app
COPY requirements.txt /app
COPY ./requirements.txt ./requirements.txt
COPY ./karton-mwdb-strings.py ./karton-mwdb-strings.py
RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip --no-cache-dir install -r /app/requirements.txt
CMD [ "python" , "karton-mwdb-strings.py" ]
