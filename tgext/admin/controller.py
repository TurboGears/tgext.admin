"""Admin Controller"""

import inspect

from tg.controllers import TGController, expose
from tg.decorators import with_trailing_slash

try:
    import tw.dojo
    from catwalk.tg2.dojo_controller import DojoCatwalk as Catwalk
except ImportError:
    try:
        from catwalk.tg2 import Catwalk
    except:
        Catwalk = None
Rum = None

from tgext.crud import CrudRestController
from tgext.admin.config import AdminConfig, RestControllerConfig

engine = 'genshi'
try:
    import chameleon.genshi
    import pylons.config
    if 'chameleon_genshi' in pylons.config['renderers']:
        engine = 'chameleon_genshi'
    else:
        import warnings
        #warnings.warn('The renderer for \'chameleon_genshi\' templates is missing.'\
        #              'Your code could run much faster if you'\
        #              'add the following line in you app_cfg.py: "base_config.renderers.append(\'chameleon_genshi\')"')
except ImportError:
    pass

from repoze.what.predicates import in_group

class SecuredCatwalk(Catwalk):
    pass
    allow_only = in_group('managers')
    
class AdminController(TGController):
    """
    A basic controller that handles User Groups and Permissions for a TG application.
    """
    allow_only = in_group('managers')

    def _make_controller(self, config):
        m = config.model
        class ModelController(CrudRestController):
            model        = m
            table        = config.table
            table_filler = config.table_filler
            new_form     = config.new_form
            edit_form    = config.edit_form
            edit_filler  = config.edit_filler
            allow_only   = config.allow_only
        return ModelController(config.session)

    def __init__(self, models, sessions=None, translations=None, config_type=None):
        if translations is None:
            translations = {}
        if config_type is None:
            config = AdminConfig(models, sessions, translations)
        else:
            config = config_type(models, sessions, translations)
            
        for model_name in config.keys():
            model_config = config[model_name]
            if isinstance(model_config, RestControllerConfig) and not hasattr(self, model_name):
                crud_controller = self._make_controller(model_config)
                setattr(self, model_config.model.__name__, crud_controller)
        
    @with_trailing_slash
    @expose(engine+':tgext.admin.templates.index')
    def index(self):
        return dict(page='index')
