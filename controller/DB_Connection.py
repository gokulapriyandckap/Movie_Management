from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.movies_management_system
users = db.users
movies = db.movies
votes = db.votes
