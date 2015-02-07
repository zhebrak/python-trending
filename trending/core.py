# coding: utf-8

import time

from datetime import datetime
from functools import partial
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

        if not callable(attr):
            return attr

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


class HackerNewsBaseRanking(Ranking):
    DEFAULT_GRAVITY = 1.8

    def __init__(self, votes_attr, created_at_attr, gravity=DEFAULT_GRAVITY):
        self.votes_attr = votes_attr
        self.created_at_attr = created_at_attr
        self.gravity = gravity

    def _get_object_info(self, obj):
        votes = self.get_ranking_attr(obj, self.votes_attr)

        created_at = self.get_ranking_attr(obj, self.created_at_attr)
        delta = datetime.now() - created_at
        hour_age = delta.days * 24 + delta.seconds / 3600

        return votes, hour_age


class HackerNewsRanking(HackerNewsBaseRanking):
    def calculate_score(self, obj):
        votes, hour_age = self._get_object_info(obj)
        return (votes - 1) / pow((hour_age + 2), self.gravity)


class HackerNewsExtendedRanking(HackerNewsBaseRanking):
    """
    gravity_conf:

    {'<feature>': [weight, score_limit]}

    """

    def __init__(
            self,
            votes_attr, created_at_attr,
            gravity_conf=None, min_gravity=1.5, max_gravity=2,
            annotate_items=False
    ):
        super(HackerNewsExtendedRanking, self).__init__(votes_attr, created_at_attr)

        self.MIN_GRAVITY = min_gravity
        self.MAX_GRAVITY = max_gravity
        self.GRAVITY_RANGE = self.MAX_GRAVITY - self.MIN_GRAVITY

        if gravity_conf is None:
            self.gravity = lambda obj: self.DEFAULT_GRAVITY

        else:
            self.gravity = partial(self._calculate_gravity, gravity_conf=gravity_conf)
            self.feature_max_impacts = self._get_feature_max_impacts(gravity_conf)

        self.annotate_items = annotate_items

    def _get_feature_max_impacts(self, gravity_conf):
        feature_max_impact_map = dict((feature, 0) for feature in gravity_conf)

        sum_weight = sum([weight for weight, _ in gravity_conf.values()])
        for feature, (weight, _) in gravity_conf.items():
            feature_max_impact_map[feature] = float(weight) / sum_weight * self.GRAVITY_RANGE

        return feature_max_impact_map

    def _calculate_gravity(self, obj, gravity_conf=None):
        gravity_impact = 0

        for feature, (weight, score_limit) in gravity_conf.items():
            feature_score = self.get_ranking_attr(obj, feature)

            if feature_score >= score_limit:
                gravity_impact += self.feature_max_impacts[feature]
                continue

            gravity_impact += float(feature_score) / score_limit * self.feature_max_impacts[feature]

        obj.gravity = self.MAX_GRAVITY - gravity_impact
        return self.MAX_GRAVITY - gravity_impact

    def calculate_score(self, obj):
        votes, hour_age = self._get_object_info(obj)
        gravity = self.gravity(obj)

        rank = (votes - 1) / pow((hour_age + 2), gravity)

        if self.annotate_items:
            obj.trending_rank = rank
            obj.trending_gravity = gravity

        return rank
