from pymongo import MongoClient

class DB_Configuration:
    def __init__(self, db_name):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db_name = db_name
        self.db = self.client[self.db_name]
        self.users = self.db.users
        self.movies = self.db.Movies
        self.vote = self.db.likes


    def check_connection(self):
        try:
            # Try fetching a document to test the connection
            document = self.client[self.db_name].users.find_one()
            if document is not None:
                print("DB Connected Successfully")
            else:
                print("DB Connection Failed")
        except Exception as e:
            print(f"DB Connection Failed: {e} ")

# DB = DB_Configuration("Movie_management_system")
# DB.check_connection()
