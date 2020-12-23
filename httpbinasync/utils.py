#!/usr/bin/env python
# coding=utf-8

'''
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2020-12-14 18:23:33
LastEditors: zmf96
LastEditTime: 2020-12-15 16:49:11
FilePath: /httpbinasync/utils.py
Description: 
'''

import random
import bisect


def weighted_choice(choices):
    """Returns a value from choices chosen by weighted random selection

    choices should be a list of (value, weight) tuples.

    eg. weighted_choice([('val1', 5), ('val2', 0.3), ('val3', 1)])

    """
    values, weights = zip(*choices)
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random.uniform(0, total)
    i = bisect.bisect(cum_weights, x)
    return values[i]

class CaseInsensitiveDict(dict):
    """Case-insensitive Dictionary for headers.

    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header.
    """

    def _lower_keys(self):
        return [k.lower() for k in self.keys()]

    def __contains__(self, key):
        return key.lower() in self._lower_keys()

    def __getitem__(self, key):
        # We allow fall-through here, so values default to None
        if key in self:
            return list(self.items())[self._lower_keys().index(key.lower())][1]