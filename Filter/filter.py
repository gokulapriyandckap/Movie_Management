from main import *
from General_Functions.General_functions import *
from bson import json_util,ObjectId

class filter:

    def __init__(self,args):
        self.args = args

    def query_builder(self):
        filter_dict = {}
        for key, value in self.args.items():
            if key[0:6:] == "filter":
                filter_dict.update({key[7::1]: value})
        return filter_dict
