# import Db_connection
import General_Functions.General_functions
from controller import DB_Connection
from main import *
import json
from bson import ObjectId, json_util
from General_Functions.General_functions import *
from pagination.pagination import *
from Filter.filter import *


# movie management class it includes crud
class movie_management():

    def __init__(self, movie_id = None, user_id = None):
        self.movie_id = ObjectId(movie_id)
        self.user_id = user_id

    def delete_data(self,collection_name,data):
        delete_single_movie = collection_name.delete_one(data)
        if delete_single_movie.deleted_count == 1:
            return "Movie deleted successfully"
        else:
            return "Id doesn't match"
    def delete_all_data(self,collectection_name,data):
        delete_multiple_movies = collectection_name.delete_many(data).deleted_count
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

        if db_check: # if movie is not exist only  update the movie.
            update(collection_name=movies,criteria=ObjectId(self.movie_id),updated_data=updated_data) # calling the update function in general functin module with respective arguments.
            return response_data(message="Movie Updated Successfully",success=True)
        else:
            update(collection_name=movies, criteria=ObjectId(self.movie_id), updated_data=updated_data)
            return response_data(message="Movie Updated Successfully",success=True)

    # create new movie with validation.
    def create_movie(self,movie_data):
        get_serialize_data = serialize_data(movie_data["movie_name"])
        checking_data = check_data(movies, {"movie_name":get_serialize_data,"user_id":movie_data["user_id"]})
        if not checking_data:
            movie_data["movie_name"] = get_serialize_data
            create(collection_name=movies, get_data=movie_data)
            return response_data(message="Movie inserted successfully", success=True)

        else:
            return response_data(message="movie name already exists", success=False)

    def show_movie(self):
            data = movies.find_one({"_id":self.movie_id, "user_id":"6526224cf548ea175603a826"}) # get movie details with given movie id.
            return data_type_change(data)
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
                data['_id'] = str(data['_id'])
                return read(output) # return all data in output variable

            else:
                return response_data(message="Movie not found", success=False)

    # show all movies function
    def show_all_movies(self, get_args):
        criteria = {"limit":get_args["limit"],"page":get_args["page"]}
        # return criteria
        pagination_object = Pagination(get_args)
        return pagination_object.data()

        filter_obj = filter(self.user_id)
        return filter_obj.check_filter(get_args)

        data = list(movies.find({"user_id":self.user_id}))
        for item in data:
            if '_id' in item:
                item['_id'] = str(item['_id'])
        return read(data)

    def delete_movie(self,get_id,user_id):
        get_id = ObjectId(get_id) # getting the data and convert to object id.
        user_id = ObjectId(user_id)
        return self.delete_data(movies,{"_id":get_id,"user_id":user_id})

    def delete_all_movie(self,user_id):
        user_id = ObjectId(user_id)
        return self.delete_all_data(movies,{"user_id":user_id})

    def search_movies(self,search_info):
        # results = movies.find({"$text": {"$search": search_info}},{"_id":0})
        # return list(results)

        query = {
            "$or": [
                {"movie_name": {"$regex": search_info, "$options": "i"}},
                {"Director": {"$regex": search_info, "$options": "i"}}
            ]
        }

        results = movies.find(query,{"_id":0})
        return list(results)


