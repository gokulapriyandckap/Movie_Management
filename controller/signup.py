from main import *
import re
import hashlib

# comment added to check discord
class User(DB_Connection.DB_Configuration): # Inherit the DB_configuration class.
     def __init__(self,email,password): # this constructor function get the paramters from the instanced object.
         super().__init__("Movie_management_system")  # Initialize the database configuration
         self.email = email
         self.password = password
         self.email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$' # This Variable is for email validation.


     def validate_input(self): # This method is validate the email and password.
         if len(self.email) < 5 or not re.match(self.email_pattern, self.email):
             raise ValueError("Email must be at least 5 characters and in a valid format")
         elif len(self.password) < 8:
             raise ValueError("Password must be at least 8 characters")
         elif not re.search(r'[A-Z]', self.password):
             raise ValueError("Password must contain at least one uppercase letter")
         elif not re.search(r'[a-z]', self.password):
             raise ValueError("Password must contain at least one lowercase letter")
         elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', self.password):
             raise ValueError("Password must contain at least one special character")
         elif not re.search(r'\d', self.password):
             raise ValueError("Password must contain at least one digit")

     def to_dict(self): # This method is return the given data to the document or dictionary.
         try:
             self.validate_input()
             hashed_password = hashlib.sha256(self.password.encode("utf-8")).hexdigest()
             return {"email": self.email, "password": hashed_password}
         except ValueError as e:
             raise ValueError(str(e))


     def save_to_db(self): # This method is used to store the data to the Database.
         user_exist = self.users.find_one({"email": self.email})
         if not user_exist:
             self.users.insert_one(self.to_dict())
             return "User Created Successfully!"
         else:
             return "Email Already Exists"




