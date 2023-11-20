package main

import (
	"encoding/hex"
	"fmt"
)

func main() {
	hexString := "4334443545343339393142304335353141464638423932353343313333314142"

	fmt.Println("Hex String: ", hexString)

	decodedByteArray, err := hex.DecodeString(hexString)

	if err != nil {
		fmt.Println("Unable to convert hex to byte. ", err)
	}

	fmt.Printf("Decoded Byte Array: %v \nDecoded String: %s", decodedByteArray, decodedByteArray)
}
