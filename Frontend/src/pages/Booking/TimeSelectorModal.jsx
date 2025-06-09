import { format } from 'date-fns';

function TimeSelectorModal({
  isOpen,
  onClose,
  selectedDate,
  selectedStartTime,
  onStartTimeChange,
  selectedEndTime,
  onEndTimeChange,
  onCheckAvailability,
  onOverlayClick
}) {
  if (!isOpen || !selectedDate) return null;

  return (
    <div className="modal-overlay" onClick={onOverlayClick}>
      <div className="time-container">
        <p className='modal-header' style={{ textAlign: 'center' }}>Select start and end time for {format(selectedDate, 'MMMM d, yyyy')}</p>
        <div className="time-inputs">
          <label>
            Start Time:
            <input
              type="time"
              value={selectedStartTime}
              onChange={(e) => onStartTimeChange(e.target.value)}
              min="00:00"
              max="23:59"
              step="300"
              required
            />
          </label>
          <label>
            End Time:
            <input
              type="time"
              value={selectedEndTime}
              onChange={(e) => onEndTimeChange(e.target.value)}
              min={selectedStartTime || "00:00"}
              max="23:59"
              step="300"
              required
            />
          </label>
        </div>
        <div className="modal-footer">
          <button className="btn btn-danger" onClick={onClose}>Cancel</button>
          <button
            className="btn btn-primary check-availability"
            onClick={onCheckAvailability}
            disabled={!selectedStartTime || !selectedEndTime || selectedStartTime >= selectedEndTime}
          >
            Check Availability
          </button>
        </div>
      </div>
    </div>
  );
}
export default TimeSelectorModal;
