from flask import Flask,flash, request,jsonify
from controller import  login
from controller.DB_Connection import *
from flask import request
from controller import signup #Imported  the signup Module from controller Directory.
from controller.movie_management import *
from controller.votes import *
import hashlib # to hash the password
import re # regex
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
import datetime
from bson import ObjectId
import requests


app = Flask(__name__)

jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "onetwothree"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=1)

@app.route("/",methods = ["GET","POST"])
def register():
    return "hello"

# This route is used to Create the register.
@app.route("/register", methods=["POST"])
def create_user():
    name = request.json['name']
    email = request.json['email'] # Get the Json data from the this route.
    password = request.json['password']

    user_instance = signup.User(name,email,password) # Instancing the class User in user module.

    return user_instance.save_to_db() # To return the save_to_db function to save the datas to the Database.

@app.route("/login",methods=["POST"])
def user_login():
    email = request.json['email']
    password = request.json['password']

    user_data = login.login(email,password)

    return user_data.login_verfication()
    

@app.route("/createmovie",methods=["POST","GET"])
@jwt_required()
def create_movie():
    request.json["user_id"] = get_jwt_identity() # get user id from jwt token and add to the user data
    return movie_object.create_movie(request.json) # call the create movie functon and passing the arguement is user_data

@app.route("/delete",methods=["DELETE"])
def delete_movie():
    get_id = request.args.get('movie_id') # I got the id
    return movie_object.delete_movie(get_id) # returing to the movie management.py

@app.route("/delete_all_data",methods = ["DELETE"])
def delete_all_movie():
    return movie_object.delete_all_movie()

# show single movie route
@app.route("/showmovie",methods=["GET"])
def show_movie():
    get_id = request.args.get('movie_id') # get movie id in query param
    return movie_object.show_movie(get_id) # passing the arguement movie id into the show movie function

# show all movies route
@app.route("/show_all_movies",methods=["GET"])
def show_all_movies():
    return movie_object.show_all_movies()

# removing like
@app.route("/remove_like",methods=["PUT"])
def remove_like():
    movie_id = request.args.get('movie_id')
    return movie_object.remove_like(movie_id)


@app.route("/update_movie", methods=["PUT"])
def update_movie():
    # Get movie_id from the request
    movie_id = request.args.get('movie_id')

    # getting the updated data from the request Json
    updated_data = {
                    "updated_movie_name" :request.json['movie_name'],
                    "updated_Duration" : request.json['Duration'],
                    "updated_DirectorName" : request.json['DirectorName']}

    return movie_object.update_movie(movie_id,updated_data) # sent the updated data to the update movie function in movie management class with movie user_id.




@app.route("/createvote/<movie_id>",methods=["POST"])
@jwt_required()
def like_movie(movie_id):
    vote = request.json["vote"] # get the vote from request.
    user_id = get_jwt_identity()

    return vote_object.vote_the_movie(movie_id,vote,user_id) # sent the given data to the vote the movie function.


if __name__ == "__main__":
    # Code inside this block will only run if the script is the main program
    # and not if it's imported as a module into another script.
    app.run(debug=True)


