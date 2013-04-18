package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"regexp"
	"runtime"
)

// represents the cache of the wizard
type Cache struct {
	GitRepositories map[string]GitRepository
	root            string
}

var cache *Cache = nil

// Gets lazilly the cache
func GetCache() (*Cache, error) {
	if cache == nil {
		cache = &Cache{
			GitRepositories: map[string]GitRepository{},
		}
		if err := cache.updateCache(); err != nil {
			return nil, err
		}
	}

	return cache, nil
}

func (c *Cache) updateCachedGitRepository(name string, g GitRepository) error {

	log.Printf("Caching git repository `%s' from `%s'.\n", name, g["url"])

	gitDir := filepath.Join(c.root, "git")

	if err := os.MkdirAll(gitDir, 0755); err != nil {
		return err
	}

	//change to git cache dir
	if cdir, err := SafeChdir(gitDir); err != nil {
		return err
	} else {
		defer os.Chdir(cdir)
	}

	// checks if the directory exist already
	if ok, _ := Exists(name); ok == false {

		if err := RunCommand("git", "clone", g["url"], name); err != nil {
			return err
		}

	}

	if err := os.Chdir(name); err != nil {
		return err
	}

	if err := RunCommand("git", "fetch", "origin"); err != nil {
		return err
	}

	if tag, hasTag := g["tag"]; hasTag == true {
		log.Printf("Fetching tag `%s'.\n", tag)

		if err := RunCommand("git", "checkout", tag); err != nil {
			return err
		}
	}

	return nil
}

func (c *Cache) ensureCacheRoot() error {
	switch runtime.GOOS {
	case "darwin":
		c.root = filepath.Join(os.Getenv("HOME"), "Library", "Cache", "oncilla-sim-wizard")
	case "windows":
		return fmt.Errorf("I do not support this os as I do not know where I can put my cache")
	default:
		c.root = filepath.Join(os.Getenv("HOME"), ".cache", "oncilla-sim-wizard")
	}

	if err := os.MkdirAll(c.root, 0755); err != nil {
		return fmt.Errorf("Could not create the cache `%s' : %s", c.root, err)
	}

	log.Println("Found cache in directory `", c.root, "'.")

	return nil
}

func (c *Cache) updateCache() error {

	log.Println("Updating cache.")

	if err := c.ensureCacheRoot(); err != nil {
		return nil
	}

	config := GetConfig()

	log.Println("Caching remote git repositories.")

	for _, g := range config.GitRepositories {

		//checks that this is a git url
		if match, _ := regexp.MatchString(`\.git\z`, g["url"]); match == false {
			return fmt.Errorf("Cannot cache git repository %s, url `%s' does not seems to refer to a git repository.", g, g["url"])
		}

		if _, hasUrl := g["url"]; hasUrl == false {
			return fmt.Errorf("Invalid repository definition %s, I need a `url' key", g)
		}

		name, hasName := g["name"]
		if hasName == false {
			return fmt.Errorf("Invalid repository definition %s, I need a `name' key", g)
		}

		if err := c.updateCachedGitRepository(name, g); err != nil {
			return err
		}
		c.GitRepositories[name] = g
	}

	return nil
}
