package main

import (
	"fmt"
	"strconv"
)

func printHexDump(str string) {
	for i := 0; i < len(str); i++ {
		// Print byte in hexadecimal format
		fmt.Printf("%02x ", str[i])

		// Print extra space after 8 bytes for better readability
		if (i+1)%8 == 0 {
			fmt.Print(" ")
		}

		// Print newline after 16 bytes
		if (i+1)%16 == 0 {
			fmt.Println()
		}
	}

	// Print newline if the length of the string is not a multiple of 16
	if len(str)%16 != 0 {
		fmt.Println()
	}
}

func main() {

	// Create a buffer to read the data
	buffer := ("\\x02\\xc9\\x008\\x010001011234567537@wlan.mnc001.mcc001.3gppnetwork.org")

	// Parse the escape sequences
	unquoted, err := strconv.Unquote(`"` + buffer + `"`)
	if err != nil {
		fmt.Println("Error parsing escape sequences:", err)
		return
	}

	//c := string(buffer)

	fmt.Printf("%x\n", unquoted)
	printHexDump(unquoted)
}
