import { useState, useRef, useEffect } from 'react';
import './JoystickControl.css';

function JoystickControl() {
  const joystickRef = useRef(null);
  const handleRef = useRef(null);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [speed, setSpeed] = useState(0);
  const [direction, setDirection] = useState('Stopped');
  const [robotStatus, setRobotStatus] = useState('Ready');
  
  // Calculate speed and direction based on joystick position
  useEffect(() => {
    // Calculate distance from center (speed)
    const distance = Math.sqrt(position.x ** 2 + position.y ** 2);
    const maxDistance = 50; // Max joystick travel distance
    const normalizedSpeed = Math.min(Math.round((distance / maxDistance) * 100), 100);
    setSpeed(normalizedSpeed);
    
    // Calculate direction based on angle
    if (normalizedSpeed < 10) {
      setDirection('Stopped');
    } else {
      // Negate the Y value to fix the direction
      const angle = Math.atan2(-position.y, position.x) * (180 / Math.PI);
      
      if (angle >= -22.5 && angle < 22.5) {
        setDirection('Right');
      } else if (angle >= 22.5 && angle < 67.5) {
        setDirection('Forward-Right');
      } else if (angle >= 67.5 && angle < 112.5) {
        setDirection('Forward');
      } else if (angle >= 112.5 && angle < 157.5) {
        setDirection('Forward-Left');
      } else if (angle >= 157.5 || angle < -157.5) {
        setDirection('Left');
      } else if (angle >= -157.5 && angle < -112.5) {
        setDirection('Backward-Left');
      } else if (angle >= -112.5 && angle < -67.5) {
        setDirection('Backward');
      } else if (angle >= -67.5 && angle < -22.5) {
        setDirection('Backward-Right');
      }
    }
    
    // Update robot status based on speed
    if (normalizedSpeed > 0) {
      setRobotStatus('Moving');
    } else {
      setRobotStatus('Ready');
    }
  }, [position]);
  
  const handleStart = (clientX, clientY) => {
    if (!joystickRef.current || !handleRef.current) return;
    
    setIsDragging(true);
    
    const joystickRect = joystickRef.current.getBoundingClientRect();
    const centerX = joystickRect.width / 2;
    const centerY = joystickRect.height / 2;
    
    updateHandlePosition(clientX, clientY, centerX, centerY, joystickRect);
  };
  
  const handleMove = (clientX, clientY) => {
    if (!isDragging || !joystickRef.current) return;
    
    const joystickRect = joystickRef.current.getBoundingClientRect();
    const centerX = joystickRect.width / 2;
    const centerY = joystickRect.height / 2;
    
    updateHandlePosition(clientX, clientY, centerX, centerY, joystickRect);
  };
  
  const updateHandlePosition = (clientX, clientY, centerX, centerY, joystickRect) => {
    // Calculate position relative to center
    let relativeX = clientX - joystickRect.left - centerX;
    let relativeY = clientY - joystickRect.top - centerY;
    
    // Limit to circular area
    const distance = Math.sqrt(relativeX ** 2 + relativeY ** 2);
    const maxDistance = 50; // Max joystick travel
    
    if (distance > maxDistance) {
      const angle = Math.atan2(relativeY, relativeX);
      relativeX = Math.cos(angle) * maxDistance;
      relativeY = Math.sin(angle) * maxDistance;
    }
    
    setPosition({ x: relativeX, y: relativeY });
  };
  
  const handleEnd = () => {
    setIsDragging(false);
    // Return to center (spring effect)
    setPosition({ x: 0, y: 0 });
  };
  
  // Mouse event handlers
  const onMouseDown = (e) => {
    handleStart(e.clientX, e.clientY);
  };
  
  const onMouseMove = (e) => {
    handleMove(e.clientX, e.clientY);
  };
  
  const onMouseUp = () => {
    handleEnd();
  };
  
  // Touch event handlers
  const onTouchStart = (e) => {
    if (e.touches && e.touches[0]) {
      handleStart(e.touches[0].clientX, e.touches[0].clientY);
    }
  };
  
  const onTouchMove = (e) => {
    if (e.touches && e.touches[0]) {
      handleMove(e.touches[0].clientX, e.touches[0].clientY);
    }
  };
  
  const onTouchEnd = () => {
    handleEnd();
  };
  
  // Set up global event listeners
  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
      document.addEventListener('touchmove', onTouchMove);
      document.addEventListener('touchend', onTouchEnd);
    }
    
    return () => {
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
      document.removeEventListener('touchmove', onTouchMove);
      document.removeEventListener('touchend', onTouchEnd);
    };
  }, [isDragging]);
  
  return (
    <div className="joystick-container">
      <div className="joystick-title">
        <h3>Robot Controls</h3>
        <div className={`status-indicator ${robotStatus.toLowerCase()}`}>
          {robotStatus}
        </div>
      </div>
      
      <div className="joystick-stats">
        <div className="stat">
          <span className="stat-label">Direction:</span>
          <span className="stat-value">{direction}</span>
        </div>
        <div className="stat">
          <span className="stat-label">Speed:</span>
          <span className="stat-value">{speed}%</span>
        </div>
      </div>
      
      <div 
        className="joystick-base"
        ref={joystickRef}
        onMouseDown={onMouseDown}
        onTouchStart={onTouchStart}
      >
        <div 
          className="joystick-direction-indicator forward">▲</div>
        <div 
          className="joystick-direction-indicator right">▶</div>
        <div 
          className="joystick-direction-indicator backward">▼</div>
        <div 
          className="joystick-direction-indicator left">◀</div>
          
        <div 
          className="joystick-handle"
          ref={handleRef}
          style={{
            transform: `translate(${position.x}px, ${position.y}px)`
          }}
        ></div>
      </div>
      
      <div className="control-instructions">
        <p>Click and drag joystick to navigate robot</p>
        <p>Release to stop movement</p>
      </div>
    </div>
  );
}

export default JoystickControl;