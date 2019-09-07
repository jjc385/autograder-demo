import operator
from gradescope_utils.autograder_utils.decorators import weight, partial_credit

class TestingException(Exception) :
    pass

class ArgSpec :
    def __init__(self, *args, **kwargs) :
        self.args = args
        self.kwargs = kwargs

    def call(self, fcn) :
        return fcn(*self.args, **self.kwargs)

class FcnTest :
    #{{{

    _fieldDict = {
            'fcn' :   None,
            'name' :  None,
            'maxScore' :    10, 
            'timeLimit' :   10, # in seconds
            'equalityTest' :  operator.eq,
            'extraArgsToEqualityTest' : False
        }


    def __init__( self, overwriteFields=True, **kwargs ) :
        self.fieldsFromDict(**kwargs, overwriteFields=overwriteFields)


    def fieldsFromDict( self, theDict={}, overwriteFields = False, **kwargs ) :
        newDict = {**theDict, **kwargs}
        for var, defVal in self.fieldDict().items() :
            writeQ = overwriteFields
            val = defVal
            if var in newDict :
                writeQ = True
                val = newDict.pop(var)
            if writeQ :
                # update value
                setattr(self, var, val)

        if len(newDict) > 0 :
            raise TestingException( "Unknown vars passed in dict or kwargs:  ", newDict )

    def fieldDict(self) :
        return self._fieldDict

    def addTestFcn( self, unittestCls ) :
        testFcn = self.toTestFcn()
        setattr(unittestCls, testFcn.__name__, testFcn)

    def toTestFcn( self ) :
        testFcn = self.toTestFcnBase()
        testFcn = partial_credit(self.maxScore)(testFcn)
        testFcn.__name__ = self.testName()
        return testFcn

    def toTestFcnBase(self) :
        def testFcn(testCaseSelf, set_score=None) : 
            def tempTestFcn() :
                self.toInnerTestFcn(testCaseSelf)
            testCaseSelf.runTestFcn(tempTestFcn, self.timeLimit, process=True)
            score = testCaseSelf.getScore(self.maxScore, self.maxIntScore())
            set_score(score)
        return testFcn

    def toInnerTestFcn(self, testCaseSelf) :
        raise Exception("toInnerTestFcn not implemented")

    def maxIntScore(self) :
        raise Exception("maxIntScore not implemented")


    def testName( self ) :
        testName = "test_" + self.name
        return testName

    def setFcn(self, fcn, name=None) :
        if fcn is None :
            return
        self.fcn = fcn
        self.name = fcn.__name__ if name is None else name

    def call(self, fcn, argSpec ) :
        if isinstance(argSpec, tuple) :
            return fcn(*argSpec)
        elif isinstance(argSpec, ArgSpec) :
            return argSpec.call(fcn)
        else :
            return fcn(argSpec)





    #}}}


class FcnVsDictTest( FcnTest ) :
    #{{{

    _newFieldDict = {
            'correctDict' : None
        }

    def __init__(self, **kwargs) :
        self.fieldsFromDict(overwriteFields=True, **kwargs)

    def toInnerTestFcn(self, testCaseSelf) :
        for x, fx in self.correctDict.items() :
            extraArgs = () if not self.extraArgsToEqualityTest else (x, fx)
            result = self.call(self.fcn, x)
            eqResult = self.equalityTest( result, fx, *extraArgs )
            if eqResult :
                testCaseSelf.incScore()
                print("Test succeeded -- name:  {}\nx:  {}\nfx:  {}".format(self.name, x, fx))
            else :
                print("Test failed -- name:  {}\nx:  {}\nfx:  {}".format(self.name, x, fx))

    def maxIntScore(self) :
        return len(self.correctDict)


    def fieldDict(self) :
        return {**super().fieldDict(), **self._newFieldDict}

    #}}}


class FcnVsFcnTest( FcnTest ) :
    #{{{

    _newFieldDict = {
            'correctFcn' : None,
            'inputList'  : None
        }

    def __init__(self, **kwargs) :
        self.fieldsFromDict(overwriteFields=True, **kwargs)

    def toInnerTestFcn(self, testCaseSelf) :
        for x in self.inputList :
            if not isinstance(x, tuple) :
                x = (x,)
            extraArgs = () if not self.extraArgsToEqualityTest else (x, self.correctFcn)
            result = self.call(self.fcn, x)
            correctResult = self.call(self.correctFcn, x)
            eqResult = self.equalityTest( result, correctResult, *extraArgs )
            fx=correctResult
            if eqResult :
                testCaseSelf.incScore()
                print("Test succeeded -- name:  {}\nx:  {}\nfx:  {}".format(self.name, x, fx))
            else :
                print("Test failed -- name:  {}\nx:  {}\nfx:  {}".format(self.name, x, fx))

    def maxIntScore(self) :
        return len(self.inputList)

    def fieldDict(self) :
        return {**super().fieldDict(), **self._newFieldDict}

    #}}}


if __name__ == '__main__' :

    def square( x ) : x**2
    FcnTest()
    FcnTest(fcn=square)
    
    FcnVsDictTest()
    FcnVsDictTest(fcn=square, correctDict={2.0:4.0})

    FcnVsFcnTest()
    FcnVsFcnTest(fcn=square, correctFcn=square, inputList=[1,2,3])



