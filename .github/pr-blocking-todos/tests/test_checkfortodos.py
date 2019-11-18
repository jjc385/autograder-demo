from checkfortodos import checkForTodos, isTodoLine

import unittest

class TestCheckForTodos(unittest.TestCase):

    def test_isTodoLine_yesAndNo(self):

        startingChars = ["*", "-"]
        todoLinesRaw = [
                "{}",
                "{} ",
                "{} this is a line",
                "{} here's a newline \n",
                "{} now a tab \t",
                "{}even with no space after the starting char",
                "{} [ ]", 
                "{} [ ] with stuff after",
                "{} [Y] having the wrong fill-in character",
            ]
        todoLines = [ 
                raw.format(startingChar) 
                for raw in todoLinesRaw 
                for startingChar in startingChars 
            ] + [
                "*- multiple start chars",
                "-* again, multiple start chars",
            ]

        notTodoLinesRaw = [
                " {} space before start char",
                "\t{} tab before start char",
                "text before start char {} (and after too)",
                "{} [x]", 
                "{} [X]", 
                "{} [x] with stuff after",
                "{} [X] with stuff after",
            ]
        notTodoLines = [ 
                raw.format(startingChar) 
                for raw in notTodoLinesRaw 
                for startingChar in startingChars 
            ] + [
                "",
                "\n",
            ]
                
        for line in todoLines:
            with self.subTest("expecting True:  line: `{}`".format(line)):
                value = isTodoLine(line)
                self.assertTrue(value, "line: `{}`".format(line))

        for line in notTodoLines:
            with self.subTest("expecting False:  line: `{}`".format(line)):
                value = isTodoLine(line)
                self.assertFalse(value, "line: `{}`".format(line))

    def test_isTodoLine_invalid(self):

        invalidInputLines = [
                None,
                10,
                [1,2,3],
            ]

        for invalidLine in invalidInputLines:
            with self.subTest("expecting False:  line: `{}`".format(invalidLine)):
                value = isTodoLine(invalidLine)
                self.assertFalse(value, "line: `{}`".format(invalidLine))



