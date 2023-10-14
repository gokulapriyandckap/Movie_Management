from main import *
class Vote():
    def __init__(self, movie_id = None, vote = None, user_id = None):
        self.movie_id = ObjectId(movie_id)
        self.user_id = ObjectId(user_id)

    def vote_the_movie(self,vote):
        # movie = movies.find_one({"_id": self.movie_id}) #checking if the movie is already exists.
        movie = check_data(movies,{"_id": self.movie_id})

        if movie:  # if given movie is in the movies collection then only we can vote or else error will occurs.
            unique_movie  = check_data(votes,{"movie_id": self.movie_id }) # checking if the movie is already exists in likes collection.
            if not unique_movie:
                vote_data = {"movie_id":self.movie_id,"vote":vote,"user_id":self.user_id}
                # votes.insert_one(vote_data)
                create(votes,vote_data)
                return response_data(message="Voted Successfully",success=True)
            else:
                return response_data(message="Already Voted", success=False)

        else:
            return response_data(message="Movie Not Found Voted", success=False)

    def update_vote(self,vote):
        filter_update_id = {"movie_id": self.movie_id, "user_id": self.user_id}
        update_data = { "$set": { "vote": vote } }

        updated_vote = votes.update_one(filter_update_id, update_data).modified_count

        if updated_vote == 1:
            return "Vote updated successfully"
        else:
            return "Vote not found or no changes made"
    def remove_like(self): # getting movie_name and user_id
        if self.movie_id:
            delete_vote = delete(votes, {"movie_id": self.movie_id, "user_id":self.user_id})  # delete document which movie_name and user_id are matched
            if delete_vote.deleted_count == 1:
                return response_data(message="Vote deleted successfully", success=True)
            else:
                return response_data(message="Vote not found", success=False)
        else:
            return response_data(message="Vote not found", success=True)