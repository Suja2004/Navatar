import { useEffect } from 'react';
import { format, isBefore, isSameDay, startOfDay } from 'date-fns';

function CalendarGrid({ calendarDays, selectedDate, onDateClick }) {
  useEffect(() => {
    const calendarElement = document.querySelector('.calendar');
    if (!calendarElement) return;
    const handleMouseMove = (e) => {
      calendarElement.style.setProperty('--x', `${e.clientX}px`);
      calendarElement.style.setProperty('--y', `${e.clientY}px`);
    };
    document.addEventListener('mousemove', handleMouseMove);
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <div className="calendar">
      {calendarDays.map((day, index) => {
        const isPast = isBefore(day, startOfDay(new Date()));
        return (
          <button
            key={index}
            className={`calendar-day ${isSameDay(day, selectedDate) ? 'selected' : ''} ${isPast ? 'past' : ''}`}
            style={{
              '--delay': `${index * 0.2}s`
            }}
            onClick={() => !isPast && onDateClick(day)}
            disabled={isPast}
          >
            {format(day, 'd')}
          </button>
        );
      })}
    </div>
  );
}
export default CalendarGrid;
