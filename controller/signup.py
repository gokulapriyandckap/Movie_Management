from main import *
from General_Functions.General_functions import *
import re
import hashlib


class User():
     def __init__(self,name,email,password): # this constructor function get the paramters from the instanced object. # Initialize the database configuration
         self.name = name
         self.email = email
         self.password = password
         self.email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$' # This Variable is for email validation.


     def validate_input(self): # This method is validate the email and password.
         if self.name == '':
             return response_data(message="Name Must not be Empty",success=False)
         if len(self.email) < 5 or not re.match(self.email_pattern, self.email):
             return response_data(message="Email must be at least 5 characters and in a valid format",success=False)
         elif len(self.password) < 8:
             return  response_data(message="Password must be at least 8 characters",success=False)
         elif not re.search(r'[A-Z]', self.password):
             return response_data(message="Password must contain at least one uppercase letter",success=False)
         elif not re.search(r'[a-z]', self.password):
             return response_data(message="Password must contain at least one uppercase letter",success=False)
         elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', self.password):
             return response_data(message="Password must contain at least one Special Character",success=False)
         elif not re.search(r'\d', self.password):
             return response_data(message="Password must contain at least one digit",success=False)

     def to_dict(self): # This method is return the given data to the document or dictionary.
         try:
             hashed_password = hashlib.sha256(self.password.encode("utf-8")).hexdigest()
             return {"name":self.name,"email": self.email, "password": hashed_password}
         except ValueError as e:
             raise ValueError(str(e))


     def save_to_db(self): # This method is used to store the data to the Database.
         if self.validate_input():
             return self.validate_input()
         user_exist = check_data(users,{"email": self.email})
         if not user_exist:
             create(collection_name=users,get_data=self.to_dict())
             return response_data(message="User Created Successfully!",success=True)
         else:
             return response_data(message="Email Already Exists!",success=False)




