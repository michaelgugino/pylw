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

'''Defines a default resource type'''
import json

class DefaultResource(object):

    def __init__(self):
        '''Initializes a Resource.
           user_objects is a convienence store of user objects and data,
           ideally initialized at the time of calling the app.  This allows us
           to access long-lived DB or Cache sessions, or other long lived
           objects and data.'''

        self.count = 0

    def __call__(self,req,resp,user_objects=None):
        if req.request_method == 'POST':
            self.on_post(req,resp,user_objects)
        elif req.request_method == 'GET':
            self.on_get(req,resp,user_objects)
        else:
            resp.status = '400 Bad Method'
            resp.body = 'Method Not Implemented %s ' % json.dumps(req.url_vars)
            resp.add_header('Content-Type','application/json')

    def on_get(self,req,resp,user_objects=None):
        pass

    def on_post(self,req,resp,user_objects=None):
        pass
