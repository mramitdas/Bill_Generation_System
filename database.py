import os
import pymongo


class Database:
    def __init__(self, local=None):
        if local:
            from dotenv import load_dotenv
            load_dotenv('.env')

        client = pymongo.MongoClient(os.environ['Database_url'])
        db = client[os.environ['Db_name']]
        self.collection = db[os.environ['Table_name']]

    def insertion(self, data):
        self.collection.insert_one(data)

    def fetch(self, uid):
        return self.collection.find_one({"_id": uid})
