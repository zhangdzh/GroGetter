import os

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

GROC_DB = "groceries"

PW = "swef22"

client = None


def connect_db():
    """
    Creates a uniform connection to the DB.
    """
    # made the mongo client only connect to cloud because we don't have
    # a local mongo server
    global client
    if client is None:
        print("No connection with client yet.")
        password = PW
        if not password:
            raise ValueError("Please set a password" +
                             "to use Mongo in the cloud")
        print("Connecting to Mongo Cloud")
        client = pm.MongoClient(f'mongodb+srv://swef22:{password}'
                                + '@cluster0.qfnmmli.mongodb.net/'
                                + '?retryWrites=true&w=majority')


def del_one(collection, filt, db=GROC_DB):
    """
    Find with a filter and return on the first doc found.
    """
    client[db][collection].delete_one(filt)


def fetch_all(collection, db=GROC_DB):
    ret = []
    for doc in client[db][collection].find():
        ret.append(doc)
    return ret


def insert_one(collection, doc, db=GROC_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


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


def fetch_keys_as_list(key, collection, db=GROC_DB):
    ret = []
    for doc in client[db][collection].find():
        del doc['_id']
        ret.append(doc[key])
    return ret
