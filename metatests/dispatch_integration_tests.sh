#!/usr/bin/env bash

## Script to dispatch all integration tests
##  * Runs each integration test in a separate docker container
##	* Runs one from the sample_submission directory
##	* Discovers others from the metatests/additional_sample_submissions directory

## Make script exit early if a command fails, as well as echo each command before executing it
set -ev  

dispatch_integration_test () {
	echo "Dispatching integration tests with arguments:  $@"
	docker run autograder /bin/sh -c \
		"chmod +x source/metatests/integration_test.sh && ./source/metatests/integration_test.sh $@"
}

## run first integration test, with default parameters
dispatch_integration_test

## run additional integration tests
##	* check all subdirectories of metatests/additional_sample_submissions
for dirname in metatests/additional_sample_submissions/*; do
	## Only dispatch an integration test if the subdirectory contains a results_expected.json file
	if [[ -f "$dirname/results_expected.json" ]]; then
		dispatch_integration_test "source/$dirname"
	fi
done

