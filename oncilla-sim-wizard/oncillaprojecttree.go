package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
)

// Represents an Oncilla Simulation project tree
type OncillaProjectTree struct {
	Path     string
	dbFile   string
	fileHash map[string]string
}

var dbFileName = ".oncilla-sim-wizard.filedb"

// Tests if the given path is a Oncilla project tree.
func IsProjectTree(path string) (bool, error) {
	stat, err := os.Stat(path)

	if err != nil {
		return false, err
	}

	if stat.IsDir() == false {
		return false, fmt.Errorf("`s' is not a directory", path)
	}

	dbFile := filepath.Join(path, dbFileName)

	if _, err := os.Stat(dbFile); err != nil {
		if os.IsNotExist(err) {
			return false, fmt.Errorf("Missing mandatory file `%s'.", dbFile)
		} else {
			return false, err
		}
	}

	return true, nil
}

// Tests if the given path is suitable for creating a new project
// tree, i.e : does not exists, or is an empty directory, or a webots
// directory without oncilla stuff.
func CanCreateProjectTree(path string) (bool, error) {
	stat, err := os.Stat(path)
	if err != nil {
		if os.IsNotExist(err) {
			return true, nil
		} else {
			return false, err
		}
	}

	if stat.IsDir() == false {
		return false, fmt.Errorf("Path `%s' exists and is not a directory.", path)
	}

	if m, err := filepath.Glob(path + "/*"); err != nil {
		return false, err
	} else if len(m) != 0 {
		return false, fmt.Errorf("Path `%s' exists and is not an empty directory.", path)
	}

	return true, nil
}

// Opens an existing OncillaProjectTree
func OpenProjectTree(path string) (*OncillaProjectTree, error) {
	dbFile := filepath.Join(path, dbFileName)

	file, err := os.Open(dbFile)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	decoder := json.NewDecoder(file)

	opt := &OncillaProjectTree{
		Path:     path,
		dbFile:   dbFile,
		fileHash: make(map[string]string),
	}

	if err = decoder.Decode(opt.fileHash); err != nil && err != io.EOF {
		return nil, err
	}

	return opt, nil
}

// Creates a new OncillaProjectTree
func CreateProjectTree(path string) (*OncillaProjectTree, error) {
	if err := os.MkdirAll(path, 0644); err != nil {
		return nil, err
	}

	dbFile := filepath.Join(path, dbFileName)

	file, err := os.Create(dbFile)
	if err != nil {
		return nil, err
	}

	file.Close()

	return OpenProjectTree(path)
}

// Updates all file in the project tree
func (o *OncillaProjectTree) UpdateFiles() error {
	return NewNotImplementedMethod("OncillaProjectTree", "UpdateFiles")
}

// Compiles all file in the project tree
func (o *OncillaProjectTree) Compile() error {
	return NewNotImplementedMethod("OncillaProjectTree", "Compile")
}
