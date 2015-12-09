# content of test_sysexit.py
import pytest
import setup_test_objects
import pylw
import pylw.request





def test_get_blank_cookies_request():
    env = setup_test_objects.EnvInput('GET','/')
    env.env.pop('HTTP_COOKIE')
    req = pylw.request.Request(env.env)
    cookies = req.get_cookies()
    assert cookies is None

def test_get_cookies_request():
    env = setup_test_objects.EnvInput('GET','/')
    req = pylw.request.Request(env.env)
    cookies = req.get_cookies()
    assert cookies == 'cookie1=value1;'

def test_post_read_body():
    env = setup_test_objects.EnvInput('POST','/')
    req = pylw.request.Request(env.env)
    req.read_post_body()
    assert req.posted_body == '{"var1" : "value 1"}'

def test_get_read_body():
    env = setup_test_objects.EnvInput('GET','/')
    req = pylw.request.Request(env.env)
    req.read_post_body()
    assert req.posted_body is None
