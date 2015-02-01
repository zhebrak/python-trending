# coding: utf-8

import unittest

from trending.core import RedditRanking

from tests.feed_mock import RedditFeed


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
