// main.jsx - Entry point for the React application (Network Incident Reporting System); responsible for rendering the main App component into the DOM
// Gheorghe Georgescu | 301377303 - SWS-212 Lab 3
import "bootstrap/dist/css/bootstrap.min.css"; // Import Bootstrap CSS for styling the UI components
import React from "react"; // Import React library for building the user interface
import ReactDOM from "react-dom/client";
import App from "./App.jsx"; // Import the main App component which contains the core logic and UI for the application
import "./styles.css"; // Import custom CSS styles for additional styling of the application

ReactDOM.createRoot(document.getElementById("root")).render( // Render the main App component inside a StrictMode wrapper; meaning it will render the App component and enable additional checks and warnings for potential issues in the application
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
