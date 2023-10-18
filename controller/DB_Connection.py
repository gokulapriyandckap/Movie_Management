from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
USERS_COLLECTION = os.getenv("USERS_COLLECTION")
MOVIES_COLLECTION = os.getenv("MOVIES_COLLECTION")
VOTES_COLLECTION = os.getenv("VOTES_COLLECTION")

client = MongoClient(os.getenv("DATABASE_URL"))
db = client[DB_NAME]
users = db[USERS_COLLECTION]
movies = db[MOVIES_COLLECTION]
votes = db[VOTES_COLLECTION]
