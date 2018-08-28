# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo





class MongoPipeline(object):
    # def __init__(self, mongo_uri, mongo_db):
    #     self.mongo_uri = mongo_uri
    #     self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        # return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DB'))
        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        # self.dbName = 'house'
        # self.collectionName = 'beijing'
        self.dbName = spider.dbName
        self.collectionName = spider.collectionName
        self.db = self.client[self.dbName]
        self.collection = self.db[self.collectionName]

    
    def process_item(self, item, spider):
        self.updateMongoDB(item)
        # self.db[item.collection].insert(dict(item))
        return item
    
    def close_spider(self, spider):
        self.client.close()

    def updateMongoDB(self, data):
        print('enter updateMongoDB')
        try:
            update_result = self.collection.update_one({'_id': data['_id']},
                                                  {'$set': data}, upsert=True)

            if update_result.matched_count > 0 and update_result.modified_count > 0:
                print('update to Mongo: %s : %s' % (self.dbName, self.collectionName))

            elif update_result.upserted_id is not None:
                print('insert to Mongo: %s : %s : %s' % (self.dbName, self.collectionName, update_result.upserted_id))

        except pymongo.errors.DuplicateKeyError as e:
            print('DuplicateKeyError to Mongo!!!: %s : %s : %s' % (self.dbName, self.collectionName, data['_id']))
        except Exception as e:
            print(e)
        print('leave updateMongoDB')