'''Defines a default resource type'''
import json

class DefaultResource(object):

    def __init__(self,req,resp):
        self.req = req
        self.resp = resp

    def __call__(self):
        if self.req.request_method == 'POST':
            self.on_post()
        elif self.req.request_method == 'GET':
            self.on_get()
        else:
            self.resp.status = '400 Bad Method'
            self.resp.body = 'Method Not Implemented %s ' % json.dumps(self.req.url_vars)
            self.resp.add_header('Content-Type','application/json')

    def on_get(self):
        pass

    def on_post(self):
        pass
