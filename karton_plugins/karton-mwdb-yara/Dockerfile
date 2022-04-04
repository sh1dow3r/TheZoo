FROM python:3.7

WORKDIR /app/service
COPY ./requirements.txt ./requirements.txt
COPY ./yara_rules ./yara_rules
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "karton-yaramatcher", "--rules", "yara_rules" ]
