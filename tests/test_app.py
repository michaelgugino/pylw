# content of test_sysexit.py
import pytest
import setup_test_objects
import pylw
import pylw.app


@pytest.fixture(scope="module")
def tapp():
    return pylw.app.App(secret_key="my-new-secret-key")


def app_add_hard_route(tapp):
    tapp.add_hard_coded_path('/home',setup_test_objects.TestHomeResource())

def start_response(*args):
    pass

def test_create_app(tapp):
    assert type(tapp) == pylw.app.App

def test_add_hard_route(tapp):
    app_add_hard_route(tapp)
    assert type(tapp.hard_coded_path['/home']) == setup_test_objects.TestHomeResource

def test_add_root_route(tapp):
    tapp.router.add_path('/',setup_test_objects.TestHomeResource())
    getenv = setup_test_objects.EnvInput('GET','/')
    assert tapp(getenv.env,start_response) == 'this is hard coded home'

def test_get_env(tapp):
    getenv = setup_test_objects.EnvInput('GET','/home')
    assert tapp(getenv.env,start_response) == 'this is hard coded home'

def test_post_env(tapp):
    postenv = setup_test_objects.EnvInput('POST','/home')
    assert tapp(postenv.env,start_response) == 'this is hard coded post home'

def test_add_route_var(tapp):
    tapp.router.add_path('/testing/v1/{var1}',setup_test_objects.TestVarResource())
    assert tapp.router.root_node_dict['testing'].children['v1'].varchild.isvar

def test_url_vars(tapp):
    varenv = setup_test_objects.EnvInput('GET','/testing/v1/testing')
    assert tapp(varenv.env,start_response) == '{"{var1}": "testing"}'

def test_existing_root_route(tapp):
    tapp.router.add_path('/testing/v2',setup_test_objects.TestHomeResource())
    getenv = setup_test_objects.EnvInput('GET','/testing/v2')
    assert tapp(getenv.env,start_response) == 'this is hard coded home'

def test_child_of_var_route(tapp):
    tapp.router.add_path('/testing/v1/{var1}/child',setup_test_objects.TestVarResource())
    getenv = setup_test_objects.EnvInput('GET','/testing/v1/testing/child')
    assert tapp(getenv.env,start_response) == '{"{var1}": "testing"}'

def test_no_key():
    with pytest.raises(Exception):
        a = pylw.app.App()

def test_raise_404(tapp):
    getenv = setup_test_objects.EnvInput('GET','/bad/path')
    assert tapp(getenv.env,start_response) == '404: no path found for: /bad/path'

def test_bad_resource(tapp):
    tapp.router.add_path('/badresource',setup_test_objects.BadResource())
    getenv = setup_test_objects.EnvInput('GET','/badresource')
    assert tapp(getenv.env,start_response) == 'Unhandled App Exception'

def test_config_dict():
    config_dict = {'secret_key' : 'config_dict_secret_key'}
    a = pylw.app.App(secret_key="my-new-secret-key",config_dict=config_dict)
    assert a.secret_key == 'config_dict_secret_key'
