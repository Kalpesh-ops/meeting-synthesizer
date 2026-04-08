from app.mcp_tools import check_calendar_availability, book_calendar_slot
from app.database import init_dummy_data, query_meeting_notes

print("--- Testing Calendar Tools ---")
print(check_calendar_availability("10:00 AM"))
print(book_calendar_slot("10:00 AM", "Prep for Engineering Sync"))
print(check_calendar_availability("10:00 AM"))

print("\n--- Testing Database Tools ---")
init_dummy_data() 
print(query_meeting_notes("engineering sync"))