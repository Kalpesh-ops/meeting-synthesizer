import os
from google import genai
from google.genai import types
from app.mcp_tools import check_calendar_availability, book_calendar_slot
from app.database import query_meeting_notes
from app.models import ChatResponse

# Initialize the client. It automatically picks up GEMINI_API_KEY from your .env
client = genai.Client()

# This is where we register our MCP/Database tools for the model to use
agent_tools = [
    check_calendar_availability,
    book_calendar_slot,
    query_meeting_notes
]

SYSTEM_INSTRUCTION = """
You are an autonomous Multi-Agent Productivity Assistant.
When a user asks you to prepare for a meeting, you must perform these steps:
1. Use the calendar tools to find an available time slot and book it for meeting prep.
2. Use the database tool to query for past notes related to the meeting topic.
3. Synthesize the confirmation of the booked time and the historical notes into a concise, professional summary and agenda for the user.

If a tool fails or returns an error (like a database connection issue), gracefully inform the user of what you *were* able to complete.
"""

def process_request(user_prompt: str) -> ChatResponse:
    """Orchestrates the Gemini model and tools to fulfill the user's request."""
    try:
        # Configure the model with our tools and instructions
        config = types.GenerateContentConfig(
            tools=agent_tools,
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.2, # Lower temperature for reliable tool execution
        )
        
        # We use the chats API because it handles the multi-turn tool execution automatically
        chat = client.chats.create(model="gemini-2.5-flash", config=config)
        
        # This single line handles the entire workflow: reasoning -> tool calling -> synthesis
        response = chat.send_message(user_prompt)
        
        return ChatResponse(
            status="success",
            final_agenda=response.text
        )
        
    except Exception as e:
        print(f"Agent Error: {e}")
        return ChatResponse(
            status="error", 
            final_agenda=f"An error occurred during agent execution: {str(e)}"
        )