import inspect
from tg import expose, redirect
from tw.forms import TextField, PasswordField
from tgext.crud import CrudRestController
from tgext.crud.decorators import registered_validate
from config import AdminConfig, CrudRestControllerConfig
from sprox.fillerbase import EditFormFiller
from sprox.formbase import FilteringSchema
from formencode.validators import FieldsMatch

dojo_loaded = False

class PasswordFieldsMatch(FieldsMatch):
    field_names = ['password', 'verify_password']
    def validate_partial(self, field_dict, state):
        #no password is set to change
        if not field_dict.get('verify_password') and not field_dict.get('password'):
            return
        for name in self.field_names:
            if not field_dict.has_key(name):
                return
        self.validate_python(field_dict, state)

try:
    import tw.dojo
    from sprox.dojo.tablebase import DojoTableBase
    from sprox.dojo.fillerbase import DojoTableFiller
    from sprox.dojo.formbase import DojoAddRecordForm, DojoEditableForm
    dojo_loaded = True
except ImportError:
    pass

try:
    import tw.jquery
    from sprox.jquery.tablebase import JQueryTableBase
    from sprox.jquery.fillerbase import JQueryTableFiller
#    from sprox.jquery.formbase import DojoAddRecordForm, DojoEditableForm
    jquery_loaded = True
except ImportError:
    pass



from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sprox.formbase import AddRecordForm, EditableForm

from sprox.fillerbase import RecordFiller, AddFormFiller

class UserControllerConfig(CrudRestControllerConfig):
    def _do_init_with_translations(self, translations):
        global TableBase, TableFiller, EditableForm, AddRecordForm
        if self.default_to_dojo and dojo_loaded:
            TableBase = DojoTableBase
            TableFiller = DojoTableFiller
            EditableForm = DojoEditableForm
            AddRecordForm = DojoAddRecordForm

        user_id_field      = translations.get('user_id',       'user_id')
        user_name_field    = translations.get('user_name',     'user_name')
        email_field        = translations.get('email_address', 'email_address')
        password_field     = translations.get('password',      'password')
        display_name_field = translations.get('display_name',  'display_name')

        if not getattr(self, 'table_type', None):
            class Table(TableBase):
                __entity__ = self.model
                __omit_fields__ = [user_id_field, '_groups', '_password', password_field]
                __url__ = '../users.json'
            self.table_type = Table

        if not getattr(self, 'table_filler_type', None):
            class MyTableFiller(TableFiller):
                __entity__ = self.model
                __omit_fields__ = ['_password', password_field]
            self.table_filler_type = MyTableFiller

        edit_form_validator =  FilteringSchema(chained_validators=(FieldsMatch('password',
                                                         'verify_password',
                                                         messages={'invalidNoMatch':
                                                         'Passwords do not match'}),))

        if not getattr(self, 'edit_form_type', None):
            class EditForm(EditableForm):
                __entity__ = self.model
                __require_fields__     = [user_name_field, email_field]
                __omit_fields__        = ['created', '_password', '_groups']
                __hidden_fields__      = [user_id_field]
                __field_order__        = [user_id_field, user_name_field, email_field, display_name_field, 'password', 'verify_password', 'groups']
                password = PasswordField('password', value='')
                verify_password = PasswordField('verify_password')
                __base_validator__ = edit_form_validator

            if email_field is not None:
                setattr(EditForm, email_field, TextField)
            if display_name_field is not None:
                setattr(EditForm, display_name_field, TextField)
            self.edit_form_type = EditForm

        if not getattr(self, 'edit_filler_type', None):
            class UserEditFormFiller(EditFormFiller):
                __entity__ = self.model
                def get_value(self, *args, **kw):
                    v = super(UserEditFormFiller, self).get_value(*args, **kw)
                    del v['password']
                    return v

            self.edit_filler_type = UserEditFormFiller

        if not getattr(self, 'new_form_type', None):
            class NewForm(AddRecordForm):
                __entity__ = self.model
                __require_fields__     = [user_name_field, email_field]
                __omit_fields__        = [password_field, 'created', '_password', '_groups']
                __hidden_fields__      = [user_id_field]
                __field_order__        = [user_name_field, email_field, display_name_field, 'groups']
            if email_field is not None:
                setattr(NewForm, email_field, TextField)
            if display_name_field is not None:
                setattr(NewForm, display_name_field, TextField)
            self.new_form_type = NewForm

    class defaultCrudRestController(CrudRestController):

        @expose('tgext.crud.templates.edit')
        def edit(self, *args, **kw):
            return CrudRestController.edit(self, *args, **kw)

        @expose()
        @registered_validate(error_handler=edit)
        def put(self, *args, **kw):
            """update"""
            if not kw['password']:
                del kw['password']
            pks = self.provider.get_primary_fields(self.model)
            for i, pk in enumerate(pks):
                if pk not in kw and i < len(args):
                    kw[pk] = args[i]

            self.provider.update(self.model, params=kw)
            redirect('../')



class GroupControllerConfig(CrudRestControllerConfig):
    def _do_init_with_translations(self, translations):
        global TableBase, TableFiller, EditableForm, AddRecordForm
        if self.default_to_dojo and dojo_loaded:
            TableBase = DojoTableBase
            TableFiller = DojoTableFiller
            EditableForm = DojoEditableForm
            AddRecordForm = DojoAddRecordForm

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
            __field_order__ = [group_name_field, 'permissions']
        self.new_form_type = GroupNewForm

        class GroupEditForm(EditableForm):
            __model__ = self.model
            __limit_fields__ = [group_id_field, group_name_field, 'permissions']
            __field_order__ = [group_id_field, group_name_field, 'permissions']
        self.edit_form_type = GroupEditForm

class PermissionControllerConfig(CrudRestControllerConfig):
    def _do_init_with_translations(self, translations):
        global TableBase, TableFiller, EditableForm, AddRecordForm
        if self.default_to_dojo and dojo_loaded:
            TableBase = DojoTableBase
            TableFiller = DojoTableFiller
            EditableForm = DojoEditableForm
            AddRecordForm = DojoAddRecordForm

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
    default_to_dojo = False

    user       = UserControllerConfig
    group      = GroupControllerConfig
    permission = PermissionControllerConfig

