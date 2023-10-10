from pymongo import MongoClient


client = MongoClient(host=['localhost:27017'])
db = client.Movie_management_system
users = db.users
movies = db.Movies
votes = db.votes
