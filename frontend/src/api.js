// api.js - API functions to interact with the backend of the Network Incident Reporting System
// Gheorghe Georgescu | 301377303 - SWS-212 Lab 3
const API_URL = "http://localhost:8000"; // Backend URL
// API functions to interact with the backend
export async function registerUser({ username, password }) { // Use JSON body to send data
  const res = await fetch(`${API_URL}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  return res.json();
}

export async function login(username, password) { // Use URLSearchParams to send form data
  const form = new URLSearchParams();
  form.append("username", username);
  form.append("password", password);

  const res = await fetch(`${API_URL}/token`, { // Use form data for login
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: form,
  });
  return res.json();
}

export async function getIncidents() { // Use JSON body to send data
  const res = await fetch(`${API_URL}/incidents`);
  return res.json();
}

export async function createIncident(token, incident) { // Use JSON body to send data
  const res = await fetch(`${API_URL}/incidents`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(incident),
  });
  return res.json();
}

export async function deleteIncident(token, id) { // Use JSON body to send data
  const res = await fetch(`${API_URL}/incidents/${id}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.json();
}