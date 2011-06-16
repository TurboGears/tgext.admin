import os
from webtest import TestApp
import tg
import tests
from tg.util import DottedFileNameFinder
from tg.configuration import AppConfig

class TestConfig(AppConfig):

    def __init__(self):
        AppConfig.__init__(self)
        self.renderers = ['json', 'genshi', 'mako']
        from pylons.configuration import config
        config['renderers'] = ['json', 'genshi', 'mako']
        self.render_functions = tg.util.Bunch()
        self.package = tests
        #self.default_renderer = 'genshi'
        self.globals = self
        self.helpers = {}
        self.auth_backend = None
        self.auto_reload_templates = False
        self.use_legacy_renderer = False
        self.use_dotted_templatenames = False
        self.use_sqlalchemy=True
        self.serve_static = False
        
        root = os.path.dirname(os.path.dirname(tests.__file__))
        test_base_path = os.path.join(root, 'tests')
        test_config_path = test_base_path #os.path.join(test_base_path, folder)
        self.paths=tg.util.Bunch(
                    root=test_base_path,
                    controllers=os.path.join(test_config_path, 'controllers'),
                    static_files=os.path.join(test_config_path, 'public'),
                    templates=[os.path.join(test_config_path, 'templates')],
                    i18n=os.path.join(test_config_path, 'i18n')
                    )
        

        #xxx: why not use memory db?
        values = {
            'sqlalchemy.url':'sqlite:///'+root+'/test.db',
            'session':tests.model.DBSession,
            'model':tests.model,
            'use_dotted_templatenames': True,
            'renderers': ['json', 'genshi', 'mako']
                  
        }
        
        #Then we overide those values with what was passed in
        for key, value in values.items():
            setattr(self, key, value)

    def setup_helpers_and_globals(self):
        tg.config['pylons.app_globals'] = self.globals
        tg.config['pylons.h'] = self.helpers
        g = tg.config['pylons.app_globals']
        g.dotted_filename_finder = DottedFileNameFinder()

        
_app = None
def app_from_config(base_config, deployment_config=None):
    global _app
    if _app is None:
        if not deployment_config:
            deployment_config = {'debug': 'true',
                                 'error_email_from': 'paste@localhost',
                                 'smtp_server': 'localhost',
                                 }
        
        env_loader = base_config.make_load_environment()
        app_maker = base_config.setup_tg_wsgi_app(env_loader)
        app = TestApp(app_maker(deployment_config, full_stack=True))
        _app = app
    return _app