package main

type PackageManager interface {
	HasPackage(name string) (bool, error)
	InstallPackage(name string) (bool, error)
	EnsurePacakage(names []string) error
}
