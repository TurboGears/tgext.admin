"""Main Controller"""
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
from tgext.admin.config import load_config

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

    def __init__(self, session, model, config=None):
        if config is None:
            config = {}
        if Catwalk is not None:
            self.catwalk     = SecuredCatwalk(session)
        if Rum is not None:
            self.rum = Rum(model)

        config = load_config(session, model, config)

        m=model
        class UserController(CrudRestController):
            model = m.User
            table = config.user_table
            table_filler = config.user_table_filler
            new_form  = config.user_new_form
            edit_form = config.user_edit_form
            edit_filler = config.user_edit_filler

        self.users       = UserController(session)

        class GroupController(CrudRestController):
            model = m.Group
            table         = config.group_table
            table_filler  = config.group_table_filler
            new_form      = config.group_new_form
            edit_form     = config.group_edit_form
            edit_filler   = config.group_edit_filler
            
        self.groups      = GroupController(session)
        
        class PermissionController(CrudRestController):
            model = m.Permission
            table         = config.permission_table
            table_filler  = config.permission_table_filler
            new_form      = config.permission_new_form
            edit_form     = config.permission_edit_form
            edit_filler   = config.permission_edit_filler
            
        self.permissions      = PermissionController(session)

    @with_trailing_slash
    @expose(engine+':tgext.admin.templates.index')
    def index(self):
        return dict(page='index')
