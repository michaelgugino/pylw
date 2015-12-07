import pylw.resource
import pylw.app as app

import json

class HelloWorld(pylw.resource.DefaultResource):

    def on_get(self):
        #cookies = self.resp.get_cookies()
        #print self.user_objects['dbcon']
        signed_cookies = self.resp.get_signed_cookie('testk')
        #unsigned_cookies = self.resp.get_cookie('unsigned_testk') or 'none'
        self.resp.status = '200 OK'
        self.resp.body = 'get method  %s' % json.dumps(signed_cookies)
        self.resp.add_signed_cookie('testk','value1')
        self.resp.add_cookie('unsigned_testk','value1')
        self.resp.add_header('Content-Type','application/json')

    def on_post(self):
        self.req.read_post_body()
        self.resp.status = '200 OK'
        bodys = json.dumps(self.req.url_vars) + json.dumps(self.req.posted_body)
        self.resp.body = 'post method %s ' % bodys
        self.resp.add_header('Content-Type','application/json')

class HelloNobody(pylw.resource.DefaultResource):

    def on_get(self):
        cookies = self.req.get_cookies()
        self.resp.status = '200 OK'
        self.resp.body = None
        #self.resp.add_cookie('testk','value1')
        self.resp.add_header('Content-Type','application/json')

class RootResource(pylw.resource.DefaultResource):

    def on_get(self):
        self.resp.status = '200 OK'
        self.resp.body = 'this is home' + json.dumps(self.req.query_dict)
        #self.resp.add_cookie('testk','value1')
        self.resp.add_header('Content-Type','text/html')

class RootHardResource(pylw.resource.DefaultResource):

    def on_get(self):
        self.resp.status = '200 OK'
        self.resp.body = 'this is hard coded home'
        #self.resp.add_cookie('testk','value1')
        self.resp.add_header('Content-Type','text/html')

myuserobject = {}
myuserobject['dbcon'] = 'mydbcon'
myapp = app.App(secret_key="my-new-secret-key",user_objects=myuserobject)

myapp.router.add_path('/testing/v1/{var1}',HelloWorld)

#Routes can be overwritten, so be careful.
#myapp.router.add_path('/testing/v1/{var1}',HelloNobody)

#You need to manually define a root resource.
myapp.router.add_path('/',RootResource)

#hard_coded_path is 5-15% faster using timeit, depending on path length.
#myapp.add_hard_coded_path('/',RootHardResource)

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
