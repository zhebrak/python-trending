# coding: utf-8

import random

from dateutil.parser import parse


class RedditFeed(object):
    class PostClass():
        pass

    post_list_main = [
        (3062, '2015-02-01T09:36:57+00:00'), (4532, '2015-02-01T04:13:51+00:00'),
        (3425, '2015-02-01T03:50:42+00:00'), (3925, '2015-02-01T02:44:17+00:00'),
        (4376, '2015-02-01T01:35:06+00:00'), (3799, '2015-02-01T01:26:44+00:00'),
        (4122, '2015-02-01T00:23:44+00:00'), (3008, '2015-02-01T01:45:48+00:00'),
        (4604, '2015-01-31T23:21:18+00:00'), (3228, '2015-02-01T01:11:13+00:00')
    ]

    post_list_subreddit = [
        (83, '2015-02-01T07:31:16+00:00'), (7, '2015-02-01T12:27:24+00:00'),
        (4, '2015-02-01T12:37:18+00:00'), (134, '2015-01-31T15:50:24+00:00'),
        (33, '2015-01-31T23:21:31+00:00'), (3, '2015-02-01T09:06:17+00:00'),
        (0, '2015-02-01T13:43:55+00:00'), (6, '2015-02-01T01:45:20+00:00'),
        (5, '2015-02-01T00:29:22+00:00'), (9, '2015-01-31T20:55:49+00:00')
    ]

    def __init__(self):
        self.main_shuffled = self._shuffle_original_list(self.post_list_main)
        self.sub_shuffled = self._shuffle_original_list(self.post_list_subreddit)

    @staticmethod
    def _shuffle_original_list(original_list):
        shuffled_list = [(idx, score, created_at) for idx, (score, created_at) in enumerate(original_list)]
        random.shuffle(shuffled_list)

        return shuffled_list

    def main_page_objects(self):
        return self._objects(self.main_shuffled)

    def subreddit_objects(self):
        return self._objects(self.sub_shuffled)

    def _objects(self, shuffled_list):
        for original_idx, post_score, post_date in shuffled_list:
            post = self.PostClass()
            post.created_at = parse(post_date)
            post.score = post_score
            post.id = original_idx

            yield post

    def check_main_page(self, ranked_list):
        return self._check_order(ranked_list, self.post_list_main)

    def check_subreddit(self, ranked_list):
        return self._check_order(ranked_list, self.post_list_subreddit)

    def _check_order(self, ranked_list, original_list):
        for idx, (ranked_post, original_post) in enumerate(zip(ranked_list, original_list)):
            if ranked_post.id != idx:
                return False

        return True
