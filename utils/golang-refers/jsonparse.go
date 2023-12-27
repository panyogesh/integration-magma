package main

import (

    "encoding/json"
    "fmt"
    "io/ioutil"
    "log"
    //"strconv"
)

type (
        // ServerConfig Encapsulates the configuration of a radius server
        RadsecConfig struct {
                Port    int    `json:"port"`
                Capath  string `json:"capath"`
                TLSpath string `json:"tlspath"`
                Keypath string `json:"keypath"`
        }

        // RadiusConfig the configuration file format
        RadiusConfig struct {
                Radsec     RadsecConfig      `json:"radsec"`
        }
)


// Read reads and parses a configuration file into a RadiusConfig
func Read(filename string) (*RadiusConfig, error) {
        configBytes, err := ioutil.ReadFile(filename)
        if err != nil {
                return nil, err
        }

        var config RadiusConfig
        err = json.Unmarshal(configBytes, &config)
        if err != nil {
                return nil, err
        }

        return &config, nil
}

func main() {
    // read our opened xmlFile as a byte array.
    conf, err := Read("./radsec.json")
    if err != nil {
        log.Fatal(err)
    }

    fmt.Println(conf)

}

///////////////////////////////////////////////////////////////////////////////////////////////////
//vagrant@radius-exp:~/radproc$ cat radsec.json
//{
//    "radsec": {
//        "port": 2082,
//        "capath": "/var/opt/magma/configs/certs/ca.cert",
//        "tlspath": "/var/opt/magma/configs/certs/tls.key",
//        "keypath": "/var/opt/magma/configs/certs/tls.key"
//    }
//}
//vagrant@radius-exp:~/radproc$
///////////////////////////////////////////////////////////////////////////////////////////////////
