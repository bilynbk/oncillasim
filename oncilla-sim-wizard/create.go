package main

import (
	"fmt"
	"log"
)

type CreateExecuter struct {
}

func (c *CreateExecuter) Execute(args []string) error {
	if len(args) != 1 {
		return fmt.Errorf("You should provide the expected location")
	}
	path := args[0]

	log.Println("Creating new project tree in `", path, "'")

	s, err := GetSystemDependencies()
	if err != nil {
		return err
	}

	_, err = s.CheckSystemDependencies()
	if err != nil {
		return fmt.Errorf("System dependencies are not met, please run `ensure-deps' command first. Depending on your platform you will most certainly need super user rights.\nUnmet dependencies : %s", err)
	}

	if ok, err := CanCreateProjectTree(path); err != nil {
		return fmt.Errorf("Could not create a new project tree in `%s', reason : %s", path, err)
	} else if ok == false {
		return fmt.Errorf("Could not create a new project tree in `%s'.", path)
	}

	oPTree, err := CreateProjectTree(path)
	if err != nil {
		return err
	}

	if err = oPTree.UpdateFiles(); err != nil {
		return err
	}

	if err = oPTree.Compile(); err != nil {
		return err
	}

	log.Printf("Successfuly created new project tree at `%s'", path)

	return nil
}

func init() {
	parser.AddCommand("create",
		"Creates a new base directory for the Oncilla simulator at the specified location",
		"This commands create a new base directory for the Oncilla Simulator. It will fetches all source files, enforce their exact version and build examples. The specified location should either not exists or be an empty directory.",
		&CreateExecuter{})
}
