'''pylw.request.  Contains Request object definition for parsing environment
   input from WSGI.'''

import Cookie
#import urlparse
import pylw.qs_parse

class Request(object):
    '''An object that holds request values'''

    def __init__(self,env):
        '''Initializes the request object.'''
        self.raw_env = env
        self.request_method = env['REQUEST_METHOD']
        self.posted_body = None
        self.path = env['PATH_INFO']
        self.url_vars = {}

        #uncomment the next line if you want to use python to parse query string.
        #This is probably safer than the C method, and it will handle url encoded
        #strings as well, whereas the c parser will not.
        #self.query_dict = urlparse.parse_qs(env['QUERY_STRING'],keep_blank_values=True)
        if env['QUERY_STRING'] == '':
            self.query_dict = {}
        else:
            self.query_dict = pylw.qs_parse.parse_qs(env['QUERY_STRING'])

        #self.read_post_body()
        if 'HTTP_COOKIE' in env:
            self.cookies = env['HTTP_COOKIE']
        else:
            self.cookies = None

    def read_post_body(self, max_read=4096):
        '''Read the body of the POST request, default max of 4096 bytes'''
        if self.request_method == 'POST':
            stream = self.raw_env['wsgi.input']
            blen = int(self.raw_env['CONTENT_LENGTH'])
            if blen > max_read:
                blen = max_read
            self.posted_body = stream.read(blen)
            stream.close()

    def get_cookies(self):
        '''return self.cookies'''
        return self.cookies
