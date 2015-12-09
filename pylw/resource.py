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
            self.on_post(req,resp,user_objects=None)
        elif req.request_method == 'GET':
            self.on_get(req,resp,user_objects=None)
        else:
            resp.status = '400 Bad Method'
            resp.body = 'Method Not Implemented %s ' % json.dumps(req.url_vars)
            resp.add_header('Content-Type','application/json')

    def on_get(self,req,resp,user_objects=None):
        pass

    def on_post(self,req,resp,user_objects=None):
        pass
