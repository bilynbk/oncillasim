// +build linux

package main

import (
	"fmt"
)

type AptManager struct {
}

func (a *AptManager) HasPackage(name string) (bool, error) {
	return false, fmt.Errorf("Not Implemented Yet")
}

func (a *AptManager) InstallPackage(name string) (bool, error) {
	return false, fmt.Errorf("Not Implemented Yet")
}

func (a *AptManager) EnsurePacakage(names []string) error {
	return fmt.Errorf("Not Implemented Yet")
}

func GetPackageManager() (*PackageManager, error) {
	return nil, fmt.Errorf("Not Implemented Yet")
}
