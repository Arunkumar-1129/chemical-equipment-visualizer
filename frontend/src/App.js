import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import './App.css';

// Use environment variable or default to localhost
// For mobile access, set REACT_APP_API_URL in .env file to your computer's IP
// Example: REACT_APP_API_URL=http://192.168.1.100:8000/api
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (token) {
      setIsAuthenticated(true);
      setUser(JSON.parse(localStorage.getItem('user') || '{}'));
    }
  }, [token]);

  const handleLogin = (authToken, userData) => {
    setToken(authToken);
    setUser(userData);
    setIsAuthenticated(true);
    localStorage.setItem('token', authToken);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} apiBaseUrl={API_BASE_URL} />;
  }

  return (
    <div className="App">
      <Dashboard 
        token={token} 
        user={user} 
        onLogout={handleLogout}
        apiBaseUrl={API_BASE_URL}
      />
    </div>
  );
}

export default App;


