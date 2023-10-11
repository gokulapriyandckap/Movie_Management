# import Db_connection
from controller import DB_Connection
from main import *
import json
from bson import ObjectId, json_util

# movie management class it includes crud
class movie_management():

    def serialize_data(self,data):
        if '_id' in data:
            data['_id'] = str(data['_id'])
            return data

    def save_db(self,collection_name,user_data):
        collection_name.insert_one(user_data)

    def delete_data(self,collection_name,data):
        # delete_criteriea =  collection_name.find_one(data) # getting all the id data from the collection_name

        # if delete_criteriea: # if Id match it will delete or it return the "Id doesn't match"
        print(collection_name.delete_one(data))
            # return "Movie deleted successfully"
        # else:
        #     return "Id doesn't match"
    def delete_all_data(self,collectection_name):
        count = collectection_name.count_documents({})
        if count > 0:
            collectection_name.delete_many({})  # this is for delete all data in the collection_name
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

    @staticmethod
    def serialize_objectid(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    # show all movies function
    def show_all_movies(self, get_user_id):

        data = movies.find({"user_id":ObjectId(get_user_id)})
        data_list = [item for item in data]
        return json.dumps(data_list, default=self.serialize_objectid)


    def delete_movie(self,get_id):
        get_id = ObjectId(get_id) # getting the data and convert to object id.
        return self.delete_data(movies,{"_id":get_id})

    def delete_all_movie(self):
        return self.delete_all_data(movies)

movie_object = movie_management()
