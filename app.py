import routing

class Response(object):
    '''Response object for sending back to WSGI server.  It holds the headers
       and body'''

    def __init__(self):
        '''Initialize our object.'''
        self.__header_dict = {}
        self.body = None
        self.status = None

    def get_headers(self):
        self.__header_dict['Content-Length'] = str(len(self.body))
        return self.__header_dict.items()

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

    def read_post_body(self):
        '''Read the body of the POST request'''
        if self.request_method == 'POST':
            stream = self.raw_env['wsgi.input']
            self.posted_body = stream.read(int(self.raw_env['CONTENT_LENGTH']))

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

    def __call__(self, env, start_response):
        '''This method is called by the WSGI server.'''

        req = Request(env)
        resp = Response()

        controller = self.router.return_path_resource(req.path,req.url_vars)(req,resp)
        controller()

        start_response(resp.status, resp.get_headers())
        return resp.body
