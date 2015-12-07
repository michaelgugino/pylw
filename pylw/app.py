'''pylw.app.  Contains Resp,Req,App object definitions.
   pylw.app.App() is the WSGI callable object.'''

import routing
import itsdangerous
import Cookie
import urlparse

class Response(object):
    '''Response object for sending back to WSGI server.  It holds the headers
       and body'''

    def __init__(self, secret_key=None, http_cookies=None):
        '''Initialize our object.'''
        self.__header_dict = {}
        self.body = None
        self.status = None
        self.s = self.create_secret_signer(secret_key=secret_key)
        self.__cookies = self.parse_http_cookies(http_cookies)

    def parse_http_cookies(self, req_cookies):
        '''Parse http cookies into a SimpleCookie object'''
        C = Cookie.SimpleCookie()
        if req_cookies:
            C.load(req_cookies)
        return C

    def create_secret_signer(self,secret_key=None):
        '''Create our secret signer object'''
        return itsdangerous.Serializer(secret_key)

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

class Request(object):
    '''An object that holds request values'''

    def __init__(self,env):
        '''Initializes the request object.'''
        self.raw_env = env
        self.request_method = env['REQUEST_METHOD']
        self.posted_body = None
        self.path = env['PATH_INFO']
        self.url_vars = {}
        self.query_dict = urlparse.parse_qs(env['QUERY_STRING'],keep_blank_values=True)
        #self.read_post_body()
        if 'HTTP_COOKIE' in env:
            self.cookies = env['HTTP_COOKIE']
        else:
            self.cookies = None

    def read_post_body(self):
        #this is probably unsafe and we should limit how much we read.
        '''Read the body of the POST request'''
        if self.request_method == 'POST':
            stream = self.raw_env['wsgi.input']
            self.posted_body = stream.read(int(self.raw_env['CONTENT_LENGTH']))

    def get_cookies(self):
        '''return self.cookies'''
        return self.cookies


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
            req = Request(env)
            resp = Response(secret_key=self.secret_key, http_cookies=req.get_cookies())

            try:
                self.hard_coded_path[req.path](req,resp,user_objects=self.user_objects)()
            except:
                self.router.return_path_resource(
                    req.path,req.url_vars)(req,resp,user_objects=self.user_objects)()
        except Exception as ex:
            code,body = ex.args
            if not code or not body:
                code = '500 Server Error'
                body = 'Unhandled App Exception'
            header_dict = {'Content-Length' : str(len(body))}
            start_response(code, header_dict.items())
            return body
        start_response(resp.status, resp.get_headers())
        return resp.body
