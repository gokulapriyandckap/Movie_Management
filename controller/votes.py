from main import *

class Vote():
    def vote_the_movie(self,movie_id,vote,user_id):
        movie = movies.find_one({"_id": ObjectId(movie_id)}) #checking if the movie is already exists.

        if movie:
            unique_movie = votes.find_one({"movie_id": movie_id,"user_id":user_id}) # checking if the movie is already exists in likes collection.

            if not unique_movie: # if given movie is in the movies collection then only we can vote or else error will occurs.
                vote_data = {"movie_id":movie_id,"vote":vote,"user_id":user_id}
                votes.insert_one(vote_data)
                return "Vote inserted Succssfully"
            else:
                return "Already Voted"
        else:
            return "Movie not Found"







vote_object = Vote()