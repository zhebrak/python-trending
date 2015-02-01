# coding: utf-8

import time

from datetime import datetime
from math import log10


class Ranking(object):
    def rank(self, iterable):
        return sorted(iterable, key=lambda obj: self.calculate_score(obj), reverse=True)

    def calculate_score(self, obj):
        raise NotImplemented

    @staticmethod
    def get_ranking_attr(obj, attr):
        if isinstance(attr, str):
            return getattr(obj, attr)

        return attr(obj)


class RedditRanking(Ranking):
    def __init__(self, score_attr, created_at_attr):
        self.score_attr = score_attr
        self.created_at_attr = created_at_attr

    def calculate_score(self, obj):
        score = self.get_ranking_attr(obj, self.score_attr)
        order = log10(max(abs(score), 1))

        if score > 0:
            sign = 1
        elif score < 0:
            sign = -1
        else:
            sign = 0

        created_at = self.get_ranking_attr(obj, self.created_at_attr)
        seconds = time.mktime(created_at.timetuple()) - 1134028003

        return round(sign * order + seconds / 45000, 7)


class HackerNewsRanking(Ranking):
    def __init__(self, votes_attr, created_at_attr, gravity=1.8):
        self.votes_attr = votes_attr
        self.created_at_attr = created_at_attr
        self.gravity = gravity

    def calculate_score(self, obj):
        votes = self.get_ranking_attr(obj, self.votes_attr)

        created_at = self.get_ranking_attr(obj, self.created_at_attr)
        delta = datetime.now() - created_at
        days, seconds = delta.days, delta.seconds
        hour_age = days * 24 + seconds / 3600

        return (votes - 1) / pow((hour_age + 2), self.gravity)
