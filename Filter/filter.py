from main import *
from General_Functions.General_functions import *
from bson import json_util,ObjectId

class filter:
    def __init__(self,user_id):
        self.user_id = user_id

    def check_filter(self, args):
        args["user_id"] = self.user_id
        data = movies.find(args)
        return json_util.dumps(data)
