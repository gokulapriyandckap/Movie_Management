# import Db_connection
import datetime

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
        print(data)
        delete_single_movie = collection_name.delete_one(data)
        print(delete_single_movie.deleted_count)
        if delete_single_movie.deleted_count == 1:
            return response_data(message="movie deleted successfully!",success=True)
        else:
            return response_data(message="movie not found!", success=False)
    def delete_all_data(self,collectection_name,data):
        delete_multiple_movies = collectection_name.delete_many(data).deleted_count
        if delete_multiple_movies > 0:
            return response_data(message="all movies deleted successfully!",success=True)
        else:
            return response_data(message="your movie collection is already empty!",success=True)

    def update_movie(self,updated_data):
        updated_movieName = updated_data["updated_movie_name"] #get the updated movie name from updated data.
        seraialize_movie_name =  serialize_data(updated_movieName) #sent the updated movie to serialize.
        updated_data["name"] = seraialize_movie_name
        # check_access = movies.count_documents({"user_id":self.user_id,"_id":self.movie_id})
        check_access = movies.find_one({"user_id":self.user_id,"_id":self.movie_id})
        # return json_util.dumps(check_access)
        if check_access:
            if check_access["name"] == seraialize_movie_name:
                update_request = movies.update_one({"name":seraialize_movie_name},{"$set":updated_data})
            else:
                exists_movie_name = movies.count_documents({"name":seraialize_movie_name})
                if exists_movie_name > 0:
                    return response_data(message="Movie name already exists", success=False)
                else:
                    movies.update_one({"_id":self.movie_id},{"$set":updated_data})
            return response_data(message="Movie updated successfully", success=True)
        else:
            return response_data(message="Movie not found", success=False)

    # create new movie with validation.
    def create_movie(self,movie_data):
        get_serialize_data = serialize_data(movie_data["name"])
        checking_data = check_data(movies, {"name":get_serialize_data,"user_id":movie_data["user_id"]})
        if not checking_data:
            movie_data["name"] = get_serialize_data
            movie_data["created_at"] = datetime.utcnow()
            create(collection_name=movies, get_data=movie_data)
            get_last_id = list(movies.find({},{"_id":1}).sort("created_at",-1).limit(1))
            return response_data(data={"movie_id":str(get_last_id[0]["_id"])},message="Movie inserted successfully", success=True)

        else:
            return response_data(message="movie name already exists", success=False)

    def show_movie(self):
        data = movies.find_one({"_id":self.movie_id})
        upvote_count = votes.count_documents({"movie_id":str(self.movie_id), "vote":1})
        downvote_count = votes.count_documents({"movie_id":str(self.movie_id), "vote":0})
        data["upvote"] = upvote_count
        data["downvote"] = downvote_count
        if data:
            data = seiralize_db_data(data)
            return response_data(data=data, message="Movie fetched successfully", success=True)
        else:
            return response_data(message="Movie not found", success=False)
        # if len(data) > 0:
        #     return response_data(data=data,message="movie fetched successfully",success=True)
        # else:
        #     return response_data(message="Movie not found",success=False)
            # data = movies.find_one({}) # get movie details with given movie id.
            # if data:
            #     liked = [] # store who liked the movie in the list
            #     disliked = [] # store who dislike the movie in the list
            #
            #     # join users and likes collection and get users name
            #     pipeline = [
            #         {
            #             "$lookup": {
            #                 "from": "users",
            #                 "localField": "user_id",
            #                 "foreignField": "_id",
            #                 "as": "details"
            #             }
            #         },
            #         {
            #             "$project": {
            #                 "_id":0,
            #                 "votes":1,
            #                 "details.name":1,
            #                 "movie_id":1
            #             }
            #         },
            #         {
            #             "$match": {
            #                 "movie_id":self.movie_id
            #             }
            #         }
            #     ]
            #
            #     value = votes.aggregate(pipeline)
            #     # return json_util.dumps(value)
            #     # check who liked and disliked the movie and store in the list
            #     for users in value:
            #         if users['vote'] == 1:
            #             liked.append(users['details'][0]['name']) # if liked members store into the liked list
            #         elif users['vote'] == 0:
            #             disliked.append(users['details'][0]['name']) # if disliked members store into the disliked list
            #
            #     data = serialize_db_data(data)
            #     # finally store the values into the output variable like liked members, dis liked members, likedCount, dislikes count and movie details
            #     output = {
            #         "movies_details":data,
            #         "likes":liked,
            #         "dislikes":disliked,
            #         "likesCount":len(liked),
            #         "dislikesCount":len(disliked)
            #     }
            #     # data['_id'] = str(data['_id'])
            #     return read(output) # return all data in output variable
            #
            # else:
            #     return response_data(message="Movie not found", success=False)

    # show all movies function
    def show_all_movies(self, get_args,get_access):
        filter_obj = filter(get_args,movies,get_access) # passing the query params to filter class
        filter_query = filter_obj.filter_query_builder() # get validate query params from filter function
        if 'limit' in get_args and 'page' in get_args:
            pagination_object = Pagination(get_args)  # pass the limit and page arguements to paginate class
        else:
            get_args["limit"] = 10
            get_args["page"] = 1
            pagination_object = Pagination(get_args)  # pass the limit and page arguements to paginate class


        data = pagination_object.data(filter_query[0],filter_query[1]) # passing the validate query params to paginate function
        return data

    def delete_movie(self):
        return self.delete_data(movies,{"_id":self.movie_id,"user_id":self.user_id})

    def delete_all_movie(self,user_id):
        return self.delete_all_data(movies,{"user_id":user_id})

    def search_movies(self,search_info):
        # results = movies.find({"$text": {"$search": search_info}},{"_id":0})
        # return list(results)

        # query = {
        #     "$or": [
        #         {"movie_name": {"$regex": search_info, "$options": "i"}},
        #         {"Director": {"$regex": search_info, "$options": "i"}}
        #     ]
        # }
        #
        # results = movies.find(query,{"_id":0})
        # return list(results)

        return search_info


