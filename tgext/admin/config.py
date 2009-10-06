import inspect
from tw.forms import TextField
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.exc import UnmappedClassError
from tgext.crud import CrudRestController
dojo_loaded = False
try:
    import tw.dojo
    from sprox.dojo.tablebase import DojoTableBase
    from sprox.dojo.fillerbase import DojoTableFiller
    from sprox.dojo.formbase import DojoAddRecordForm, DojoEditableForm
    dojo_loaded = True
except ImportError:
    pass
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sprox.formbase import AddRecordForm, EditableForm

from sprox.fillerbase import RecordFiller, AddFormFiller

class CrudRestControllerConfig(object):
    allow_only        = None
    defaultCrudRestController = CrudRestController

    def _post_init(self):
        
        #RecordFillerClass = type('RecordFillerClass', (RecordFiller,),{})
        #AddFormFillerClass = type('AddFormFillerClass', (AddFormFiller,),{})
       
        #this insanity is caused by some weird python scoping.
        # see previous changesets for first attempts
        if self.default_to_dojo and dojo_loaded:
            TableBaseClass = type('TableBaseClass', (DojoTableBase,), {})
            TableFillerClass = type('TableBaseClass', (DojoTableFiller,), {})
            EditableFormClass = type('EditableFormClass', (DojoEditableForm,), {})
            AddRecordFormClass = type('AddRecordFormClass', (DojoAddRecordForm,),{})
        else: 
            TableBaseClass = type('TableBaseClass', (TableBase,), {})
            TableFillerClass = type('TableBaseClass', (TableFillerBase,), {})
            EditableFormClass = type('EditableFormClass', (EditableForm,), {})
            AddRecordFormClass = type('AddRecordFormClass', (AddRecordForm,),{})
        
        if not hasattr(self, 'table_type'):
            class Table(TableBaseClass):
                __entity__=self.model
            self.table_type = Table

        if not hasattr(self, 'table_filler_type'):
            class MyTableFiller(TableFillerClass):
                __entity__ = self.model
            self.table_filler_type = MyTableFiller
        
        if not hasattr(self, 'edit_form_type'):
            class EditForm(EditableFormClass):
                __entity__ = self.model
            self.edit_form_type = EditForm
        
        if not hasattr(self, 'edit_filler_type'):
            class EditFiller(RecordFiller):
                __entity__ = self.model
            self.edit_filler_type = EditFiller
    
        if not hasattr(self, 'new_form_type'):
            class NewForm(AddRecordFormClass):
                __entity__ = self.model
            self.new_form_type = NewForm
        
        if not hasattr(self, 'new_filler_type'):
            class NewFiller(AddFormFiller):
                __entity__ = self.model
            self.new_filler_type = NewFiller
    
    
    def __init__(self, model, translations=None, default_to_dojo=True):
        super(CrudRestControllerConfig, self).__init__()
        self.model = model
        self.default_to_dojo = default_to_dojo
        self._do_init_with_translations(translations)
        self._post_init()

    def _do_init_with_translations(self, translations):
        pass


class AdminConfig(object):
    
    DefaultControllerConfig    = CrudRestControllerConfig
    
    default_index_template =  None
    allow_only = None
    include_left_menu = True
    default_to_dojo = True

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
                models[model.__name__.lower()] = model
            except UnmappedClassError:
                pass
        self.models = models
        self.translations = translations
        self.index_template = self.default_index_template

    def lookup_controller_config(self, model_name):
        model_name_lower = model_name.lower()
        if hasattr(self, model_name_lower):
            return getattr(self, model_name_lower)(self.models[model_name], self.translations, self.default_to_dojo)
        return self.DefaultControllerConfig(self.models[model_name], self.translations, self.default_to_dojo)

