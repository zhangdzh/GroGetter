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
    # TODO: found out that the github actions doesn't pass when using
    # mongo from cloud. But to test, it would make sense for it to
    # use the cloud. I'm not sure what to do with that.
    global client
    if client is None:
        print("No connection with client yet.")
    #     password = PW
    #     if not password:
    #         raise ValueError("Please set a password" +
    #                          "to use Mongo in the cloud")
    #     print("Connecting to Mongo Cloud")
    #     client = pm.MongoClient(f'mongodb+srv://swef22:{password}'
    #                             + '@cluster0.qfnmmli.mongodb.net/'
    #                             + '?retryWrites=true&w=majority')
    if os.environ.get("LOCAL_MONGO", LOCAL) == CLOUD:
        password = PW
        if not password:
            raise ValueError("Please set a password" +
                             "to use Mongo in the cloud")
        print("Connecting to Mongo Cloud")
        client = pm.MongoClient(f'mongodb+srv://swef22:{password}'
                                + '@cluster0.qfnmmli.mongodb.net/'
                                + '?retryWrites=true&w=majority')
    else:
        print("Connecting to MongoDB locally.")
        client = pm.MongoClient()


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


def fetch_one(collection, filt: dict, db=GROC_DB):
    """
    Find with a filter and return on the first doc found.
    """
    for doc in client[db][collection].find(filt):
        return doc


def fetch_all_as_dict(key, collection, db=GROC_DB):
    ret = {}
    for doc in client[db][collection].find({}):
        del doc['_id']
        ret[doc[key]] = doc
    return ret


def fetch_keys_as_list(key, collection, db=GROC_DB):
    return list(client[db][collection].find({}))
