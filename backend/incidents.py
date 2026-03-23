# incidents.py - API route definitions for the Network Incident Reporting application.
# Gheorghe Georgescu | 301377303 - SWS-212 Lab 3
from fastapi import APIRouter, Depends, HTTPException # FastAPI components for routing and error handling
from bson import ObjectId # Import ObjectId for handling MongoDB objects
from auth import get_current_user
from models import IncidentCreate, IncidentUpdate, IncidentResponse
from typing import List
from database import collection # Import the MongoDB collection from the db module
from datetime import datetime # Import datetime for timestamping records
# Define the API router for incidents
router = APIRouter()

def serialize_doc(doc) -> dict: # Helper function to convert MongoDB document to a serializable format
    #doc["_id"] = str(doc["_id"]) # Convert ObjectId to string for JSON serialization
    return {
        "id": str(doc["_id"]),
        "device_name": doc["device_name"],
        "location": doc["location"],
        "incident_type": doc["incident_type"],
        "severity": doc["severity"],
        "description": doc["description"],
        "status": doc["status"],
        "created_at": str(doc["created_at"]),
        "updated_at": str(doc["updated_at"]),
    } # Return the serialized document

def incident_check(id:str): # Helper function to check if an incident with the given ID exists in the MongoDB collection. It validates the ID format and checks for the existence of the document, returning the document if found or raising appropriate HTTP exceptions if not.
    if not ObjectId.is_valid(id): # Validate that the provided ID is in a valid format for MongoDB ObjectId. If not, raise a 400 Bad Request error with a message indicating the issue.
        raise HTTPException(status_code=400, detail="Invalid ID format")
    doc = collection.find_one({"_id": ObjectId(id)}) # Query the MongoDB collection for a document with the matching _id field.
    if not doc: # If no document is found with the specified ID, raise a 404 Not Found error with a message indicating that the incident was not found.
        raise HTTPException(status_code=404, detail="Incident not found")
    return doc # If a document is found, return it for further processing in the API routes that require incident validation by ID.

# CRUD Endpoints in the router for managing requests in the Network Incident Reporting application
@router.get("/incidents", response_model=list[IncidentResponse]) # Get all incidents
def get_all_incidents():
    docs = list(collection.find()) # Retrieve all documents from the MongoDB "incidents" collection and convert the cursor to a list
    return [serialize_doc(doc) for doc in docs] # Serialize each document in the list using the serialize_doc() function and return it as a list of incidents

@router.get("/incidents/{id}", response_model=IncidentResponse) # Return one incident - Get specific incident by ID
def get_one_incident(id: str): # of type string, which is the unique identifier for the incident in MongoDB.
    doc = incident_check(id) # Call the incident_check helper function to validate the ID and retrieve the corresponding document from the MongoDB collection. This function will handle errors related to invalid ID format and non-existent incidents, ensuring that only valid requests are processed further.
    return serialize_doc(doc) # converts the MongoDB document to string and then to a JSON format; returns it as the response for the GET request to retrieve a specific incident by ID.

@router.post("/incidents", response_model=IncidentResponse, status_code=201) # Create new incidents
def create_incident(data: IncidentCreate, user=Depends(get_current_user)): # data parameter will contain the details of the incident request sent in the request body with authentication dependency. May prompt 401 error in not authenticated.
    incident_data = data.model_dump() # .model_dump() method to convert the Pydantic model instance (data) into a dictionary format that can be easily manipulated and stored in the MongoDB collection. This allows the API route to work with the incident data in a format suitable for database operations, such as inserting a new document into the collection.
    # Set the created_at and updated_at timestamps to the current time when creating a new incident request
    incident_data["created_at"] = datetime.now()
    incident_data["updated_at"] = datetime.now()
    # Insert the validated and timestamped data into the MongoDB collection and return a success message along with the ID of the newly created incident request
    result = collection.insert_one(incident_data)
    new_doc = collection.find_one({"_id": result.inserted_id})
    return serialize_doc(new_doc) # Serialize the newly created document using the serialize_doc() function and return it as the response for the POST request to create a new incident.

@router.put("/incidents/{id}", response_model=IncidentResponse) # Update incident status only
def update_status(id: str, data: IncidentUpdate, user=Depends(get_current_user)): # Intake of incident ID as a string and a data dictionary ideally containing the updated status value for the incident request with authentication dependency. May prompt 401 error in not authenticated.
    existing_doc = incident_check(id) # Call the incident_check helper function to validate the ID and retrieve the existing document from the MongoDB collection. This ensures that the incident exists and is valid before attempting to update its status, and it will handle errors related to invalid ID format and non-existent incidents appropriately.
    update_data = data.model_dump(exclude_unset=True) # .model_dump(exclude_unset=True) method to convert the Pydantic model instance (data) into a dictionary format while excluding any fields that were not explicitly set in the request. This allows the API route to work with only the provided fields for updating the incident status, ensuring that only the intended changes are applied to the MongoDB document without affecting other fields that were not included in the update request.
    if not update_data: # If the resulting update_data dictionary is empty (i.e., no fields were provided for update), raise a 400 Bad Request error with a message indicating that no fields were provided for the update operation. This ensures that the API route requires at least one field to be updated in order to proceed with the status update of the incident request in the MongoDB collection.
        raise HTTPException(status_code=400, detail="No fields provided for update") # Checks done in models.py for literals, so no need to check for valid status values here.

    update_data["updated_at"] = datetime.now() # Update the updated_at timestamp to the current time whenever an update is made to an incident request, ensuring that the record reflects the most recent modification time in the MongoDB collection.

    # Update the specified fields of the incident in the MongoDB collection
    collection.update_one(
        {"_id": existing_doc["_id"]}, # Use the _id field from the existing document to identify which document to update in the MongoDB collection.
        {"$set": update_data} # Use the $set operator to specify the fields to be updated with the new values provided in the update_data dictionary, allowing for partial updates of the incident request in the MongoDB collection without affecting other fields that were not included in the update request.
    )

    updated_doc = collection.find_one({"_id": existing_doc["_id"]}) # Retrieve the updated document from the MongoDB collection after the update operation to return the latest state of the incident request in the response.
    return serialize_doc(updated_doc) # Serialize the updated document using the serialize_doc() function and return it as the response for the PUT request to update the status of a specific incident by ID.

@router.delete("/incidents/{id}") # Delete incident by ID
def delete_incident(id: str, user=Depends(get_current_user)): # Intake of incident ID as a string to identify which incident request to delete from the MongoDB collection with authentication dependency. May prompt 401 error in not authenticated.

    incident_check(id) # Call the incident_check helper function to validate the ID and ensure that the incident exists in the MongoDB collection before attempting to delete it. This function will handle errors related to invalid ID format and non-existent incidents, ensuring that only valid delete requests are processed further.
    
    result = collection.delete_one({"_id": ObjectId(id)}) # Attempt to delete the document with the specified ID from the MongoDB collection using the delete_one method, which returns a result object containing information about the deletion operation, including how many documents were deleted.
    
    if result.deleted_count == 0: # If no document was deleted (such as in, no document was found with the specified ID), raise a 404 Not Found error with a message indicating that the incident was not found.
        raise HTTPException(status_code=404, detail="Incident not found")
    # If the deletion was successful, return a success message indicating that the incident has been deleted.
    return {"message": "Incident deleted"}