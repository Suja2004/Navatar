import { useNavigate } from 'react-router-dom';
import Navbar from '../components/common/Navbar';
import './LandingPage.css';
import logo from "../assets/logo.png";  // Clean up the comment

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      <Navbar />
      
      <main className="landing-hero">
        <div className="hero-content container">
          <div className="hero-text">
            <h1 className="slide-in-up">Welcome to Navatar</h1>
            <h2 className="slide-in-up">Revolutionizing Remote Patient Care</h2>
            <p className="slide-in-up">
              Navatar is a cutting-edge video conferencing solution mounted on 4 wheels
              allowing doctors to remotely navigate to patients ward of beds for
              face-to-face consultations with patients, relatives, and nursing staff.
            </p>
            <div className="hero-buttons slide-in-up">
              <button 
                className="btn btn-primary btn-lg"
                onClick={() => navigate('/login')}
              >
                Login as Doctor
              </button>
            </div>
          </div>
          
          <div className="hero-image slide-in-up">
            <img 
              src={logo}   // Fix: Use the imported logo variable in curly braces
              alt="Medical robot with video conferencing"
              className="robot-image"
            />
          </div>
        </div>
      </main>
      
      <section className="features container">
        <h2>Key Features</h2>
        
        <div className="feature-cards">
          <div className="feature-card fade-in">
            <div className="feature-icon">🎥</div>
            <h3>HD Video Conferencing</h3>
            <p>Crystal clear video and audio for seamless doctor-patient communication.</p>
          </div>
          
          <div className="feature-card fade-in">
            <div className="feature-icon">🕹️</div>
            <h3>Remote Navigation</h3>
            <p>Intuitive joystick controls for precise robot movement to patient bedsides.</p>
          </div>
          
          <div className="feature-card fade-in">
            <div className="feature-icon">📅</div>
            <h3>Smart Scheduling</h3>
            <p>Efficient robot booking system to optimize doctor time and patient care.</p>
          </div>
          
          <div className="feature-card fade-in">
            <div className="feature-icon">🔒</div>
            <h3>Secure Communication</h3>
            <p>End-to-end encryption ensuring private and secure patient consultations.</p>
          </div>
        </div>
      </section>
      
      <footer className="footer">
        <div className="container">
          <p>&copy; 2025 Navatar Health Technologies. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default LandingPage;