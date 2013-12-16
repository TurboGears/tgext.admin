from tgext.crud.utils import sprox_with_tw2

try:
    from tgext.crud.utils import SortableTableBase as TableBase
except:
    from sprox.tablebase import TableBase

from sprox.formbase import AddRecordForm, EditableForm


class _BootstrapWidgetArgs(dict):
    OPTIONS = {'css_class': 'form-control',
               'container_attrs': {'class': 'form-group'}}

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            return self.OPTIONS

    def __contains__(self, item):
        return True

if sprox_with_tw2():
    from tw2.core import ChildParam
    from tw2.forms.widgets import BaseLayout

    class BootstrapFormLayout(BaseLayout):
        resources = []
        template = 'tgext.admin.templates.bootstrap_form_layout'

        field_wrapper_attrs = ChildParam('Extra attributes to include in the element wrapping '
                                         'the widget itself.', default={})
        field_label_attrs = ChildParam('Extra attributes to include in the label of '
                                       'the widget itself.', default={})

    class AdminTableBase(TableBase):
        __base_widget_args__ = {'css_class': 'table table-striped'}

    class AdminAddRecordForm(AddRecordForm):
        DEFAULT_FIELD_OPTIONS = _BootstrapWidgetArgs.OPTIONS
        __base_widget_args__   = {'child': BootstrapFormLayout}
        __field_widget_args__  = _BootstrapWidgetArgs()

    class AdminEditableForm(EditableForm):
        DEFAULT_FIELD_OPTIONS = _BootstrapWidgetArgs.OPTIONS
        __base_widget_args__   = {'child': BootstrapFormLayout}
        __field_widget_args__  = _BootstrapWidgetArgs()
else:
    class AdminTableBase(TableBase):
        pass

    class AdminAddRecordForm(AddRecordForm):
        DEFAULT_FIELD_OPTIONS = {}

    class AdminEditableForm(EditableForm):
        DEFAULT_FIELD_OPTIONS = {}