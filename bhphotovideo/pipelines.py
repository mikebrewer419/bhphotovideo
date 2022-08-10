# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from peewee import *
db = SqliteDatabase('bhphotovideo.db')

class Product(Model):
    category = CharField(null=True)
    name = CharField(null=True)
    price = CharField(null=True)
    image_url = CharField(null=True)
    bh_id = CharField(null=True)
    manufacture_number = CharField(null=True)
    reviews = CharField(null=True)
    key_features = CharField(null=True)
    
    class Meta:
        database = db
        table_name = "products"

class BhphotovideoPipeline:
    def open_spider(self, spider):
        global db
        db.connect()
        db.create_tables([Product])
        self.count = 0

    def process_item(self, item, spider):
        Product.create(**item)
        print(self.count)
        self.count += 1
        return item
        
    def close_spider(self, spider):
        db.close()
