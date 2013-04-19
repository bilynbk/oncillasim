package main

import (
	"bytes"
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

func prepareCommand(cmd_ string, args []string) (*exec.Cmd, *bytes.Buffer) {
	cmd := exec.Command(cmd_, args...)

	if options.Verbose == true {
		cmd.Stderr = os.Stderr
		cmd.Stdout = os.Stdout
		return cmd, nil
	}

	var out bytes.Buffer
	cmd.Stderr = &out
	cmd.Stdout = &out

	return cmd, &out

}

func RunCommand(cmd_ string, args ...string) error {
	cmd, out := prepareCommand(cmd_, args)

	if err := cmd.Run(); err != nil {
		if options.Verbose {
			return fmt.Errorf("Error while executing %s : %s", cmd.Args, err)
		} else {
			return fmt.Errorf("Error while executing %s : %s\nProgram out :\n%s", cmd.Args, err, out)
		}
	}

	return nil

}

func RunCommandOutput(cmd_ string, args ...string) ([]byte, error) {
	cmd, cerr := prepareCommand(cmd_, args)

	cmd.Stdout = nil

	out, err := cmd.Output()

	if err != nil {
		if options.Verbose {
			return out, fmt.Errorf("Error while executing %s : %s", cmd.Args, err)
		} else {
			return out, fmt.Errorf("Error while executing %s : %s\n.Program stderr :\n%s", cmd.Args, err, cerr)
		}
	}

	return out, err

}
