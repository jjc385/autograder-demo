import sys

def checkForTodos(fnameToCheck):
    """Check for file containing todos

    If there are TODOs found, print them

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
                if len(line) > 0 and line[0] == '*':
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
        exit(2)

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

