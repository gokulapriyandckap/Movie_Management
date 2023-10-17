import json

from main import *

class login():
     def __init__(self,email,password):
         self.email = email
         self.password = hashlib.sha256(password.encode("utf-8")).hexdigest()

     def login_verfication(self):
         user_exist = users.find_one({"email":self.email})
         if user_exist:
             if user_exist["password"] == self.password:
                 jwt_token = create_access_token(identity=str(user_exist["_id"]))
                 return response_data(message="Loginned Succesfully!",data=jwt_token,success=True)
             else:
                 return response_data(messgae="Password not match",success=False)
         else:
             return response_data(messgae="Email not found", success=False)
