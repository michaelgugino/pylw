#!/usr/bin/env python

# Copyright 2015 Michael Gugino
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pylw
import timeit
import gc
import pylw.app
import pylw.resource
import pylw.routing

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
        resp.status = '200 OK'
        resp.body = ('everything looks good')



def start_response(*args):
#    print args
    pass

#a = pylw.app.App(secret_key='test')
#a.router.add_route(path1,None,HelloWorld())
a = pylw.app.App(secret_key='test')
a.router.add_path(path2,HelloWorld())
#a.add_hard_coded_path(path1,HelloWorld())

#hard coded paths can be about 40% faster
b = pylw.app.App(secret_key='test')
b.add_hard_coded_path(path1,HelloWorld())

#CRouter is about 40% when compile with Cython, but not much faster
#when using normal python
c = pylw.app.App(secret_key='test')
c.router = pylw.routing.CRouter()
c.router.add_path(path2,HelloWorld())

gc.collect()

def runa():
        a(env, start_response)


def runb():
        b(env, start_response)

def runc():
        b(env, start_response)

print 'pylw'
sum1 = 0
sum1 += timeit.timeit(runa,number=260000)
sum1 += timeit.timeit(runa,number=260000)
sum1 += timeit.timeit(runa,number=260000)
#sum1 += timeit.timeit(runa,number=10)


sum2 = 0
gc.collect()
sum2 += timeit.timeit(runb,number=260000)
sum2 += timeit.timeit(runb,number=260000)
sum2 += timeit.timeit(runb,number=260000)
#sum2 += timeit.timeit(runb,number=10)

sum3 = 0
gc.collect()
sum3 += timeit.timeit(runc,number=260000)
sum3 += timeit.timeit(runc,number=260000)
sum3 += timeit.timeit(runc,number=260000)

av1 = sum1/3
av2 = sum2/3
av3 = sum3/3

print 'av1:', av1
print 'av2:', av2
print 'av3:', av3

diff = av1 - av2
print 'diff a-b:', diff
print 'diff% :', diff/av1

diff = av1 - av3
print 'diff a-c:', diff
print 'diff% :', diff/av1

#a(env, start_response)
