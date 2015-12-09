'''pylw.request.  Contains Request object definition for parsing environment
   input from WSGI.'''

import Cookie
import urlparse

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
