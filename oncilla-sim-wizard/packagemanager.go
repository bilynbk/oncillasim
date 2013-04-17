package main

import (
	"fmt"
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

func (s *SystemDependencies) SystemDependenciesAreMet() (bool, error) {

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

	return true, nil
}

func (s *SystemDependencies) EnsureSystemDependencies() error {

	if err := s.EnsureRepositoryListed(); err != nil {
		return err
	}

	if err := s.EnsurePackages(); err != nil {
		return err
	}

	return nil
}

func (s *SystemDependencies) EnsureRepositoryListed() error {
	for _, r := range s.repDefs {

		listed, err := s.manager.DoesListRepository(r)
		if err != nil {
			return err
		}

		if listed == true {
			continue
		}

		err = s.manager.AddRepository(r)
		if err != nil {
			return err
		}

	}

	return nil
}

func (s *SystemDependencies) EnsurePackages() error {
	for _, p := range s.packages {

		ins, err := s.manager.HasPackage(p)
		if err != nil {
			return err
		}

		if ins == true {
			continue
		}

		err = s.manager.InstallPackage(p)
		if err != nil {
			return err
		}

	}

	return nil
}
