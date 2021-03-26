package main

import (
	"testing"

	api "github.com/vaslabs/pi-web-agent/pkg"
)

func TestOsReleaseParsing(t *testing.T) {
	expectedOsId := "raspbian"
	os_info := api.OS_Info_From("test-resources", "os-release")

	if os_info.Id != expectedOsId {
		expectationFailure(expectedOsId, os_info.Id, t)
	}
}

func TestTempMeasure(t *testing.T) {
	expectedTemp := "49.2'C"
	temperature := api.Measure_Temperature_From("echo", "temp=49.2'C")
	if (temperature.Temp != expectedTemp) {
		expectationFailure(expectedTemp, temperature.Temp, t)
	}
}

func expectationFailure(expected string, got string, t *testing.T) {
	t.Errorf("Expected %s but got %s", expected, got)
}