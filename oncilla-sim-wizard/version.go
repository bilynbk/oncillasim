package main

import (
	"fmt"
)

type Version struct {
	Major, Minor, Patch, Tweak string
}

func (v Version) String() string {
	val := v.Major + "." + v.Minor
	if len(v.Patch) > 0 {
		val += "." + v.Patch
	}

	if len(v.Tweak) > 0 {
		val += "." + v.Tweak
	}

	return val
}

var version = Version{Major: "0", Minor: "3", Patch: "0~go1"}

type VersionExecuter struct {
}

func (v *VersionExecuter) Execute(args []string) error {
	if len(args) > 0 {
		return fmt.Errorf("version does not take arguments")
	}

	fmt.Printf("oncilla-sim-wizard version %s.\n", version)
	return nil
}

func init() {
	parser.AddCommand("version",
		"Prints the current version of the program",
		"The version command prints the version of the system",
		&VersionExecuter{})
}
