import inspect
from tw.forms import TextField
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.exc import UnmappedClassError
try:
    import tw.dojo
    from sprox.dojo.tablebase import DojoTableBase as TableBase
    from sprox.dojo.fillerbase import DojoTableFiller as TableFiller
except ImportError:
    from sprox.tablebase import TableBase
    from sprox.fillerbase import TableFiller

from sprox.fillerbase import RecordFiller, AddFormFiller
from sprox.formbase import AddRecordForm, EditableForm


class RestControllerConfig(object):
    allow_only        = None

    def _post_init(self):
        if not hasattr(self, 'table_type'):
            class Table(TableBase):
                __entity__=self.model
            self.table_type = Table
        if not hasattr(self, 'table_filler_type'):
            class MyTableFiller(TableFiller):
                __entity__ = self.model
            self.table_filler_type = MyTableFiller
        
        if not hasattr(self, 'edit_form_type'):
            class EditForm(EditableForm):
                __entity__ = self.model
            self.edit_form_type = EditForm
        
        if not hasattr(self, 'edit_filler_type'):
            class EditFiller(RecordFiller):
                __entity__ = self.model
            self.edit_filler_type = EditFiller
    
        if not hasattr(self, 'new_form_type'):
            class NewForm(AddRecordForm):
                __entity__ = self.model
            self.new_form_type = NewForm
        
        if not hasattr(self, 'new_filler_type'):
            class NewFiller(AddFormFiller):
                __entity__ = self.model
            self.new_filler_type = NewFiller
    
    
    def __init__(self, model, translations=None):
        super(RestControllerConfig, self).__init__()
        self.model = model

        self._do_init_with_translations(translations)
            
        self._post_init()

    def _do_init_with_translations(self, translations):
        pass
    
class UserControllerConfig(RestControllerConfig):
    def _do_init_with_translations(self, translations):
        
        user_id_field      = translations.get('user_id',       'user_id')
        user_name_field    = translations.get('user_name',     'user_name')
        email_field        = translations.get('email_address', 'email_address')
        password_field     = translations.get('password',      'password')
        display_name_field = translations.get('display_name',  'display_name')
    
        class Table(TableBase):
            __entity__ = self.model
            __omit_fields__ = [user_id_field, '_password', password_field, 'lastName']
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
    
class GroupControllerConfig(RestControllerConfig):
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
    
class PermissionControllerConfig(RestControllerConfig):
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

class AdminConfig(object):
    
    User       = UserControllerConfig
    Group      = GroupControllerConfig
    Permission = PermissionControllerConfig
    
    DefaultControllerConfig    = RestControllerConfig
    
    default_index_template =  None
    
    def __init__(self, models, translations=None):

        if translations is None:
            translations = {}
        
        if inspect.ismodule(models):
            models = [getattr(models, model) for model in dir(models) if inspect.isclass(getattr(models, model))]

        #purge all non-model objects
        try_models = models
        models = {}
        for model in try_models:
            if not inspect.isclass(model):
                continue
            try:
                mapper = class_mapper(model)
                models[model.__name__] = model
            except UnmappedClassError:
                pass
        self.models = models
        self.translations = translations
        self.index_template = self.default_index_template

    def lookup_controller_config(self, model_name):
        if hasattr(self, model_name):
            return getattr(self, model_name)(self.models[model_name], self.translations)
        return self.DefaultControllerConfig(self.models[model_name], self.translations)
    
def old_crap():



    return config