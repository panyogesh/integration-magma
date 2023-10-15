# Procedures for freeradius

## Setting up of freeradius on Jammy
```
wget  https://github.com/FreeRADIUS/freeradius-server/releases/download/release_3_2_3/freeradius-server-3.2.3.tar.gz
tar -zxvf freeradius-server-3.2.3.tar.gz
cd freeradius-server-3.2.3/
sudo apt-get install libtalloc-devel
sudo apt-get install libtalloc-dev
sudo apt-get install libssl-dev
./configure
make
sudo make install
```

### Setting up freeradius on Focal
```
 sudo apt-get install libtalloc-dev
 sudo apt-get install libssl-dev
 sudo apt-get install libkqueue-dev
 git clone https://github.com/FreeRADIUS/freeradius-server.git
 cd freeradius-server/
 ./configure --with-modules="rlm_sim" --with-modules="rlm_sim_files"
 make
 sudo make install
```
### Reference
https://lists.freeradius.org/pipermail/freeradius-users/2013-January/064426.html

## Testing freeradius
```
1.
/usr/local/etc/raddb/clients.conf

client localhost {
  ipaddr = 127.0.0.1
  secret = testing123
}

2.
/usr/local/etc/raddb/users
testing Cleartext-Password := "password"  <<<<<< Add this line
```
## Radtest config
```
radtest -x testing password localhost 0 testing123
radtest -x -t mschap testing password localhost 0 testing123
```

## General issues
1. make: *** No rule to make target 'src/modules/rlm_lua/example.lua',
Need to clean up all temporary git files and do 'make clean; make ; sudo make install'
Reference : https://lists.freeradius.org/pipermail/freeradius-users/2017-July/088260.html
