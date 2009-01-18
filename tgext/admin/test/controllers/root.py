from tg.controllers import TGController
from tgext.admin import AdminController
from tgext.admin.test.model import DBSession
import tgext.admin.test.model as model


class UnSecuredAdminController(AdminController):
    allow_only = None


class RootController(TGController):
    admin =UnSecuredAdminController(model, DBSession)
    
    