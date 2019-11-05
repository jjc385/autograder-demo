import unittest
import multiprocessing as mp

import os
import shutil
import tempfile
import sys

import traceback

class MyTestCase(unittest.TestCase):

    # Setup functions #{{{
    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.tempdir = None

    def setUp(self):
        self.scoreQueue = mp.Queue()

    def incScore(self, delta=1) : 
        self.scoreQueue.put(delta)
        return delta

    def getScore(self, maxScore, intToFloatFactor, initialScore=0) :
        score=initialScore
        while not self.scoreQueue.empty() :
            score += self.scoreQueue.get()
        print( "int score:  {} out of {}".format(score, intToFloatFactor) )

        finalScore = score * maxScore / intToFloatFactor
        print("final score:  {}".format(finalScore))
        return finalScore

    def runTestFcn( self, testFcn, timeLimit=0, process=True ) : 
        args = ()
        if process :
            redirected = self.outputRedirected(testFcn, testFcn.__name__)
            process = mp.Process(target=redirected, args=args)
            process.start()
            process.join(timeLimit) # Wait `timeLimit` seconds for the process to run or terminate on its own
            if process.exitcode is None : # The process is still running
                process.terminate()
                print("Test timed out")
            self.getRedirected(testFcn.__name__)
        else :
            testFcn(*args)

    def outputRedirected(self, fcn, name) :
        if self.tempdir is None :
            self.tempdir = tempfile.mkdtemp()
        def wrapper(*args, **kwargs) :
            error = None
            with open(os.path.join(self.tempdir, name), 'w') as f :
                val = None
                sys.stdout = f
                try :
                    val = fcn(*args, **kwargs)
                except Exception as theError :
                    traceback.print_exc(file=f)
                    error = theError
                finally :
                    sys.stdout = sys.__stdout__
            if error is not None :
                raise error
            return val
        return wrapper

    def getRedirected(self, name) :
        print("fetching output from test:")
        with open(os.path.join(self.tempdir, name)) as f :
            output = f.read()
            print(output)

        shutil.rmtree(self.tempdir)
        self.tempdir = None


    #}}}
