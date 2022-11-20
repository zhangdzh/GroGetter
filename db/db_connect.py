import os

import pymongo as pm

REMOTE = "0"
LOCAL = "1"

GROC_DB = "grocdb"

client = None


def connect_db():
    """
    Creates a uniform connection to the DB.
    """
    global client
    if client is None:
        print("No connection with client yet.")
        if os.environ.get("LOCAL_MONGO", LOCAL) == LOCAL:
            print("Connecting to MongoDB locally.")
            client = pm.MongoClient()


def fetch_all(collection, db=GROC_DB):
    ret = []
    for doc in client[db][collection].find():
        ret.append(doc)
    return ret


def insert_one(collection, doc, db=GROC_DB):
    """
    Insert a single doc into collection.
    """
    client[db][collection].insert_one(doc)


def fetch_one(collection, filt, db=GROC_DB):
    """
    Find with a filter and return on the first doc found.
    """
    for doc in client[db][collection].find(filt):
        return doc


def fetch_all_as_dict(key, collection, db=GROC_DB):
    ret = {}
    for doc in client[db][collection].find():
        del doc['_id']
        ret[doc[key]] = doc
    return ret
