import unittest
from tests.testutils import outputredirected
from tests.testutils.outputredirected import OutputRedirected

import multiprocess as mp
import time

class TestOutputRedirected(unittest.TestCase):

    def test_simple(self):

        lines = ["output line 1", "\toutput line 2"]
        output_expected = "\n".join(lines) + "\n"

        redirector = OutputRedirected()
        @redirector
        def fcn():
            for line in lines:
                print(line)

        fcn()
        output = redirector.get_redirected()
        self.assertEqual(output, output_expected)

    def test_noOutput(self):

        output_expected = ""

        redirector = OutputRedirected()
        @redirector
        def fcn():
            pass

        fcn()
        output = redirector.get_redirected()
        self.assertEqual(output, output_expected)

    def test_nestedRedirects(self):

        redirectorOuter = OutputRedirected()
        redirectorInner = OutputRedirected()

        linesOuter = ["outer output line 1", "\touter output line 2"]
        output_expectedOuter = "\n".join(linesOuter) + "\n"

        linesInner = ["inner output line 1", "\tinner output line 2"]
        output_expectedInner = "\n".join(linesInner) + "\n"

        @redirectorInner
        def fcnInner():
            for line in linesInner:
                print(line)

        @redirectorOuter
        def fcnOuter():
            print(linesOuter[0])
            ind = 1
            fcnInner()
            for i in range(ind, len(linesOuter)):
                print(linesOuter[i])

        fcnOuter()

        outputOuter = redirectorOuter.get_redirected()
        self.assertEqual(outputOuter, output_expectedOuter)

        outputInner = redirectorInner.get_redirected()
        self.assertEqual(outputInner, output_expectedInner)

    def test_serialRedirects(self):

        redirector1 = OutputRedirected()
        redirector2 = OutputRedirected()

        lines1 = ["fcn1 output line 1", "\tfcn1 output line 2"]
        output_expected1 = "\n".join(lines1) + "\n"

        lines2 = ["fcn2 output line 1", "\tfcn2 output line 2"]
        output_expected2 = "\n".join(lines2) + "\n"

        @redirector1
        def fcn1():
            for line in lines1:
                print(line)

        @redirector2
        def fcn2():
            for line in lines2:
                print(line)

        fcn1()
        fcn2()

        output1 = redirector1.get_redirected()
        self.assertEqual(output1, output_expected1)

        output2 = redirector2.get_redirected()
        self.assertEqual(output2, output_expected2)

    def test_exception(self):

        lines = ["output line 1", "\toutput line 2"]
        output_expected = "\n".join(lines[:1]) + "\n"

        redirector = OutputRedirected()
        @redirector
        def fcn():
            for line in lines:
                print(line)
                heres_an_undeclared_name_which_will_raise_an_error

        with self.assertRaises(NameError):
            fcn()

        output = redirector.get_redirected()
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

    def test_multiprocess(self):
        ## Test outputredirected in another process

        lines = ["output line 1", "\toutput line 2"]
        output_expected = "\n".join(lines) + "\n"

        redirector = OutputRedirected()
        @redirector
        def fcn():
            for line in lines:
                print(line)

        process = mp.Process(target=fcn)
        process.start()
        process.join()

        output = redirector.get_redirected()
        self.assertEqual(output, output_expected)


    def test_multiprocess_terminated(self):
        ## Test outputredirected in another process which is forcefully terminated

        lines = ["output line 1", "\toutput line 2"]
        output_expected = "\n".join(lines[:1]) + "\n"

        redirector = OutputRedirected()
        @redirector
        def fcn():
            for line in lines:
                print(line)
                time.sleep(100)

        process = mp.Process(target=fcn)
        process.start()
        process.join(outputredirected.MIN_RUN_TIME)
        process.terminate()

        output = redirector.get_redirected(False)
        self.assertEqual(output, output_expected)


