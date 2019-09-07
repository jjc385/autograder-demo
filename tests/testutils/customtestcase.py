import unittest
import multiprocessing as mp

import os
import shutil
import tempfile
import sys

class CustomTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.tempdir = None
        #self.createTests()

    ## Old method -- create tests from a list of specs #{{{
    #@classmethod
    #def createTests(cls, source=allTests) :
    #    for i, testObj in enumerate(source) :
    #        cls.createSingleTest(testObj, i)


    #def createSingleTest(cls, testObj, ind=None) :

    #    (name, fcn, correctDict, maxScore, equalityTest, extraArgsToEqualityTest, timeLimit) = testObj.toTuple()

    #    def fcnVsDict(innerSelf, set_score=None ) :
    #        def tempTestFcn() :
    #            for x, fx in correctDict.items() :
    #                if not isinstance(x, tuple) :
    #                    x = (x,)
    #                extraArgs = () if not extraArgsToEqualityTest else (x, fx)
    #                result = fcn(*x)
    #                eqResult = equalityTest( result, fx, *extraArgs )
    #                if eqResult :
    #                    innerSelf.incScore()
    #                    print("Test succeeded -- name:  {}\nx:  {}\nfx:  {}".format(name, x, fx))
    #                else :
    #                    print("Test failed -- name:  {}\nx:  {}\nfx:  {}".format(name, x, fx))

    #        process = mp.Process(target=tempTestFcn)
    #        process.start()
    #        process.join(timeLimit) # Wait `timeLimit` seconds for the process to run or terminate on its own
    #        if process.exitcode is None : # The process is still running
    #            process.terminate()

    #        score = innerSelf.getScore( score_per_test, len(correctDict) )
    #        print("about-to-set score:  ", score)
    #        set_score( score )
    #        return score

    #    testFcn = fcnVsDict
    #    indString = "" if ind is None else "_"+str(ind)
    #    testFcnName = "test_" + testFcn.__name__ + indString + "_" + name
    #    testFcn.__name__ = testFcnName
    #    testFcn = partial_credit(maxScore)(testFcn)

    #    setattr(cls, testFcnName, testFcn)

    ##}}}



    def setUp(self):
        self.scoreQueue = mp.Queue()
#        self.correct_factorial_dict = {0: 1, 1: 1, 2: 2, 3: 6, 4: 24, 5: 120, 6: 720, 7: 5040, 8: 40320, 9: 362880}
#        self.correct_binom_dict={(5,3):10,(5,5):1,(5,1):5,(5,0):1,(3,0):1,(1,0):1,(10,10):1,(10,5):252,(100,51):98913082887808032681188722800,(100,0):1}

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
            self.getRedirected(testFcn.__name__)
        else :
            testFcn(*args)

    def outputRedirected(self, fcn, name) :
        if self.tempdir is None :
            self.tempdir = tempfile.mkdtemp()
        def wrapper(*args, **kwargs) :
            with open(os.path.join(self.tempdir, name), 'w') as f :
                (defOut, defErr) = (sys.stdout, sys.stderr)
                sys.stdout = f
                #sys.stderr = f
                val = fcn(*args, **kwargs)
                (sys.stdout, sys.stderr) = (defOut, defErr) 
            return val
        return wrapper

    def getRedirected(self, name) :
        print("fetching output from test:")
        with open(os.path.join(self.tempdir, name)) as f :
            output = f.read()
            print(output)

        shutil.rmtree(self.tempdir)
        self.tempdir = None



