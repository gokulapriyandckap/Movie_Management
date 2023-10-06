# import Db_connection
from controller import DB_Connection
from main import *
import json
from bson import objectid

# movie management class it includes crud
class movie_management(DB_Connection.DB_Configuration):
    def __init__(self,db_name):
        super().__init__(db_name)

    # save data to db
    def save_db(self,collection_name,user_data):
        collection_name.insert_one(user_data)

    # check the movie name is already exist or not
    def existing_validate(self,collection_name, check_data):
        all_movie_name = [] # store movie name only in the list

        for movie_name in self.movies.find({},{"_id":0}):
            all_movie_name.append(movie_name["movie_name"])

        if check_data in all_movie_name: # check the value is exist or not
            return "false"
        else:
            return "true"

    # create new movie with validation
    def create_movie(self, get_data):
        filter_value = get_data["movie_name"].replace(" ","").lower() # change the movie name into removing space and converted intoo lower case

        validated_data = self.existing_validate(self.movies,filter_value) # store the output of the existing method

        if validated_data == "true": # if the existing method return true the data passing the save_dp method else return already exist
            self.save_db(self.movies, get_data)
            return "movie created successfully"
        else:
            return "already exits"

movie_object = movie_management("Movie_management_system")
