import sys
import time
from Queue import Queue
from threading import Thread


class ThreadWrapper():
    def __init__(self, func, io=None):
        self.func = func
        self.io = io
        self.thread = None
        self.failed = False

    def _run_func(self):
        try:
            self._result = func()
        except SystemExit as e:
            if e.code:
                self.failed = True
        except Exception as e:
            print e
            self.failed = True
        finally:
            self._duration = int(time.time() - self._start_time)
            if self.io is not None:
                self.io.exit()

    def start(self):
        if self.thread and thread.isAlive():
            return False

        if self.io is not None:
            self.io.enter()

        self._start_time = time.time()
        thread = Thread(target=self.run_func)
        thread.start()
        return True

    def is_running(self):
        return self.thread is not None and self.thread.isAlive()

    def duration(self):
        if self.is_running():
            return time.time() - self._start_time
        return self._duration

    def get_result(self):
        return self._result

    def wait_till_terminate(self):
        if self.thread:
            self.thrad.join()


class ThreadIO():
    enter = __enter__
    exit = __exit__

    def __init__(self, stdin=None):
        self.input_q = None
        if stdin:
            self.input_q = Queue()
            for s in stdin:
                self.input_q.put(s)

        self.output_q = Queue()
        self.output = ''

    def __enter__(self):
        # Overwrite input
        self._stdin = None
        if self.input_q is not None:
            self._stdin = sys.stdin
            sys.stdin = self
        # Overwrite output
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = sys.stderr = self

    def __exit__(self, *argv):
        if self._stdin is not None:
            self.stdin = self._stdin
        sys.stdout = self._stdout
        sys.stderr = self._stderr

    def readline(self):
        return self.input_q.get()

    def write(self, s):
        self.output_q.put(s)

    def get_messages(self):
        while not self.output_q.empty():
            self.output += self.output_q.get()
        return self.output
