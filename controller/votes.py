from main import *

class Vote(DB_Connection.DB_Configuration):
    def init(self):
        super().__init__("Movie_management_system")

    def vote_the_movie(self,movie_name,vote,user_id):
        if movie_name == '': # checking the movie is not empty
            return "Movie name doesn't empty"
        movie = self.vote.find_one({"movie_name": movie_name}) #checking if the movie is already exists.
        if movie:
            return "Movie already Exists"
        else:
            vote_data = {"movie_name":movie_name,"vote":vote,"user_id":user_id}
            self.vote.insert_one(vote_data)
            return "Vote inserted Succssfully"







vote_object = Vote("Movie_management_system")