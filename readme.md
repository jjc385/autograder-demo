# Gradescope autograder demo

## About this project

I (Jared Claypooole) created this repository
to rebuild and document the enhancements
I made to [Gradescope][gradescope.com]'s
example [python autograder][gs-py-autograder] implemenation.
See also Gradescope's [autograder documentation][gs-autograder-docs].

I made these changes in their original form
to fit the needs of our course
while working as a teaching assistant
for UCLA's Physics 180N course (Computational Physics Lab),
supervised by the course instructor Josh Samani.

[gradescope.com]: https://www.gradescope.com/
[gs-autograder-docs]: https://gradescope-autograders.readthedocs.io/en/latest/
[gs-py-autograder]: https://github.com/gradescope/autograder_samples/tree/master/python/src

### Development notes

I originally made these modifications in a fairly "quick and dirty" manner,
with a lot of things I've since decided to clean up.
I also need to keep private the exact tests we developed
to (partially) grade students' code,
so that these may be reused in future iterations of the course.

As such, I've created this separate public demo,
so that others may adapt my autograder improvements to their courses.
I've attempted to use the following principles to improve the quality of the
project:

* Write cleaner code that's easier to read and maintain
* Use automated (meta) tests to unit test the code
* Employ integration tests (in a Docker container) to simulate Gradescope's
  use of the autograder and make sure everything is working properly
* Simulate a review process by reviewing github pull requests
  and addressing issues identified there
* Include better project and code documentation for ease of use

## Project progress

My original modifications included 5 major changes:

* pull-from-git
  * Allow updates to the autograder to be dynamically pulled via git
* required-files
  * Automate filename copying and checking (with feedback to students)
* time-limited
  * Integrate time limits by running tests in their own processes, redirecting stdout/stderr
* fcn-tests
  * Automate scanning a matrix of parameters in tests, particularly for numerical functions
* correct-with-git
  * Create a framework for grader to incrementally correct students' code using git,
    preventing minor mistakes from disproportionately affecting grades

So far, the first two changes have been merged into this project,
and the remaining are in development
(likely with some code being pushed on branches on this repo,
or even with open pull requests).

### pull-from-git

Gradescope's default autograder configuration workflow requires
the grader to upload the autograder in a zip file,
which Gradescope then uses to build a Docker image --
an image which will then be used to spawn an autograder instance
every time the autograder is run on a students' submission.
The problem is that this build process takes a few minutes,
and this Docker image needs to be rebuilt every time
the grader wishes to make a change to the autograder.
This often creates a frustrating bottleneck in the debugging process.

With this pull-from-git enchancement,
we can circumvent the need to rebuild the autograder image
by downloading updates dynamically via git.
Every time the autograder is run on a student's assignment submission,
the autograder checks for any updates that have been pushed to the
remote repository since the autograder was configured
(i.e., since the project directory was zipped and uploaded to Gradescope's
website, and the setup script was run).
The autograder uses the settings in the project's `.git` directory
to pull any such updates.


Notes:

* This type of enhancement was explicitly
  [suggested][gs-docs-pull-from-git]
  in the Gradescope's autograder docs,
  and my code is partially based on their
  [example code][gs-gh-pull-from-git-ex].
* The update process is performed
  not only just before the autograder is run on a student's submission,
  but also just after
  the autograder is uploaded to Gradescope -- when `setup.sh` is run
* The autograder runs `git reset --hard` before doing this,
  which is a workaround for Windows users.  This means that any changes to the
  autograder *must* be committed (using `git commit`) before being uploaded
  (see [issue \#2][issue-2])
  * Once can disable this reset by removing or commenting out
    the `git reset --hard` line from `update.sh`


Inner workings:

* The remote repository must be specified in the project's `.git` directory
* The `.git` directory retains its settings from before the project directory
  is zipped and uploaded to Gradescope during the "configure autograder" step
  * Relevant settings are current branch, that branch's upstream remote, and
    that remote repository's url
* The autograder will only check for updates in a remote repository that is set
  as the "upstream" for the current branch
  * This is most easily done by adding the `-u` flag to a typical `git push`
    command -- e.g., `git push -u <remote-name> <branch-name>`
  * See also `git branch --set-upsteam`
* The autograder needs read-access to the remote repository
  in order to fetch updates
  * Assuming your remote repo isn't public
    (or else students could get explicit access to your tests),
    you probably want to authenticate with an SSH key.
    For a repository on Github,
    this can either be a "deploy key" or a "machine key"
  * Make sure you've set up your remote repo with an ssh url rather than an
    http one
    * You can verify this by running `git remote -v` and verifying that your
      remote has a url which looks like
      `git@github.com:<username>/<repo-name>.git`
      rather than
      `https://github.com/<username>/<repo-name>.git`

Again, this enhancement works best when all changes you've made before zipping
and uploading to the "create autograder" page are committed, and pushed to the
remote repo.  Otherwise the updating process is likely to break, possibly in
silent or unexpected ways.


[gs-docs-pull-from-git]: https://gradescope-autograders.readthedocs.io/en/latest/git_pull/
[gs-gh-pull-from-git-ex]: https://github.com/gradescope/autograder_samples/tree/master/deploy_keys
[issue-2]: https://github.com/jjc385/autograder-demo/issues/2


### required-files

Gradescope's autograder places student submissions in the
`\autograder\submission` directory, but the default python implementation
runs tests from the `\autograder\tests` directory,
generally requiring any files tested to be moved there.

This enhancement allows the user to simply list all files that are required in
`required-files.txt`, and then the autograder automatically copies them over
and verifies their existence, with feedback for students.

Inner workings:

* A "required file" is any filename listed in `required-files.txt`
* A series of unit tests within `tests/test_file_existence.py`
  check that each required file exists
  * If a file doesn't exist in a students' submission,
    the Gradescope web interface will show this to the student as a failed test
* Before unit tests are run on a student's submission,
  required files are automatically copied
  from `\autograder\submission` to `\autograder\tests`,
  using the `copy_files.py` script


### time-limited

Gradescope's autograder allows individual tests to run indefinitely,
but limits the total autograder runtime for an individual submission to
20 minutes,
at which point the autograder crashes and the submission receives no credit.

This module allows tests to be given time limits,
by running tests in their own processes.
Crucially, stdout and any exceptions are redirected to give feedback to
students.


### fcn-tests

We found that our tests of students' code tended to involve verifying that a
long list of inputs gave the correct output.
Since python's unittest framework lends itself better to more individual
test cases,
I created essentially a factory for test methods.
The factory builds these methods primarily
from a list of inputs or a dict of inputs mapped to expected outputs.


### correct-with-git

Often a student would make a relatively minor mistake that would drastically
affect their autograder score.
Moreover, when trying to understand students' code,
it helped to have the ability to make changes and see how the test results were
affected -- essentially providing a debugging process for the graders.

This was accomplished by version controlling students' submissions using git,
and pulling any changes that might have been made by the grader on the remote.

* Create a branch for each student
* Create a different repo for each assignment
  * Could also have named branches with assignmentname/studentname
* Stage and commit all files (and changes thereto) in the submission directory,
  including metadata
* Push to the remote
* Attempt to pull any changes from the remote
  * This will only be successful if the student has NOT updated their
    submission (i.e., there was nothing to push).
    Otherwise nothing will be pulled.
  * Any changes that are pulled will be changes the grader made to the
    assignment

Notes on scoring:

* Obviously correcting students' code will increase their score
* Typically the grader will want the student to partial (or zero) credit
  for the mistakes that were corrected
* In my implementation this was done entirely manually,
  in a dedicated manually graded "problem" called something like
  "Modifications to the autograder score"
* It would be possible for these score modifications to be done in some
  automated way via git (perhaps in a json file or something),
  but I haven't implemented anything of that sort

What the student sees:

* If the student weren't notified somehow, they wouldn't realize
  the code being graded by the autograder was a modified version of
  their submission
* I accomplished this through a printout of the git log
  (which displays the commit messages)
  in a dedicate autograder test
  * This depends upon the grader to create descriptive commit messages
    detailing the changes made


## Using this package

### Getting started

First, see Gradescope's [autograder documentation][gs-autograder-docs],
which explains how to use and customize the autograder.

Then clone this repository and add to the `tests` directory acording to your
needs.
Any files of the form `tests/test*.py` will be searched for unit tests.

Modify `required_files.txt` to list the names of files
you expect in students' submissions.

**Important:**
Before zipping, be sure to either `git commit` all your changes
or remove the `git reset --hard` line from `update.sh`.
(See the `pull-from-git` section above for more details.)

Finally, zip the contents of this directory and upload it to
gradescope, during the "Autograder Configuration" step.

### Usage suggestions

* I strongly recommend creating a separate branch
  for each assignment on gradescope
    * Use the `git branch` or `git checkout -b` command,
      or see one of the numerous online tutorials
      about creating a new branch in git
    * I originally made the mistake of keeping a separate copy of the
      entire autograder in a new directory for each assignment,
      which quickly turned into a mess when it came to keeping track of which
      changes were made to which assignment's autograder copy.  Git branches
      are designed precisely to make this sort of thing much less painless

