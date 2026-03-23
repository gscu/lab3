// App.jsx - Main React component for the frontend Network Incident Reporting System 
// Gheorghe Georgescu | 301377303 - SWS-212 Lab 3
import { useEffect, useState } from "react"; // React hooks for state and side effects
import {
  Alert,
  Button,
  Card,
  Col,
  Container,
  Form,
  Row,
} from "react-bootstrap"; // UI components from React Bootstrap
import {
  registerUser,
  login,
  getIncidents,
  createIncident,
  deleteIncident,
} from "./api"; // API functions to interact with the backend
// Main App component
export default function App() { // State variables for authentication, alerts, incidents, and form data
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [authUser, setAuthUser] = useState(
    localStorage.getItem("authUser") || ""
  );
  const [alert, setAlert] = useState({ variant: "", text: "" });
  const [incidents, setIncidents] = useState([]);

  const [registerForm, setRegisterForm] = useState({
    username: "",
    password: "",
  });

  const [loginForm, setLoginForm] = useState({
    username: "",
    password: "",
  });

  const [incidentForm, setIncidentForm] = useState({ // Initial form state for creating an incident
    device_name: "",
    location: "",
    incident_type: "",
    severity: "low",
    description: "",
    status: "open",
  });

  function showAlert(variant, text) { // Helper function to show alerts
    setAlert({ variant, text });
    setTimeout(() => setAlert({ variant: "", text: "" }), 3500);
  }

  async function loadIncidents() { // Load incidents from the backend
    const data = await getIncidents();
    if (data.detail) {
      showAlert("danger", data.detail);
      return;
    }
    setIncidents(data);
  }

  useEffect(() => { // Load incidents on component mount; meaning when the app first loads, it will fetch the list of incidents from the backend
    loadIncidents();
  }, []);

  async function handleRegister(e) { // Handle registration form submission; meaning when the user submits the registration form, this function will be called to create a new user account
    e.preventDefault();

    const data = await registerUser(registerForm);

    if (data.detail) {
      showAlert("danger", data.detail);
      return;
    }

    showAlert("success", `Registered ${data.username}`);
    setRegisterForm({ username: "", password: "" });
  }

  async function handleLogin(e) { // Handle login form submission; meaning when the user submits the login form, this function will be called to authenticate the user and store the token
    e.preventDefault(); // Prevent default form submission behavior; meaning it prevents the page from reloading when the form is submitted

    const data = await login(loginForm.username, loginForm.password); // Call the login API function from api.js with the username and password from the form

    if (!data.access_token) { // If login fails, show an error alert; meaning if the login API does not return an access token, it will display an error message to the user
      showAlert("danger", data.detail || "Login failed");
      return;
    }

    setToken(data.access_token);
    setAuthUser(loginForm.username);
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("authUser", loginForm.username);

    showAlert("success", `Logged in as ${loginForm.username}`); // Show success alert on successful login; meaning it will display a success message indicating that the user has logged in successfully
    setLoginForm({ username: "", password: "" });
  }

  function handleLogout() { // Handle user logout; meaning when the user clicks the logout button, this function will clear the authentication state and remove the token from local storage
    setToken("");
    setAuthUser("");
    localStorage.removeItem("token");
    localStorage.removeItem("authUser");
    showAlert("info", "Logged out");
  }

  async function handleCreateIncident(e) { // Handle create incident form submission; meaning when the user submits the form to create a new incident, this function will be called to send the incident data to the backend and create a new incident
    e.preventDefault();

    if (!token) {
      showAlert("warning", "Please log in first");
      return;
    }

    const data = await createIncident(token, incidentForm);

    if (data.detail) {
      showAlert("danger", data.detail);
      return;
    }

    showAlert("success", "Incident created");

    setIncidentForm({
      device_name: "",
      location: "",
      incident_type: "",
      severity: "low",
      description: "",
      status: "open",
    });

    loadIncidents();
  }

  async function handleDeleteIncident(id) { // Handle delete incident; meaning when the user clicks the delete button for an incident, this function will be called to remove the incident from the backend
    if (!token) {
      showAlert("warning", "Please log in first");
      return;
    }

    const data = await deleteIncident(token, id);

    if (data.detail) {
      showAlert("danger", data.detail);
      return;
    }

    showAlert("success", "Incident deleted");
    loadIncidents();
  }

  return ( // Main JSX return statement to render the UI components; meaning this part defines the structure and layout of the user interface using React Bootstrap components
    <Container className="appContainer">
      <Row className="mb-3">
        <Col>
          <h1 className="appTitle">Network Incident Reporting System</h1>
          <p className="appSubtitle">
            Login → View incidents → Create incidents → Delete incidents
          </p>
        </Col>
      </Row>

      {alert.text && (
        <Row className="mb-3">
          <Col>
            <Alert variant={alert.variant}>{alert.text}</Alert>
          </Col>
        </Row>
      )}

      <Row>
        <Col lg={5} className="mb-4">
          <Card className="mb-4">
            <Card.Body>
              <Card.Title>Register</Card.Title>
              <Form onSubmit={handleRegister}>
                <Form.Group className="mb-3">
                  <Form.Label>Username</Form.Label>
                  <Form.Control
                    type="text"
                    value={registerForm.username}
                    onChange={(e) =>
                      setRegisterForm({
                        ...registerForm,
                        username: e.target.value,
                      })
                    }
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    type="password"
                    value={registerForm.password}
                    onChange={(e) =>
                      setRegisterForm({
                        ...registerForm,
                        password: e.target.value,
                      })
                    }
                  />
                </Form.Group>

                <Button type="submit" variant="success">
                  Register
                </Button>
              </Form>
            </Card.Body>
          </Card>

          <Card className="mb-4">
            <Card.Body>
              <Card.Title>Login</Card.Title>
              <Form onSubmit={handleLogin}>
                <Form.Group className="mb-3">
                  <Form.Label>Username</Form.Label>
                  <Form.Control
                    type="text"
                    value={loginForm.username}
                    onChange={(e) =>
                      setLoginForm({
                        ...loginForm,
                        username: e.target.value,
                      })
                    }
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    type="password"
                    value={loginForm.password}
                    onChange={(e) =>
                      setLoginForm({
                        ...loginForm,
                        password: e.target.value,
                      })
                    }
                  />
                </Form.Group>

                <Button type="submit" className="me-2">
                  Login
                </Button>

                <Button variant="secondary" onClick={handleLogout}>
                  Logout
                </Button>
              </Form>

              {token && (
                <div className="tokenBox">
                  <div className="tokenLabel">Logged in as:</div>
                  <div>{authUser}</div>
                  <div className="tokenLabel mt-3">JWT Token:</div>
                  <div className="tokenValue">{token}</div>
                </div>
              )}
            </Card.Body>
          </Card>

          <Card>
            <Card.Body>
              <Card.Title>Create Incident</Card.Title>
              <Form onSubmit={handleCreateIncident}>
                <Form.Group className="mb-3">
                  <Form.Label>Device Name</Form.Label>
                  <Form.Control
                    type="text"
                    value={incidentForm.device_name}
                    onChange={(e) =>
                      setIncidentForm({
                        ...incidentForm,
                        device_name: e.target.value,
                      })
                    }
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Location</Form.Label>
                  <Form.Control
                    type="text"
                    value={incidentForm.location}
                    onChange={(e) =>
                      setIncidentForm({
                        ...incidentForm,
                        location: e.target.value,
                      })
                    }
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Incident Type</Form.Label>
                  <Form.Control
                    type="text"
                    value={incidentForm.incident_type}
                    onChange={(e) =>
                      setIncidentForm({
                        ...incidentForm,
                        incident_type: e.target.value,
                      })
                    }
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Severity</Form.Label>
                  <Form.Select
                    value={incidentForm.severity}
                    onChange={(e) =>
                      setIncidentForm({
                        ...incidentForm,
                        severity: e.target.value,
                      })
                    }
                  >
                    <option value="low">low</option>
                    <option value="medium">medium</option>
                    <option value="high">high</option>
                    <option value="critical">critical</option>
                  </Form.Select>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Description</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={4}
                    value={incidentForm.description}
                    onChange={(e) =>
                      setIncidentForm({
                        ...incidentForm,
                        description: e.target.value,
                      })
                    }
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Status</Form.Label>
                  <Form.Select
                    value={incidentForm.status}
                    onChange={(e) =>
                      setIncidentForm({
                        ...incidentForm,
                        status: e.target.value,
                      })
                    }
                  >
                    <option value="open">open</option>
                    <option value="investigating">investigating</option>
                    <option value="resolved">resolved</option>
                  </Form.Select>
                </Form.Group>

                <Button type="submit">Create Incident</Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>

        <Col lg={7}>
          <Card>
            <Card.Body>
              <Card.Title>Incident List</Card.Title>

              {incidents.length === 0 ? (
                <p>No incidents found.</p>
              ) : (
                incidents.map((incident) => (
                  <Card key={incident.id} className="mb-3">
                    <Card.Body>
                      <Card.Title>{incident.device_name}</Card.Title>
                      <Card.Text>
                        <strong>Location:</strong> {incident.location}
                        <br />
                        <strong>Type:</strong> {incident.incident_type}
                        <br />
                        <strong>Severity:</strong> {incident.severity}
                        <br />
                        <strong>Status:</strong> {incident.status}
                        <br />
                        <strong>Description:</strong> {incident.description}
                      </Card.Text>
                      <Button
                        variant="danger"
                        onClick={() => handleDeleteIncident(incident.id)}
                      >
                        Delete
                      </Button>
                    </Card.Body>
                  </Card>
                ))
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}