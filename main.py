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

import pylw.resource
import pylw.app as app

import json

class HelloWorld(pylw.resource.DefaultResource):

    def on_get(self,req,resp,user_objects=None):
        #cookies = resp.get_cookies()
        #print self.user_objects['dbcon']
        signed_cookies = resp.get_signed_cookie('testk')
        #unsigned_cookies = resp.get_cookie('unsigned_testk') or 'none'
        resp.status = '200 OK'
        print req.query_dict
        resp.body = 'get method  %s' % json.dumps(signed_cookies)
        resp.add_signed_cookie('testk','value1')
        resp.add_cookie('unsigned_testk','value1')
        resp.add_header('Content-Type','application/json')

    def on_post(self,req,resp,user_objects=None):
        req.read_post_body()
        resp.status = '200 OK'
        bodys = json.dumps(req.url_vars) + json.dumps(req.posted_body)
        resp.body = 'post method %s ' % bodys
        resp.add_header('Content-Type','application/json')

class HelloNobody(pylw.resource.DefaultResource):

    def on_get(self,req,resp,user_objects=None):
        cookies = req.get_cookies()
        resp.status = '200 OK'
        resp.body = None
        #resp.add_cookie('testk','value1')
        resp.add_header('Content-Type','application/json')

class RootResource(pylw.resource.DefaultResource):

    def on_get(self,req,resp,user_objects=None):
        resp.status = '200 OK'
        resp.body = 'this is home' + json.dumps(req.query_dict)
        #resp.add_cookie('testk','value1')
        resp.add_header('Content-Type','text/html')

class RootHardResource(pylw.resource.DefaultResource):

    def on_get(self,req,resp,user_objects=None):
        resp.status = '200 OK'
        resp.body = 'this is hard coded home'
        #resp.add_cookie('testk','value1')
        resp.add_header('Content-Type','text/html')

myuserobject = {}
myuserobject['dbcon'] = 'mydbcon'
myapp = app.App(secret_key="my-new-secret-key",user_objects=myuserobject)

myapp.router.add_path('/testing/v1/{var1}',HelloWorld())

#Routes can be overwritten, so be careful.
#myapp.router.add_path('/testing/v1/{var1}',HelloNobody)

#You need to manually define a root resource.
myapp.router.add_path('/',RootResource())

#hard_coded_path is 5-15% faster using timeit, depending on path length.
myapp.add_hard_coded_path('/',RootHardResource())

#adding a root variable is not supported.
#myapp.router.add_path('/{rootvar}',HelloWorld)
#myapp.router.add_path('/favicon.ico',HelloNobody)

from wsgiref import simple_server



def run():
    #api = myapp.MyAPI()
    httpd = simple_server.make_server('127.0.0.1', 8000, myapp)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
