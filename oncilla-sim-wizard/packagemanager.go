package main

import (
	"fmt"
	"log"
)

type RepositoryDefinition map[string]string

// A package manager is a tool that is used to install software and
// their dependencies. OS independant abstraction of a package
// manager. It needs two concepts :
// 
// * package : represent a software unit.
// * repository : a package manager can often list packages
//   precompiled on a repository. It said listed on the system

type PackageManager interface {
	// Checks if a given package is installed
	HasPackage(name string) (bool, error)
	// Installs a given package
	InstallPackage(name string) error
	// Checks if a repository is listed on a system
	DoesListRepository(repo RepositoryDefinition) (bool, error)
	// Adds the repository in the list of sources of the package
	// manager
	AddRepository(repo RepositoryDefinition) error
}

// Represents all system dependencies
type SystemDependencies struct {
	manager  PackageManager
	packages []string
	repDefs  []RepositoryDefinition
}

// Checks that all system dependencies are met
func (s *SystemDependencies) CheckSystemDependencies() (bool, error) {
	log.Printf("Ensuring that all system dependencies are present....")

	for _, r := range s.repDefs {

		ok, err := s.manager.DoesListRepository(r)
		if err != nil {
			return false, err
		}

		if ok == false {
			return false, fmt.Errorf("Repository %s is not listed", r)
		}

	}

	for _, p := range s.packages {

		ok, err := s.manager.HasPackage(p)
		if err != nil {
			return false, err
		}

		if ok == false {
			return false, fmt.Errorf("Package %s is not installed", p)
		}

	}

	log.Println("done.")

	return true, nil
}

// Ensures that all dependencies are met on the system. Stops on the
// first error
func (s *SystemDependencies) EnsureSystemDependencies() error {

	log.Println("Ensuring all system dependencies are present")

	if err := s.EnsureRepositoryListed(); err != nil {
		return err
	}

	if err := s.EnsurePackages(); err != nil {
		return err
	}

	return nil
}

// Ensures that all repositories are listed on the 
func (s *SystemDependencies) EnsureRepositoryListed() error {

	log.Println("  Ensuring package manager list all repositories")

	for _, r := range s.repDefs {

		listed, err := s.manager.DoesListRepository(r)
		if err != nil {
			return err
		}

		if listed == true {
			log.Println("    Repository `", r, "' is listed in the system.")
			continue
		}

		log.Printf("    Adding repository `%s' to the system.....", r)

		err = s.manager.AddRepository(r)
		if err != nil {
			return err
		}

		log.Println("done.")

	}

	return nil
}

// Ensures that all packages are installed on the system

func (s *SystemDependencies) EnsurePackages() error {

	log.Println("  Ensuring all packages are installed")

	for _, p := range s.packages {

		ins, err := s.manager.HasPackage(p)
		if err != nil {
			return err
		}

		if ins == true {
			log.Println("    Package `", p, "' is installed.")
			continue
		}
		log.Printf("    Installing package `%s'.....", p)
		err = s.manager.InstallPackage(p)
		if err != nil {
			return err
		}
		log.Println("done.")

	}

	return nil
}
