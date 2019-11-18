import sys

def isTodoLine(line):
    """Check whether the given line (a string) is considered a TODO line

    TODO lines are formatted like top-level markdown bullet points
    
    * Starts with `*` or `-`
    * Doesn't have ` [x]` or ` [X]` as the following chars
    * No white space before the first character
    """

    ## ensure line is a string
    if not isinstance(line, str):
        return False

    ## check first character
    if len(line) < 1:
        return False
    firstChar = line[0]
    allowedStartingChars = {'*', '-'}
    if firstChar not in allowedStartingChars:
        return False

    ## ensure following characters don't indicate a checked off list
    if len(line) >= 5:
        nextChars = line[1:5]
        allowedNextChars = { ' [{}]'.format(x) for x in ('x', 'X') }
        if nextChars in allowedNextChars:
            return False

    return True


def checkForTodos(fnameToCheck):
    """Check for file containing todos

    If there are TODOs found, print them
    See documentation for `isTodoLine` for which lines are considered todos

    Return the exit code to return to the shell

    0 -- No TODOs; all is well
    1 -- TODOs found
    2 -- TODO file not found
    3 -- No/ invalid TODO file name specified
    """

    ## ensure fnameToCheck is valid
    if ( fnameToCheck is None 
           or not isinstance(fnameToCheck, str) 
           or len(fnameToCheck) < 1
        ):
        return 3

    try:
        ## attempt to open file
        with open(fnameToCheck, 'r') as f:
            for line in f:
                if isTodoLine(line):
                    ## TODOs have been found
                    return 1

    except FileNotFoundError:
        ## file containing TODOs not found
        return 2

    ## no TODOs found; all is well
    return 0


if __name__ == '__main__':

    if len(sys.argv) > 1:
        fnameToCheck = sys.argv[1]
    else:
        print("Expected one argument -- path to the file to check for TODOs")
        exit(3)

    statusCode = checkForTodos(fnameToCheck)
    if statusCode == 1:
        print("TODOs have been found:  \n\n")
        ## echo the TODOs file
        with open(fnameToCheck, 'r') as f:
            for line in f:
                print(line)
    elif statusCode == 2:
        print(
                "Could not find file with potential TODOs"
                "\nThis file should still be present even if there are no"
                "TODOs.  In such a case it can be empty"
            )
    elif statusCode == 3:
        print("Invalid filename argument")

    exit(statusCode)

