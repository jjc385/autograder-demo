import unittest
from tests.testutils import timelimited
from tests.testutils.timelimited import TimeLimited

import time

class TestTimeLimited(unittest.TestCase):

    def test_simple_finishing(self):

        lines = ["Output line 1", "\tOutput line 2"]
        output_expected = "\n".join(lines + [""])

        limiter = TimeLimited(timelimited.MIN_RUN_TIME)

        @limiter
        def fcn():
            for line in lines:
                print(line)

        fcn()
        self.assertEqual(limiter.get_output(), output_expected)

    def test_noOutput_finishing(self):
        limiter = TimeLimited(timelimited.MIN_RUN_TIME)

        @limiter
        def fcn():
            pass

        fcn()
        self.assertEqual(limiter.get_output(), "")

    def test_exception(self):

        lines = ["output line 1", "\toutput line 2"]
        output_expected = "\n".join(lines[:1]) + "\n"

        limiter = TimeLimited(timelimited.MIN_RUN_TIME)

        @limiter
        def fcn():
            for line in lines:
                print(line)
                heres_an_undeclared_name_which_will_raise_an_error

        fcn()

        output = limiter.get_output()
        outputSplit = output.split("\n")

        # First the printed line
        self.assertEqual(outputSplit[0], lines[0])
        # The next line is the start of the error traceback
        self.assertEqual(outputSplit[1], "Traceback (most recent call last):")
        # The last (meaningful) line is the text of the error
        self.assertEqual(outputSplit[-2],
                "NameError: name"
                " 'heres_an_undeclared_name_which_will_raise_an_error'"
                " is not defined"
            )
        # The last characters is a newline, so the last "line" is empty
        self.assertEqual(outputSplit[-1], "")

    def test_timeout(self):
        lines = ["output line 1", "\toutput line 2", "output line 3"]
        output_expected = "\n".join(lines[:2]) + "\n"

        limiter = TimeLimited(timelimited.MIN_RUN_TIME)

        @limiter
        def fcn():
            for line in lines[:2]:
                print(line)
            time.sleep(10)
            for line in lines[2:]:
                print(line)

        fcn()

        output = limiter.get_output()
        self.assertEqual(output, output_expected)

    def test_timeoutWithNoOutput(self):
        limiter = TimeLimited(timelimited.MIN_RUN_TIME)

        @limiter
        def fcn():
            time.sleep(10)

        fcn()
        output = limiter.get_output()
        self.assertEqual(output, "")




