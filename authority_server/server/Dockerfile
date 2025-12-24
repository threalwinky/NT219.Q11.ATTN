FROM python:3.11-bullseye

RUN apt update -y && \
	apt install bison flex libmariadb3 libmariadb-dev tpm2-tools -y
	
WORKDIR /tmp

COPY pbc-0.5.14.tar.gz .

RUN tar -xvf pbc-0.5.14.tar.gz && \
	cd pbc-0.5.14 && \
	./configure --prefix=/usr && \
	make && make install

RUN git clone https://github.com/JHUISI/charm.git && \
	cd charm && \
	./configure.sh && \
	make && make install

COPY . /server
WORKDIR /server

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]