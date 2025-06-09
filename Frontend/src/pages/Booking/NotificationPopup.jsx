function NotificationPopup({ isOpen, message, type, onClose }) {
  if (!isOpen) return null;

  return (
    <div className='popup'>
      <button className={`popup-content ${type}`} onClick={onClose}>
        {message}
      </button>
      <div className={`popup-indicator ${type}`}></div>
    </div>
  );
}
export default NotificationPopup;
