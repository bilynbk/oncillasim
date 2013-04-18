package main

import (
	"fmt"
	"log"
)

type RepositoryDefinition map[string]string

type PackageManager interface {
	HasPackage(name string) (bool, error)
	InstallPackage(name string) error
	DoesListRepository(repo RepositoryDefinition) (bool, error)
	AddRepository(repo RepositoryDefinition) error
}

type SystemDependencies struct {
	manager  PackageManager
	packages []string
	repDefs  []RepositoryDefinition
}

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
