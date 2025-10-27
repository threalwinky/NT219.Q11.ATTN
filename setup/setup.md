GMP 5.x
PBC 0.5.14
OpenSSL
PyParsing 2.1.5
Hypothesis

## GMP 5.x

sudo apt-get install libgmp-dev

## PBC 0.5.14

sudo apt-get update
sudo apt-get install libgmp3-dev flex bison libssl-dev

wget http://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz

tar xf pbc-0.5.14.tar.gz
cd pbc-0.5.14
./configure
make
sudo make install

## OpenSSL

sudo apt install openssl

## PyParsing

requirements.txt

## charm

git clone https://github.com/JHUISI/charm.git

pip install setuptools

not found.  This version of Charm requires the python development environment (probably in python3-dev package).

sudo apt install python3-dev
