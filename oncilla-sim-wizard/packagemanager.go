package main

type PackageManager interface {
	HasPackage(name string) (bool, error)
	InstallPackage(name string) error
}

func EnsurePackages(pm PackageManager, packages []string) error {
	for _, p := range packages {
		ins, err := pm.HasPackage(p)
		if err != nil {
			return err
		}

		if ins == true {
			continue
		}

		err = pm.InstallPackage(p)
		if err != nil {
			return err
		}
	}
	return nil
}
