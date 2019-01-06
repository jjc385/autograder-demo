import unittest
from gradescope_utils.autograder_utils.decorators import weight
import os.path


class TestEvaluator(unittest.TestCase):
    def setUp(self):
        pass

    @weight(0.01)
    def test_py(self):
        """Test existence of sample_module.py"""
        self.assertTrue(os.path.isfile("sample_module.py"))

    @weight(0.01)
    def test_ipynb(self):
        """Test existence of sample_report.ipynb"""
        self.assertTrue(os.path.isfile("sample_report.ipynb"))

