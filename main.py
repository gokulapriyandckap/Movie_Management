from flask import Flask,flash, request
from controller import  login
from controller import DB_Connection
from flask import request
from controller import signup #Imported  the signup Module from controller Directory.
from controller.movie_management import *
import hashlib # to hash the password
import re # regex
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
import datetime

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
    email = request.json['email'] # Get the Json data from the this route.
    password = request.json['password']

    user_instance = signup.User(email,password) # Instancing the class User in user module.

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


if __name__ == "__main__":
    # Code inside this block will only run if the script is the main program
    # and not if it's imported as a module into another script.
    app.run(debug=True)