from main import *

class Vote():
    def vote_the_movie(self,movie_name,vote,user_id):
        if movie_name == '': # checking the movie is not empty
            return "Movie name doesn't empty"
        movie = votes.find_one({"movie_name": movie_name}) #checking if the movie is already exists.
        movie_collection = movies.find_one({"movie_name": movie_name}) # checking if the given movie is alreafy exists in movies collection.
        if movie:
            return "Movie already Exists"
        else:
            if movie_collection: # if given movie is in the movies collection then only we can vote or else error will occurs.
                vote_data = {"movie_name":movie_name,"vote":vote,"user_id":user_id}
                votes.insert_one(vote_data)
                return "Vote inserted Succssfully"
            else:
                return "Movie doesn't found"







vote_object = Vote()