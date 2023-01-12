from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient

def dbconnect():
    load_dotenv(find_dotenv())
    password = os.environ.get("MONGODB_PWD")

    connection_string = f"mongodb+srv://frknksp:{password}@cluster0.pvyetgo.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    return client






