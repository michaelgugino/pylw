#!/usr/bin/env python
import pylw
import things
import timeit
import gc
import pylw.app
import pylw.resource
import falcon
import sys
import json
path1 = '/things/to/long/path/test'
path2 = '/things/to/long/path/{var1}'

env2 = {
'REQUEST_METHOD' : 'GET',
'PATH_INFO' : path1
}




env = {
    'SERVER_PROTOCOL': 'HTTP 1.1',
    'SERVER_SOFTWARE': 'gunicorn/0.17.0',
    'SCRIPT_NAME': 'app',
    'REQUEST_METHOD': 'GET',
    'PATH_INFO': path1,
    'HTTP_USER_AGENT': 'curl/7.24.0 (x86_64-apple-darwin12.0)',
    'REMOTE_PORT': '65133',
    'RAW_URI': path1,
    'REMOTE_ADDR': '127.0.0.1',
    'SERVER_NAME': 'localhost',
    'SERVER_PORT': '8000',
    'QUERY_STRING': 'a&=1b=2',
    'wsgi.url_scheme': '',
    'wsgi.input': 'some body',
    'wsgi.errors': sys.stderr,
    'wsgi.multithread': False,
    'wsgi.multiprocess': True,
    'wsgi.run_once': False
}

class HelloWorld(pylw.resource.DefaultResource):

    def on_get(self, req, resp, user_objects):
        """Handles GET requests"""
        resp.status = '200 OK'  # This is the default status
        resp.body = ('\nTwo things awe me most, the starry sky '
                     'above me and the moral law within me.\n'
                     '\n'
                     '    ~ Immanuel Kant\n\n')



def start_response(*args):
#    print args
    pass

#a = pylw.app.App(secret_key='test')
#a.router.add_route(path1,None,HelloWorld())
a = pylw.app.App(secret_key='test')
a.router.add_path(path2,HelloWorld())
a.add_hard_coded_path(path1,HelloWorld())
b = things.app

gc.collect()

def runa():
        a(env, start_response)


def runb():
        b(env, start_response)

print 'pylw'
sum1 = 0
sum1 += timeit.timeit(runa,number=10000)
sum1 += timeit.timeit(runa,number=10000)
sum1 += timeit.timeit(runa,number=10000)
#sum1 += timeit.timeit(runa,number=10)
print 'falcon'

sum2 = 0
gc.collect()
sum2 += timeit.timeit(runb,number=10000)
sum2 += timeit.timeit(runb,number=10000)
sum2 += timeit.timeit(runb,number=10000)
#sum2 += timeit.timeit(runb,number=10)
av1 = sum1/3
av2 = sum2/3

print 'av1:', av1
print 'av2:', av2

diff = av1 - av2
print 'diff:', diff
print 'diff% :', diff/av1
#a(env, start_response)
