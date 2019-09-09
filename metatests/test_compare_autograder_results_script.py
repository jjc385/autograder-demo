import sys
import unittest
from compare_autograder_results import compare_autograder_results

class TestCompareAutograderResults(unittest.TestCase):
    """Test the script used to compare autograder results"""

    def setUp(self):
        path = "metatests/test_files/"
        self.fname1 = path+"results_simple1.json"
        self.fname2 = path+"results_simple2.json"  ## only execution time differs from simple1
        self.fname3 = path+"results_simple3.json"  ## one test result differs from simple1 

    def test_compareIdentical(self):
        self.assertTrue( compare_autograder_results(self.fname1, self.fname1) )

    def test_compareEquivalent(self):
        self.assertTrue( compare_autograder_results(self.fname1, self.fname2) )

    def test_compareDifferent(self):
        sys.stdout = None  ## Redirect stdout to ignore print statements
        self.assertFalse( compare_autograder_results(self.fname1, self.fname3) )
        sys.stdout = sys.__stdout__

