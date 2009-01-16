"""Admin Controller"""
from sqlalchemy.orm import class_mapper
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
from tgext.admin.tgadminconfig import TGAdminConfig

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

    def __init__(self, models, session, translations=None, config_type=None):
        if translations is None:
            translations = {}
        if config_type is None:
            config = TGAdminConfig(models, translations)
        else:
            config = config_type(models, translations)

        if config.index_template:
            engines =  engines = self.index.decoration.engines
            text_engine = engines.get('text/html')
            template = config.index_template.split(':')
            template.extend(text_engine[2:])
            engines['text/html'] = template
        
        if config.allow_only:
            self.allow_only = config.allow_only

        self.config = config
        self.session = session
        
    @with_trailing_slash
    @expose(engine+':tgext.admin.templates.index')
    def index(self):
        return dict(page='index', models=[model.__name__ for model in self.config.models.values()])
 
    def _make_controller(self, config, session):
        m = config.model
        class ModelController(CrudRestController):
            model        = m
            table        = config.table_type(session)
            table_filler = config.table_filler_type(session)
            new_form     = config.new_form_type(session)
            new_filler   = config.new_filler_type(session)
            edit_form    = config.edit_form_type(session)
            edit_filler  = config.edit_filler_type(session)
            allow_only   = config.allow_only
        return ModelController(session)
    
    @expose()
    def lookup(self, model_name, *args):
        model = self.config.models[model_name]
        config = self.config.lookup_controller_config(model_name)
        controller = self._make_controller(config, self.session)
        return controller, args
