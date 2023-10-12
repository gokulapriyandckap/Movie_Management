from main import *


class Vote():

    def __init__(self, movie_id = None, vote = None, user_id = None):
        self.movie_id = ObjectId(movie_id)
        self.vote = vote
        self.user_id = ObjectId(user_id)

    def vote_the_movie(self):
        movie = movies.find_one({"_id": self.movie_id}) #checking if the movie is already exists.

        if movie:  # if given movie is in the movies collection then only we can vote or else error will occurs.
            unique_movie = votes.find_one({"movie_id": self.movie_id }) # checking if the movie is already exists in likes collection.
            if not unique_movie:
                vote_data = {"movie_id":self.movie_id,"vote":self.vote,"user_id":self.user_id}
                votes.insert_one(vote_data)
                return "Vote inserted Succssfully"
            else:
                return "Already Voted"
        else:
            return "Movie not Found"

    def remove_like(self): # getting movie_name and user_id
        if self.movie_id:
            delete_vote = votes.delete_one({"movie_id": self.movie_id, "user_id":self.user_id})  # delete document which movie_name and user_id are matched
            if delete_vote.deleted_count == 1:
                return "Vote deleted successfully"
            else:
                return "user not found"
        else:
            return "Movie name not matched"