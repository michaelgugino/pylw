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

'''pylw.response.  Contains Response object definition.  Holds body, header,
   and parses/signs cookies.'''

import Cookie

class Response(object):
    '''Response object for sending back to WSGI server.  It holds the headers
       and body'''

    def __init__(self, http_cookies=None, signer=None):
        '''Initialize our object.'''
        self.__header_dict = {}
        self.body = None
        self.status = None
        self.s = signer
        self.__cookies = self.parse_http_cookies(http_cookies)

    def parse_http_cookies(self, req_cookies):
        '''Parse http cookies into a SimpleCookie object'''
        C = Cookie.SimpleCookie()
        if req_cookies:
            C.load(req_cookies)
        return C

    def HTTP404Error(self):
        self.status = '404 Not Found'
        self.body = 'The requested URL was not found.'

    def get_headers(self):
        '''Returns headers in a list of tuples that is usable by WSGI'''
        if not self.body:
            self.body = ''
        self.__header_dict['Content-Length'] = str(len(self.body))

        cookies = []
        if self.__cookies:
            cookies += [("set-cookie", c.OutputString())
            for c in self.__cookies.values()]
        return self.__header_dict.items() + cookies

    def get_cookies(self):
        return self.__cookies.output()

    def get_cookie(self,cookie):
        '''Return the value a cookie.'''
        try:
            return self.__cookies[cookie].value
        except:
            return None

    def get_signed_cookie(self,cookie):
        '''Return the value of a signed cookie.'''
        try:
            return self.s.loads(self.__cookies[cookie].value)
        except:
            return None

    def add_signed_cookie(self,k,v):
        '''Add a signed cookie'''
        v = self.s.dumps(v)
        self.__cookies[k] = v

    def add_cookie(self,k,v):
        '''Add an unsigned cookie'''
        self.__cookies[k] = v

    def add_header(self,k,v):
        '''Add a response header'''
        self.__header_dict[k] = v
