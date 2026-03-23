# jwt_utils.py - Utility functions for creating and verifying JWT tokens
# Gheorghe Georgescu | 301377303 - SWS-212 Lab 3
from datetime import datetime, timedelta, timezone # Import datetime, timedelta, and timezone for handling token expiration and time-related operations
from jose import jwt, JWTError # Import JWT handling functions from the python-jose library for encoding and decoding JWT tokens

SECRET_KEY = "gheorghegeorgescu_lab3_secret_key" # Secret key used for signing JWT tokens
ALGORITHM = "HS256" # Algorithm used for signing JWT tokens (HMAC with SHA-256)
ACCESS_TOKEN_EXPIRE_MINUTES = 10 # Token expiration time in minutes (10 minutes for this application)
# Function to create a JWT token 
def create_access_token(subject: str, role: str): 
    expire = datetime.now(timezone.utc) + timedelta( # Set the expiration time for the token by adding the defined number of minutes to the current UTC time
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = { # Define the payload of the JWT token, including the subject (username), role, and expiration time
        "sub": subject,
        "role": role,
        "exp": expire 
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) # Encode the payload into a JWT token using the secret key and specified algorithm, and return the generated token

def verify_token(token: str): # Function to verify a JWT token and return its payload if valid, or None if invalid or expired
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError: # If the token is invalid or expired, a JWTError will be raised, and the function will catch it and return None to indicate that the token verification failed.
        return None
