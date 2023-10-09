# This document is about generating the certificates

## Reference
http://www.netprojnetworks.com/creating-fake-certificates-hostapd-mana-hostapd/

## Steps for getting IMSI's privacy key and certs
* openssl req -new -x509 -sha256 -newkey rsa:2048 -nodes -days 7500 -keyout imsi-privacy-key.pem -out imsi-privacy-cert.pem
```
openssl req -new -x509 -sha256 -newkey rsa:2048 -nodes -days 7500 -keyout imsi-privacy-key.pem -out imsi-privacy-cert.pem

Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:CA
Locality Name (eg, city) []:Melono Park
Organization Name (eg, company) [Internet Widgits Pty Ltd]:mycompany
Organizational Unit Name (eg, section) []:Connectivity
Common Name (e.g. server FQDN or YOUR name) []:Yogesh Pandey
Email Address []:yogesh@mycompany.ai
```
* Files created imsi-privacy-cert.pem & imsi-privacy-key.pem
