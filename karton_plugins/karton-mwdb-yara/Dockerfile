# FROM python:3.7

# WORKDIR /app/service
# COPY ./requirements.txt ./requirements.txt
# COPY ./yara_rules ./yara_rules
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt
# CMD [ "karton-yaramatcher", "--rules", "yara_rules" ]


FROM python:3.12-alpine
LABEL maintainer="0xalamri@layer0.xyz"

WORKDIR /app
COPY ./requirements.txt ./requirements.txt
COPY ./yara_rules ./yara_rules
RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip --no-cache-dir install -r /app/requirements.txt
CMD [ "karton-yaramatcher", "--rules", "yara_rules"  ]
