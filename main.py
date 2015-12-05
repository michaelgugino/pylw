import app
import resource
import json

class HelloWorld(resource.DefaultResource):

    def on_get(self):
        #cookies = self.resp.get_cookies()
        signed_cookies = self.resp.get_signed_cookie('testk')
        #unsigned_cookies = self.resp.get_cookie('unsigned_testk') or 'none'
        self.resp.status = '200 OK'
        self.resp.body = 'get method  %s' % json.dumps(signed_cookies)
        self.resp.add_signed_cookie('testk','value1')
        self.resp.add_cookie('unsigned_testk','value1')
        self.resp.add_header('Content-Type','application/json')

    def on_post(self):
        self.resp.status = '200 OK'
        self.resp.body = 'post method %s ' % json.dumps(self.req.url_vars)
        self.resp.add_header('Content-Type','application/json')

class HelloNobody(resource.DefaultResource):

    def on_get(self):
        cookies = self.req.get_cookies()
        self.resp.status = '200 OK'
        self.resp.body = None
        #self.resp.add_cookie('testk','value1')
        self.resp.add_header('Content-Type','application/json')


myapp = app.App()
myapp.secret_key="my-new-secret-key"
myapp.router.add_path('/testing/v1/{var1}',HelloWorld)
myapp.router.add_path('/favicon.ico',HelloNobody)

from wsgiref import simple_server



def run():
    #api = myapp.MyAPI()
    httpd = simple_server.make_server('127.0.0.1', 8000, myapp)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
