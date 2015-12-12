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

'''pylw.app.  Contains Resp,Req,App object definitions.
   pylw.app.App() is the WSGI callable object.'''
import itsdangerous

import routing
import request
import response

class App(object):
    '''This class implements a bare minimum WSGI application'''
    def __init__(self, secret_key=None, config_dict=None, user_objects=None):
        self.router = routing.DefaultRouter()
        self.user_objects = user_objects
        self.hard_coded_path = {}
        self.s = self.create_secret_signer(secret_key=secret_key)
        if config_dict:
            self.parse_config_dict(config_dict)
        if not secret_key:
            raise Exception('secret key missing')

    def parse_config_dict(self, config_dict):
        '''Override self.__dict__[x] for x in config_dict'''
        for k,v in config_dict.iteritems():
            self.__dict__[k] = config_dict[k]

    def create_secret_signer(self,secret_key=None):
        '''Create our secret signer object'''
        return itsdangerous.Serializer(secret_key)

    def add_hard_coded_path(self,uri,resource):
        '''Add a hard coded path to the application.  You cannot use variables
           here, but the look up time will be much faster than normal.'''

        self.hard_coded_path[uri] = resource

    def __call__(self, env, start_response):
        '''This method is called by the WSGI server.'''


        req = request.Request(env)
        resp = response.Response(
            http_cookies=req.get_cookies(),
            signer=self.s)
        try:
            self.hard_coded_path[req.path](req,resp,user_objects=self.user_objects)
        except:
            try:
                self.router.return_path_resource(
                    req.path,req.url_vars)(req,resp,user_objects=self.user_objects)
            except:
                resp.HTTP404Error()

        start_response(resp.status, resp.get_headers())
        return resp.body
