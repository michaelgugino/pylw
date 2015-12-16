# content of test_sysexit.py
import pytest
import setup_test_objects
import pylw
import pylw.routing

@pytest.fixture(scope="module")
def trouter():
    return pylw.routing.DefaultRouter()

@pytest.fixture(scope="module")
def tcrouter():
    return pylw.routing.CRouter()

def somefun():
    pass

def test_router_add_path(trouter):
    trouter.add_path('/rootnode',setup_test_objects.TestHomeResource())
    assert type(trouter.root_node_dict['rootnode']) == pylw.routing.Node

def test_router_rootnode_404(trouter):
    with pytest.raises(Exception):
        uri = '/badroot/somechild'
        vardict = dict()
        a = trouter.return_path_resource(uri,var_dict)()

def test_router_childnode_404(trouter):
    with pytest.raises(Exception):
        uri = '/rootnode/badchild'
        vardict = dict()
        a = trouter.return_path_resource(uri,var_dict)()

def test_router_add_varchild(trouter):
    trouter.add_path('/rootnode/{var1}',setup_test_objects.TestHomeResource())
    assert type(trouter.root_node_dict['rootnode'].varchild) == pylw.routing.Node

def test_router_get_var_resource(trouter):
    a = trouter.return_path_resource('/rootnode/test',dict())
    assert type(a) == setup_test_objects.TestHomeResource

def test_add_route_no_leading_slash(trouter):
    trouter.add_path('rootnode/somechild/child2',setup_test_objects.TestHomeResource())


#####
# CRouter functions below
#####

def test_router_add_path(tcrouter):
    tcrouter.add_path('/rootnode',setup_test_objects.TestHomeResource())
    assert type(tcrouter.root_node_dict['rootnode']) == pylw.routing.Node

def test_router_rootnode_404(tcrouter):
    with pytest.raises(Exception):
        uri = '/badroot/somechild'
        vardict = dict()
        a = tcrouter.return_path_resource(uri,var_dict)()

def test_router_childnode_404(tcrouter):
    with pytest.raises(Exception):
        uri = '/rootnode/badchild'
        vardict = dict()
        a = tcrouter.return_path_resource(uri,var_dict)()

def test_router_add_varchild(tcrouter):
    tcrouter.add_path('/rootnode/{var1}',setup_test_objects.TestHomeResource())
    assert type(tcrouter.root_node_dict['rootnode'].varchild) == pylw.routing.Node

def test_router_get_var_resource(tcrouter):
    a = tcrouter.return_path_resource('/rootnode/test',dict())
    assert type(a) == setup_test_objects.TestHomeResource

def test_add_route_no_leading_slash(tcrouter):
    tcrouter.add_path('rootnode/somechild/child2',setup_test_objects.TestHomeResource())
