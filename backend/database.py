# database.py - Database connection and setup for the Network Incident Reporting System application.
# Gheorghe Georgescu | 301377303 - SWS-212 Lab 3
import os
from pathlib import Path
from dotenv import load_dotenv # Load environment variables from a .env file located in the parent directory of the current file
from pymongo import MongoClient # Import MongoDB client to connect to the database

BASE_DIR = Path(__file__).resolve().parent.parent # Define the base directory as the parent directory of the current file, which is used to locate the .env file for loading environment variables such as the MongoDB connection string.
load_dotenv(BASE_DIR / ".env") # Load environment variables from the .env file located in the base directory, allowing the application to access configuration values such as the MongoDB connection string (MONGO_URL) for connecting to the database. This is essential for securely managing sensitive information and ensuring that the application can connect to the database without hardcoding credentials in the source code.

MONGO_URL = os.getenv("MONGO_URL") # Retrieve the MongoDB connection string from the environment variable MONGO_URL, which is defined in the .env file. This connection string is used to establish a connection to the MongoDB database for storing and retrieving data related to network incidents and user management in the Network Incident Reporting System application.
client = MongoClient(MONGO_URL) # Create a MongoDB client using the connection string from the environment variable MONGO_URL, which allows the application to connect to the MongoDB database for storing and retrieving data related to network incidents and user management in the Network Incident Reporting System application.

db = client["gheorghegeorgescu_network_incidents_db"] # Access the specific database for the application
collection = db["incidents"] # Access the collection incidents created within the database for incidents
users_collection = db["users"] # Access the collection users created within the database for users