#!/usr/bin/env bash
cd /autograder

mkdir results 
cp -r source/sample_submission/ submission/ 
./run_autograder 
cat results/results.json

python3 source/metatests/compare_autograder_results.py \
	results/results.json \
	submission/results_expected.json
