import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/common/Navbar';
import './Login.css';

function Login() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const demoUsers = [
    {
      email: 'doctor@example.com',
      password: 'password',
      user: { id: '1', name: 'Sarah Johnson', email: 'doctor@example.com', role: 'doctor' }
    },
    {
      email: 'doctor2@example.com',
      password: 'password',
      user: { id: '2', name: 'John Smith', email: 'doctor2@example.com', role: 'doctor' }
    }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const matchedUser = demoUsers.find(u =>
      u.email === formData.email && u.password === formData.password
    );

    if (matchedUser) {
      login(matchedUser.user);
      navigate('/booking');
    } else {
      setError('Invalid credentials. Please try again.');
    }

    setLoading(false);
  };


  return (
    <div className="login-page">
      <Navbar />

      <div className="login-container container fade-in">
        <div className="login-card card">
          <div className="login-header">
            <h2>Doctor Login</h2>
            <p>Sign in to access the Navatar remote consultation system</p>
          </div>

          {error && <div className="error-message">{error}</div>}

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="email" className="form-label">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                className="form-input"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder="your.email@hospital.com"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password" className="form-label">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                className="form-input"
                value={formData.password}
                onChange={handleChange}
                required
                placeholder="••••••••"
              />
            </div>

            <div className="form-footer">
              <button
                type="submit"
                className="btn btn-primary btn-lg login-button"
                disabled={loading}
              >
                {loading ? 'Logging in...' : 'Login'}
              </button>
            </div>
          </form>

          <div className="login-help">
            <p>
              <small>
                Demo credentials: <br />
                Email: doctor@example.com <br />
                Password: password
              </small>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;