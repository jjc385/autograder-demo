import json
import sys

if __name__ == '__main__':

    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        print("Expected at least one argument -- the json file to read")
        exit(1)

    with open(fname, 'r') as f:
        rawDict = json.load(f)

    for testEntry in rawDict["tests"]:
        message = "{0} New test {0}".format("#"*5)
        padding = "#"*len(message)
        print(padding, message, padding, "", sep='\n')
        for k, v in testEntry.items():
            print("{}:\n{}\n".format(k,v))

