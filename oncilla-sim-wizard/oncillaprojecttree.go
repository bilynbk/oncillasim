package main

import (
	"bufio"
	"crypto/md5"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"
	"regexp"
)

type relDest string
type relSrce string

// Hexadecimal encoded checksum
type checksum string

// Represents an Oncilla Simulation project tree
type OncillaProjectTree struct {
	Path     string
	dbFile   string
	fileHash map[relDest]checksum
}

const (
	repoListFile = ".oncilla-sim-wizard.list"
	repoMakefile = ".oncilla-sim-wizard.make"
	dbFileName   = ".oncilla-sim-wizard.filedb"
)

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
		fileHash: make(map[relDest]checksum),
	}

	if err = decoder.Decode(opt.fileHash); err != nil && err != io.EOF {
		return nil, err
	}

	return opt, nil
}

// Creates a new OncillaProjectTree
func CreateProjectTree(path string) (*OncillaProjectTree, error) {
	if err := os.MkdirAll(path, 0755); err != nil {
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

// Saves the project tree file database on the system
func (o *OncillaProjectTree) updateFileDb() {

	file, err := os.Create(o.dbFile)
	if err != nil {
		log.Panicf("Could not open tree file database, it may be corrupted. Reason : %s.", err)
	}
	defer file.Close()

	encoder := json.NewEncoder(file)

	err = encoder.Encode(o.fileHash)
	if err != nil {
		log.Panicf("Could not encode tree file database, it may be corrupted. Reason : %s", err)
	}

}

// Parses a list file for the repo. Returns the list of source file *indexed* by their destination
func parseRepoListFile(r io.Reader) (map[relDest]relSrce, error) {
	res := make(map[relDest]relSrce)
	reg, _ := regexp.Compile(`\A\s*([^\s#]+)\s+([^\s#]+)?`)

	reader := bufio.NewReader(r)

	for {
		line, err := reader.ReadString('\n')

		if err == io.EOF {
			break
		} else if err != nil {
			return res, err
		}

		m := reg.FindStringSubmatch(line)
		if m == nil {
			continue
		}

		src := m[1]
		dest := m[2]

		if len(dest) == 0 {
			dest = src
		}

		res[relDest(dest)] = relSrce(src)

	}

	return res, nil
}

func getChecksum(path string) (checksum, error) {
	file, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer file.Close()

	h := md5.New()
	_, err = io.Copy(h, file)
	if err != nil {
		return "", err
	}

	cs := hex.EncodeToString(h.Sum(nil))

	return checksum(cs), nil
}

func copyFile(src, dest string) error {
	srcFile, err := os.Open(src)
	if err != nil {
		return err
	}
	defer srcFile.Close()

	destDir := filepath.Dir(dest)
	if err = os.MkdirAll(destDir, 0755); err != nil {
		return err
	}

	destFile, err := os.Create(dest)
	if err != nil {
		return err
	}
	defer destFile.Close()

	if _, err = io.Copy(destFile, srcFile); err != nil {
		return err
	}

	return nil
}

func (o *OncillaProjectTree) copyFile(srcAbsPath string, dest relDest, cs checksum) error {

	destPath := filepath.Join(o.Path, string(dest))

	if err := copyFile(srcAbsPath, destPath); err != nil {
		return err
	}

	o.fileHash[dest] = cs

	return nil

}

// Givens a cache repo file, a src file and a dest, update the file
func (o *OncillaProjectTree) updateFile(cacheDir string, src relSrce, dest relDest) error {
	destAbsPath := filepath.Join(o.Path, string(dest))
	srcAbsPath := filepath.Join(cacheDir, string(src))

	srcCs, err := getChecksum(srcAbsPath)
	if err != nil {
		return err
	}

	dbCs, controlled := o.fileHash[dest]
	//checks if the file is not under src control
	if controlled == false {
		//if file exists, this is a failure
		if ok, _ := Exists(destAbsPath); ok == true {
			return fmt.Errorf("Error file `%s' already exists, but not under control", dest)
		}

		//now simply copy the file
		if err = o.copyFile(srcAbsPath, dest, srcCs); err != nil {
			return err
		}

		return nil
	}

	//file is under src control, we get installed checksum :
	destCs, err := getChecksum(destAbsPath)
	if os.IsNotExist(err) {
		//user deleted the file, simply reinstall it
		log.Printf("Re-installing deleted file %s", dest)
		if err = o.copyFile(srcAbsPath, dest, srcCs); err != nil {
			return err
		}

		return nil
	} else if err != nil {
		return err
	}

	if dbCs == srcCs {
		//no modification of the file, we skip update. If user
		//modified it, we suppose this is ok
		return nil
	}

	// check if there is user modification
	if destCs != dbCs {
		backupPath := destAbsPath + ".bak"

		log.Printf("It seems that you modified %s, it will be backuped in %s", dest, string(dest)+".bak")
		copyFile(destAbsPath, backupPath)
	}

	//now the target location is free for modification !
	if err = o.copyFile(srcAbsPath, dest, srcCs); err != nil {
		return err
	}

	return nil
}

// Given the path of  a cached repo, updates all the file
func (o *OncillaProjectTree) updateFilesFromRepo(cacheRepoPath string) error {

	file, err := os.Open(filepath.Join(cacheRepoPath, repoListFile))
	if err != nil {

		if os.IsNotExist(err) == true {
			return fmt.Errorf("Repository does not contains any list file `%s'.", repoListFile)
		}

		return err
	}
	defer file.Close()

	filesByDest, err := parseRepoListFile(file)
	if err != nil {
		return err
	}

	for dest, src := range filesByDest {
		err = o.updateFile(cacheRepoPath, src, dest)
		if err != nil {
			return err
		}
	}

	return nil
}

// Updates all file in the project tree
func (o *OncillaProjectTree) UpdateFiles() error {
	// By the fucking awesome power of go, in any case, we will
	// execute this function to maintain the tree database
	defer o.updateFileDb()

	// get the cache

	cache, err := GetCache()
	if err != nil {
		return err
	}

	for n, g := range cache.CachedGitRepositories() {
		log.Printf("Updating files from repo %s", n)
		if err = o.updateFilesFromRepo(g); err != nil {
			return err
		}
	}

	return nil
}

// Returns all directories under control. i.e. contained in the path
// of a sourced file
func (o *OncillaProjectTree) getListOfDirectories() map[string]bool {
	res := make(map[string]bool)

	for file, _ := range o.fileHash {
		for {
			dir := filepath.Dir(string(file))
			if dir == "." {
				break
			}
			res[dir] = true
		}
	}

	return res
}

// Compiles all file in the project tree
func (o *OncillaProjectTree) Compile() error {

	// dirs := o.getListOfDirectories()

	cache, err := GetCache()
	if err != nil {
		return err
	}

	for _, cacheDir := range cache.CachedGitRepositories() {

		//		for dir, _ := range dirs {

		cachedMakefile := filepath.Join(cacheDir, repoMakefile)
		makefile := filepath.Join(o.Path, repoMakefile)

		if ok, _ := Exists(cachedMakefile); ok {

			err = copyFile(cachedMakefile, makefile)
			if err != nil {
				return err
			}

			if err := RunCommand("make", "-f", makefile); err != nil {
				return err
			}
		}

	}
	return nil
}
