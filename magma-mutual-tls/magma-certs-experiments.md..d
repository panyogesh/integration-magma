## Layout of Magma Certs
  
Checkout : https://github.com/zubair1024/mutual-tls-authentication

## Run Client on AGW & Server on host
Client Certs :
 ca: fs.readFileSync("/var/opt/magma/certs/rootCA.pem"),
 key: fs.readFileSync("/var/opt/magma/certs/gateway.key"),
 cert: fs.readFileSync("/var/opt/magma/certs/gateway.crt"),

Server Certs:
  key: fs.readFileSync("keys/controller.key"),
  cert: fs.readFileSync("keys/controller.crt"),
  ca: fs.readFileSync("keys/certifier.pem"),

## Reference 
* https://medium.com/weekly-webtips/how-to-generate-keys-for-mutual-tls-authentication-a90f53bcec64
