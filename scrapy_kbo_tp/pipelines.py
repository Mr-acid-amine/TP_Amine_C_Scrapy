import pymongo
from scrapy.exceptions import DropItem

class MongoPipeline:
    def open_spider(self, spider):
        # Connexion à MongoDB Atlas
        mongo_uri = "mongodb+srv://mino:Minososo1234@cluster.fkflmzu.mongodb.net/"
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client["entreprises_db"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if 'numero' not in item:
            raise DropItem("Item sans numéro d'entreprise.")
        
        collection_name = spider.name  
        self.db[collection_name].update_one(
            {'numero': item['numero']},
            {'$set': dict(item)},
            upsert=True
        )
        return item

