#!/usr/bin/env python
# coding=utf-8

'''
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2020-12-22 15:10:30
LastEditors: zmf96
LastEditTime: 2020-12-22 15:10:40
FilePath: /httpbinasync/structures.py
Description: 
'''
"""
httpbin.structures
~~~~~~~~~~~~~~~~~~~

Data structures that power httpbin.
"""


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
