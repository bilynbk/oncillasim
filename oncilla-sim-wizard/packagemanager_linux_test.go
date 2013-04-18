package main

import (
	"strings"
	"testing"
)

func TestDebianRepositoryListFileParsing(t *testing.T) {
	m := AptManager{}

	m.repositories = make(map[string]RepositoryDefinition)

	fooUrl := "https://foo.bar.com/ubuntu"
	barUrl := "http://bar.bar.com/ubuntu"

	fooCpts := "main"
	barCpts := "main testing free universe"

	aptFile := `# This a comment it should not be parsed
deb ` + fooUrl + ` precise ` + fooCpts + ` # comment
# deb http://bite.com/ubuntu lucid should_not_appear
deb ` + barUrl + ` precise ` + barCpts + `
`

	if err := m.addRepoFromList(strings.NewReader(aptFile)); err != nil {
		t.Errorf("Could not parse the file : %s", err)
	}

	_, containsComment := m.repositories["http://bite.com/ubuntu"]
	if containsComment == true || len(m.repositories) > 2 {
		t.Errorf("Manager %s contains a commented repository listing", m)
	}

	foo, containsFoo := m.repositories[fooUrl]
	bar, containsBar := m.repositories[barUrl]

	if containsFoo == false || containsBar == false {
		t.Errorf("Parsing is incomplete : %s", m)
	}

	if foo["components"] != fooCpts {
		t.Errorf("Mismatched %s components, got : `%s' , expected `%s'", fooUrl, foo["components"], fooCpts)
	}

	if bar["components"] != barCpts {
		t.Errorf("Mismatched %s components, got : `%s' , expected `%s'", barUrl, bar["components"], barCpts)
	}

}
