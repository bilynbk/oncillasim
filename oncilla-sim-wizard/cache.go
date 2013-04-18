package main

import (
	"fmt"
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
	gitDir := filepath.Join(c.root, "git")

	if err := os.MkdirAll(gitDir, 0644); err != nil {
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

	if err := os.MkdirAll(c.root, 0644); err != nil {
		return fmt.Errorf("Could not create the cache `%s' : %s", c.root, err)
	}

	return nil
}

func (c *Cache) updateCache() error {

	if err := c.ensureCacheRoot(); err != nil {
		return nil
	}

	config := GetConfig()
	for _, g := range config.Repositories {
		reg, _ := regexp.Compile(`([\w\-]+).git\z`)
		m := reg.FindStringSubmatch(g["url"])
		if m == nil {
			return fmt.Errorf("Cannot cache git repository %s, url `%s' does not seems to refer to a git repository.", g, g["url"])
		}
		name := m[1]
		if err := c.updateCachedGitRepository(name, g); err != nil {
			return err
		}
		c.GitRepositories[name] = g
	}

	return nil
}
