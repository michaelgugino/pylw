# content of test_sysexit.py
import pytest
import setup_test_objects
import pylw
import pylw.app


def create_app():
    return pylw.app.App(secret_key="my-new-secret-key")

def app_add_hard_route(app):
    app.add_hard_coded_path('/',setup_test_objects.TestResource)

def test_all():
    print 'creating app'
    app = create_app()
    app_add_hard_route(app)
    assert type(app) == pylw.app.App
