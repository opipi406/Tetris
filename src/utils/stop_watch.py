import time
from functools import wraps


def stop_watch(func):
    """ メソッドの処理時間を計測 """

    @wraps(func)
    def passage(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start
        print('{}() : {:.4f}s'.format(func.__name__, elapsed_time))
        return result

    return passage


class StopWatch:

    def __init__(self):
        self._t = 0
        self._delta_t = 0

    def initialized(self):
        self._t = time.time()

    def print(self, text='', initialized=True):
        self._delta_t = time.time() - self._t
        if text != '': text += ' : '
        print('{}{:.4f}s'.format(text, self._delta_t))

        if initialized:
            self.initialized()