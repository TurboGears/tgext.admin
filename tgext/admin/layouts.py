from .widgets import *

__all__ = ['BasicAdminLayout', 'BootstrapAdminLayout']


class BasicAdminLayout(object):
    TableBase = AdminTableBase
    AddRecordForm = AdminAddRecordForm
    EditableForm = AdminEditableForm


class BootstrapAdminLayout(object):
    TableBase = BoostrapAdminTableBase
    AddRecordForm = BootstrapAdminAddRecordForm
    EditableForm = BootstrapAdminEditableForm