import pymongo
from pymongo import MongoClient
import sys
from extraFunctions import *
import arrow

test_db = 'test_db'

import secrets.client_secrets
import secrets.admin_secrets
MONGO_CLIENT_URL = "mongodb://{}:{}@localhost:{}/{}".format(
    secrets.client_secrets.db_user,
    secrets.client_secrets.db_user_pw,
    secrets.admin_secrets.port, 
    'test_db')
MONGO_ADMIN_URL = "mongodb://{}:{}@{}:{}/admin".format(
    secrets.admin_secrets.admin_user,
    secrets.admin_secrets.admin_pw,
    secrets.admin_secrets.host, 
    secrets.admin_secrets.port)

try:
    print('Deleting existing database {}'.format(test_db))
    dbclient = MongoClient(MONGO_ADMIN_URL)
    removeDB = getattr(dbclient, test_db)
    print("Attempting drop users")
    removeDB.remove_user(secrets.client_secrets.db_user)
    print("Dropped database users for {}".format(test_db))
    removeDB.command( {"dropDatabase": 1 } )
    print("Dropped database {}".format(test_db))
except Exception as err:
    print("Failed")
    print(err)

try:
    print('Creating the database {}'.format(test_db))
    dbclient = MongoClient(MONGO_ADMIN_URL)
    db = getattr(dbclient, test_db)
    collection = db.dated
    print("Got database {}".format(test_db))
    print("Attempting to create user")
    db.add_user(secrets.client_secrets.db_user,
                password=secrets.client_secrets.db_user_pw)
    print("Created user {}".format(secrets.client_secrets.db_user))
except Exception as err:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)

def test_addandremove1():
    assert len(get_memos(collection)) == 0
    
    add_memo(collection, arrow.utcnow().to('local'), 'memo msg here')
    memo_list = get_memos(collection)
    assert len(memo_list) == 1
    assert memo_list[0].get('date').lower() == 'today'
    assert memo_list[0].get('text') == 'memo msg here'
    delete_memo(collection, memo_list[0].get('_id'))
    assert len(get_memos(collection)) == 0
    
def test_yesterday():
    add_memo(collection, arrow.utcnow().to('local').replace(days=-1), 'new memo')
    memo_list = get_memos(collection)
    assert len(memo_list) == 1
    assert memo_list[0].get('date').lower() == 'yesterday'
    assert memo_list[0].get('text') == 'new memo'
    delete_memo(collection, memo_list[0].get('_id'))
    
def test_tomorrow():
    add_memo(collection, arrow.utcnow().to('local').replace(days=-1), 'new memo')
    memo_list = get_memos(collection)
    assert len(memo_list) == 1
    assert memo_list[0].get('date').lower() == 'yesterday'
    assert memo_list[0].get('text') == 'new memo'
    delete_memo(collection, memo_list[0].get('_id'))
    
def test_addmultiple():
    add_memo(collection, arrow.utcnow().to('local').replace(days=-1), 'new memo')
    memo0 = get_memos(collection)[0].get('_id')
    add_memo(collection, arrow.utcnow().to('local').replace(days=-1), 'new memo')

    assert len(memo_list) == 2
    delete_memo(collection, get_memos(collection)[1].get('_id'))
    assert len(memo_list) == 1
    assert memo0 == get_memos(collection)[0].get('_id')
