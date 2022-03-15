FROM python:3.7

WORKDIR /app/service
COPY ./requirements.txt ./requirements.txt
COPY ./my_yara_dir	./my_yara_dir
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "karton-yaramatcher", "--rules", "my_yara_dir" ]
