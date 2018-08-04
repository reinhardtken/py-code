from pymongo import MongoClient
from pymongo import errors


client = MongoClient()
db = client['stock-adjust']



def dropAll():
    for one in STOCK_LIST:
        collection = db['cwsj-' + one]
        collection.drop()