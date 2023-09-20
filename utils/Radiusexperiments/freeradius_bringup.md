# Procedures for freeradius

## Setting up of freeradius
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
