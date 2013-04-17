// +build linux

package main

import (
	"fmt"
	"os/exec"
	"regexp"
)

type AptManager struct {
}

func NewAptManager() (*AptManager, error) {
	if _, err := exec.LookPath("apt-get"); err != nil {
		return nil, fmt.Errorf("Could not find apt-get executable :%s", err)
	}
	if _, err := exec.LookPath("apt-cache"); err != nil {
		return nil, fmt.Errorf("Could not find apt-cache executable :%s", err)
	}
	return &AptManager{}, nil
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
	return NewNotImplementedMethod("AptManager", "InstallPackage")
}

func (a *AptManager) DoesListRepository(r RepositoryDefinition) (bool, error) {
	return false, NewNotImplementedMethod("AptManager", "DoesListRepository")
}

func (a *AptManager) AddRepository(r RepositoryDefinition) error {
	return NewNotImplementedMethod("AptManager", "AddRepository")
}

func GetPackageManager() (*SystemDependencies, error) {
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
