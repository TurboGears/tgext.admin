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
from tgext.admin.widgets import load_config

"""
class GroupController(CrudRestController):
    table = group_table
    table_filler = group_table_filler
    model = Group

class PermissionController(CrudRestController):
    table = permission_table
    table_filler = permission_table_filler
    model = Permission
"""
from repoze.what.predicates import in_group

class SecuredCatwalk(Catwalk):
    pass
    #allow_only = in_group('managers')


class AdminController(TGController):
    """
    A basic controller that handles User Groups and Permissions for a TG application.
    """
    def __init__(self, session, model):
        if Catwalk is not None:
            self.catwalk     = SecuredCatwalk(session)
        if Rum is not None:
            self.rum = Rum(model)

        config = load_config(session, model)

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
    @expose('tgext.admin.templates.index')
    def index(self):
        return dict(page='index')
