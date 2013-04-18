package main

import (
	"log"
	"os"
)

func main() {
	//logger is used like stodut removable print
	log.SetFlags(0)
	log.SetOutput(os.Stdout)

	if _, err := parser.Parse(); err != nil {
		os.Exit(1)
	}
}
