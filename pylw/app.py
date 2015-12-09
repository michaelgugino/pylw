'''pylw.app.  Contains Resp,Req,App object definitions.
   pylw.app.App() is the WSGI callable object.'''

import routing
import request
import response

class App(object):
    '''This class implements a bare minimum WSGI application'''
    def __init__(self, secret_key=None, user_objects=None):
        self.router = routing.DefaultRouter()
        self.secret_key = secret_key
        self.user_objects = user_objects
        self.hard_coded_path = {}
        if not self.secret_key:
            raise Exception('secret key missing')

    def add_hard_coded_path(self,uri,resource):
        '''Add a hard coded path to the application.  You cannot use variables
           here, but the look up time will be faster than normal.'''

        self.hard_coded_path[uri] = resource

    def __call__(self, env, start_response):
        '''This method is called by the WSGI server.'''

        try:
            req = request.Request(env)
            resp = response.Response(secret_key=self.secret_key, http_cookies=req.get_cookies())
            try:
                self.hard_coded_path[req.path](req,resp,user_objects=self.user_objects)
            except:
                self.router.return_path_resource(
                    req.path,req.url_vars)(req,resp,user_objects=self.user_objects)
        except Exception as ex:
            code = None
            body = None
            try:
                code,body = ex.args
            except:
                if not code or not body: # pragma: no cover
                    code = '500 Server Error'
                    body = 'Unhandled App Exception'
            header_dict = {'Content-Length' : str(len(body))}
            start_response(code, header_dict.items())
            return body

        start_response(resp.status, resp.get_headers())
        return resp.body
