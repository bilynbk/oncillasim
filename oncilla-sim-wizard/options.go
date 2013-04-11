package main

import (
	"github.com/jessevdk/go-flags"
	"fmt"
	"path/filepath"
)


/* General options for oncilla-sim-wizard */
type Options struct {
	Verbose bool `short:"v" long:"verbose" description:"Verbose output"`
	LiboncillaRepo map[string]string `long:"liboncilla" description:"URL of the liboncilla repo. accepts 'remote' and 'tag' key, remote is mandatory."`
	LiboncillaWebotsRepo map[string]string `long:"liboncilla-webots" description:"URL of the liboncilla-webots repo. accepts 'remote' and 'tag' key, remote is mandatory."`
	CCAOncillaRepo map[string]string `long:"ccaoncilla" description:"URL of the ccaoncilla repo. accepts 'remote' and 'tag' key, remote is mandatory."`
	Base string
	ConfigFilename string
}

type GenerateConfig struct {
	Path string `short:"p" long:"path" description:"Path for generating the ini file"`
}

func (g *GenerateConfig) Execute(args []string) error {
	if len(args) > 0 {
		return fmt.Errorf("generate-config do not take arguments")
	}

	filename := filepath.Join(options.Base,options.ConfigFilename)
	if err := parser.WriteIniToFile(filename, flags.IniIncludeComments | flags.IniIncludeDefaults); err != nil {
		return err
	}

	return nil
}

/* Sensible good default for the options, no tags, but good remotes */

var options = &Options {
LiboncillaRepo: map[string]string{
		"remote":"https://redmine.amarsi-project.eu/git/quaddrivers.git",
	},
LiboncillaWebotsRepo: map[string]string{
		"remote":"https://redmine.amarsi-project.eu/git/liboncilla-webots.git",
	},
CCAOncillaRepo: map[string]string{
		"remote":"https://redmine.amarsi-project.eu/git/oncilla-cca.git",
	}, 
	Base: "/usr/share/oncilla-sim",
	ConfigFilename: "wizard.config",
}

/* load the config from a config file on the system */


var parser = flags.NewParser(options, flags.Default)


func init() {
	parser.ParseIniFile(filepath.Join(options.Base,options.ConfigFilename))
}

