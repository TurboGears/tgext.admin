from tg import config
from tgext.admin.controller import AdminController
from tg.controllers import TGController
from tgext.admin.test.model import DBSession
import tgext.admin.test.model as model

class UnSecuredAdminController(AdminController):
    allow_only = None

class RootController(TGController):
    admin =UnSecuredAdminController(model, DBSession)
    
    