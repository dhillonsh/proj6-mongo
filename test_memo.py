from pymongo import MongoClient
import sys
from extraFunctions import *
import arrow

try: 
    dbclient = MongoClient(MONGO_ADMIN_URL)
    db = getattr(dbclient, 'test_db')
    print("Got database")
    print("Attempting drop users")
    # db.command( {"dropAllUsersFromDatabase": 1 } )
    db.remove_user(secrets.client_secrets.db_user)
    print("Dropped database users for {}".format(secrets.client_secrets.db))
    db.command( {"dropDatabase": 1 } )
    print("Dropped database {}".format(secrets.client_secrets.db))
except Exception as err:
    print("Failed")
    print(err)
    
try: 
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, 'test_db')
    collection = db.dated

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)
    
def test_standard200():
    add_memo(collection, '2016-11-04', 'test')
    
    test_memos = get_memos(collection)
    for memo in test_memos: 
        print("Memo: " + str(memo))
