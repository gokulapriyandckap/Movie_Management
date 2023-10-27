from main import *
from General_Functions.General_functions import *
from bson import json_util,ObjectId

class filter:

    def __init__(self,args,collection_name,get_access,get_user_id):
        self.args = args
        self.query = {}
        self.collection_name = collection_name
        self.access = get_access
        self.user_id = get_user_id

    def filter_query_builder(self):
        for key, value in self.args.items():
            if key[0:6:] == "filter":
                self.query.update({key[7::1]: value})
            elif key == "search":
                self.search_query_builder()

        if self.access:
            self.query.update({"user_id":self.access})

        # criteria = self.collection_name.find(self.query)

        pipeline = [
            # {
            #     "$addFields": {
            #         "movie_id_objectId": {"$toObjectId": "$movie_id"}
            #     }
            # },
            {
                '$lookup': {
                    'from': 'votes',
                    'localField': '_id',
                    'foreignField': "movie_id",
                    'as': 'likes'
                }
            },
            {
                '$match':self.query
            },
            {
                '$addFields': {
                    'likecount': {
                        '$size': {
                            '$filter': {
                                'input': '$likes',
                                'as': 'like',
                                'cond':{
                                    "$and":[
                                        {'$eq': ['$$like.vote', 1]},
                                        {'$eq': ['$$like.user_id', self.user_id]}
                                    ]
                                }
                            }
                        }
                    },
                    'dislikeCount': {
                        '$size': {
                            '$filter': {
                                'input': '$likes',
                                'as': 'like',
                                'cond':{
                                    "$and":[
                                        {'$eq': ['$$like.vote', 0]},
                                        {'$eq': ['$$like.user_id', self.user_id]}
                                    ]
                                }
                            }
                        }
                    }
                }
            },
            {
                "$project":{
                    "likes.movie_id":0,
                    "likes._id":0
                }
            }
        ]


        count_documents = self.collection_name.count_documents(self.query)
        data_counts = [pipeline, count_documents]
        return data_counts

    def search_query_builder(self):
        query = {
            "$or":[{"name": {"$regex": self.args["search"], "$options": "i"}},{"director_name": {"$regex": self.args["search"], "$options": "i"}}]
        }
        self.query.update(query)
