package main

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

// Gets a lazily initalized config object
func GetConfig() *Config {
	if config == nil {
		config = &Config{}
	}

	return config
}

func (c *Config) GetRepositoriesForOS(os string) ([]RepositoryDefinition, error) {
	return []RepositoryDefinition{}, NewNotImplementedMethod("Config", "GetRepositoriesForOS")
}

func (c *Config) GetPackagesForOS(os string) (PackageList, error) {
	return PackageList{}, NewNotImplementedMethod("Config", "GetPackagesForOS")
}
