# FROM python:3.7

# WORKDIR /app/service
# COPY ./requirements.txt ./requirements.txt
# RUN curl "https://objects.githubusercontent.com/github-production-release-asset-2e65be/52993349/e64e2a80-67c6-11eb-877e-802bf4ccc8b8?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20220311%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220311T103946Z&X-Amz-Expires=300&X-Amz-Signature=6c469d474494ca2ad62fd78fa9e239fde02229cdb6f8777767751c22fce5a8cd&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=52993349&response-content-disposition=attachment%3B%20filename%3Dfloss-v1.7.0-linux.zip&response-content-type=application%2Foctet-stream" -o ./floss.zip
# RUN curl https://github.com/mandiant/flare-floss/releases/download/v1.7.0/floss-v1.7.0-linux.zip -L -o ./floss.zip
# RUN apt install unzip
# RUN unzip ./floss.zip -d ./floss
# RUN cp floss/floss /usr/bin/
# COPY ./karton-mwdb-flare-floss.py ./karton-mwdb-flare-floss.py
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt
# CMD [ "python" , "karton-mwdb-flare-floss.py" ]


FROM python:3.12-slim

LABEL maintainer="0xalamri@layer0.xyz"

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl unzip && \
    apt-get clean

WORKDIR /app

# Download and install FLOSS
RUN curl -L -o floss.zip https://github.com/mandiant/flare-floss/releases/download/v3.1.1/floss-v3.1.1-linux.zip && \
    unzip floss.zip -d ./floss && \
    mv ./floss/floss /usr/bin/floss && \
    chmod +x /usr/bin/floss && \
    rm -rf floss.zip ./floss

# Copy and install Python dependencies
COPY requirements.txt /app
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# Copy script
COPY ./karton-mwdb-flare-floss.py /app/karton-mwdb-flare-floss.py

CMD [ "/app/venv/bin/python", "/app/karton-mwdb-flare-floss.py" ]
