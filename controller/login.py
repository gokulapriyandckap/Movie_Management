import json
from main import *
from General_Functions.General_functions import *

class login():
     def __init__(self,email,password):
         self.email = email
         self.password = hashlib.sha256(password.encode("utf-8")).hexdigest()

     def login_verfication(self):
         user_exist = users.find_one({"email":self.email})
         if user_exist:
             if user_exist["password"] == self.password:
                 jwt_token = create_access_token(
                     identity={"user_id": str(user_exist["_id"]), "email": user_exist["email"],
                               "name": user_exist["name"]}
                 )
                 refresh_token = create_refresh_token(identity={"user_id": str(user_exist["_id"]), "email": user_exist["email"],
                               "name": user_exist["name"]})
                 return response_data(message="Loginned Succesfully!",data={"token":jwt_token,"refresh_token":refresh_token},success=True)
             else:
                 return response_data(message="Password not match",success=False)
         else:
             return response_data(message="Email not found", success=False)
