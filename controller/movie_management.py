# import Db_connection
from controller import DB_Connection
from main import *
import json
from bson import ObjectId, json_util

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

        # loop the movies and store into the all_movie_name list
        for movie_name in self.movies.find({},{"_id":0}):
            all_movie_name.append(movie_name["movie_name"].replace(" ","").lower())

        if check_data in all_movie_name: # check the value is exist or not if exit it return flase else true
            return "false"
        else:
            return "true"

    # show all data its a general function. it get two parameter one is collection name and another one is expect fields
    def show_all_data(self,get_collection,except_data):
        all_data = get_collection.find({},except_data) # It returns the data you give the collection name
        return all_data

    # create new movie with validation
    def create_movie(self, get_data):
        filter_value = get_data["movie_name"].replace(" ","").lower() # change the movie name into removing space and converted intoo lower case

        validated_data = self.existing_validate(self.movies,filter_value) # store the output of the existing method
        if validated_data == "true": # if the existing method return true the data passing the save_db method else return already exist
            self.save_db(self.movies, get_data)
            return "movie created successfully"
        else:
            return "already exits"

    def show_movie(self, get_movie_id):
        liked = [] # store who liked the movie in the list
        disliked = [] # store who dislike the movie in the list

        # join users and likes collection and get users name
        pipeline = [
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "details"
                }
            },
            {
                "$project":{
                    "_id":0,
                    "like":1,
                    "details.name":1,
                    "movie_id":1
                }
            },
            {
                "$match":{
                    "movie_id":ObjectId(get_movie_id)
                }
            }
        ]

        datas = list(self.vote.aggregate(pipeline)) # store the return value into the datas variable

        # check who liked and disliked the movie and store in the list
        for users in datas:
            if users['like'] == 1:
                liked.append(users['details'][0]['name']) # if liked members store into the liked list
            elif users['like'] == 0:
                disliked.append(users['details'][0]['name']) # if disliked members store into the disliked list


        data = self.movies.find_one({"_id":ObjectId(get_movie_id)},{"_id":0,"user_id":0}) # get movie details with given movie id

        # finally store the values into the output variable like liked members, dis liked members, likedCount, dislikes count and movie details
        output = {
            "movies_details":data,
            "likes":liked,
            "dislikes":disliked,
            "likesCount":len(liked),
            "dislikesCount":len(disliked)
        }
        return output # return all data in output variable

    # show all movies function
    def show_all_movies(self):
        data = self.show_all_data(self.movies,{"_id":0,"user_id":0}) # call the show_all_data funciton and pass the arguement called collection name
        return json_util.dumps(data) # it return the movie collection data

movie_object = movie_management("Movie_management_system")

