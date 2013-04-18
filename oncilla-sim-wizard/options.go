package main

import (
	"github.com/jessevdk/go-flags"
)

/* General options for oncilla-sim-wizard */
type Options struct {
	Verbose    bool   `short:"v" long:"verbose" description:"Verbose output"`
	ConfigPath string `short:"c" long:"config"  description:"Path to the JSON config file. Could be over http"`
}

/* Sensible good default for the options, no tags, but good remotes */

var options = &Options{
	Verbose:    false,
	ConfigPath: "http://biorob2.epfl.ch/users/tuleu/data/oncilla-sim-wizard-config.json",
}

/* load the config from a config file on the system */
var parser = flags.NewParser(options, flags.Default)
