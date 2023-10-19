from main import *
from General_Functions.General_functions import *
from bson import json_util,ObjectId

class filter:

    def __init__(self,args,collection_name):
        self.args = args
        self.query = {}
        self.collection_name = collection_name

    def filter_query_builder(self):
        for key, value in self.args.items():
            if key[0:6:] == "filter":
                self.query.update({key[7::1]: value})
        criteria = self.collection_name.find(self.query)
        # documents_count = self.collection_name.find(self.query).count()

        # filtered_data = [criteria, documents_count]
        return criteria

    def search_query_builder(self):
        query = {"$or":[{"movie_name": {"$regex": search_info, "$options": "i"}},{"Director": {"$regex": search_info, "$options": "i"}}]}

        results = movies.find(query,{"_id":0})
        return list(results)
