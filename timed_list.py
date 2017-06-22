import threading
import time


class TimedList(object):
    def __init__(self):
        """
        计时列表，每个项目都有时效性
        """

        # 格式: {item: (timestamp, limit_secs)}
        self.data = dict()
        self._lock = threading.Lock()

    def set(self, item, limit_secs):
        with self._lock:
            self.data[item] = time.time(), limit_secs

    def secs_left(self, item):
        if item in self.data:
            timestamp, limit_secs = self.data[item]
            if limit_secs > 0:
                return limit_secs - (time.time() - timestamp)
            return 999
        return 0

    def remove(self, item):
        if item in self.data:
            del self.data[item]

    def __contains__(self, item):
        return bool(self.secs_left(item) > 0)


if __name__ == '__main__':
    tl = TimedList()
    a = 1
    assert a not in tl
    tl.set(a, 2)
    assert a in tl
    time.sleep(1)
    assert a in tl
    assert round(tl.secs_left(a)) == 1
    time.sleep(1)
    assert a not in tl
    tl.set(a, -1)
    assert tl.secs_left(a) == 999
    tl.remove(a)
    assert tl.secs_left(a) == 0
    assert a not in tl
    print('all tests pass')
