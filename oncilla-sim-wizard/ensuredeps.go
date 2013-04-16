package main

import (
	"fmt"
)

type EnsureDependencyExecuter struct {
	//for future extension
	//Dry bool `short:"y" long:"dry-run" description:"Do not install anything, just perform a dry run"`
}

func (e *EnsureDependencyExecuter) Execute(args []string) error {
	if len(args) > 0 {
		return fmt.Errorf("ensure-deps do not take arguments")
	}

	return NewNotImplementedMethod("EnsureDependencyExecuter", "Execute")
}

func init() {
	parser.AddCommand("ensure-deps",
		"Ensures that all dependency of the simulator are installed on the system",
		"Depending on the current OS, it will use a supported package manager to check that dependencies are installed on the system",
		&EnsureDependencyExecuter{})

}
