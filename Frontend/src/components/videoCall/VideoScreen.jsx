import { useState, useEffect } from 'react';
import './VideoScreen.css';

function VideoScreen() {
  const [isMuted, setIsMuted] = useState(false);
  const [isVideoOff, setIsVideoOff] = useState(false);
  const [isFullScreen, setIsFullScreen] = useState(false);
  const [participantCount, setParticipantCount] = useState(2); // Doctor + patient initially
  
  // Mock connection status
  const [connectionStatus, setConnectionStatus] = useState('connecting');
  
  useEffect(() => {
    // Simulate connection establishing
    const timer = setTimeout(() => {
      setConnectionStatus('connected');
    }, 2000);
    
    return () => clearTimeout(timer);
  }, []);
  
  // Mock adding a participant after some time (e.g., nurse joins)
  useEffect(() => {
    if (connectionStatus === 'connected') {
      const timer = setTimeout(() => {
        setParticipantCount(3);
      }, 5000);
      
      return () => clearTimeout(timer);
    }
  }, [connectionStatus]);
  
  const toggleMute = () => {
    setIsMuted(!isMuted);
  };
  
  const toggleVideo = () => {
    setIsVideoOff(!isVideoOff);
  };
  
  const toggleFullScreen = () => {
    setIsFullScreen(!isFullScreen);
  };
  
  const endCall = () => {
    if (window.confirm('Are you sure you want to end this consultation?')) {
      // In a real app, would disconnect and navigate back
      window.history.back();
    }
  };
  
  return (
    <div className={`video-screen ${isFullScreen ? 'fullscreen' : ''}`}>
      {connectionStatus === 'connecting' ? (
        <div className="connecting-overlay">
          <div className="connecting-spinner"></div>
          <p>Connecting to Navatar...</p>
        </div>
      ) : (
        <>
          <div className="main-video">
            {isVideoOff ? (
              <div className="video-off-indicator">
                <span className="video-off-icon">📵</span>
                <p>Camera Off</p>
              </div>
            ) : (
              <img 
                src="https://images.pexels.com/photos/3938023/pexels-photo-3938023.jpeg" 
                alt="Patient view"
                className="video-feed"
              />
            )}
            <div className="participant-label">Patient Room</div>
          </div>
          
          <div className="video-controls">
            <button 
              className={`control-button ${isMuted ? 'active' : ''}`}
              onClick={toggleMute}
            >
              {isMuted ? '🔇' : '🔊'}
              <span className="control-label">{isMuted ? 'Unmute' : 'Mute'}</span>
            </button>
            
            <button 
              className={`control-button ${isVideoOff ? 'active' : ''}`}
              onClick={toggleVideo}
            >
              {isVideoOff ? '📵' : '📹'}
              <span className="control-label">{isVideoOff ? 'Start Video' : 'Stop Video'}</span>
            </button>
            
            <button 
              className="control-button"
              onClick={toggleFullScreen}
            >
              {isFullScreen ? '⬜' : '⬛'}
              <span className="control-label">{isFullScreen ? 'Exit Fullscreen' : 'Fullscreen'}</span>
            </button>
            
            <button 
              className="control-button end-call"
              onClick={endCall}
            >
              📞
              <span className="control-label">End Call</span>
            </button>
          </div>
          
          <div className="participants-grid">
            <div className="participant-video self-video">
              <img 
                src="https://images.pexels.com/photos/5452293/pexels-photo-5452293.jpeg" 
                alt="Doctor (You)"
                className="video-feed"
              />
              <div className="participant-label">You (Doctor)</div>
              {isMuted && <div className="mute-indicator">🔇</div>}
            </div>
            
            {participantCount > 2 && (
              <div className="participant-video">
                <img 
                  src="https://images.pexels.com/photos/5452201/pexels-photo-5452201.jpeg" 
                  alt="Nurse"
                  className="video-feed"
                />
                <div className="participant-label">Nurse Johnson</div>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default VideoScreen;