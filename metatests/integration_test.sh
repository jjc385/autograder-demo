#!/usr/bin/env bash

## Script to run integration tests (see metatests/readme.md)
##	* Intended to be run in a docker container simulating
##		Gradescope's autograder, as defined in metatests/Dockerfile

cd /autograder

# Copy the sample submission into the correct directory
cp -r source/sample_submission/ submission/ 

# Create the directory where results.json will live
mkdir results 

# Run the (simulated) autograder
./run_autograder 

# Print the autograder results for easy inspection
cat results/results.json

# Compare the results against the expected results
#	* Will return nonzero if the results differ
python3 source/metatests/compare_autograder_results.py \
	results/results.json \
	submission/results_expected.json
