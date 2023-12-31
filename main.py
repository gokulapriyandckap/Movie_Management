from flask import Flask,flash, request,jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import timedelta,datetime
from controller import  login
from controller.DB_Connection import *
from flask import request
from controller import signup #Imported  the signup Module from controller Directory.
from controller.movie_management import *
from controller.votes import *
from pagination.pagination import *
import hashlib # to hash the password
import re # regex
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, unset_jwt_cookies
from bson import ObjectId
import requests


# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
 # Allow CORS for all domains on all routes
CORS(app)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Parse the JWT_ACCESS_TOKEN_EXPIRES from the environment variable
jwt_expires_seconds = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 86400))
jwt_expires_timedelta = timedelta(seconds=jwt_expires_seconds)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = jwt_expires_timedelta


@app.route("/",methods = ["GET","POST"])
def register():
    data = movies.find({})
    return seiralize_db_data(data)
  



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
    

@app.route("/createmovie",methods=["POST"])
@jwt_required()
def create_movie():
    movie_obj = movie_management()
    movie_data = {}
    name = request.form.get('name')
    release_year = request.form.get('release_year')
    duration = request.form.get('duration')
    director_name = request.form.get('director_name')
    star_rating = int(request.form.get('star_rating'))
    description = request.form.get('description')
    genre = request.form.get('genre')
    image_file = request.files.get('image_path')
    is_favourite = int(request.form.get('is_favourite'))
    if image_file:
        image_path = f'static/uploads/{image_file.filename}'
        image_file.save(image_path)
        movie_data.update({"name":name,"release_year":release_year, "duration":duration, "director_name":director_name, "star_rating":star_rating,"description":description, "genre":genre, "image_path":image_path, "is_favourite":is_favourite,"user_id":get_jwt_identity()["user_id"]})
    else:
        movie_data.update({"name":name,"release_year":release_year, "duration":duration, "director_name":director_name, "star_rating":star_rating, "description":description,"genre":genre,"is_favourite":is_favourite,"user_id":get_jwt_identity()["user_id"]})

    return movie_obj.create_movie(movie_data) # call the create movie functon and passing the arguement is user_data

@app.route("/delete/<movie_id>",methods=["DELETE"])
@jwt_required()
def delete_movie(movie_id):
    user_id = get_jwt_identity()["user_id"]
    movie_object = movie_management(movie_id,user_id)
    return movie_object.delete_movie() # returing to the movie management.py

@app.route("/delete_all_data",methods = ["DELETE"])
@jwt_required()
def delete_all_movie():
    user_id = get_jwt_identity()["user_id"]
    return movie_management().delete_all_movie(user_id)

# show single movie route
@app.route("/showmovie/<movie_id>",methods=["GET"])
@jwt_required()
def show_movie(movie_id):
    movie_obj = movie_management(movie_id,get_jwt_identity()["user_id"])
    return movie_obj.show_movie() # passing the arguement movie id into the show movie function

# show all movies route
@app.route("/showmovie",methods=["GET"])
@jwt_required()
def show_all_movies():
    movie_obj = movie_management(user_id=get_jwt_identity()["user_id"])
    return movie_obj.show_all_movies(request.args.to_dict(),get_access=False)

@app.route("/showmovie/my_movie",methods=["GET"])
@jwt_required()
def show_my_movie():
    movie_obj = movie_management(user_id=get_jwt_identity()["user_id"])
    return movie_obj.show_all_movies(request.args.to_dict(),get_jwt_identity()["user_id"])

@app.route("/update_movie/<movie_id>", methods=["PUT"])
@jwt_required()
def update_movie(movie_id):
    # getting the updated data from the request Json
    user_id = get_jwt_identity()["user_id"]

    movie_object = movie_management(movie_id,user_id)
    return movie_object.update_movie(request.json) # sent the updated data to the update movie function in movie management class with movie user_id.


@app.route("/createvote/<movie_id>",methods=["POST"])
@jwt_required()
def like_movie(movie_id):
    vote = request.json["vote"] # get the vote from request.
    user_id = get_jwt_identity()["user_id"]
    vote_object = Vote(movie_id,user_id)
    return vote_object.vote_the_movie(vote)

@app.route('/update_vote/<movie_id>',methods=['PUT'])
@jwt_required()
def update_vote(movie_id):
    vote = request.json['vote']
    user_id = get_jwt_identity()["user_id"]

    vote_object = Vote(movie_id,user_id)
    return vote_object.update_vote(vote)
@app.route("/delete_like/<movie_id>",methods=["DELETE"])
@jwt_required()
def remove_like(movie_id):
     vote_obj = Vote(movie_id=movie_id, user_id=get_jwt_identity()["user_id"])
     return vote_obj.remove_like() # passing two arguements like movie_name and user_id

@app.route('/search_movies',methods=["GET"])
def search():
    # search = request.json['search_info']
    search = request.args['search_info']
    return movie_management().search_movies(search)



@app.route("/checkfilter",methods=["GET"])
@jwt_required()
def check_filter():
    args = request.args.to_dict()
    move_obj = movie_management(user_id=get_jwt_identity()["user_id"])
    return move_obj.check_filter(args)

@app.route("/logout",methods=["POST"])
@jwt_required()
def logout():
    current_user_id = get_jwt_identity()
    # Unset JWT cookies to invalidate the token on the client side
    resp = jsonify({'message': 'Logged out successfully'})
    unset_jwt_cookies(resp)
    return resp



if __name__ == "__main__":
    # Code inside this block will only run if the script is the main program
    # and not if it's imported as a module into another script.
    app.run(debug=True)

