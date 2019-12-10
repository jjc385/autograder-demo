import os
import shutil
import tempfile
import sys

import functools
import traceback

## Ad hoc constant displaying the minimum time required to properly redirect output
##      Unit tests which run for less time typically fail with a file-not-found error
MIN_RUN_TIME = 0.2 # time in seconds

class OutputNotFoundError(FileNotFoundError):
    """Indicates that the output redirection file was not found

    This could be because the redirection file was deleted or corrupted,
    or because it was never created
    """
    pass

class OutputNotReadyError(OutputNotFoundError):
    """Indicates that the output redirection file was never fully set up

    This is more specific than OutputNotFoundError,
        which is essentially a wrapper for FileNotFoundError
    """
    pass

def generate_outfile():
    outdir = tempfile.mkdtemp()
    outfile = os.path.join(outdir, "redirected.out")
    return outfile

def delete_generated_outfile(outfile):
    tempdir = os.path.dirname(outfile)
    shutil.rmtree(tempdir)

def get_redirected(outfile, to_delete=False):
    with open(outfile, 'r') as f :
        output = f.read()
    if to_delete:
        delete_generated_outfile(outfile)
    return output

def print_redirected(outfile, to_delete=False):
    print(get_redirected(outfile, to_delete))


class OutputRedirected:
    """Wrapper function to redirect the output of a function

    Useful for intercepting stdout and stderr from a subprocess
    """


    def __init__(self, outfile=None):
        self._outfile_dir_is_temp = False
        if outfile is None:
            outfile = generate_outfile()
            self._outfile_dir_is_temp = True
        self._outfile = outfile
        self._is_redirected = False
        ## Allow stdout to be reset to its original value in the case of a failure
        #       Allows the possibility that sys.stdout has already been redirected
        self._default_stdout = sys.stdout


    def get_outfile(self):
        return self_outfile

    def __call__(self, fcn):

        @functools.wraps(fcn)
        def wrapper(*args, **kwargs) :
            error = None
            with open(self._outfile, 'w', buffering=1) as f :
                val = None
                default_stdout = sys.stdout
                sys.stdout = f
                self._is_redirected = True
                try :
                    val = fcn(*args, **kwargs)
                except Exception as theError :
                    traceback.print_exc(file=f)
                    error = theError
                finally :
                    sys.stdout = default_stdout
            if error is not None :
                raise error
            return val
        
        return wrapper

    def reset_stdout(self):
        """Only to be used if for some reason stdout is not un-redirected during __call__"""
        sys.stdout = self._default_stdout
        self._is_redirected = False

    def cleanup(self):
        if self._is_redirected:
            self.reset_stdout()
        if self._outfile_dir_is_temp:
            delete_generated_outfile(self._outfile)

    def get_redirected(self, to_cleanup=True):
        output = None
        error = None
        try:
            output = get_redirected(self._outfile, False)
            if to_cleanup:
                self.cleanup()
        except FileNotFoundError as e:
            newMessage = ( "A FileNotFoundError was generated when attempting"
                    " to retrieve redirected output."
                    "\n"
                    "This often happens if the output was redirected from"
                    " a separate process, and that process was terminated"
                    " before the output file was fully created."
                    "\n"
                    "This issue is usually resolved if the process is allowed"
                    " to run for at least MIN_RUN_TIME seconds."
                )
            originalTraceback = traceback.format_exc()
            fullMessage = newMessage + '\n\nOriginal exception:\n' + originalTraceback
            error = OutputNotFoundError(fullMessage)
        finally:
            if error:
                raise error
        return output

    def print_redirected(self, to_cleanup=True):
        output = print_redirected(self._outfile, False)
        if to_cleanup:
            self.cleanup()

