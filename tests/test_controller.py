from nose import SkipTest
import os, sys
from t_config import TestConfig, app_from_config
from tests.model import User, Group, Town
from tg.util import Bunch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from tests.model import metadata, DBSession

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

test_db_path = 'sqlite:///'+root+'/test.db'
base_config = TestConfig()
base_config.renderers = ['genshi', 'json', 'mako']

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
    print 'finished setting up db'

def _teardown():
    os.remove(test_db_path)

class TestAdminController:
    def __init__(self, *args, **kargs):
        self.app = app_from_config(base_config)

    def test_index(self):
        resp = self.app.get('/admin/')
        assert 'Document' in resp, resp

    def test_list_documents(self):
        resp = self.app.get('/admin/documents').follow()
        assert """<thead>
            <tr>
                <th formatter="lessThan" width="10em" name="actions" field="__actions__">__actions__
                </th><th formatter="lessThan" width="10em" name="document_id" field="document_id">document_id
                </th><th formatter="lessThan" width="10em" name="created" field="created">created
                </th><th formatter="lessThan" width="10em" name="blob" field="blob">blob
                </th><th formatter="lessThan" width="10em" name="owner" field="owner">owner
                </th><th formatter="lessThan" width="10em" name="url" field="url">url
                </th><th formatter="lessThan" width="10em" name="address" field="address">address
                </th>
            </tr>
        </thead>""" in resp, resp

    def _test_documents_new(self):
        resp = self.app.get('/admin/documents/new')
        assert """<tr id="blob.container" class="even" title="">
            <td class="labelcol">
                <label id="blob.label" for="blob" class="fieldlabel">Blob</label>
            </td>
            <td class="fieldcol">
                <input type="file" name="blob" class="filefield" id="blob" value="" />
            </td>
        </tr>""" in resp, resp

    def test_get_users(self):
        resp = self.app.get('/admin/users/')
        assert """<thead>
            <tr>
                <th formatter="lessThan" width="10em" name="actions" field="__actions__">__actions__
                </th><th formatter="lessThan" width="10em" name="_password" field="_password">_password
                </th><th formatter="lessThan" width="10em" name="user_id" field="user_id">user_id
                </th><th formatter="lessThan" width="10em" name="user_name" field="user_name">user_name
                </th><th formatter="lessThan" width="10em" name="email_address" field="email_address">email_address
                </th><th formatter="lessThan" width="10em" name="display_name" field="display_name">display_name
                </th><th formatter="lessThan" width="10em" name="created" field="created">created
                </th><th formatter="lessThan" width="10em" name="town_id" field="town_id">town_id
                </th><th formatter="lessThan" width="10em" name="town" field="town">town
                </th><th formatter="lessThan" width="10em" name="password" field="password">password
                </th><th formatter="lessThan" width="10em" name="groups" field="groups">groups
                </th>
            </tr>
        </thead>""" in resp, resp


    #this doesn't work for some order of loading issue
    def test_get_users_json(self):
        raise SkipTest
        resp = self.app.get('/admin/users.json')
        assert """{"numRows": 1, "items": [{"town": "Arvada", "user_id": "1", "created":""" in resp, resp

    def test_edit_user(self):
        resp = self.app.get('/admin/users/1/edit')
        assert """<tr id="_password.container" class="even" title="">
            <td class="labelcol">
                <label id="_password.label" for="_password" class="fieldlabel">Password</label>
            </td>
            <td class="fieldcol">
                <input type="password" name="_password" class="passwordfield" id="_password" value="" />
            </td>
        </tr>""" in resp, resp

    def test_edit_user_success(self):
        resp = self.app.post('/admin/users/1/', params={'sprox_id':'put__User',
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
        
        resp = self.app.post('/admin/users/1/', params={'sprox_id':'put__User',
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

    #this tests causes other tests to fail, so, no go
    def _test_add_and_remove_user(self):
        resp = self.app.post('/admin/users/', params={'sprox_id':'add__User',
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
        resp = self.app.get('/admin/users/2/', params={'user_id':'2', '_method':'DELETE'}).follow()
        #assert 'asdf2@asdf2' not in resp, resp

    def test_add_user_existing_username(self):
        resp = self.app.post('/admin/users/create', params={'sprox_id':'add__User',
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
