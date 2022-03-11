FROM python:3.7

WORKDIR /app/service
COPY ./requirements.txt ./requirements.txt
COPY ./karton-mwdb-strings.py ./karton-mwdb-strings.py
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python" , "karton-mwdb-strings.py" ]
