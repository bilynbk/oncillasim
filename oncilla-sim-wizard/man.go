package main

import (
	"github.com/jessevdk/go-flags"
	"os"
)


type Options struct {
}

func main() {
	parser := flags.NewParser(&Options{},flags.Default)
	parser.ApplicationName = "oncilla-sim-wizard"

	parser.WriteManPage(os.Stdout,
		"`oncilla-sim-wizard' is an easy to use script for using the oncilla simulator")
}