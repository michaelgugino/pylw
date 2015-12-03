import app
import resource
import json

class HelloWorld(resource.DefaultResource):

    def on_get(self):
        self.resp.status = '200 OK'
        self.resp.body = 'get method %s ' % json.dumps(self.req.url_vars)
        self.resp.add_header('Content-Type','application/json')

    def on_post(self):
        self.resp.status = '200 OK'
        self.resp.body = 'post method %s ' % json.dumps(self.req.url_vars)
        self.resp.add_header('Content-Type','application/json')


myapp = app.App()
myapp.router.add_path('/testing/v1/{var1}',HelloWorld)

from wsgiref import simple_server



def run():
    #api = myapp.MyAPI()
    httpd = simple_server.make_server('127.0.0.1', 8000, myapp)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
