import time

class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        # if self._start_time is not None:
        #     raise TimerError(f"Timer is running. Use .stop() to stop it")

        if self._start_time is None:
            self._start_time = time.time()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is not None:
            elapsed_time = time.time() - self._start_time
        
        self._start_time = None
        print("Elapsed time: {} seconds".format(elapsed_time))