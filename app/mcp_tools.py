from typing import Dict

# Mock state to simulate a calendar database
mock_calendar_state: Dict[str, str] = {
    "09:00 AM": "Daily Standup",
    "10:00 AM": "Free",
    "11:00 AM": "Free",
    "01:00 PM": "Client Call"
}

def check_calendar_availability(time_slot: str) -> str:
    """Tool: Checks if a specific time slot is free on the calendar today.
    Args:
        time_slot: The time to check (e.g., '10:00 AM', '01:00 PM').
    """
    status = mock_calendar_state.get(time_slot, "Time slot not found in today's hours.")
    if status == "Free":
        return f"The time slot {time_slot} is currently available."
    return f"The time slot {time_slot} is booked with: {status}."

def book_calendar_slot(time_slot: str, meeting_title: str) -> str:
    """Tool: Books a free time slot on the calendar.
    Args:
        time_slot: The time to book (e.g., '10:00 AM').
        meeting_title: The title or purpose of the meeting.
    """
    status = mock_calendar_state.get(time_slot)
    if status == "Free":
        mock_calendar_state[time_slot] = meeting_title
        return f"SUCCESS: Successfully booked '{meeting_title}' at {time_slot}."
    elif status:
         return f"FAILED: Cannot book {time_slot}. It is already occupied by '{status}'."
    else:
         return f"FAILED: Invalid time slot format."