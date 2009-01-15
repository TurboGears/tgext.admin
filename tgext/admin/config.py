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


def load_config(DBSession, model, load_config):
    config = Bunch()
    m = model
    
    if not 'translations' in load_config:
        load_config['translations']  = {}
        
#    config_vars = ['user_id', 'user_name', 'email_address', 'password', 'display_name', 'group_id']
    user_id_field      = load_config['translations'].get('user_id', 'user_id')
    user_name_field    = load_config['translations'].get('user_name', 'user_name')
    email_field        = load_config['translations'].get('email_address', 'email_address')
    password_field     = load_config['translations'].get('password', 'password')
    display_name_field = load_config['translations'].get('display_name', 'display_name')
    group_id_field     = load_config['translations'].get('group_id', 'group_id')
    group_name_field     = load_config['translations'].get('group_name', 'group_name')
    permission_id_field              = load_config['translations'].get('permission_id', 'permission_id')
    permission_name_field            = load_config['translations'].get('permission_name', 'permission_name')
    permission_description_field     = load_config['translations'].get('permission_description', 'description')
    
    if 'user_table' not in load_config:
        class UserTable(TableBase):
            __model__ = m.User
            #__limit_fields__ = ['display_name', 'email_address']
            __omit_fields__ = [user_id_field, '_password', password_field]
            __url__ = '../users.json'
        config.user_table = UserTable(DBSession)
    else:
        config.user_table = load_config.user_table
        
    if 'user_table_filler' not in load_config:
        class UserTableFiller(TableFiller):
            __model__ = m.User
            __omit_fields__ = ['_password', password_field]
        config.user_table_filler = UserTableFiller(DBSession)
    else:
        config.user_table_filler = load_config.user_table_filler

    class UserEditForm(EditableForm):
        __model__ = m.User
        __require_fields__     = [user_name_field, email_field]
        __omit_fields__        = [password_field, 'created', '_password']
        __hidden_fields__      = [user_id_field]
        __field_order__        = [user_name_field, email_field, display_name_field, 'groups']
    if email_field is not None:
        setattr(UserEditForm, email_field, TextField)
    if display_name_field is not None:
        setattr(UserEditForm, display_name_field, TextField)

    config.user_edit_form = UserEditForm(DBSession)

    class UserNewForm(AddRecordForm):
        __model__ = m.User
        __require_fields__     = [user_name_field, email_field]
        __omit_fields__        = [password_field, 'created', '_password']
        __hidden_fields__      = [user_id_field]
        __field_order__        = [user_name_field, email_field, display_name_field, 'groups']
    if email_field is not None:
        setattr(UserNewForm, email_field, TextField)
    if display_name_field is not None:
        setattr(UserNewForm, display_name_field, TextField)

    config.user_new_form = UserNewForm(DBSession)

    class UserEditFiller(RecordFiller):
        __model__ = m.User
    config.user_edit_filler = UserEditFiller(DBSession)

    class GroupTable(TableBase):
        __model__ = m.Group
        __limit_fields__ = [group_name_field, 'permissions']
        __url__ = '../groups.json'
    config.group_table = GroupTable(DBSession)

    class GroupTableFiller(TableFiller):
        __model__ = m.Group
        __limit_fields__ = [group_id_field, group_name_field, 'permissions']
    config.group_table_filler = GroupTableFiller(DBSession)

    class GroupNewForm(AddRecordForm):
        __model__ = m.Group
        __limit_fields__ = [group_name_field, 'permissions']
    config.group_new_form = GroupNewForm(DBSession)

    class GroupEditForm(EditableForm):
        __model__ = m.Group
        __limit_fields__ = [group_id_field, 'group_name', 'permissions']
    config.group_edit_form = GroupEditForm(DBSession)

    class GroupEditFiller(RecordFiller):
        __model__ = m.Group
    config.group_edit_filler = GroupEditFiller(DBSession)

    class PermissionTable(TableBase):
        __model__ = m.Permission
        __limit_fields__ = [permission_name_field, permission_description_field, 'groups']

        __url__ = '../permissions.json'
    config.permission_table = PermissionTable(DBSession)

    class PermissionTableFiller(TableFiller):
        __model__ = m.Permission
        __limit_fields__ = [permission_id_field, permission_name_field, permission_description_field, 'groups']
    config.permission_table_filler = PermissionTableFiller(DBSession)

    class PermissionNewForm(AddRecordForm):
        __model__ = m.Permission
        __limit_fields__ = [permission_name_field, permission_description_field, 'groups']
    config.permission_new_form = PermissionNewForm(DBSession)

    class PermissionEditForm(EditableForm):
        __model__ = m.Permission
        __limit_fields__ = [permission_name_field, permission_description_field,'groups']
    config.permission_edit_form = PermissionEditForm(DBSession)

    class PermissionEditFiller(RecordFiller):
        __model__ = m.Permission
    config.permission_edit_filler = PermissionEditFiller(DBSession)

    return config