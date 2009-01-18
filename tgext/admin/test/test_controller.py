import os, sys
import tgext.admin
from tg.test_stack import TestConfig, app_from_config
from tgext.admin.test.model import User, Group, Town
from tg.util import Bunch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tgext.admin.test.model import metadata, DBSession

root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, root)
test_db_path = 'sqlite:///'+root+'/test.db'
paths=Bunch(
            root=root,
            controllers=os.path.join(root, 'controllers'),
            static_files=os.path.join(root, 'public'),
            templates=os.path.join(root, 'templates')
            )

base_config = TestConfig(folder = 'rendering',
                         values = {'use_sqlalchemy': True,
                                   'model':tgext.admin.test.model,
                                   'session':tgext.admin.test.model.DBSession,
                                   'pylons.helpers': Bunch(),
                                   'use_legacy_renderer': False,
                                   # this is specific to mako
                                   # to make sure inheritance works
                                   'use_dotted_templatenames': True,
                                   'paths':paths,
                                   'package':tgext.admin.test,
                                   'sqlalchemy.url':test_db_path
                                  }
                         )

def setup_records(session):


    #session.expunge_all()

    user = User()
    user.user_name = u'asdf'
    user.email_address = u"asdf@asdf.com"
    user.password = u"asdf"
    session.add(user)

    arvada = Town(name=u'Arvada')
    session.add(arvada)
    session.flush()
    user.town = arvada

    session.add(Town(name=u'Denver'))
    session.add(Town(name=u'Golden'))
    session.add(Town(name=u'Boulder'))

    #test_table.insert(values=dict(BLOB=FieldStorage('asdf', StringIO()).value)).execute()
    #user_reference_table.insert(values=dict(user_id=user.user_id)).execute()

#    print user.user_id
    for i in ['managers', 'users']:
        group = Group(group_name=unicode(i))
        session.add(group)

    user.groups.append(group)

    session.flush()
    return user

def setup():
    engine = create_engine(test_db_path)
    metadata.bind = engine
    metadata.drop_all()
    metadata.create_all()
    session = sessionmaker(bind=engine)()
    setup_records(session)
    session.commit()

def teardown():
    os.remove(test_db_path[10:])

class TestAdminController:
    def __init__(self, *args, **kargs):
        self.app = app_from_config(base_config)

    def test_index(self):
        resp = self.app.get('/admin/')
        assert 'Document' in resp, resp

    def test_list_documents(self):
        resp = self.app.get('/admin/document').follow()
        assert """<table dojoType="dojox.grid.DataGrid" id="" store="_store" columnReordering="true" rowsPerPage="20" delayScroll="true" class="">
    <thead>
            <tr>
                <th field="__actions__">actions</th>
                <th field="document_id" width="auto">document_id
                </th><th field="created" width="auto">created
                </th><th field="blob" width="auto">blob
                </th><th field="owner" width="auto">owner
                </th><th field="url" width="auto">url
                </th><th field="address" width="auto">address
                </th>
            </tr>
    </thead>
    <div dojoType="dojox.data.QueryReadStore" jsId="_store" id="_store" url=".json"></div>
</table>
""" in resp, resp

    def test_documents_new(self):
        resp = self.app.get('/admin/document/new')
        assert """<tr id="blob.container" class="even" title="">
            <td class="labelcol">
                <label id="blob.label" for="blob" class="fieldlabel">Blob</label>
            </td>
            <td class="fieldcol">
                <input type="file" name="blob" class="filefield" id="blob" value="" />
            </td>
        </tr>""" in resp, resp

    def test_get_users(self):
        resp = self.app.get('/admin/user/')
        assert """<table dojoType="dojox.grid.DataGrid" id="" store="_store" columnReordering="true" rowsPerPage="20" delayScroll="true" class="">
    <thead>
            <tr>
                <th field="__actions__">actions</th>
                <th field="user_name" width="auto">user_name
                </th><th field="email_address" width="auto">email_address
                </th><th field="display_name" width="auto">display_name
""" in resp, resp

    def test_get_users_json(self):
        resp = self.app.get('/admin/user.json')
        assert """{"numRows": 1, "items": [{"town": "Arvada", "user_id": "1", "created":""" in resp, resp

    def test_edit_user(self):
        resp = self.app.get('/admin/user/1/edit')
        assert """<td class="fieldcol">
                <input type="text" name="user_name" class="textfield required" id="user_name" value="asdf" />
            </td>
        </tr><tr id="email_address.container" class="odd" title="">
            <td class="labelcol">
                <label id="email_address.label" for="email_address" class="fieldlabel required">Email Address</label>
            </td>
            <td class="fieldcol">
                <input type="text" name="email_address" class="textfield required" id="email_address" value="asdf@asdf.com" />
            </td>""" in resp, resp

    def test_edit_user_success(self):
        resp = self.app.post('/admin/user/1/', params={'sprox_id':'put__User',
                                                         '_method':'PUT',
                                                                   'user_name':'someone',
                                                                   'display_name':'someone2',
                                                                   'email_address':'asdf2@asdf2.com',
                                                                   '_password':'pass',
                                                                   'password':'pass',
                                                                   'town':'1',
                                                                   'town_id':'1',
                                                                   'user_id':'1',
                                                                   'created':'2009-01-11 13:54:01'}).follow()
        #resp = self.app.get('/admin/user.json')
        #assert """"email_address": "asdf2@asdf2.com",""" in resp, resp
        
        resp = self.app.post('/admin/user/1/', params={'sprox_id':'put__User',
                                                         '_method':'PUT',
                                                                   'user_name':'someone',
                                                                   'display_name':'someone2',
                                                                   'email_address':'asdf@asdf.com',
                                                                   '_password':'pass',
                                                                   'password':'pass',
                                                                   'town':'1',
                                                                   'town_id':'1',
                                                                   'user_id':'1',
                                                                   'created':'2009-01-11 13:54:01'}).follow()
#        resp = self.app.get('/admin/user.json')
#        assert """"email_address": "asdf@asdf.com",""" in resp, resp

    def _test_add_and_remove_user(self):
        resp = self.app.post('/admin/user/', params={'sprox_id':'add__User',
                                                                   'user_name':'someone',
                                                                   'display_name':'someone2',
                                                                   'email_address':'asdf2@asdf2.com',
                                                                   '_password':'pass',
                                                                   'password':'pass',
                                                                   'town':'1',
                                                                   'town_id':'1',
                                                                   'user_id':'2',
                                                                   'created':'2009-01-11 13:54:01'}).follow()
        #assert '<td>asdf2@asdf2' in resp, resp
        resp = self.app.get('/admin/user/2/', params={'user_id':'2', '_method':'DELETE'}).follow()
        #assert 'asdf2@asdf2' not in resp, resp

    def test_add_user_existing_username(self):
        resp = self.app.post('/admin/user/create', params={'sprox_id':'add__User',
                                                                   'user_name':u'asdf',
                                                                   'display_name':'someone2',
                                                                   'email_address':'asdf2@asdf2.com',
                                                                   '_password':'pass',
                                                                   'password':'pass',
                                                                   'town':'1',
                                                                   'town_id':'1',
                                                                   'user_id':'2',
                                                                   'created':'2009-01-11 13:54:01'})
        assert 'That value already exists' in resp, resp
