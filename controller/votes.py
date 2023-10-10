from main import *

class Vote(DB_Connection.DB_Configuration):
    def init(self):
        super().__init__("Movie_management_system")

    def vote_the_movie(self,movie_name,vote,user_id):
        if movie_name == '': # checking the movie is not empty
            return "Movie name doesn't empty"
        movie = self.vote.find_one({"movie_name": movie_name}) #checking if the movie is already exists.
        movie_collection = self.movies.find_one({"movie_name": movie_name}) # checking if the given movie is alreafy exists in movies collection.
        if movie:
            return "Movie already Exists"
        else:
            if movie_collection: # if given movie is in the movies collection then only we can vote or else error will occurs.
                vote_data = {"movie_name":movie_name,"vote":vote,"user_id":user_id}
                self.vote.insert_one(vote_data)
                return "Vote inserted Succssfully"
            else:
                return "Movie doesn't found"

    def remove_like(self,movie_name, user_id): # getting movie_name and user_id
        if movie_name:
            self.vote.delete_one({"movie_name":movie_name, "user_id":user_id}) # delete document which movie_name and user_id are matched
            return 'Removed your vote successfully'
        else:
            return "Movie name not matched"

vote_object = Vote("Movie_management_system")