import routing
import itsdangerous
import Cookie

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
        C = Cookie.SimpleCookie()
        if req_cookies:
            C.load(req_cookies)
        return C

    def create_secret_signer(self,secret_key=None):
        return itsdangerous.Serializer(secret_key)

    def get_headers(self):
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
        try:
            return self.__cookies[cookie].value
        except:
            return None

    def get_signed_cookie(self,cookie):
        try:
            return self.s.loads(self.__cookies[cookie].value)
        except:
            return None

    def add_signed_cookie(self,k,v):
        v = self.s.dumps(v)
        self.__cookies[k] = v

    def add_cookie(self,k,v):
        self.__cookies[k] = v

    def add_header(self,k,v):
        self.__header_dict[k] = v

class Request(object):
    '''An object that holds request values'''

    def __init__(self,env):
        self.raw_env = env
        self.request_method = env['REQUEST_METHOD']
        self.posted_body = None
        self.path = env['PATH_INFO']
        self.url_vars = {}
        self.path_parsed = self.parse_path(self.path)
        self.read_post_body()
        if 'HTTP_COOKIE' in env:
            self.cookies = env['HTTP_COOKIE']
        else:
            self.cookies = None

    def read_post_body(self):
        '''Read the body of the POST request'''
        if self.request_method == 'POST':
            stream = self.raw_env['wsgi.input']
            self.posted_body = stream.read(int(self.raw_env['CONTENT_LENGTH']))

    def get_cookies(self):
        return self.cookies

    def parse_path(self, url):
        l = url.split('/')
        if l[0] == '':
            l = l[1:]
        l.reverse()
        return l


class App(object):
    '''This class implements a bare minimum WSGI application'''
    def __init__(self):
        self.router = routing.DefaultRouter()
        self.secret_key = None

    def __call__(self, env, start_response):
        '''This method is called by the WSGI server.'''
        if not self.secret_key:
            print "secret_key not set, exiting"
            exit()
        req = Request(env)
        resp = Response(secret_key=self.secret_key, http_cookies=req.get_cookies())

        controller = self.router.return_path_resource(req.path,req.url_vars)(req,resp)
        controller()

        start_response(resp.status, resp.get_headers())
        return resp.body
