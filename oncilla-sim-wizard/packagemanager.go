package main

type PackageManager interface {
	HasPackage(name string) (bool, error)
	InstallPackage(name string) (bool, error)
}

func EnsurePackages(p *PackageManager, name []string) error {
	return NewNotImplementedFunction("EnsurePackages")
}
