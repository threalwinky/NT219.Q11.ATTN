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

sudo apt update
sudo apt install -y libxcb-xinerama0 libxcb-xinerama0-dev libxcb-icccm4 libxcb-icccm4-dev libxkbcommon-x11-0 libxkbcommon-x11-dev libxcb-render-util0 libxcb-render-util0-dev libxcb-shape0 libxcb-shape0-dev libxcb-keysyms1 libxcb-keysyms1-dev

sudo apt install -y libx11-xcb1 libxcb1 libxcb-util1 libxcb-image0 libxcb-randr0