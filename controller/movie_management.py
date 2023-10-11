# import Db_connection
from controller import DB_Connection
from main import *
import json
from bson import ObjectId, json_util

# movie management class it includes crud
class movie_management():

    def save_db(self,collection_name,user_data):
        collection_name.insert_one(user_data)

    def delete_data(self,collection_name,data):
        delete_criteriea =  collection_name.find_one(data) # getting all the id data from the collection_name

        if delete_criteriea: # if Id match it will delete or it return the "Id doesn't match"
            collection_name.delete_one(data)
            return "Movie deleted successfully"
        else:
            return "Id doesn't match"
    def delete_all_data(self,collectection_name):
        count = collectection_name.count_documents({})
        if count > 0:
            collectection_name.delete_many({})  # this is for delete all data in the collection_name
            return "all Movies Deleted Successfully!"
        else:
            return "Movie Collection is Already Empty"

    # check the movie name is already exist or not
    def existing_validate(self, check_data):
        split_data = check_data.split()
        add_space = " ".join(split_data)
        validate_data = add_space.title()
        db_data = movies.find_one({"movie_name":validate_data},{"_id":0})
        if db_data:
            return False
        else:
            return validate_data

    def update_movie(self, movie_id,updated_data):
        updated_movieName = updated_data["updated_movie_name"]
        movie_validation =  self.existing_validate(updated_movieName)

        # return movie_validation
        if movie_validation:
            movie_id = ObjectId(movie_id)
            updated_Duration = updated_data["updated_Duration"]
            updated_DirectorName = updated_data["updated_DirectorName"]

            # checking if the given movie id is existing or not. if existing update the data with given data.
            movies.update_one({"_id": movie_id},
                                  {
                                      "$set": {
                                          "movie_name": movie_validation,
                                          "Duration": updated_Duration,
                                          "DirectorName": updated_DirectorName
                                      }
                                  },
                                  upsert=True
                                  )
            return "Movie Updated Successfully"
        else:
            return "movie already exists"



    # show all data its a general function. it get two parameter one is collection name and another one is expect fields
    def show_all_data(self,get_collection,except_data):
        all_data = get_collection.find({},except_data) # It returns the data you give the collection name
        return all_data

    # create new movie with validation
    def create_movie(self, get_data):
        validation = self.existing_validate(get_data["movie_name"])
        if validation:
            get_data["movie_name"] = validation
            movies.insert_one(get_data)
            return "movie inserted successfully"
        else:
            return "movie already exists"

    def show_movie(self, get_movie_name):
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
                    "movie_name":1,
                }
            },
            {
                "$match":{
                    "movie_name":get_movie_name
                }
            }
        ]

        datas = list(votes.aggregate(pipeline)) # store the return value into the datas variable

        # check who liked and disliked the movie and store in the list
        for users in datas:
            if users['like'] == 1:
                liked.append(users['details'][0]['name']) # if liked members store into the liked list
            elif users['like'] == 0:
                disliked.append(users['details'][0]['name']) # if disliked members store into the disliked list


        data = movies.find_one({"_id":ObjectId(get_movie_id)},{"_id":0,"user_id":0}) # get movie details with given movie id

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
        data = self.show_all_data(movies,{"_id":0,"user_id":0}) # call the show_all_data funciton and pass the arguement called collection name
        return json_util.dumps(data) # it return the movie collection data



    def delete_movie(self,get_id):
        get_id = ObjectId(get_id) # getting the data and convert to object id.
        return self.delete_data(movies,{"_id":get_id})

    def delete_all_movie(self):
        return self.delete_all_data(movies)

movie_object = movie_management()

