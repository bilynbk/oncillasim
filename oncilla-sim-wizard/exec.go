package main

import (
	"fmt"
	"os"
	"os/exec"
)

// Changes dir to path, and report current dir
// Simply use it like :
// if cdir,err := SafeChdir(newPath); err != nil {
//     return err
// } else {
//     defer os.Chdir(cdir)
// }
func SafeChdir(path string) (string, error) {
	curdir, err := os.Getwd()
	if err != nil {
		return "", err
	}

	err = os.Chdir(path)

	return curdir, err

}

func Exists(path string) (bool, error) {
	_, err := os.Stat(path)
	if err == nil {
		return true, nil
	}
	if os.IsNotExist(err) {
		return false, nil
	}
	return false, err
}

func prepareCommand(cmd_ string, args []string) *exec.Cmd {
	cmd := exec.Command(cmd_, args...)

	if options.Verbose == true {
		cmd.Stderr = os.Stderr
		cmd.Stdout = os.Stdout
	} else {
		cmd.Stderr = nil
		cmd.Stdout = nil
	}

	return cmd

}

func RunCommand(cmd_ string, args ...string) error {
	cmd := prepareCommand(cmd_, args)

	if err := cmd.Run(); err != nil {
		return fmt.Errorf("Error while executing %s : %s", cmd.Args, err)
	}

	return nil

}

func RunCommandOutput(cmd_ string, args ...string) ([]byte, error) {
	cmd := prepareCommand(cmd_, args)

	out, err := cmd.Output()

	if err != nil {
		return out, fmt.Errorf("Error while executing %s : %s", cmd.Args, err)
	}

	return out, err

}
