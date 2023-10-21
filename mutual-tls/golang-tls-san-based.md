# Program to create a golang client/server over TLS

## Reference
https://medium.com/@harsha.senarath/how-to-implement-tls-ft-golang-40b380aae288

## Generate Certs
### Step 1: Generate a self-signed CA
```
vagrant@radius-exp:~/certs$ openssl req -nodes -new -newkey rsa:2048 -keyout ca.key -x509 -sha256 -days 365 -out ca.crt
Generating a RSA private key
....................................................................................................................................................................................................................+++++
................+++++
writing new private key to 'ca.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:IN
State or Province Name (full name) [Some-State]:TELANGANA
Locality Name (eg, city) []:HYDERABAD
Organization Name (eg, company) [Internet Widgits Pty Ltd]:mycompany
Organizational Unit Name (eg, section) []:connectivity
Common Name (e.g. server FQDN or YOUR name) []:YP
Email Address []:yp@mycompany.com
vagrant@radius-exp:~/certs$
vagrant@radius-exp:~/certs$

vagrant@radius-exp:~/certs$ ls
ca.crt  ca.key
```

### Step 2: Create a configuration file for the server certificate

```
vagrant@radius-exp:~/certs$ cat server.cnf
[req]
default_md = sha256
prompt = no
req_extensions = v3_ext
distinguished_name = req_distinguished_name

[req_distinguished_name]
CN = localhost

[v3_ext]
keyUsage = critical,digitalSignature,keyEncipherment
extendedKeyUsage = critical,serverAuth,clientAuth
subjectAltName = DNS:localhost
vagrant@radius-exp:~/certs$
```

### Step 3: Generate server certificate using the self-signed CA
```
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -config server.cnf
openssl req -noout -text -in server.csr
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -sha256 -extfile server.cnf -extensions v3_ext

vagrant@radius-exp:~/certs$ ls
ca.crt  ca.key  ca.srl  server.cnf  server.crt  server.csr  server.key
vagrant@radius-exp:~/certs$
```

### Step 4: Implement the server using Golang
```
import (
  "crypto/tls"
  "log"
  "net/http"
)

const (
  port         = ":8443"
  responseBody = "Hello, TLS!"
)

cert, err := tls.LoadX509KeyPair("server.crt", "server.key")
if err != nil {
  log.Fatalf("Failed to load X509 key pair: %v", err)
}


config := &tls.Config{
  Certificates: []tls.Certificate{cert},
}


router := http.NewServeMux()
router.HandleFunc("/", handleRequest)


server := &http.Server{
  Addr:      port,
  Handler:   router,
  TLSConfig: config,
}


log.Printf("Listening on %s...", port)
err = server.ListenAndServeTLS("", "")
if err != nil {
  log.Fatalf("Failed to start server: %v", err)
}


func handleRequest(w http.ResponseWriter, r *http.Request) {
  w.WriteHeader(http.StatusOK)
  w.Write([]byte(responseBody))
}
```

### Step 5: Implement the server using Golang

```
vagrant@radius-exp:~/certs$ cat clients_tls.go
package main

import (
  "crypto/tls"
  "crypto/x509"
  "io/ioutil"
  "log"
  "net/http"
)

const (
  url = "https://localhost:8443"
)

func main() {
  cert, err := ioutil.ReadFile("ca.crt")
  if err != nil {
    log.Fatalf("Failed to read certificate file: %v", err)
  }

  caCertPool := x509.NewCertPool()
  caCertPool.AppendCertsFromPEM(cert)

  tlsConfig := &tls.Config{
    RootCAs: caCertPool,
  }

  tr := &http.Transport{
    TLSClientConfig: tlsConfig,
  }

  client := &http.Client{Transport: tr}
  resp, err := client.Get(url)
  if err != nil {
    log.Fatalf("Failed to get response: %v", err)
  }

  defer resp.Body.Close()

  body, err := ioutil.ReadAll(resp.Body)
  if err != nil {
    log.Fatalf("Failed to read response body: %v", err)
  }

  log.Printf("Response body: %s\n", body)
}
vagrant@radius-exp:~/certs$
```

### Step 6: Verification of the certs

```
vagrant@radius-exp:~/certs$ go run server_tls.go
2023/10/21 05:58:05 Listening on :8443...

vagrant@radius-exp:~/certs$ go run clients_tls.go
2023/10/21 05:58:15 Response body: Hello, TLS!
vagrant@radius-exp:~/certs$
```
