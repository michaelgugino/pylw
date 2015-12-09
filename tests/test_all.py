# content of test_sysexit.py
import pytest
import setup_test_objects
import pylw
import pylw.app


def create_app():
    return pylw.app.App(secret_key="my-new-secret-key")

def app_add_hard_route(app):
    app.add_hard_coded_path('/',setup_test_objects.TestHomeResource)

def start_response(*args):
    pass

def test_all():
    print 'creating app'

    app = create_app()
    assert type(app) == pylw.app.App

    app_add_hard_route(app)
    assert app.hard_coded_path['/'] == setup_test_objects.TestHomeResource

    getenv = setup_test_objects.EnvInput('GET','/')
    assert app(getenv.env,start_response) == 'this is hard coded home'

    postenv = setup_test_objects.EnvInput('POST','/')
    assert app(postenv.env,start_response) == 'this is hard coded post home'

    app.router.add_path('/testing/v1/{var1}',setup_test_objects.TestVarResource)
    assert app.router.root_node_dict['testing'].children['v1'].varchild.isvar

    varenv = setup_test_objects.EnvInput('GET','/testing/v1/testing')
    assert app(varenv.env,start_response) == '{"{var1}": "testing"}'
