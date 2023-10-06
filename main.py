from flask import Flask,flash
from flask import request
from controller import user #Imported  the user Module from controller Directory.
from controller import DB_Connection #Imported the DB_connection Module from controller Directory.
import hashlib # to hash the password
import re # regex


app = Flask(__name__)

# Set a secret key
app.secret_key = 'movie@123' # set the secret key for our application.

@app.route("/",methods = ["GET","POST"])
def register():
    return "hello"


# This route is used to Create the register.
@app.route("/register", methods=["POST"])
def create_user():
    email = request.json['email'] # Get the Json data from the this route.
    password = request.json['password']

    user_instance = user.User(email,password) # Instancing the class User in user module.

    return user_instance.save_to_db() # To return the save_to_db function to save the datas to the Database.



if __name__ == "__main__":
    # Code inside this block will only run if the script is the main program
    # and not if it's imported as a module into another script.
    app.run(debug=True)