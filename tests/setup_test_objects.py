import pylw
import pylw.app, pylw.resource
import cStringIO
import json

body_dict = {
'var1' : 'value 1',
'var2' : 'value 2'
}

test_input_buff = cStringIO.StringIO(json.dumps(body_dict))


test_post_env = {
    'wsgi.input' : test_input_buff,
    'CONTENT_LENGTH' : str(len(test_input_buff.getvalue())),
    'HTTP_COOKIE' : 'cookie1=value1;',
    'QUERY_STRING' : '?x=1&y=2',
    'REQUEST_METHOD' : 'POST'
}

test_get_env = {
    'wsgi.input' : '',
    'CONTENT_LENGTH' : '0',
    'HTTP_COOKIE' : 'cookie1=value1;',
    'QUERY_STRING' : '?x=1&y=2',
    'REQUEST_METHOD' : 'GET'
}

class EnvInput(object):

    def __init__(self, type, path):
        if type == 'POST':
            self.test_input_buff = cStringIO.StringIO(json.dumps(body_dict))

            self.env = {
                'wsgi.input' : self.test_input_buff,
                'CONTENT_LENGTH' : str(len(self.test_input_buff.getvalue())),
                'HTTP_COOKIE' : 'cookie1=value1;',
                'QUERY_STRING' : '?x=1&y=2',
                'REQUEST_METHOD' : type,
                'PATH_INFO' : path
            }

        elif type == 'GET':
            self.test_input_buff = cStringIO.StringIO('')
            self.env = {
                'wsgi.input' : self.test_input_buff,
                'CONTENT_LENGTH' : str(len(self.test_input_buff.getvalue())),
                'HTTP_COOKIE' : 'cookie1=value1;',
                'QUERY_STRING' : '?x=1&y=2',
                'REQUEST_METHOD' : type,
                'PATH_INFO' : path
            }

class TestHomeResource(pylw.resource.DefaultResource):
    def on_get(self,req,resp,user_objects=None):
        resp.status = '200 OK'
        resp.body = 'this is hard coded home'
        #resp.add_cookie('testk','value1')
        resp.add_header('Content-Type','text/html')

    def on_post(self,req,resp,user_objects=None):
        resp.status = '200 OK'
        resp.body = 'this is hard coded post home'
        #resp.add_cookie('testk','value1')
        resp.add_header('Content-Type','text/html')

class TestVarResource(pylw.resource.DefaultResource):
    def on_get(self,req,resp,user_objects=None):
        resp.status = '200 OK'
        resp.body = json.dumps(req.url_vars)
        #resp.add_cookie('testk','value1')
        resp.add_header('Content-Type','text/html')


#test_app = pylw.app.App(secret_key="my-new-secret-key")
