from tgext.crud.utils import sprox_with_tw2

try:
    from tgext.crud.utils import SortableTableBase as TableBase
except:
    from sprox.tablebase import TableBase

from sprox.formbase import AddRecordForm, EditableForm

__all__ = ['AdminTableBase', 'AdminAddRecordForm', 'AdminEditableForm',
           'BoostrapAdminTableBase', 'BootstrapAdminAddRecordForm', 'BootstrapAdminEditableForm']


def _merge_dicts(d1, d2):
    # A both dicts should be string keys only, dict(d1, **d2)
    # should always work, but this is actually the safest way.
    d = d1.copy()
    d.update(d2)
    return d


class AdminTableBase(TableBase):
    pass


class AdminAddRecordForm(AddRecordForm):
    FIELD_OPTIONS = {}


class AdminEditableForm(EditableForm):
    FIELD_OPTIONS = {}


if sprox_with_tw2():
    from tw2.core import ChildParam
    from tw2.forms.widgets import BaseLayout

    class _BootstrapFormLayout(BaseLayout):
        resources = []
        template = 'tgext.admin.templates.bootstrap_form_layout'

        field_wrapper_attrs = ChildParam('Extra attributes to include in the element wrapping '
                                         'the widget itself.', default={})
        field_label_attrs = ChildParam('Extra attributes to include in the label of '
                                       'the widget itself.', default={})

    class _BootstrapAdminFormMixin(object):
        # Implemented as a MixIn instead of FormBase subclass
        # to avoid third party users confusion over MRO when subclassing.
        FIELD_OPTIONS = {'css_class': 'form-control',
                         'container_attrs': {'class': 'form-group'}}

        def _admin_init_attrs(self):
            if 'child' not in self.__base_widget_args__:
                self.__base_widget_args__['child'] = _BootstrapFormLayout

            for f in self.__fields__:
                self.__field_widget_args__[f] = _merge_dicts(self.FIELD_OPTIONS,
                                                             self.__field_widget_args__.get(f, {}))

    class BoostrapAdminTableBase(AdminTableBase):
        def _do_init_attrs(self):
            super(BoostrapAdminTableBase, self)._do_init_attrs()

            if 'css_class' not in self.__base_widget_args__:
                self.__base_widget_args__['css_class'] = 'table table-striped'

    class BootstrapAdminAddRecordForm(_BootstrapAdminFormMixin, AdminAddRecordForm):
        def _do_init_attrs(self):
            super(BootstrapAdminAddRecordForm, self)._do_init_attrs()
            self._admin_init_attrs()

    class BootstrapAdminEditableForm(_BootstrapAdminFormMixin, AdminEditableForm):
        def _do_init_attrs(self):
            super(BootstrapAdminEditableForm, self)._do_init_attrs()
            self._admin_init_attrs()
else:
    BoostrapAdminTableBase = AdminTableBase
    BootstrapAdminAddRecordForm = AdminAddRecordForm
    BootstrapAdminEditableForm = AdminEditableForm