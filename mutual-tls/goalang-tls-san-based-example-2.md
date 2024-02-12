# Another example for testing San based tls certs

## Server Config
```
package main

import (
    "crypto/rand"
    "crypto/tls"
    "crypto/x509"
    "log"
    "net"
    "os"
    "time"
)

func main() {
    cert, err := tls.LoadX509KeyPair("/var/opt/magma/certs/radsec.tls.crt",
                                     "/var/opt/magma/certs/radsec.tls.key")
    if err != nil {
        log.Fatalf("server: loadkeys: %s", err)
    }
    config := tls.Config{Certificates: []tls.Certificate{cert}}
    config.Time = time.Now
    config.Rand = rand.Reader

    cabytes, _ := os.ReadFile("/var/opt/magma/certs/ca.crt")
    pool := x509.NewCertPool()
    pool.AppendCertsFromPEM(cabytes)
    config.ClientCAs = pool

    service := "radsec.nmslocal.pmn-dev.wavelabs.in:8000"
    listener, err := tls.Listen("tcp", service, &config)
    if err != nil {
        log.Fatalf("server: listen: %s", err)
    }
    log.Print("server: listening")
    for {
        conn, err := listener.Accept()
        if err != nil {
            log.Printf("server: accept: %s", err)
            break
        }
        defer conn.Close()
        log.Printf("server: accepted from %s", conn.RemoteAddr())
        tlscon, ok := conn.(*tls.Conn)
        if ok {
            log.Print("ok=true")
            state := tlscon.ConnectionState()
            for _, v := range state.PeerCertificates {
                log.Print(x509.MarshalPKIXPublicKey(v.PublicKey))
            }
        }
        go handleClient(conn)
    }
}

func handleClient(conn net.Conn) {
    defer conn.Close()
    buf := make([]byte, 512)
    for {
        log.Print("server: conn: waiting")
        n, err := conn.Read(buf)
        if err != nil {
            if err != nil {
                log.Printf("server: conn: read: %s", err)
            }
            break
        }
        log.Printf("server: conn: echo %q\n", string(buf[:n]))
        n, err = conn.Write(buf[:n])
        log.Printf("server: conn: wrote %d bytes", n)

        if err != nil {
            log.Printf("server: write: %s", err)
            break
        }
    }
    log.Println("server: conn: closed")
}
```

## Client Config
```
package main

import (
    "crypto/tls"
    "crypto/x509"
    "fmt"
    "io"
    "io/ioutil"
    "log"
    "os"
    "time"
)

func newClientConfig(rootCAPath string,
                     clientCertPath string,
                     clientKeyPath  string) (*tls.Config, error) {

        caCert, err := ioutil.ReadFile(rootCAPath)
        if err != nil {
            log.Fatalf("Failed to read certificate file: %v", err)
        }

        caCertPool := x509.NewCertPool()
        caCertPool.AppendCertsFromPEM(caCert)

        clientCert, clientErr := tls.LoadX509KeyPair(clientCertPath, clientKeyPath)
        if clientErr != nil {
            log.Fatalf("server: loadkeys: %s", err)
        }

        urandom, randErr:= os.Open("/dev/urandom")
        if randErr != nil {
                return nil, err
        }

        return &tls.Config{
                Certificates: []tls.Certificate{clientCert},
                Time:         time.Now,
                RootCAs:      caCertPool,
                Rand:         urandom,
                InsecureSkipVerify: false,
        }, nil
}

func main() {

    config, certIntErr := newClientConfig("/var/opt/magma/certs/ca.crt",
                              "/var/opt/magma/certs/client.tls.crt",
                              "/var/opt/magma/certs/client.tls.key")

    if certIntErr != nil {
        log.Fatalf("client: cert error")

    }

    conn, err := tls.Dial("tcp", "radsec.nmslocal.pmn-dev.wavelabs.in:8000", config)
    if err != nil {
        log.Fatalf("client: dial: %s", err)
    }
    defer conn.Close()
    log.Println("client: connected to: ", conn.RemoteAddr())

    state := conn.ConnectionState()
    for _, v := range state.PeerCertificates {
        fmt.Println(x509.MarshalPKIXPublicKey(v.PublicKey))
        fmt.Println(v.Subject)
    }
    log.Println("client: handshake: ", state.HandshakeComplete)
    log.Println("client: mutual: ", state.NegotiatedProtocolIsMutual)

    message := "Hello\n"
    n, err := io.WriteString(conn, message)
    if err != nil {
        log.Fatalf("client: write: %s", err)
    }
    log.Printf("client: wrote %q (%d bytes)", message, n)

    reply := make([]byte, 256)
    n, err = conn.Read(reply)
    log.Printf("client: read %q (%d bytes)", string(reply[:n]), n)
    log.Print("client: exiting")
}
```
