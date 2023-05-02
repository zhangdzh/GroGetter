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
    global client
    if client is None:
        print("No connection with client yet.")

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

    :param collection: collection to search
    :param filt: filter to use
    :param db: database to search
    :return: list of results
    """
    return client[db][collection].delete_one(filt)


def delete_many(collection, filt, db=GROC_DB):
    """
    Deletes multiple based on filter

    :param collection: collection to search
    :param filt: filter to use
    :param db: database to search
    :return: list of results
    """
    return client[db][collection].delete_many(filt)


def fetch_all(collection, db=GROC_DB):
    """
    Find with a filter and return all results

    :param collection: collection to search
    :param db: database to search
    :return: list of results
    """
    ret = []
    for doc in client[db][collection].find():
        ret.append(doc)
    return ret


def insert_one(collection, doc, db=GROC_DB):
    """
    Insert a single doc into collection.

    :param collection: collection to insert into
    :param doc: doc to insert
    :param db: database to insert into
    :return: result of insert
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


def fetch_one(collection, filt: dict, db=GROC_DB):
    """
    Find with a filter and return on the first doc found.

    :param collection: collection to search
    :param filt: filter to use
    :param db: database to search
    :return: list of results
    """
    for doc in client[db][collection].find(filt):
        del doc['_id']
        return doc


def fetch_all_filtered(collection, filt: dict, db=GROC_DB) -> list:
    """
    Find with a filter and return all results

    :param collection: collection to search
    :param filt: filter to use
    :param db: database to search
    :return: list of results
    """
    ret = []
    for doc in client[db][collection].find(filt):
        del doc['_id']
        ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=GROC_DB):
    """
    Find with a filter and return all results

    :param key: key to use as dict key
    :param collection: collection to search
    :param db: database to search
    :return: dict of results
    """
    ret = {}
    for doc in client[db][collection].find({}):
        del doc['_id']
        ret[doc[key]] = doc
    return ret


def fetch_keys_as_list(key, collection, db=GROC_DB):
    """
    Find with a filter and return all results

    :param key: key to use as dict key
    :param collection: collection to search
    :param db: database to search
    :return: dict of results
    """
    return list(client[db][collection].find({}))


def update_one(collection, filt: dict, new, db=GROC_DB):
    """
    Find with a filter and return on the first doc found.

    :param collection: collection to search
    :param filt: filter to use
    :param new: new values to set
    :param db: database to search
    :return: list of results
    """
    return client[db][collection].update_one(filt, {"$set": new})
