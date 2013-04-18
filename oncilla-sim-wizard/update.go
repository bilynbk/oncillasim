package main

import (
	"fmt"
)

// Executer for "update" command
type UpdateExecuter struct {
}

func (e *UpdateExecuter) Execute(args []string) error {
	if len(args) != 1 {
		return fmt.Errorf("`update' command need the path")
	}

	path := args[0]

	if ok, err := IsProjectTree(path); err != nil {
		return fmt.Errorf("Could not update `%s' as it does not seem to be a project tree, reason : %s",
			path,
			err)
	} else if ok != false {
		return fmt.Errorf("Could not update `%s' as it does not seem to be a project tree.",
			path)
	}

	oPTree, err := OpenProjectTree(path)
	if err != nil {
		return nil
	}

	if err = oPTree.UpdateFiles(); err != nil {
		return err
	}

	if err = oPTree.Compile(); err != nil {
		return err
	}

	return nil
}

func init() {
	parser.AddCommand("update",
		"Updates an existing Oncilla simulator project tree",
		"Updates the project tree given as a mandatory argument. It will try to update all the file to the last version. It will try to detect modification of the file of the project inside the project tree, and detect conflicts",
		&UpdateExecuter{})

}
