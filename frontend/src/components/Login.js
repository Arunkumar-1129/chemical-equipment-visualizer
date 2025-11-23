import React, { useState } from 'react';
import axios from 'axios';
import './Login.css';

const Login = ({ onLogin, apiBaseUrl }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const endpoint = isLogin ? 'login' : 'register';
      const data = isLogin 
        ? { username, password }
        : { username, password, email };

      const response = await axios.post(`${apiBaseUrl}/${endpoint}/`, data);
      
      onLogin(response.data.token, {
        id: response.data.user_id,
        username: response.data.username
      });
    } catch (err) {
      if (err.response) {
        // Server responded with error
        setError(err.response.data?.error || `Server error: ${err.response.status}`);
      } else if (err.request) {
        // Request made but no response
        setError('Cannot connect to server. Is the backend running at ' + apiBaseUrl + '?');
      } else {
        // Something else happened
        setError('An error occurred: ' + err.message);
      }
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Chemical Equipment Visualizer</h1>
        <p className="subtitle">Sign in to continue</p>
        
        {error && <div className="error">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          
          {!isLogin && (
            <div className="input-group">
              <label>Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          )}
          
          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Please wait...' : (isLogin ? 'Login' : 'Register')}
          </button>
        </form>
        
        <p className="toggle-text">
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <span 
            className="toggle-link" 
            onClick={() => {
              setIsLogin(!isLogin);
              setError('');
            }}
          >
            {isLogin ? 'Register' : 'Login'}
          </span>
        </p>
      </div>
    </div>
  );
};

export default Login;









