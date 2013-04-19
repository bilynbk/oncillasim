package main

import (
	"strings"
	"testing"
)

func expectSameMap(t *testing.T, expected, tested map[relDest]relSrce) bool {
	res := true
	for expKey, expValue := range expected {
		testedValue, ok := tested[expKey]
		if ok == false {
			t.Errorf("%s does not contains %s", tested, expKey)
			res = false
			continue
		}
		if testedValue != expValue {
			t.Errorf("Value for `%s' does not match. Expected `%s', got `%s'", expKey, expValue, testedValue)
			res = false
		}
	}
	return res
}

func TestRepositoryListParsing(t *testing.T) {
	fileA := "foo/bar" //same dest
	fileB := "foo/baz" //other dest
	fileBDest := "foo/foo/baz"
	fileC := "foo/boo" //multi dest
	fileCDest1 := "foo/boo"
	fileCDest2 := "foo/foo/boo"

	list := `#This line is a comment
` + fileA + ` # this is commented
` + fileB + ` ` + fileBDest + ` # other destination
` + fileC + ` ` + fileCDest1 + ` # first dest
` + fileC + ` ` + fileCDest2 + ` # second dest
								`

	fileByDest, err := parseRepoListFile(strings.NewReader(list))
	if err != nil {
		t.Errorf("Could not parse list file : %s\nList file is :\n%s", err, list)
	}

	expectedRes := map[relDest]relSrce{
		relDest(fileA):      relSrce(fileA),
		relDest(fileBDest):  relSrce(fileB),
		relDest(fileCDest1): relSrce(fileC),
		relDest(fileCDest2): relSrce(fileC),
	}
	if expectSameMap(t, expectedRes, fileByDest) == false {
		t.Errorf("List files is :\n%s", list)
	}

}
