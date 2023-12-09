// Package required: go get github.com/seehuhn/mt19937
// go run <FileName>
package main

import (
        "fmt"
        "math/rand"
        "time"

        "github.com/seehuhn/mt19937"
)

func main() {
        rng := rand.New(mt19937.New())
        rng.Seed(time.Now().UnixNano())
        fmt.Println(rng.Intn(999999))
}
