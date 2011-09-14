from config import AdminConfig
from controller import AdminController
import inspect
from tgadminconfig import UserControllerConfig, GroupControllerConfig, PermissionControllerConfig

class MongoAdminConfig(AdminConfig):
    def __init__(self,models,translations = None):
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
            models[model.__name__.lower()] = model
        self.models = models
        self.translations = translations

    def lookup_controller_config(self, model_name):
        model_name_lower = model_name.lower()
        if hasattr(self, model_name_lower):
            return getattr(self, model_name_lower)(self.models[model_name], self.translations, False)
        return self.DefaultControllerConfig(self.models[model_name], self.translations, False)

class MongoAdmin(AdminController):
    def __init__(self,models):
        super(MongoAdmin,self).__init__(models,None,config_type=MongoAdminConfig)
        self.models = models

class TGMongoAdminConfig(MongoAdminConfig):
    user       = UserControllerConfig
    group      = GroupControllerConfig
    permission = PermissionControllerConfig 

    def __init__(self, models, translations=None):
        if not translations:
            translations =  {'group_id':'_id',
                              'user_id':'_id',
                        'permission_id':'_id'}

        super(MongoAdminConfig, self).__init__(models, translations)
