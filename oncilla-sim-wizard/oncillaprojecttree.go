package main

// Represents an Oncilla Simulation project tree
type OncillaProjectTree struct {
	Path string
}

// Tests if the given path is a Oncilla project tree.
func IsProjectTree(path string) (bool, error) {

	if _, err := GetCache(); err != nil {
		return false, err
	}

	return false, NewNotImplementedFunction("IsProjectTree")
}

// Tests if the given path is suitable for creating a new project
// tree, i.e : does not exists, or is an empty directory, or a webots
// directory without oncilla stuff.
func CanCreateProjectTree(path string) (bool, error) {

	return false, NewNotImplementedFunction("IsInstallable")
}

// Opens an existing OncillaProjectTree
func OpenProjectTree(path string) (*OncillaProjectTree, error) {
	return nil, NewNotImplementedFunction("OpenProjectTree")
}

// Creates a new OncillaProjectTree
func CreateProjectTree(path string) (*OncillaProjectTree, error) {
	return nil, NewNotImplementedFunction("CreateProjectTree")
}

// Updates all file in the project tree
func (o *OncillaProjectTree) UpdateFiles() error {
	return NewNotImplementedMethod("OncillaProjectTree", "UpdateFiles")
}

// Compiles all file in the project tree
func (o *OncillaProjectTree) Compile() error {
	return NewNotImplementedMethod("OncillaProjectTree", "Compile")
}
