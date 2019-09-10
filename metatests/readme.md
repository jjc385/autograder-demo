# Dir `metatests`

Directory to hold tests of the autograder (and utilities) itself.

Not to be confused with the `tests` directory, 
which contains unit tests for students' submissions;
i.e., the actually autograding.

## Types of (meta)tests

### Unit (meta)tests

These test the code itself and run directly in this repository

### Integration tests

* These ensure the autograder is behaving as expected
* These run inside a Docker container which mimics the one used by Gradescope
* A python script, `metatests/compare_test_results.py`, is used to compare
	simulated autograder results against the expected results,
	by examining the results.json output


