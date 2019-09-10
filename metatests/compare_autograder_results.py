import sys
import json

def compare_autograder_results(fname_actual, fname_expected):
    """Compare the json results of two gradescope autograder runs

    Return the number of meaningful differences between the results
    """

    with open(fname_actual, 'r') as f:
        actual = json.load(f)
    with open(fname_expected, 'r') as f:
        expected = json.load(f)

    diff_count = 0

    ignored_keys = set()
    ignored_keys.add("execution_time")
    checked_keys = set()

    ## Verify results of all tests are identical
    checked_keys.add("tests")
    if len(actual["tests"]) != len(expected["tests"]):
        print("Expected results to mention {} tests, not {}"
                .format(len(expected["tests"]), len(actual["tests"]))
            )
        diff_count += 1
    for testDict_expected, testDict_actual in zip(expected["tests"], actual["tests"]):
        for key in testDict_expected:
            if testDict_actual[key] != testDict_expected[key]:
                print("Mismatch in key {} "
                        "between expected test {} "
                        "and actual test {}"
                        .format(key, testDict_expected, testDict_actual)
                    )
                diff_count += 1

    ## Check total scores
    checked_keys.add("score")
    if actual["score"] != expected["score"]:
        print("Expected total score to be {}, not {}"
                .format(expected["score"], actual["score"])
            )
        diff_count += 1

    ## Check remaining expected keys at top level in the json dict
    for key in expected:
        if key in checked_keys or key in ignored_keys:
            continue
        if actual[key] != expected[key]:
            print("Expected key {} to have value {}, not {}"
                    .format(key, expected[key], actual[key])
                )
            diff_count += 1

    return diff_count
                    



if __name__ == '__main__':
    if len(sys.argv) < 2+1:
        raise Error("Expected two filenames as arguments")

    fname_actual = sys.argv[1]
    fname_expected = sys.argv[2]

    diff_count = compare_autograder_results(fname_actual, fname_expected)
    exit(diff_count)

