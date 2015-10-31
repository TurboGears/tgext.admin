from nose import SkipTest
import os, sys
from .t_config import TestConfig, app_from_config
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
    user.user_name = 'asdf'
    user.email_address = "asdf@asdf.com"
    user.password = "asdf"
    session.add(user)

    arvada = Town(name='Arvada')
    session.add(arvada)
    session.flush()
    user.town = arvada

    session.add(Town(name='Denver'))
    session.add(Town(name='Golden'))
    session.add(Town(name='Boulder'))

    #test_table.insert(values=dict(BLOB=FieldStorage('asdf', StringIO()).value)).execute()
    #user_reference_table.insert(values=dict(user_id=user.user_id)).execute()

#    print user.user_id
    for i in ['managers', 'users']:
        group = Group(group_name=i)
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
    print('finished setting up db')

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
            <th class="col_0">
                actions
            </th><th class="col_1">
                <a href="http://localhost/admin/documents/?order_by=document_id">document_id</a>
            </th><th class="col_2">
                <a href="http://localhost/admin/documents/?order_by=created">created</a>
            </th><th class="col_3">
                <a href="http://localhost/admin/documents/?order_by=blob">blob</a>
            </th><th class="col_4">
                <a href="http://localhost/admin/documents/?order_by=owner">owner</a>
            </th><th class="col_5">
                <a href="http://localhost/admin/documents/?order_by=url">url</a>
            </th><th class="col_6">
                <a href="http://localhost/admin/documents/?order_by=address">address</a>
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
            <th class="col_0">
                actions
            </th><th class="col_1">
                <a href="http://localhost/admin/users/?order_by=_password">_password</a>
            </th><th class="col_2">
                <a href="http://localhost/admin/users/?order_by=user_id">user_id</a>
            </th><th class="col_3">
                <a href="http://localhost/admin/users/?order_by=user_name">user_name</a>
            </th><th class="col_4">
                <a href="http://localhost/admin/users/?order_by=email_address">email_address</a>
            </th><th class="col_5">
                <a href="http://localhost/admin/users/?order_by=display_name">display_name</a>
            </th><th class="col_6">
                <a href="http://localhost/admin/users/?order_by=created">created</a>
            </th><th class="col_7">
                <a href="http://localhost/admin/users/?order_by=town_id">town_id</a>
            </th><th class="col_8">
                town
            </th><th class="col_9">
                <a href="http://localhost/admin/users/?order_by=password">password</a>
            </th><th class="col_10">
                groups
            </th>
        </tr>
        </thead>""" in resp, resp


    def test_get_users_json(self):
        resp = self.app.get('/admin/users.json')
        json = resp.json
        values = json.get('value_list', {})
        assert values.get('total', 0) == 1
        assert values.get('page', 0) == 1

    def test_edit_user(self):
        resp = self.app.get('/admin/users/1/edit')

        # Check password field available in edit
        assert """<tr class="odd" id="sx_password:container">
        <th><label for="sx_password">Password</label></th>
        <td>""" in resp, resp

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
                                                                   'user_name':'asdf',
                                                                   'display_name':'someone2',
                                                                   'email_address':'asdf2@asdf2.com',
                                                                   '_password':'pass',
                                                                   'password':'pass',
                                                                   'town':'1',
                                                                   'town_id':'1',
                                                                   'user_id':'2',
                                                                   'created':'2009-01-11 13:54:01'})
        assert 'That value already exists' in resp, resp
