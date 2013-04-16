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
	return nil, NewNotImplementedFunction("NewAptManager")
}

func (a *AptManager) HasPackage(name string) (bool, error) {
	return false, NewNotImplementedMethod("AptManager", "HasPackage")
}

func (a *AptManager) InstallPackage(name string) (bool, error) {
	return false, NewNotImplementedMethod("AptManager", "InstallPackage")
}

func GetPackageManager() (PackageManager, error) {
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

	return NewAptManager()
}
