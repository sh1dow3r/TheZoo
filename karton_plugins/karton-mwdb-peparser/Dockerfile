FROM python:3.7

WORKDIR /app/service
COPY ./requirements.txt ./requirements.txt
COPY ./karton-mwdb-peparser.py ./karton-mwdb-peparser.py
COPY ./PEParser.py ./PEParser.py
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python" , "karton-mwdb-peparser.py" ]
