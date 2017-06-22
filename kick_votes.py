import threading
import time


class KickVotes(object):
    def __init__(self, limit_secs=0):
        """
        对于每个项目在限定时间内增加的数量
        超出限定时间后再增加，则将该项目数量重新设为 1

        :param limit_secs: 限定的秒数
        """

        # 格式: {to_kick: ({voter, ...}, timestamp)}
        self.votes = dict()

        self.limit_secs = limit_secs
        self._lock = threading.Lock()

    def vote(self, voter, to_kick):
        """投票, 返回 最新票数，剩余秒数"""
        with self._lock:
            if self.secs_left(to_kick) < 0:
                self.votes[to_kick] = {voter}, time.time()
            else:
                self.votes[to_kick][0].add(voter)
            return len(self.votes[to_kick][0]), self.secs_left(to_kick)

    def secs_left(self, to_kick):
        """剩余秒数，不存在时为 -1"""
        if to_kick in self.votes:
            return self.limit_secs - (time.time() - self.votes[to_kick][1])
        else:
            return -1

    def get(self, to_kick, default=(None, None)):
        return self.votes.get(to_kick, default=default)

    def __contains__(self, to_kick):
        return to_kick in self.votes

    def __getitem__(self, to_kick):
        return self.votes[to_kick]

    def __delitem__(self, to_kick):
        if to_kick in self.votes:
            del self.votes[to_kick]

    def __repr__(self):
        return repr(self.votes)
