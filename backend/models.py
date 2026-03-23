# models.py - Pydantic models for the Network Incident Reporting System application.
# Gheorghe Georgescu | 301377303 - SWS-212 Lab 3
from pydantic import BaseModel, Field
from typing import Literal, Optional

RoleType = Literal["engineer"] # Define a type for user roles, allowing only "engineer" as valid values for the role field in user-related operations within the network incident reporting system. This helps enforce role-based access control and ensures that only valid roles are assigned to users during registration and authentication processes.
SeverityType = Literal["low", "medium", "high", "critical"] # Define a type for incident severity levels, allowing only "low", "medium", "high", or "critical" as valid values for the severity field in incident-related operations within the network incident reporting system. This helps standardize the severity levels assigned to incidents and ensures that only valid severity values are used when creating or updating incident records in the MongoDB collection.
StatusType = Literal["open", "investigating", "resolved"] # Define a type for incident statuses, allowing only "open", "investigating", or "resolved" as valid values for the status field in incident-related operations within the network incident reporting system. This helps standardize the status values assigned to incidents and ensures that only valid status values are used when creating or updating incident records in the MongoDB collection.

class RegisterRequest(BaseModel): # Pydantic model for user registration requests, defining the expected fields and their validation rules for registering a new user in the network incident reporting system.
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=6, max_length=72)
    role: RoleType = "engineer" # Default role is set to "engineer" if not provided during registration, ensuring that new users are assigned a valid role in the system while allowing for flexibility in specifying the role if needed. This helps maintain consistency in user roles and simplifies the registration process for typical users who will be engineers by default.

class UserPublic(BaseModel): # Pydantic model for representing public user information, defining the fields that will be exposed when listing users in the network incident reporting system. This model includes only non-sensitive information such as the username and role, while excluding sensitive data like password hashes to ensure that user privacy is maintained when retrieving user lists or displaying user information in the application.
    username: str
    role: RoleType

class TokenResponse(BaseModel): # Pydantic model for representing the response returned after a successful login, defining the fields that will be included in the response when a user authenticates and receives a JWT token. This model includes the access_token field, which contains the generated JWT token for authenticated users, and the token_type field, which indicates the type of token (e.g., "bearer") to specify how the token should be used in subsequent requests for authentication when accessing protected routes in the network incident reporting system.
    access_token: str
    token_type: str

class IncidentBase(BaseModel): # Pydantic model for representing the base structure of an incident, defining the expected fields and their validation rules for creating and updating incident records in the network incident reporting system. This model includes fields such as device_name, location, incident_type, severity, description, and status, with appropriate validation rules to ensure that the data provided for incidents is consistent and adheres to the defined types and constraints when interacting with the MongoDB collection for incident management.
    device_name: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    incident_type: str = Field(..., min_length=1)
    severity: SeverityType
    description: str = Field(..., min_length=1)
    status: StatusType

class IncidentCreate(IncidentBase): # Pydantic model for creating a new incident, inheriting the fields and validation rules from the IncidentBase model. This model is used when submitting a request to create a new incident in the network incident reporting system.
    pass

class IncidentUpdate(BaseModel): # Pydantic model for updating an existing incident, defining the fields that can be updated and their validation rules. This model allows for partial updates by making all fields optional, enabling users to update only specific fields of an incident record in the MongoDB collection without requiring all fields to be provided in the update request.
    device_name: Optional[str] = Field(default=None, min_length=1)
    location: Optional[str] = Field(default=None, min_length=1)
    incident_type: Optional[str] = Field(default=None, min_length=1)
    severity: Optional[SeverityType] = None
    description: Optional[str] = Field(default=None, min_length=1)
    status: Optional[StatusType] = None

class IncidentResponse(IncidentBase): # Pydantic model for representing the response returned when retrieving incident information, inheriting the fields and validation rules from the IncidentBase model and adding additional fields such as id, created_at, and updated_at to provide a complete representation of an incident record when it is retrieved from the MongoDB collection in the network incident reporting system. This model is used when returning incident data in API responses for operations such as retrieving all incidents or retrieving a specific incident by ID.
    id: str
    created_at: str
    updated_at: str