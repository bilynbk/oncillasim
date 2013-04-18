package main

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"runtime"
)

// Represents an Oncilla Simulation project tree
type OncillaProjectTree struct {
	Path string
}

// Tests if the given path is a Oncilla project tree.
func IsProjectTree(path string) (bool, error) {
	if err := updateCache(); err != nil {
		return false, err
	}

	return false, NewNotImplementedFunction("IsProjectTree")
}

// Tests if the given path is suitable for creating a new project
// tree, i.e : does not exists, or is an empty directory, or a webots
// directory without oncilla stuff.
func CanCreateProjectTree(path string) (bool, error) {

	return false, NewNotImplementedFunction("IsInstallable")
}

// Opens an existing OncillaProjectTree
func OpenProjectTree(path string) (*OncillaProjectTree, error) {
	return nil, NewNotImplementedFunction("OpenProjectTree")
}

// Creates a new OncillaProjectTree
func CreateProjectTree(path string) (*OncillaProjectTree, error) {
	return nil, NewNotImplementedFunction("CreateProjectTree")
}

// Updates all file in the project tree
func (o *OncillaProjectTree) UpdateFiles() error {
	return NewNotImplementedMethod("OncillaProjectTree", "UpdateFiles")
}

// Compiles all file in the project tree
func (o *OncillaProjectTree) Compile() error {
	return NewNotImplementedMethod("OncillaProjectTree", "Compile")
}

func updateCachedGitRepository(cacheDir, name string, g GitRepository) error {
	gitDir := filepath.Join(cacheDir, "git")

	if err := os.MkdirAll(gitDir, 0644); err != nil {
		return err
	}

	//change to cache dir
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

func ensureCache() (string, error) {
	var cacheDir string
	switch runtime.GOOS {
	case "darwin":
		cacheDir = filepath.Join(os.Getenv("HOME"), "Library", "Cache", "oncilla-sim-wizard")
	case "windows":
		return "", fmt.Errorf("I do not support this os as I do not know where I can put my cache")
	default:
		cacheDir = filepath.Join(os.Getenv("HOME"), ".cache", "oncilla-sim-wizard")
	}

	if err := os.MkdirAll(cacheDir, 0644); err != nil {
		return "", fmt.Errorf("Could not create the cache `%s' : %s", cacheDir, err)
	}

	return cacheDir, nil
}

func updateCache() error {

	cacheDir, err := ensureCache()
	if err != nil {
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
		if err = updateCachedGitRepository(cacheDir, name, g); err != nil {
			return err
		}
	}

	return nil
}
