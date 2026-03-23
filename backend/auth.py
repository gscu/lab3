# auth.py - Authentication and user management for the Network Incident Reporting System application
# Gheorghe Georgescu | 301377303 - SWS-212 Lab 3
from database import users_collection as users # Import the users collection from the db module for user management in the authentication system of the Network Incident Reporting System application.
from passlib.context import CryptContext # Utility functions for password hashing and verification using Argon2.
from fastapi.security import OAuth2PasswordBearer # OAuth2PasswordBearer is a FastAPI utility for handling OAuth2 authentication with password and bearer token.
from fastapi import Depends, HTTPException # FastAPI components for dependency injection and error handling
from jwt_utils import verify_token # Import the verify_token function from the jwt_utils module to validate JWT tokens in the authentication process.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # Define the OAuth2 password bearer scheme, specifying that the token will be obtained from the "/token" endpoint. 
# This is used to handle authentication in the application by expecting clients to provide a bearer token in the Authorization header of requests to protected routes.

pwd_context = CryptContext( # Initialize the password context for hashing and verifying passwords, specifying the hashing algorithm and deprecation policy.
    schemes=["argon2"], # Use Argon2 as the hashing algorithm for password hashing, which is a secure and modern choice for password storage.
    deprecated="auto" # Automatically mark any older hashing schemes as deprecated, ensuring that only the specified algorithm (Argon2) is used for new password hashes.
)

def hash_password(password: str) -> str: # Function to hash a password using the defined password context and return the resulting hash as a string.
    return pwd_context.hash(password) # hashing

def verify_password(password: str, password_hash: str) -> bool: # Function to verify a password against its hash using the password context, returning True if the password is correct and False otherwise.
    return pwd_context.verify(password, password_hash) # verification

def get_current_user(token: str = Depends(oauth2_scheme)): # Rerieve the current user based on the provided JWT token using the OAuth2 password bearer scheme for authentication.
    payload = verify_token(token) # Verify the provided JWT token using the verify_token function.
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token") # If the token is invalid or expired, raise a 401 Unauthorized error with a message indicating the issue.
    return payload

# CRUD functions for user management in the authentication system of the Network Incident Reporting System application.
def register_user(username: str, password: str, role: str) -> bool: # Function to register a new user with the provided username, password, and role.
    if users.find_one({"username": username}): # Checks if the username already exists in the users collection.
        return False

    users.insert_one( # Insert a new user document into the users collection in the MongoDB database with the provided username, hashed password, and role. 
        {
            "username": username,
            "password_hash": hash_password(password), # Password is hashed using the hash_password function to ensure secure storage of user credentials.
            "role": role
        }
    )
    return True # Return True to indicate that the user was successfully registered.

def authenticate_user(username: str, password: str) -> bool: # Function to authenticate a user by verifying their username and password against the stored user data in the users collection.
    user = users.find_one({"username": username}) # Query the users collection in the MongoDB database to find a user document that matches the provided username.
    if not user: # If no user with the provided username is found in the users collection, return False to indicate that authentication has failed.
        return False
    return verify_password(password, user["password_hash"]) # If a user is found, verify the provided password against the stored password hash using the verify_password function. Return True if the password is correct, and False otherwise.

def get_user_role(username: str) -> str | None: # Function to retrieve the role of a user based on their username. 
    user = users.find_one({"username": username}) # Query the users collection in the MongoDB database to find a user document that matches the provided username.
    if not user:
        return None
    return user.get("role") # If a user with the provided username is found, return the value of the "role" field from the user document. If the "role" field does not exist, return None.

def list_users_safe(): # Return only safe fields like username and role, excluding sensitive information such as password hashes.
    cursor = users.find({}, {"_id": 0, "username": 1, "role": 1}) # 0 means exclude the _id field, while 1 means include the username and role fields in the returned documents. This ensures that sensitive information like password hashes is not included in the output when listing users.
    return list(cursor) # Convert the cursor to a list and return it as the output of the function, providing a list of user documents with only the username and role fields.

def delete_user(username: str) -> bool: # Function to delete a user from the users collection based on the provided username. It returns True if the user was successfully deleted, and False if no user with the given username was found.
    result = users.delete_one({"username": username}) # Attempt to delete a single document from the users collection that matches the specified username. The delete_one method returns a result object that contains information about the deletion operation, including how many documents were deleted.
    return result.deleted_count > 0 # Check if the deleted_count attribute of the result object is greater than 0, which indicates that at least one document was deleted. If so, return True; otherwise, return False to indicate that no user with the given username was found and deleted.