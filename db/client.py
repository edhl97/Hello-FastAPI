# This file manages the connection with our MongoDB database

from pymongo import MongoClient

# Connection to local database
# db_client = MongoClient().local

# Conexión to remote database
db_client = MongoClient("mongodb+srv://test:test@cluster0.jkexg0j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test

