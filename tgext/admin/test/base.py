# -*- coding: utf-8 -*-

import os, shutil
from unittest import TestCase
from xmlrpclib import loads, dumps

import beaker
from paste.registry import RegistryManager
from webtest import TestApp
from paste import httpexceptions

import tg
from routes import Mapper
from tg.controllers import TGController
from pylons.testutil import ControllerWrap, SetupCacheGlobal

from beaker.middleware import CacheMiddleware

from pylons.configuration import response_defaults
response_defaults['headers']['Content-Type'] = None

data_dir = os.path.dirname(os.path.abspath(__file__))
session_dir = os.path.join(data_dir, 'session')

def setup_session_dir():
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)

def teardown_session_dir():
    shutil.rmtree(session_dir, ignore_errors=True)


default_environ = {
    'pylons.use_webob' : True,
    'pylons.routes_dict': dict(action='index'),
    'paste.config': dict(global_conf=dict(debug=True))
}

default_map = Mapper()

# Setup a default route for the error controller:
default_map.connect('error/:action/:id', controller='error')
# Setup a default route for the root of object dispatch
default_map.connect('*url', controller='root', action='routes_placeholder')


def make_app(controller_klass=None, environ=None):
    """Creates a `TestApp` instance."""
    if environ is None:
        environ = {}
    environ['pylons.routes_dict'] = {}
    environ['pylons.routes_dict']['action'] = "routes_placeholder"

    if controller_klass is None:
        controller_klass = TGController
        
    app = ControllerWrap(controller_klass)
    app = SetupCacheGlobal(app, environ, setup_cache=True, setup_session=True)
    app = RegistryManager(app)
    app = beaker.middleware.SessionMiddleware(app, {}, data_dir=session_dir)
    app = CacheMiddleware(app, {}, data_dir=os.path.join(data_dir, 'cache'))
    app = httpexceptions.make_middleware(app)
    return TestApp(app)
