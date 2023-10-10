import json

from main import *
class login(DB_Connection.DB_Configuration):
     def __init__(self,email,password):
         super().__init__("Movie_management_system")
         self.email = email
         # self.password = password
         self.password = hashlib.sha256(password.encode("utf-8")).hexdigest()

     def login_verfication(self):
         user_exist = self.users.find_one({"email":self.email})
         print(user_exist["_id"])
         if user_exist:
             if user_exist["password"] == self.password:
                 return create_access_token(identity=str(user_exist["_id"]))
             else:
                 return "password not match"
         else:
             return "Email not found"