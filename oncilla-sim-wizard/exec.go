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

func RunCommand(cmd string, args ...string) error {
	cmd_ := exec.Command(cmd, args...)

	if options.Verbose == true {
		cmd_.Stderr = os.Stderr
		cmd_.Stdout = os.Stdout
	} else {
		cmd_.Stderr = nil
		cmd_.Stdout = nil
	}

	if err := cmd_.Run(); err != nil {
		return fmt.Errorf("Error while executing %s : %s", cmd_.Args, err)
	}

	return nil

}
