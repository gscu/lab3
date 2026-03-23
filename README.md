# SWS-212 — Lab 3: Network Incident Reporting System (FastAPI, React, MongoDB Atlas, Render)

This repository contains a full-stack Network Incident Reporting System using a FastAPI backend, React frontend, JWT-based authentication, MongoDB Atlas for persistence, and Render for cloud deployment. It demonstrate proper server-side ownership of persistence with protected routes, secure password hashing practices, and simple client-side integration through a light frontend UI.

## Project structure

- `backend/` — FastAPI app and related modules
  - `main.py` — FastAPI application entrypoint
  - `auth.py` — authentication and user management logic
  - `jwt_utils.py` — JWT token generation and validation helpers
  - `database.py` — MongoDB Atlas connection setup
  - `incidents.py` — incident CRUD API routes
  - `models.py` — Pydantic request/response models
  - `requirements.txt` — Python dependencies
- `frontend/` — React frontend and related modules
  - `src/` — React source files
  - `package.json` — Node dependencies and scripts
- `README.md` — setup and usage documentation
- `demo.mp4` — assignment demonstration video

## Prerequisites

- Python 3.12+ installed
- Node.js and npm installed
- MongoDB Atlas account
- VSCode IDE
- Browser for HTTP interfacing

## Setup

From the project root:

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

And if project setup steps above are already installed, you may simply reactivate with:

```powershell
venv\Scripts\activate
```

of the \backend directory.

## Run the backend

From `backend/`:

```powershell
unicorn main:app --reload
```
By default the server runs at `http://127.0.0.1:8000` and more useful is: `http://127.0.0.1:8000/docs` for JSON payload testing.

To run an overall healthcheck test go to `http://127.0.0.1:8000/health` route.

## Database Setup

For MongoDB Atlas:

Create a MongoDB Atlas cluster and configure a database user and connection string.
Then set the required environment variables for backend usage.
For instance:

Database name: example_network_incidents_db
```powershell
$env:MONGO_URI="your_mongodb_atlas_connection_string"
$env:JWT_SECRET="the_secret_key"
$env:JWT_ALGORITHM="HS256"
$env:ACCESS_TOKEN_EXPIRE_MINUTES="30"
```
## Run the frontend

From `frontend/`:

```powershell
npm install
npm run dev
```
By default the server runs at `http://localhost:5173` in a local environment.

If using a frontend environment variable, create a .env file inside frontend/ and add: `VITE_API_URL=http://127.0.0.1:8000` as deemed fit.

## Endpoints

Endpoints

System
- `GET /` — The welcome homepage - 200 okay status code.
- `GET /health` — Returns API health status - 200 okay status code.
Incidents
- `GET /incidents` — Retrieves all incidents - 200 okay status code.
- `GET /incidents/{id}` — Retrieves a specific incident by ID - 200 okay status code.
- `POST /incidents` — Submits an incident in JSON format (CURL or FastAPI UI) - 201 creation code.
- `PUT /incidents/{id}` — Updates a specific incident by ID - 200 okay status code.
- `DELETE /incidents/{id}` — Deletes a specific incident by ID - 200 okay status code.
Users
- `POST /register` — Create a new user - 201 okay creation code.
- `POST /token` — Login as a user and retrieve JWT token - 200 okay status code.

## Backend POST for users collection

Afer uvicorn main:app --reload
and redirecting to `http://127.0.0.1:8000/docs`

or from the frontend UI option for registration; running at `http://localhost:5173`

You may POST users via Swagger UI using the following values of input:
```JSON
{
  "username": "networkuser",
  "password": "engineer@123"
}
```
In either case, we can see that the POST request was successful and is saved in MongoDB Atlas users collection.

## Example Error: Backend POST user

For FastAPI's Swagger UI sign up:
```JSON
{
  "username": "admin_error",
  "password": "admin12345",
  "role": "adam"
}
```
This should output a 422 Unprocessable Content or 400 Bad Request.

## POST for incidents

Afer unicorn app:app --reload
and redirecting to `http://127.0.0.1:8000/docs`

or navigating frontend UI to create an incident ticket at `http://localhost:5173` 

You may POST tickets via Swagger UI or manually type values in frontend:
```JSON
{
  "device_name": "Core Router R1",
  "location": "Toronto Data Center",
  "incident_type": "routing failure",
  "severity": "high",
  "description": "The router is dropping OSPF neighbors and causing intermittent packet loss.",
  "status": "open"
}

{
  "device_name": "Firewall FW-01",
  "location": "Main Office",
  "incident_type": "service disruption",
  "severity": "critical",
  "description": "Users are unable to establish VPN connections.",
  "status": "investigating"
}

{
  "device_name": "Cisco Switch S2",
  "location": "Building A-3",
  "incident_type": "device outage",
  "severity": "medium",
  "description": "A floor switch is unreachable and users are reporting connectivity issues.",
  "status": "open"
}
```
We can see that the POST request was successful and is saved in MongoDB incidents collection.

## Example Error: POST incidents

From FastAPI's Swagger UI, add the following JSON snippet after authorized login in order to create a incident:
```JSON
{
  "service_name": "Wi-Fi Network",
  "priority": "low",
  "status": "open"
}
```
This should output a 422 Unprocessable Content or 400 Bad Request.


## Example: Login request

The `/token` endpoint uses OAuth2PasswordRequestForm, so login must be sent as follows for example:
username=networkuser
password=engineer123

Output response being:
```JSON
{
  "access_token": "example_jwt_token",
  "token_type": "bearer"
}
```
Or simply the token in the frontend to be displayed.

## Render Deployment

Create a Render Web Service - if pushed to GitHub choose Git Provider to connect repo - and configure:
Root directory: `backend`
Build: `pip install -r requirements.txt`
Then start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

Add the following backend environment variables in Render if needed:
- MONGO_URI
- JWT_SECRET
- JWT_ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES

For frontend deployment, create a Render Static Site and configure:
Root directory: `frontend`
Build: `npm install && npm run build`
Set Public Directory: `dist`
Add environment variable to point to: `VITE_API_URL=https://your-backend-service.onrender.com` 

## Notes

- This README documents the minimal steps to run and test the Lab 3 backend and frontend in a deployment setup. This assumes proper setup of MongoDB Atlas database and collection. 
- Updates to GitHub repo should pose no issues on Render's end as it will perform redeployment as needed.

## Author

Gheorghe Georgescu | 301377303

