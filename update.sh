cd /autograder/source

## Pull from git
# * /autograder/source must be a git repository, meaning autograder.zip must
# 	    have contained a .git directory
# * The correct branch must already be checked out
# * The current branch should be set to track the desired upstream branch on
#       the already-configured remote, so that `git pull` works correctly
# * The remote must have an ssh url (e.g., git@github.com:<username>/<repo>),
#       not an http url (e.g., http://www.github.com/<username>/<repo>)
git pull

## Install (updated) python requirements
pip3 install -r python-requirements.txt
