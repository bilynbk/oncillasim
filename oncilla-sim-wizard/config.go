package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
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
	GitRepositories []GitRepository
	packagesByOS    map[string]PackageList
	repDefByOS      map[string]repoDefsList
}

var config *Config = nil

func initConfigFromJSON(c *Config) error {
	log.Println("Fetching configuration from `", options.ConfigPath, "'")
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

func initDefault(c *Config) {
	c.GitRepositories = []GitRepository{
		GitRepository{
			"name": "liboncilla",
			"url":  "https://redmine.amarsi-project.eu/git/quaddrivers.git",
		},
		GitRepository{
			"name": "liboncilla-webots",
			"url":  "https://redmine.amarsi-project.eu/git/liboncilla-webots.git",
		},
		GitRepository{
			"name": "libcca-oncilla",
			"url":  "https://redmine.amarsi-project.eu/git/oncilla-cca.git",
		},
	}

	c.packagesByOS = map[string]PackageList{
		"ubuntu/precise": PackageList{"liboncilla-dev", "git"},
		"darwin":         PackageList{"liboncilla"},
	}

	c.repDefByOS = map[string]repoDefsList{
		"ubuntu/precise": repoDefsList{
			RepositoryDefinition{
				"url":        "http://biorob2.epfl.ch/users/tuleu/ubuntu",
				"components": "main",
				"key":        "http://biorob2.epfl.ch/users/tuleu/ubuntu/gpg.key",
			},
			RepositoryDefinition{
				"url":        "http://packages.cor-lab.de/ubuntu/",
				"components": "main",
				"key":        "http://packages.cor-lab.de/keys/cor-lab.asc",
			},
		},
	}
}

// Gets a lazily initalized config object
func GetConfig() *Config {
	if config == nil {

		config = &Config{}
		initDefault(config)
		err := initConfigFromJSON(config)
		if err != nil {
			log.Printf("[WARNING] error while reading config : %s\n", err)
		}

	}

	return config
}

func (c *Config) GetRepositoriesForOS(os string) ([]RepositoryDefinition, error) {
	res, ok := c.repDefByOS[os]
	if ok == false {
		return []RepositoryDefinition{}, fmt.Errorf("Unsupported OS `%s'", os)
	}

	return res, nil

}

func (c *Config) GetPackagesForOS(os string) (PackageList, error) {
	res, ok := c.packagesByOS[os]
	if ok == false {
		return PackageList{}, fmt.Errorf("Unsupported OS `%s'", os)
	}

	return res, nil

}
