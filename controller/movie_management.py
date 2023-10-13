# import Db_connection
import General_Functions.General_functions
from controller import DB_Connection
from main import *
import json
from bson import ObjectId, json_util
from General_Functions.General_functions import *


# movie management class it includes crud
class movie_management():

    def __init__(self, movie_id = None, user_id = None):
        self.movie_id = ObjectId(movie_id)
        self.user_id = ObjectId(user_id)

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

    def update_movie(self,updated_data):
        updated_movieName = updated_data["updated_movie_name"] #get the updated movie name from updated data.
        seraialize_movie_name =  serialize_data(updated_movieName) #sent the updated movie to serialize.

        db_check = check_data(movies,{"movie_name":seraialize_movie_name,"user_id":self.user_id}) #check if the movie is already exists in db.

        updated_Duration = updated_data["updated_Duration"] #get the updated Duration name from updated data.
        updated_DirectorName = updated_data["updated_DirectorName"] #get the Updated Director Name name from updated data.

        updated_data =  {"movie_name":seraialize_movie_name,"Duration":updated_Duration,"DirectorName":updated_DirectorName} # Storing the all updated data in dict with respect keyas and values.

        if not db_check: # if movie is not exist only  update the movie.
           return update(collection_name=movies,criteria=ObjectId(self.movie_id),updated_data=updated_data) # calling the update function in general functin module with respective arguments.
        else:
            return update(collection_name=movies, criteria=ObjectId(self.movie_id), updated_data=updated_data)

    # create new movie with validation.
    def create_movie(self):
        get_serialize_data = self.serialize_data(self.updated_data["movie_name"])
        checking_data = check_data(movies, {"movie_name":get_serialize_data,"user_id":self.updated_data["user_id"]})
        if not checking_data:
            self.updated_data["movie_name"] = get_serialize_data
            movies.insert_one(self.updated_data)
            return "movie inserted successfully"
        else:
            return "movie already exists"

    def show_movie(self):
            data = movies.find_one({"_id":self.movie_id,"user_id":self.user_id}) # get movie details with given movie id.
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
                            "movie_id":self.movie_id
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
                return json.dumps(output, default=serialize_objectid) # return all data in output variable
            else:
                return "Not found"

    # show all movies function
    def show_all_movies(self):
        data = movies.find({"user_id":self.user_id})
        data_list = [item for item in data]
        return json.dumps(data_list, default=serialize_objectid)

    def delete_movie(self,get_id):
        get_id = ObjectId(get_id) # getting the data and convert to object id.
        return self.delete_data(movies,{"_id":get_id})

    def delete_all_movie(self):
        return self.delete_all_data(movies)

