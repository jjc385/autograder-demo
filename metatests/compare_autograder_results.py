import sys
import json

def compare_autograder_results(fname_actual, fname_expected):

    with open(fname_actual, 'r') as f:
        actual = json.load(f)

    with open(fname_expected, 'r') as f:
        expected = json.load(f)

    all_correct = True

    ignored_keys = set()
    ignored_keys.add("execution_time")

    checked_keys = set()
    ## verify tests are identical
    checked_keys.add("tests")
    if len(actual["tests"]) != len(expected["tests"]):
        print("Expected results to mention {} tests, not {}"
                .format(len(expected["tests"]), len(actual["tests"]))
            )
        all_correct = False
    for testDict_expected, testDict_actual in zip(expected["tests"], actual["tests"]):
        for key in testDict_expected:
            if testDict_actual[key] != testDict_expected[key]:
                print("Mismatch in key {} "
                        "between expected test {} "
                        "and actual test {}"
                        .format(key, testDict_expected, testDict_actual)
                    )
                all_correct = False

    ## Check total scores
    checked_keys.add("score")
    if actual["score"] != expected["score"]:
        print("Expected total score to be {}, not {}"
                .format(expected["score"], actual["score"])
            )
        all_correct = False

    ## Check remaining expected keys
    for key in expected:
        if key in checked_keys or key in ignored_keys:
            continue
        if actual[key] != expected[key]:
            print("Expected key {} to have value {}, not {}"
                    .format(key, expected[key], actual[key])
                )

    return all_correct
                    



if __name__ == '__main__':
    if len(sys.argv) < 2+1:
        raise Error("Expected two filenames as arguments")

    fname_actual = sys.argv[1]
    fname_expected = sys.argv[2]

    all_correct = compare_autograder_results(fname_actual, fname_expected)
    exit(0 if all_correct else 1)

