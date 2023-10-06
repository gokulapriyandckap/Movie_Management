# import Db_connection
from controller import DB_Connection
from main import *
import json
from bson import ObjectId

# movie management class it includes crud
class movie_management(DB_Connection.DB_Configuration):
    def __init__(self,db_name):
        super().__init__(db_name)

    # save data to db
    def save_db(self,collection_name,user_data):
        collection_name.insert_one(user_data)

    def delete_data(self,collection_name,data):
        delete_criteriea =  self.movies.find_one(data) # getting all the id data from the collection_name
        if delete_criteriea: # if Id match it will delete or it return the "Id doesn't match"
            collection_name.delete_one(data)
            return "Movie deleted successfully"
        else:
            return "Id doesn't match"
    def delete_all_data(self,collectection_name):
        collectection_name.delete_many({})  # this is for delete all data in the collection_name
        return "all deleted"



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

    def delete_movie(self,get_id):
        get_id = ObjectId(get_id) # getting the data and convert to object id.
        return self.delete_data(self.movies,{"_id":get_id})

    def delete_all_movie(self):
        return self.delete_all_data(self.movies)







movie_object = movie_management("Movie_management_system")
