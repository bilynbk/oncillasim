// +build linux

package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
)

type AptManager struct {
	repositories map[string]RepositoryDefinition
	distribution string
}

func NewAptManager() (*AptManager, error) {
	if _, err := exec.LookPath("apt-get"); err != nil {
		return nil, fmt.Errorf("Could not find apt-get executable :%s", err)
	}
	if _, err := exec.LookPath("apt-cache"); err != nil {
		return nil, fmt.Errorf("Could not find apt-cache executable :%s", err)
	}
	return &AptManager{
		repositories: map[string]RepositoryDefinition{},
		distribution: "precise",
	}, nil
}

func (a *AptManager) HasPackage(name string) (bool, error) {
	cmd := exec.Command("apt-cache", "policy", name)

	out, err := cmd.Output()
	if err != nil {
		return false, err
	}

	if len(out) == 0 {
		return false, fmt.Errorf("Could not find a package named %s", name)
	}

	if notInstalled, _ := regexp.MatchString(`Installed:\s(none)`, string(out)); notInstalled == true {
		return false, nil
	}

	return true, nil
}

func (a *AptManager) InstallPackage(name string) error {
	args := []string{
		"install",
		"-y",
		name,
	}

	cmd := exec.Command("apt-get", args...)

	cmd.Stdin = os.Stdin
	cmd.Stderr = os.Stderr
	cmd.Stdout = os.Stdout

	if err := cmd.Run(); err != nil {
		return err
	}

	return nil
}

func (a *AptManager) AddRepoFromListFile(listFile string) error {
	return NewNotImplementedMethod("AptManager", "AddRepoFromListFile")
}

func (a *AptManager) UpdateCurrentRepositories() error {
	//I assume here that a debian system should have at least one apt repository listed
	if len(a.repositories) > 0 {
		return nil
	}

	listFiles, err := filepath.Glob("/etc/apt/sources.list.d/*.list")
	if err != nil {
		return err
	}

	listFiles = append(listFiles, "/etc/apt/sources.list")

	for _, l := range listFiles {
		err = a.AddRepoFromListFile(l)
		if err != nil {
			return err
		}
	}

	return nil
}

func (a *AptManager) repDefIsConform(r RepositoryDefinition) (bool, error) {

	if _, hasUrl := r["url"]; hasUrl == false {
		return false, fmt.Errorf("Repository Definition should have an url")
	}

	if _, hasKey := r["key"]; hasKey != false {
		return false, fmt.Errorf("Repository definition should contain a key")
	}

	return true, nil
}

func (a *AptManager) DoesListRepository(r RepositoryDefinition) (bool, error) {
	if err := a.UpdateCurrentRepositories(); err != nil {
		return false, err
	}

	if _, err := a.repDefIsConform(r); err != nil {
		return false, err
	}

	_, ok := a.repositories[r["url"]]

	return ok, nil
}

func (a *AptManager) AddRepository(r RepositoryDefinition) error {
	if err := a.UpdateCurrentRepositories(); err != nil {
		return err
	}

	if _, err := a.repDefIsConform(r); err != nil {
		return err
	}

	components, ok := r["components"]
	if ok == false {
		components = "main"
	}

	//adds repositories key
	cmd := exec.Command("apt-key", "adv", "--fetch-keys", r["key"])

	if err := cmd.Run(); err != nil {
		return err
	}

	//adds repositories sources
	f, err := os.OpenFile("/etc/apt/sources.lists.d/oncilla-sim-wizard.list",
		os.O_RDWR|os.O_CREATE|os.O_APPEND,
		0666)

	if err != nil {
		return err
	}

	fmt.Fprintf(f, "deb %s %s %s\n", r["url"], a.distribution, components)

	//update sources
	cmd = exec.Command("apt-get", "update")

	err = cmd.Run()
	if err != nil {
		return err
	}

	return nil

}

func GetSystemDependencies() (*SystemDependencies, error) {
	cmd := exec.Command("lsb_release", "-i", "-c")

	out, err := cmd.Output()
	if err != nil {
		return nil, fmt.Errorf("I only support ubuntu precise, and I do not seems to be run on this system since I cannot process `lsb_release -i -c' : %s", err)
	}

	isUbuntu, _ := regexp.MatchString("[uU]buntu", string(out))
	isPrecise, _ := regexp.MatchString("[Pp]recise", string(out))

	if isUbuntu != true || isPrecise != true {
		return nil, fmt.Errorf("I do not seems to be runned on ubuntu precise, output of `lsb_release -c -i' is :\n%s", out)
	}

	m, err := NewAptManager()
	if err != nil {
		return nil, err
	}

	return &SystemDependencies{
		manager:  m,
		packages: []string{"liboncilla-webots-dev", "git"},
		repDefs: []RepositoryDefinition{
			RepositoryDefinition{"url": "http://biorob2.epfl.ch/users/tuleu/ubuntu",
				"components": "main",
				"key":        "http://biorob2.epfl.ch/users/tuleu/ubuntu/gpg.key"},
			RepositoryDefinition{"url": "http://packages.cor-lab.de/ubuntu",
				"components": "main",
				"key":        "http://packages.cor-lab.de/keys/corlab.asc"},
		},
	}, nil
}
