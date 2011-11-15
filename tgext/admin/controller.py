"""Admin Controller"""
import inspect

from tg.controllers import TGController
from tg.decorators import with_trailing_slash, override_template, expose
from tg.exceptions import HTTPNotFound
from tg import config as tg_config

from tgext.crud import CrudRestController
from config import AdminConfig

engine = 'genshi'
try:
    import chameleon.genshi
    import pylons.config
    if 'renderers' in pylons.config and 'chameleon_genshi' in pylons.config['renderers']:
        engine = 'chameleon_genshi'
except ImportError:
    pass

from repoze.what.predicates import in_group

class AdminController(TGController):
    """
    A basic controller that handles User Groups and Permissions for a TG application.
    """
    allow_only = in_group('managers')

    def __init__(self, models, session, config_type=None, translations=None):
        super(AdminController, self).__init__()
        if translations is None:
            translations = {}
        if config_type is None:
            config = AdminConfig(models, translations)
        else:
            config = config_type(models, translations)

        if config.allow_only:
            self.allow_only = config.allow_only

        self.config = config
        self.session = session

        default_renderer = getattr(tg_config,'default_renderer', 'genshi')
        
        self.default_index_template = ':'.join((default_renderer, self.index.decoration.engines.get('text/html')[1]))
        if self.config.default_index_template:
            self.default_index_template = self.config.default_index_template

        self.controllers_cache = {}

    @with_trailing_slash
    @expose('tgext.admin.templates.index')
    def index(self):
        #overrides the template for this method
        original_index_template = self.index.decoration.engines['text/html']
        new_engine = self.default_index_template.split(':')
        new_engine.extend(original_index_template[2:])
        self.index.decoration.engines['text/html'] = new_engine
        return dict(models=[model.__name__ for model in self.config.models.values()])

    def _make_controller(self, config, session):
        m = config.model
        Controller = config.defaultCrudRestController
        class ModelController(Controller):
            model        = m
            table        = config.table_type(session)
            table_filler = config.table_filler_type(session)
            new_form     = config.new_form_type(session)
            new_filler   = config.new_filler_type(session)
            edit_form    = config.edit_form_type(session)
            edit_filler  = config.edit_filler_type(session)
            allow_only   = config.allow_only
        menu_items = None
        if self.config.include_left_menu:
            menu_items = self.config.models
        return ModelController(session, menu_items)

    @expose()
    def _lookup(self, model_name, *args):
        model_name = model_name[:-1]
        try:
            model = self.config.models[model_name]
        except KeyError:
            raise HTTPNotFound().exception

        try:
            controller = self.controllers_cache[model_name]
        except KeyError:
            config = self.config.lookup_controller_config(model_name)
            controller = self.controllers_cache[model_name] = self._make_controller(config, self.session)

        return controller, args

    @expose()
    def lookup(self, model_name, *args):
        return self._lookup(model_name, *args)
