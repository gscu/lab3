# main.py - Main application file - Network Incident Reporting System
# Gheorghe Georgescu | 301377303 - SWS-212 Lab 3
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm # Import OAuth2PasswordRequestForm for handling login requests with username and password.
from fastapi.middleware.cors import CORSMiddleware # Import CORS middleware to handle Cross-Origin Resource Sharing, allowing the frontend application to communicate with the backend API without issues related to cross-origin requests.
from pydantic import BaseModel, Field
from models import RegisterRequest, UserPublic, TokenResponse # Import Pydantic models for request and response validation, including RegisterRequest for user registration, UserPublic for representing public user information, and TokenResponse for representing the response returned after a successful login with a JWT token.
from typing import Literal, List
import incidents # Import API routes from the routes module
from jwt_utils import create_access_token # Import the create_access_token function from the jwt_utils module to generate JWT tokens for authenticated users.
# Import authentication functions and user management functions from the auth module.
from auth import (
    authenticate_user,
    get_current_user,
    get_user_role,
    register_user,
    list_users_safe
)

# Main application setup
app = FastAPI()

app.add_middleware( 
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes for authentication and user management in the network incident application, including registration, login, protected route access, and listing users.
@app.get("/") # Home route for testing if the API is running
def home():
    return {"message": "Network Incident Reporting System API is running!"} 

@app.get("/health") # Health check route to verify that the API is running and responsive. This can be used for monitoring and testing purposes to ensure that the application is operational.
def health():
    return {"status": "ok"} # Return a simple JSON response indicating that the API is healthy and running without issues.

@app.post("/register", status_code=201) # Route for user registration
def register(req: RegisterRequest):
    ok = register_user(req.username, req.password, "engineer") # Call the register_user function from the auth module to attempt to register a new user.
    if not ok:
        raise HTTPException(status_code=409, detail="Username already exists") # If the username already exists, raise a 409 Conflict error with an appropriate message.
    return {"message": "User registered", "username": req.username, "role": "engineer"} # Return a success message along with the registered username and role if registration is successful. 

@app.post("/token", response_model=TokenResponse) # Route for user login, which authenticates the user and returns a JWT token if the credentials are valid.
def login(form: OAuth2PasswordRequestForm = Depends()): # The login function takes an OAuth2PasswordRequestForm as input for handling authentication using Depends() to declare this form as a dependency.
    if not authenticate_user(form.username, form.password): # Verify the provided username and password using the authenticate_user function from the auth module.
        raise HTTPException(status_code=401, detail="Invalid credentials")

    role = get_user_role(form.username) # Retrieve the role of the authenticated user using the get_user_role function from the auth module, which is necessary for including the user's role in the generated JWT token.
    token = create_access_token(form.username, role) # Generate a JWT token for the authenticated user using the create_access_token function from the jwt_utils module, passing the username and role as parameters to include them in the token's payload.

    return {"access_token": token, "token_type": "bearer"} # Return the generated JWT token in the response, along with the token type (bearer) to indicate how the token should be used in subsequent requests for authentication.

@app.get("/users", response_model=List[UserPublic]) # List all team users (engineer role only)
def users_list(user=Depends(get_current_user)):
    if user["role"] != "engineer": # Only allow access to the list of team users if the current user's role is "engineer". This is a simple authorization check to restrict access to sensitive information about users in the network incident reporting system.
        raise HTTPException(status_code=403, detail="Access forbidden") # To be strict: require engineer role.
    return list_users_safe() # Call the list_users_safe function from the auth module to retrieve a list of users with only safe fields (username and role) and return it as the response.

app.include_router(incidents.router) # Include the API routes defined in the incidents module, which contains the endpoints for managing incidents in the network incident reporting system.
# This allows the application to handle requests related to incident creation, retrieval, and management as defined in the incidents.py file.
