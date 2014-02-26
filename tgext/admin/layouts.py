from .widgets import *
from tgext.crud.resources import crud_script, CSSSource

__all__ = ['BasicAdminLayout', 'BootstrapAdminLayout']


class BasicAdminLayout(object):
    template_index = 'tgext.admin.templates.index'
    crud_templates = {}

    TableBase = AdminTableBase
    AddRecordForm = AdminAddRecordForm
    EditableForm = AdminEditableForm
    TableFiller = AdminTableFiller


class BootstrapAdminLayout(object):
    template_index = 'tgext.admin.templates.bootstrap_index'
    crud_templates = {'get_all': ['genshi:tgext.admin.templates.bootstrap_crud.get_all'],
                      'edit': ['genshi:tgext.admin.templates.bootstrap_crud.edit',
                               'jinja:tgext.admin.templates.bootstrap_crud.edit',
                               'mako:tgext.admin.templates.bootstrap_crud.edit'],
                      'new': ['genshi:tgext.admin.templates.bootstrap_crud.new',
                              'jinja:tgext.admin.templates.bootstrap_crud.new',
                              'mako:tgext.admin.templates.bootstrap_crud.new']}
    crud_resources = [crud_script,
                      CSSSource(location='headbottom',
                                src='''
.crud-sidebar .active {
    font-weight: bold;
    border-left: 3px solid #eee;
}
''')]

    TableBase = BoostrapAdminTableBase
    AddRecordForm = BootstrapAdminAddRecordForm
    EditableForm = BootstrapAdminEditableForm
    TableFiller = BootstrapAdminTableFiller