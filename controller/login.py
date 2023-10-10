import json

from main import *
class login():
     def __init__(self,email,password):
         self.email = email
         # self.password = password
         self.password = hashlib.sha256(password.encode("utf-8")).hexdigest()

     def login_verfication(self):
         user_exist = users.find_one({"email":self.email})
         if user_exist:
             if user_exist["password"] == self.password:
                 return create_access_token(identity=str(user_exist["_id"]))
             else:
                 return "password not match"
         else:
             return "Email not found"