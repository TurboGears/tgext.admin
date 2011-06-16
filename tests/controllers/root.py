print 'loading root'

from tg import config
from tgext.admin.controller import AdminController
from tg.controllers import TGController
from tests.model import DBSession
import tests.model as model

class UnSecuredAdminController(AdminController):
    allow_only = None

class RootController(TGController):
    admin =UnSecuredAdminController(model, DBSession)
    
    