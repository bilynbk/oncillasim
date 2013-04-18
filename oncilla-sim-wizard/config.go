package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"regexp"
)

type GitRepository map[string]string

type PackageList []string

type repoDefsList []RepositoryDefinition

// Represents all dynamic configuration, getable from local config
// file or from a server.
type Config struct {
	Repositories []GitRepository
	packagesByOS map[string]PackageList
	repDefByOS   map[string]repoDefsList
}

var config *Config = nil

func initConfigFromJSON(c *Config) error {
	var r io.Reader
	if ok, _ := regexp.MatchString(`\Ahttp://`, options.ConfigPath); ok == true {

		resp, err := http.Get(options.ConfigPath)
		if err != nil {
			return err
		}

		r = resp.Body
		defer resp.Body.Close()

	} else {

		r, err := os.Open(options.ConfigPath)
		if err != nil {
			return err
		}

		defer r.Close()
	}

	d := json.NewDecoder(r)

	if err := d.Decode(c); err != nil {
		return err
	}

	return nil

}

// Gets a lazily initalized config object
func GetConfig() *Config {
	if config == nil {

		config = &Config{}
		err := initConfigFromJSON(config)
		if err != nil && options.Verbose == true {
			fmt.Fprintf(os.Stderr, "Warning during config reading : %s\n", err)
		}

	}

	return config
}

func (c *Config) GetRepositoriesForOS(os string) ([]RepositoryDefinition, error) {
	return []RepositoryDefinition{}, NewNotImplementedMethod("Config", "GetRepositoriesForOS")
}

func (c *Config) GetPackagesForOS(os string) (PackageList, error) {
	return PackageList{}, NewNotImplementedMethod("Config", "GetPackagesForOS")
}
