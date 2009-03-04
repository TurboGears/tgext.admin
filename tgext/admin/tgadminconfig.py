import inspect
from tw.forms import TextField
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.exc import UnmappedClassError
from config import AdminConfig, CrudRestControllerConfig

try:
    import tw.dojo
    from sprox.dojo.tablebase import DojoTableBase as TableBase
    from sprox.dojo.fillerbase import DojoTableFiller as TableFiller
    from sprox.dojo.formbase import DojoAddRecordForm as AddRecordForm, DojoEditableForm as EditableForm
except ImportError:
    from sprox.tablebase import TableBase
    from sprox.fillerbase import TableFiller
    from sprox.formbase import AddRecordForm, EditableForm

from sprox.fillerbase import RecordFiller, AddFormFiller

class UserControllerConfig(CrudRestControllerConfig):
    def _do_init_with_translations(self, translations):
        
        user_id_field      = translations.get('user_id',       'user_id')
        user_name_field    = translations.get('user_name',     'user_name')
        email_field        = translations.get('email_address', 'email_address')
        password_field     = translations.get('password',      'password')
        display_name_field = translations.get('display_name',  'display_name')
    
        class Table(TableBase):
            __entity__ = self.model
            __omit_fields__ = [user_id_field, '_password', password_field]
            __url__ = '../users.json'
        self.table_type = Table
        
        class MyTableFiller(TableFiller):
            __entity__ = self.model
            __omit_fields__ = ['_password', password_field]
        self.table_filler_type = MyTableFiller

        class EditForm(EditableForm):
            __entity__ = self.model
            __require_fields__     = [user_name_field, email_field]
            __omit_fields__        = [password_field, 'created', '_password']
            __hidden_fields__      = [user_id_field]
            __field_order__        = [user_name_field, email_field, display_name_field, 'groups']
        if email_field is not None:
            setattr(EditForm, email_field, TextField)
        if display_name_field is not None:
            setattr(EditForm, display_name_field, TextField)
        self.edit_form_type = EditForm
    
        class NewForm(AddRecordForm):
            __entity__ = self.model
            __require_fields__     = [user_name_field, email_field]
            __omit_fields__        = [password_field, 'created', '_password']
            __hidden_fields__      = [user_id_field]
            __field_order__        = [user_name_field, email_field, display_name_field, 'groups']
        if email_field is not None:
            setattr(NewForm, email_field, TextField)
        if display_name_field is not None:
            setattr(NewForm, display_name_field, TextField)
        self.new_form_type = NewForm
    
class GroupControllerConfig(CrudRestControllerConfig):
    def _do_init_with_translations(self, translations):
        group_id_field       = translations.get('group_id', 'group_id')
        group_name_field     = translations.get('group_name', 'group_name')
        
        class GroupTable(TableBase):
            __model__ = self.model
            __limit_fields__ = [group_name_field, 'permissions']
            __url__ = '../groups.json'
        self.table_type = GroupTable
    
        class GroupTableFiller(TableFiller):
            __model__ = self.model
            __limit_fields__ = [group_id_field, group_name_field, 'permissions']
        self.table_filler_type = GroupTableFiller
    
        class GroupNewForm(AddRecordForm):
            __model__ = self.model
            __limit_fields__ = [group_name_field, 'permissions']
        self.new_form_type = GroupNewForm
    
        class GroupEditForm(EditableForm):
            __model__ = self.model
            __limit_fields__ = [group_id_field, 'group_name', 'permissions']
        self.edit_form_type = GroupEditForm
    
class PermissionControllerConfig(CrudRestControllerConfig):
    def _do_init_with_translations(self, translations):
        permission_id_field              = translations.get('permission_id', 'permission_id')
        permission_name_field            = translations.get('permission_name', 'permission_name')
        permission_description_field     = translations.get('permission_description', 'description')

        class PermissionTable(TableBase):
            __model__ = self.model
            __limit_fields__ = [permission_name_field, permission_description_field, 'groups']
            __url__ = '../permissions.json'
        self.table_type = PermissionTable
    
        class PermissionTableFiller(TableFiller):
            __model__ = self.model
            __limit_fields__ = [permission_id_field, permission_name_field, permission_description_field, 'groups']
        self.table_filler_type = PermissionTableFiller
    
        class PermissionNewForm(AddRecordForm):
            __model__ = self.model
            __limit_fields__ = [permission_name_field, permission_description_field, 'groups']
        self.new_form_type = PermissionNewForm
    
        class PermissionEditForm(EditableForm):
            __model__ = self.model
            __limit_fields__ = [permission_name_field, permission_description_field,'groups']
        self.edit_form_type = PermissionEditForm
    
        class PermissionEditFiller(RecordFiller):
            __model__ = self.model
        self.edit_filler_type = PermissionEditFiller

class TGAdminConfig(AdminConfig):
    user       = UserControllerConfig
    group      = GroupControllerConfig
    permission = PermissionControllerConfig
    
