import inspect
from tw.forms import TextField
from sqlalchemy.orm import class_mapper, sessionmaker
from tg.util import Bunch
try:
    import tw.dojo
    from sprox.dojo.tablebase import DojoTableBase as TableBase
    from sprox.dojo.fillerbase import DojoTableFiller as TableFiller
except ImportError:
    from sprox.tablebase import TableBase
    from sprox.fillerbase import TableFiller

from sprox.fillerbase import RecordFiller, AddFormFiller
from sprox.formbase import AddRecordForm, EditableForm


class RestControllerConfig(Bunch):
    allow_only        = None

    @property
    def table_type(self):
        class Table(TableBase):
            __entity__=self.model
        return Table
    @property
    def table_filler_type(self):
        class MyTableFiller(TableFiller):
            __entity__ = self.model
        return MyTableFiller

    @property
    def edit_filler_type(self):
        class EditFiller(RecordFiller):
            __entity__ = self.model
        return EditFiller

    @property
    def new_filler_type(self):
        class NewFiller(AddFormFiller):
            __entity__ = self.model
        return NewFiller
    
    @property
    def edit_form_type(self):
        class EditForm(EditableForm):
            __entity__ = self.model
        return EditForm

    @property
    def new_form_type(self):
        class NewForm(AddRecordForm):
            __entity__ = self.model
        return NewForm
    
    def __init__(self, model, session, translations=None):
        super(RestControllerConfig, self).__init__()

        self.model = model
        self.session = session
        
        if translations is not None:
            self._do_init_with_translations(translations)

        #assign the model to all the tables
        attrs = ['table_type', 'table_filler_type', 'edit_form_type', 'edit_filler_type', 'new_form_type', 'new_filler_type']

        for attr_type in attrs:
            attr = attr_type[:-5]
            if not hasattr(self, attr):
                form = getattr(self, attr_type)(session)
                form.__entity__ = model
                setattr(self, attr, form)
            
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
        self.table = Table(self.session)
        
        class MyTableFiller(TableFiller):
            __entity__ = self.model
            __omit_fields__ = ['_password', password_field]
        self.table_filler = MyTableFiller(self.session)

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
        self.edit_form = EditForm(self.session)
    
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
        self.new_form = NewForm(self.session)
    
class GroupControllerConfig(RestControllerConfig):
    def _do_init_with_translations(self, translations):
        group_id_field       = translations.get('group_id', 'group_id')
        group_name_field     = translations.get('group_name', 'group_name')
        
class PermissionControllerConfig(RestControllerConfig):
    def _do_init_with_translations(self, translations):
        permission_id_field              = translations.get('permission_id', 'permission_id')
        permission_name_field            = translations.get('permission_name', 'permission_name')
        permission_description_field     = translations.get('permission_description', 'description')

class AdminConfig(Bunch):
    
    User_config_type = UserControllerConfig
    Group_config_type = GroupControllerConfig
    Permission_config_type = PermissionControllerConfig
    Default_config_type = RestControllerConfig
    
    index_template =  'genshi:tgext.admin.templates.index'
    
    def __init__(self, models, sessions=None, translations=None, list_non_configured_models=True):

        if sessions is None:
            sessions = []
        if not isinstance(sessions, list):
            sessions = [sessions,]
        if translations is None:
            translations = Bunch()
        
        if inspect.ismodule(models):
            models = [getattr(models, model) for model in dir(models) if inspect.isclass(getattr(models, model))]

        #purge all non-model objects
        try_models = models
        models = []
        for model in try_models:
            try:
                mapper = class_mapper(model)
                models.append(model)
            except:
                pass
            
        for model in models:
            model_name = model.__name__
            mapper = class_mapper(model)
            engine = mapper.tables[0].bind

            session = None
            for session in sessions:
                if session.bind is engine:
                    model_session = session
            if session is None:
                model_session = sessionmaker(bind=engine)
                sessions.append(model_session)

            controller_type_name = model_name+'_config_type'
            if hasattr(self, controller_type_name):
                controller_config = getattr(self, controller_type_name)(model, model_session, translations)
            else:
                controller_config = self.Default_config_type(model, model_session, translations)
            setattr(self, model.__name__, controller_config)

        self.session = sessions
        self.translations = translations

def old_crap():

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