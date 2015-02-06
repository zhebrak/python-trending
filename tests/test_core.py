# coding: utf-8

from datetime import datetime

import unittest

from trending.core import RedditRanking, HackerNewsExtendedRanking

from tests.feed_mock import RedditFeed, RandomExtendedFeed


class RedditTest(unittest.TestCase):
    def setUp(self):
        self.feed = RedditFeed()

    def test_str_attrs(self):
        ranking = RedditRanking(score_attr='score', created_at_attr='created_at')
        main_ranked_list = ranking.rank(self.feed.main_page_objects())
        sub_ranked_list = ranking.rank(self.feed.subreddit_objects())

        self.assertTrue(self.feed.check_main_page(main_ranked_list))
        self.assertTrue(self.feed.check_subreddit(sub_ranked_list))

    def test_callable_attrs(self):
        ranking = RedditRanking(
            score_attr=lambda obj: getattr(obj, 'score'),
            created_at_attr=lambda obj: getattr(obj, 'created_at')
        )

        main_ranked_list = ranking.rank(self.feed.main_page_objects())
        sub_ranked_list = ranking.rank(self.feed.subreddit_objects())

        self.assertTrue(self.feed.check_main_page(main_ranked_list))
        self.assertTrue(self.feed.check_subreddit(sub_ranked_list))


class RandomExtendedTest(unittest.TestCase):
    def setUp(self):
        self.feed = RandomExtendedFeed(limit=100)
        self.gravity_conf = {
            'comments': [2, 100],
            'views': [1, 200]
        }

    def test_working_test(self):
        ranking = HackerNewsExtendedRanking(
            votes_attr='score', created_at_attr='created_at',
            gravity_conf=self.gravity_conf
        )

        for post in ranking.rank(self.feed.objects()):
            print '{0} min ago / score: {1} comments: {2} views: {3}, gravity: {4}'.format(
                (datetime.now() - post.created_at).seconds / 60, post.score,
                post.comments, post.views, post.gravity
            )
