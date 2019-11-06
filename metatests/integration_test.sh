#!/usr/bin/env bash

## Script to run a single integration test (see metatests/readme.md)
##	* Intended to be run in a docker container simulating
##		Gradescope's autograder, as defined in metatests/Dockerfile

cd /autograder

## Set parameters based on script arguments
if [[ $# -eq 0 ]]; then # zero arguments
	## use defaults for the first integration test
	source_dir="source/sample_submission"
	required_files_dir="source/"
elif [[ $# -eq 1 ]]; then # one argument
	## same source and required_files directories
	source_dir="$1"
	required_files_dir="$source_dir"
else	# two or more arguments
	## different (non-default) source and required_files directories
	source_dir="$1"
	required_files_dir="$2"
fi

echo ""
echo "###########"
echo "## Running integration test for sample submission located at: $source_dir ##"
echo "###########"
echo ""

# Copy the sample submission into the expected directory
cp -r "$source_dir" submission/ 

# Move the required_files.txt file to the expected location
mv "$required_files_dir/required_files.txt" "source/required_files.txt"

# Create the directory where results.json will live
mkdir results 

# Run the (simulated) autograder
./run_autograder 

# Print the autograder results for easy inspection
echo "[Printing results.json]"
cat results/results.json
echo " "
echo "[Pretty printing test results]"
python3 source/metatests/print-json-results.py results/results.json
echo " "
echo " "

# Compare the results against the expected results
#	* Will return nonzero if the results differ
echo "[Compare against expected results.json]"
python3 source/metatests/compare_autograder_results.py \
	results/results.json \
	"$source_dir/results_expected.json"



