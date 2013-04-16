// +build linux

package main

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

func GetPackageManager() (*PackageManager, error) {
	return nil, NewNotImplementedFunction("GetPackageManager")
}
