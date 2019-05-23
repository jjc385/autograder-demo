import unittest
from gradescope_utils.autograder_utils.decorators import weight

import os

from parameterized import parameterized

with open("required_files.txt", 'r') as f:
    required_files = [ line.strip() for line in f ]


class TestFileExistence(unittest.TestCase):

    @parameterized.expand(
            [ (fname, fname, True) for fname in required_files ]
    )
    @weight(0.01)
    def test_file_existence(self, name, test_input, expected):
        fileExists = os.path.isfile(test_input)
        if fileExists:
            status = "exists"
        else:
            print("WARNING\n")
            status = "DOES NOT exist"
        print("File \"{}\" {} in your submission\n".format(test_input, status))
        self.assertTrue(fileExists)


