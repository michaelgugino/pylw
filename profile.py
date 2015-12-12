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
import pylw.app
import pylw.resource
path1 = '/things/to/long/path/test'
path2 = '/things/to/long/path/{var1}'



env = {
    'SERVER_PROTOCOL': 'HTTP 1.1',
    'SERVER_SOFTWARE': 'WSGIREF',
    'SCRIPT_NAME': 'app',
    'REQUEST_METHOD': 'GET',
    'PATH_INFO': path1,
    'HTTP_USER_AGENT': 'curl/7.24.0 (x86_64-apple-darwin12.0)',
    'REMOTE_PORT': '65123',
    'RAW_URI': path1,
    'REMOTE_ADDR': '127.0.0.1',
    'SERVER_NAME': 'localhost',
    'SERVER_PORT': '8000',
    'QUERY_STRING': 'a&=1b=2',
    'wsgi.input': 'some body'
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
a.add_hard_coded_path(path1,HelloWorld())

def runa():
        a(env, start_response)

if __name__ == '__main__':
    runa()
