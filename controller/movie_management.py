# import Db_connection
from controller import DB_Connection
from main import *
import json
from bson import ObjectId, json_util


# movie management class it includes crud
class movie_management():

    def __init__(self,movie_id,user_id,updated_data):
        self.movie_id = ObjectId(movie_id)
        self.updated_data = updated_data
        self.user_id = ObjectId(user_id)

    def save_db(self,collection_name,user_data):
        collection_name.insert_one(user_data)

    def delete_data(self,collection_name,data):
        delete_single_movie = collection_name.delete_one(data).deleted_count
        if delete_single_movie == 1:
            return "Movie deleted successfully"
        else:
            return "Id doesn't match"
    def delete_all_data(self,collectection_name):
        delete_multiple_movies = collectection_name.delete_many({}).deleted_count
        if delete_multiple_movies > 0:
            return "all Movies Deleted Successfully!"
        else:
            return "Movie Collection is Already Empty"

    # check the movie name is already exist or not
    def serialize_data(self, check_data):
        split_data = check_data.split()
        add_space = " ".join(split_data)
        validate_data = add_space.title()
        return validate_data

    def check_data(self, collection_name, get_check_data):
        return collection_name.find_one(get_check_data)

    def update_movie(self):
        updated_movieName = self.updated_data["updated_movie_name"]
        seraialize_movie_name =  self.serialize_data(updated_movieName)

        db_check = self.check_data(movies,{"movie_name":seraialize_movie_name,"user_id":self.user_id})
        updated_Duration = self.updated_data["updated_Duration"]
        updated_DirectorName = self.updated_data["updated_DirectorName"]

        if not db_check:
            movies.update_one({"_id": ObjectId(self.movie_id)},{"$set": {"movie_name": seraialize_movie_name,"Duration": updated_Duration,"DirectorName": updated_DirectorName}},upsert=False)
            return "Movie Updated Successfully"
        else:
            if db_check["movie_name"] == seraialize_movie_name and db_check["Duration"] == updated_Duration and db_check["DirectorName"] == updated_DirectorName:
                return "Please make it any changes"
            else:
                movies.update_one({"_id": ObjectId(self.movie_id)},{"$set": {"movie_name": seraialize_movie_name,"Duration": updated_Duration,"DirectorName": updated_DirectorName}},upsert=False)
                return "movie updated successfully"



    # create new movie with validation
    def create_movie(self, get_data):
        get_serialize_data = self.serialize_data(get_data["movie_name"])
        checking_data = self.check_data(movies, {"movie_name":get_serialize_data,"user_id":get_data["user_id"]})
        if not checking_data:
            get_data["movie_name"] = get_serialize_data
            movies.insert_one(get_data)
            return "movie inserted successfully"
        else:
            return "movie already exists"

    def show_movie(self, get_movie_id, user_id):
            data = movies.find_one({"_id":ObjectId(get_movie_id),"user_id":user_id},{"_id":0,"user_id":0}) # get movie details with given movie id

            if data:
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
                        "$project": {
                            "_id":0,
                            "votes":1,
                            "details.name":1,
                            "movie_id":1
                        }
                    },
                    {
                        "$match": {
                            "movie_id":ObjectId(get_movie_id)
                        }
                    }
                ]

                value = votes.aggregate(pipeline)

                # check who liked and disliked the movie and store in the list
                for users in value:
                    if users['votes'] == 1:
                        liked.append(users['details'][0]['name']) # if liked members store into the liked list
                    elif users['votes'] == 0:
                        disliked.append(users['details'][0]['name']) # if disliked members store into the disliked list

                # finally store the values into the output variable like liked members, dis liked members, likedCount, dislikes count and movie details
                output = {
                    "movies_details":data,
                    "likes":liked,
                    "dislikes":disliked,
                    "likesCount":len(liked),
                    "dislikesCount":len(disliked)
                }
                return output # return all data in output variable
            else:
                return "Not found"

    # show all movies function
    def show_all_movies(self, get_user_id):

        data = movies.find({"user_id":ObjectId(get_user_id)})
        data_list = [item for item in data]
        return json.dumps(data_list, default=serialize_objectid)


    def delete_movie(self,get_id):
        get_id = ObjectId(get_id) # getting the data and convert to object id.
        return self.delete_data(movies,{"_id":get_id})

    def delete_all_movie(self):
        return self.delete_all_data(movies)




def serialize_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")