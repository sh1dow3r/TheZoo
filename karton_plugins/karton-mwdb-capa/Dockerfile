FROM python:3.9

WORKDIR /app/service
COPY ./requirements.txt ./requirements.txt
RUN git clone https://github.com/mandiant/capa.git /app/service/capa 
RUN cd /app/service/capa; git submodule update --init rules
RUN pip install -e /app/service/capa 
RUN pip install --no-cache-dir -r requirements.txt
RUN cp /usr/local/bin/capa /usr/bin/capa
COPY ./karton-mwdb-flare-capa.py ./karton-mwdb-flare-capa.py
CMD [ "python" , "karton-mwdb-flare-capa.py" ]
