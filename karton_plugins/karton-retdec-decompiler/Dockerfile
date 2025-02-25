FROM ubuntu:focal



RUN apt-get -y update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y   \
	build-essential                                     \
	cmake                                               \
	git                                                 \
	python3                                             \
	doxygen                                             \
	graphviz                                            \
	upx                                                 \
	openssl                                             \
	libssl-dev                                          \
	zlib1g-dev                                          \
	autoconf                                            \
	automake                                            \
	pkg-config                                          \
	m4                                                  \
	libtool						    \
	python3-pip					    \
	python3

RUN useradd -m retdec
USER retdec
RUN mkdir -p /home/retdec/samples/
RUN chown retdec /home/retdec/samples/
WORKDIR /home/retdec/samples/
ENV HOME /home/retdec
RUN git clone https://github.com/avast/retdec && \
	cd retdec && \
	mkdir build && \
	cd build && \
	cmake .. -DCMAKE_INSTALL_PREFIX=/home/retdec/retdec-install -DCMAKE_LIBRARY_PATH=/usr/lib/gcc/x86_64-linux-gnu/7/ && \
	make -j$(nproc) && \
	make install

ENV PATH /home/retdec/retdec-install/bin:$PATH
COPY ./requirements.txt ./requirements.txt
COPY ./karton-retdec-decompiler.py ./karton-retdec-decompiler.py
RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip --no-cache-dir install -r /app/requirements.txt
CMD [ "python3" , "karton-retdec-decompiler.py" ]
