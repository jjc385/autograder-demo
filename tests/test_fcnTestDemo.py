from testutils.fcntest import FcnVsDictTest
from testutils.mytestcase import MyTestCase

from sample_module import return_integer, return_integer_list


class TestModule(MyTestCase):
    pass

allTests = []

## set up tests

# test return_integer
testDict = {
        (1,1): 2,
        (0,0): 0,
        (3,):  5,
        }
test = FcnVsDictTest()
test.setFcn(return_integer)
test.correctDict = testDict
allTests.append(test)

# test return_integer_list
testDict = {
        (1,1): [1,1],
        (0,0): [0,0],
        (3,):  [3,2],
        }
test = FcnVsDictTest()
test.setFcn(return_integer_list)
test.correctDict = testDict
allTests.append(test)



## handle scoring

totalScore = 5

weightTotal = 0
for test in allTests :
    weightTotal += test.maxScore

## add tests

for test in allTests :
    test.maxScore *= totalScore / weightTotal
    test.addTestFcn(TestModule)
