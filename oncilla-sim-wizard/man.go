package main

import (
	"os"
)



func main() {
	parser.ApplicationName = "oncilla-sim-wizard"

	parser.WriteManPage(os.Stdout,
		"`oncilla-sim-wizard' is an easy to use script for using the oncilla simulator")
}