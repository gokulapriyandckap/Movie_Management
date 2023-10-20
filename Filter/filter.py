from main import *
from General_Functions.General_functions import *
from bson import json_util,ObjectId

class filter:

    def __init__(self,args,collection_name):
        self.args = args
        self.query = {}
        self.collection_name = collection_name

    def filter_query_builder(self):
        self.search_query_builder()
        for key, value in self.args.items():
            if key[0:6:] == "filter":
                self.query.update({key[7::1]: value})

        criteria = self.collection_name.find(self.query)
        count_documents = self.collection_name.count_documents(self.query)
        data_counts = [criteria, count_documents]
        return data_counts

    def search_query_builder(self):
        query = {
            "$or":[{"name": {"$regex": self.args["search"], "$options": "i"}},{"director_name": {"$regex": self.args["search"], "$options": "i"}}]
        }
        self.query.update(query)
