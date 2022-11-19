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
