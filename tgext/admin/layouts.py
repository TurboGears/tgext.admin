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
    crud_templates = {'get_all': ['genshi:tgext.admin.templates.bootstrap_crud.get_all',
                                  'jinja:tgext.admin.templates.bootstrap_crud.get_all',
                                  'mako:tgext.admin.templates.bootstrap_crud.get_all',
                                  'kajiki:tgext.admin.templates.bootstrap_crud.get_all'],
                      'edit': ['genshi:tgext.admin.templates.bootstrap_crud.edit',
                               'jinja:tgext.admin.templates.bootstrap_crud.edit',
                               'mako:tgext.admin.templates.bootstrap_crud.edit',
                               'kajiki:tgext.admin.templates.bootstrap_crud.edit'],
                      'new': ['genshi:tgext.admin.templates.bootstrap_crud.new',
                              'jinja:tgext.admin.templates.bootstrap_crud.new',
                              'mako:tgext.admin.templates.bootstrap_crud.new',
                              'kajiki:tgext.admin.templates.bootstrap_crud.new']}
    crud_resources = [crud_script,
                      CSSSource(location='headbottom',
                                src='''
.crud-sidebar .active {
    font-weight: bold;
    border-left: 3px solid #eee;
}

.subdocument {
    border-left: 12px solid #eee;
    padding: 0 0 0 10px;
    margin: 5px 0 0 0;
    list-style-type: none;
}

.subdocuments {
    position: relative;
}

.subdocuments .subdocuments-delete {
    position: absolute;
    font-family: 'Glyphicons Halflings';
    font-style: normal;
    font-weight: 400;
    font-size: 8px;
    line-height: 1;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    margin-top: 2px;
    visibility: hidden;
}

.subdocuments .subdocuments-delete:before {
    content: "\\e014";
    visibility: visible;
    color: red;
}

.subdocuments .subdocuments-delete:hover {
    text-decoration: none;
}

.subdocuments .subdocuments-add {
    position: absolute;
    right: 5px;
    top: -25px;
    visibility: hidden;
    font-family: 'Glyphicons Halflings';
    font-style: normal;
    font-weight: 400;
    font-size: 8px;
    line-height: 1;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.subdocuments .subdocuments-add:after {
    visibility: visible;
    color: green;
    content: "\\2b";
}

.subdocuments .subdocuments-add:hover {
    text-decoration: none;
}


@media (max-width: 991px) {
    .pull-sm-right {
        float: right;
    }
}

@media (min-width: 992px) {
    .pull-md-right {
        float: right;
    }
}
''')]

    TableBase = BootstrapAdminTableBase
    AddRecordForm = BootstrapAdminAddRecordForm
    EditableForm = BootstrapAdminEditableForm
    TableFiller = BootstrapAdminTableFiller


class GroupedBootstrapAdminLayout(BootstrapAdminLayout):
    template_index = 'tgext.admin.templates.bootstrap_grouped_index'
