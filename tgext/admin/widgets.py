from tw.forms import TextField

from tg.util import Bunch
#from tgtest.model import DBSession, User, Group, Permission
try:
    import tw.dojo
    from sprox.dojo.tablebase import DojoTableBase as TableBase
    from sprox.dojo.fillerbase import DojoTableFiller as TableFiller
except ImportError:
    from sprox.tablebase import TableBase
    from sprox.fillerbase import TableFiller

from sprox.fillerbase import RecordFiller
from sprox.formbase import AddRecordForm, EditableForm


def load_config(DBSession, model):
    config = Bunch()
    m = model

    class UserTable(TableBase):
        __model__ = m.User
        #__limit_fields__ = ['display_name', 'email_address']
        __omit_fields__ = ['user_id', '_password', 'password', 'town_id']
        __url__ = '../users.json'
    config.user_table = UserTable(DBSession)

    class UserTableFiller(TableFiller):
        __model__ = m.User
    #    __limit_fields__ = ['user_id', 'display_name', 'email_address']
        __omit_fields__ = ['_password', 'password', 'town_id']
    config.user_table_filler = UserTableFiller(DBSession)

    class UserEditForm(EditableForm):
        __model__ = m.User
        __require_fields__     = ['user_name', 'email_address']
        __omit_fields__        = ['password', 'created', '_password']
        __hidden_fields__      = ['user_id']
        __field_order__        = ['user_name', 'email_address', 'display_name', 'groups']
        email_address          = TextField
        display_name           = TextField

    config.user_edit_form = UserEditForm(DBSession)

    class UserNewForm(AddRecordForm):
        __model__ = m.User
        __require_fields__     = ['user_name', 'email_address']
        __omit_fields__        = ['_password', 'created', 'password']
        __hidden_fields__      = ['user_id']
        __field_order__        = ['user_name', 'email_address', 'display_name', 'groups']
        email_address          = TextField
        display_name           = TextField
    config.user_new_form = UserNewForm(DBSession)

    class UserEditFiller(RecordFiller):
        __model__ = m.User
    config.user_edit_filler = UserEditFiller(DBSession)

    class GroupTable(TableBase):
        __model__ = m.Group
        __limit_fields__ = ['group_name', 'permissions']
        __url__ = '../groups.json'
    config.group_table = GroupTable(DBSession)

    class GroupTableFiller(TableFiller):
        __model__ = m.Group
        __limit_fields__ = ['group_id', 'group_name', 'permissions']
    config.group_table_filler = GroupTableFiller(DBSession)

    class GroupNewForm(AddRecordForm):
        __model__ = m.Group
        __limit_fields__ = ['group_name', 'permissions']
    config.group_new_form = GroupNewForm(DBSession)

    class GroupEditForm(EditableForm):
        __model__ = m.Group
        __limit_fields__ = ['group_id', 'group_name', 'permissions']
    config.group_edit_form = GroupEditForm(DBSession)

    class GroupEditFiller(RecordFiller):
        __model__ = m.Group
    config.group_edit_filler = GroupEditFiller(DBSession)

    class PermissionTable(TableBase):
        __model__ = m.Permission
        __limit_fields__ = ['permission_name', 'description', 'groups']

        __url__ = '../permissions.json'
    config.permission_table = PermissionTable(DBSession)

    class PermissionTableFiller(TableFiller):
        __model__ = m.Permission
        __limit_fields__ = ['permission_id', 'permission_name', 'description', 'groups']
    config.permission_table_filler = PermissionTableFiller(DBSession)

    class PermissionNewForm(AddRecordForm):
        __model__ = m.Permission
        __limit_fields__ = ['permission_name', 'description', 'groups']
    config.permission_new_form = PermissionNewForm(DBSession)

    class PermissionEditForm(EditableForm):
        __model__ = m.Permission
        __limit_fields__ = ['permission_name', 'description','groups']
    config.permission_edit_form = PermissionEditForm(DBSession)

    class PermissionEditFiller(RecordFiller):
        __model__ = m.Permission
    config.permission_edit_filler = PermissionEditFiller(DBSession)

    return config