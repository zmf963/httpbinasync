#!/usr/bin/env python
# coding=utf-8

'''
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2020-12-15 14:16:39
LastEditors: zmf96
LastEditTime: 2020-12-15 14:55:30
FilePath: /tests/test_httpbinasync.py
Description: 
'''

from httpbinasync import __version__,tmpl_dir
import requests

def test_version():
    assert __version__ == '0.1.0'

def test_temp_dir():
    print(tmpl_dir)
    assert tmpl_dir != None

class TestClassHttpbinasync:
    def test_uuid(self):
        assert 1 == 1
        r = requests.get('http://127.1:5000/uuid')
        assert r.status_code == 200