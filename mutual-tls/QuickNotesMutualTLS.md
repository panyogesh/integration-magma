## Refernece 
https://medium.com/weekly-webtips/how-to-generate-keys-for-mutual-tls-authentication-a90f53bcec64

## Steps tried
```
vagrant@oai-gnb-ue-sim:~$ cd mutual-tls-authentication/keys/
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$ ls
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$ openssl req -new -x509 -days 9999 -keyout ca-key.pem -out ca-crt.pem
Generating a RSA private key
...............+++++
.............................................+++++
writing new private key to 'ca-key.pem'
Enter PEM pass phrase:
Verifying - Enter PEM pass phrase:
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:CA
Locality Name (eg, city) []:Menlo Park
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Facebook
Organizational Unit Name (eg, section) []:Magma
Common Name (e.g. server FQDN or YOUR name) []:rootca.yourdomain.com
Email Address []:admin@yourdomain.com
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$ openssl genrsa -out server-key.pem 4096
Generating RSA private key, 4096 bit long modulus (2 primes)
.++++
..............................................................................++++
e is 65537 (0x010001)
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$ openssl req -new -key server-key.pem -out server-csr.pem
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:CA
Locality Name (eg, city) []:Menlo Park
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Facebook
Organizational Unit Name (eg, section) []:Magma
Common Name (e.g. server FQDN or YOUR name) []:server.yourdomain.com
Email Address []:admin@yourdomain.com

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$ ls
ca-crt.pem  ca-key.pem  server-csr.pem  server-key.pem
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$ openssl x509 -req -days 9999 -in server-csr.pem -CA ca-crt.pem -CAkey ca-key.pem -CAcreateserial -out server-crt.pem
Signature ok
subject=C = US, ST = CA, L = Menlo Park, O = Facebook, OU = Magma, CN = server.yourdomain.com, emailAddress = admin@yourdomain.com
Getting CA Private Key
Enter pass phrase for ca-key.pem:
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$ openssl verify -CAfile ca-crt.pem server-crt.pem
server-crt.pem: OK
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$ openssl genrsa -out client1-key.pem 4096
Generating RSA private key, 4096 bit long modulus (2 primes)
....................++++
...........................................++++
e is 65537 (0x010001)
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$ openssl req -new -key client1-key.pem -out client1-csr.pem
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:CA
Locality Name (eg, city) []:Menlo Park
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Facebook
Organizational Unit Name (eg, section) []:Magma
Common Name (e.g. server FQDN or YOUR name) []:client.yourdomain.com
Email Address []:admin@yourdomain.com

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$ openssl x509 -req -days 9999 -in client1-csr.pem -CA ca-crt.pem -CAkey ca-key.pem -CAcreateserial -out client1-crt.pem
Signature ok
subject=C = US, ST = CA, L = Menlo Park, O = Facebook, OU = Magma, CN = client.yourdomain.com, emailAddress = admin@yourdomain.com
Getting CA Private Key
Enter pass phrase for ca-key.pem:
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$ openssl verify -CAfile ca-crt.pem client1-crt.pem
client1-crt.pem: OK
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication/keys$ cd ..
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication$ ls
client.js  keys  package.json  server.js
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication$ node server.js
server bound
server connected authorized
^C
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication$ node server.js
server bound
^R
^R
^C
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication$ vim /etc/hosts
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication$ vim server.js
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication$
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication$
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication$
vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication$
```

## Final output
```vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication$ node server.js
server bound
server connected authorized

vagrant@oai-gnb-ue-sim:~/mutual-tls-authentication$ node client.js
client connected authorized
welcome!
```
