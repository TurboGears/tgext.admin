"""Admin Controller"""
import logging
log = logging.getLogger('tgext.admin')

from tg.controllers import TGController
from tg.decorators import with_trailing_slash, override_template, expose
from tg.exceptions import HTTPNotFound
from tg import config as tg_config, request
from tg import tmpl_context

from .config import AdminConfig
from .utils import make_pager_args

try:
    from tg.predicates import in_group
except ImportError:
    from repoze.what.predicates import in_group

try:
    from tg.configuration import milestones
except ImportError:
    milestones = None


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

        if config.allow_only is not None:
            self.allow_only = config.allow_only

        self.config = config
        self.session = session
        self.missing_template = False

        if self.config.default_index_template:
            expose(self.config.default_index_template)(self.index)
        else:
            if milestones is None:
                self._choose_index_template()
            else:
                milestones.renderers_ready.register(self._choose_index_template)

        self.controllers_cache = {}

    @classmethod
    def _get_default_renderer(cls):
        default_renderer = getattr(tg_config, 'default_renderer', 'genshi')
        if default_renderer not in ['genshi', 'mako', 'jinja', 'kajiki']:
            if 'genshi' in tg_config.renderers:
                default_renderer = 'genshi'
            elif 'kajiki' in tg_config.renderers:
                default_renderer = 'kajiki'
            elif 'mako' in tg_config.renderers:
                default_renderer = 'mako'
            elif 'jinja' in tg_config.renderers:
                default_renderer = 'jinja'
            else:
                default_renderer = None
                log.warn('TurboGears admin supports only Genshi, Kajiki, Mako and Jinja.'
                         ' please make sure you add at least one of those to your config/app_cfg.py'
                         ' base_config.renderers list.')

        return default_renderer

    def _choose_index_template(self):
        default_renderer = self._get_default_renderer()
        if not default_renderer:
            self.missing_template = True
            return

        index_template = ':'.join((default_renderer, self.config.layout.template_index))
        expose(index_template)(self.index)

    @with_trailing_slash
    @expose()
    def index(self):
        if self.missing_template:
            raise Exception(
                'TurboGears admin supports only Genshi, Kajiki, Mako and Jinja.'
                ' please make sure you add at least one of those to your config/app_cfg.py'
                ' base_config.renderers list.'
            )

        return dict(config=self.config,
                    payoff=self.config.index_payoff,
                    project_name=self.config.project_name or tg_config['package_name'].capitalize(),
                    model_config=lambda model: (model.lower(),
                                                getattr(self.config, model.lower(),
                                                        self.config.DefaultControllerConfig)),
                    models=[model.__name__ for model in self.config.models.values()])

    @classmethod
    def make_controller(cls, config, session, left_menu_items=None):
        """New CRUD controllers using the admin configuration can be created using this."""
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

            if hasattr(config.layout, 'crud_resources'):
                resources = config.layout.crud_resources

            def _before(self, *args, **kw):
                super(self.__class__, self)._before(*args, **kw)

                tmpl_context.make_pager_args = make_pager_args

                if request.response_type not in ('application/json',):
                    default_renderer = AdminController._get_default_renderer()
                    for action in ('get_all', 'new', 'edit'):
                        for template in config.layout.crud_templates.get(action, []):
                            if template.startswith(default_renderer):
                                override_template(getattr(self, action), template)

        return ModelController(session, left_menu_items)

    @expose()
    def _lookup(self, model_name, *args):
        model_name = model_name[:-1]
        try:
            model = self.config.models[model_name]
        except KeyError:
            raise HTTPNotFound()

        try:
            controller = self.controllers_cache[model_name]
        except KeyError:
            config = self.config.lookup_controller_config(model_name)

            menu_items = None
            if self.config.include_left_menu:
                menu_items = self.config.models

            controller = self.controllers_cache[model_name] = self.make_controller(config, self.session,
                                                                                   left_menu_items=menu_items)

        return controller, args

    @expose()
    def lookup(self, model_name, *args):
        return self._lookup(model_name, *args)
