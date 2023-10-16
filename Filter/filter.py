from main import *
from General_Functions.General_functions import *
from bson import json_util,ObjectId

class filter:

    def __init__(self,args):
        self.args = args

    def query_builder(self):
        self.args.pop("limit")
        self.args.pop("page")
        return self.args
