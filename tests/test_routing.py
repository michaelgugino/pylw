# content of test_sysexit.py
import pytest
import setup_test_objects
import pylw
import pylw.routing

@pytest.fixture(scope="module")
def trouter():
    return pylw.routing.DefaultRouter()

def test_router_404(trouter):
    with pytest.raises(Exception):
        uri = '/not/implemented'
        vardict = dict()
        a = trouter.return_path_resource(uri,var_dict)()
