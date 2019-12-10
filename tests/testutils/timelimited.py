#import multiprocessing as mp
import multiprocess as mp # use rather than multiprocessing to avoid pickle issues
from . import outputredirected
from .outputredirected import OutputRedirected
import time

import functools

## Ad hoc constant displaying the minimum time required to properly redirect output
##      Unit tests which run for less time typically fail with a file-not-found error
MIN_RUN_TIME = outputredirected.MIN_RUN_TIME


class TimeLimited:
    """Decorator to limit the time spent executing a function"""

    def __init__(self, time_limit=0, 
                terminated_callback=None, unterminated_callback=None,
                output_wrapper=None
            ):
        self._time_limit = time_limit
        self._output = None
        self._terminated_callback = terminated_callback
        self._unterminated_callback = unterminated_callback
        self._output_wrapper = output_wrapper

    def __call__(self, fcn):
        @functools.wraps(fcn)
        def time_limited_fcn(*args, **kwargs):
            redirector = OutputRedirected()
            fcn_redirected = redirector(fcn)

            process = mp.Process(target=fcn_redirected, args=args, kwargs=kwargs)
            process.start()
            process.join(self._time_limit) # Wait `timeLimit` seconds for the process to run or terminate on its own

            if process.exitcode is None : # The process is still running
                process.terminate()
                if self._terminated_callback is not None:
                    self._terminated_callback()
            else:
                if self._unterminated_callback is not None:
                    self._unterminated_callback()

#            self._output = redirector.get_redirected()
            self._output = redirector.get_redirected(False)
            if self._output_wrapper is not None:
                self._output_wrapper(self._output)
        return time_limited_fcn

    def get_output(self):
        return self._output

