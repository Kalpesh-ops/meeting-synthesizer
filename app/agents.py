import os
import time
from google import genai
from google.genai import types
from app.mcp_tools import check_calendar_availability, book_calendar_slot
from app.database import query_meeting_notes
from app.models import ChatResponse

# Initialize the client
client = genai.Client()

# Register our MCP/Database tools
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

# Fallback cascade: Primary -> Fast/Free Lite -> Reliable Pro
MODELS_TO_TRY = [
    "gemini-2.5-flash",
    "gemini-3.1-flash-lite", 
    "gemini-2.5-pro"
]

def process_request(user_prompt: str) -> ChatResponse:
    """Orchestrates the Gemini model and tools, with automatic failover."""
    config = types.GenerateContentConfig(
        tools=agent_tools,
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.2, # Lower temperature for reliable tool execution
    )
    
    last_error = None
    
    # Iterate through our models. If one fails, try the next.
    for model_name in MODELS_TO_TRY:
        try:
            print(f"Attempting execution with {model_name}...")
            chat = client.chats.create(model=model_name, config=config)
            
            # This single line handles the entire workflow: reasoning -> tool calling -> synthesis
            response = chat.send_message(user_prompt)
            
            print(f"Success with {model_name}!")
            return ChatResponse(
                status="success",
                final_agenda=response.text
            )
            
        except Exception as e:
            last_error = str(e)
            print(f"Error with {model_name}: {last_error}. Falling back to next model...")
            time.sleep(1) # Brief 1-second pause to prevent rate-limiting the fallback
            continue

    # If the loop finishes without returning, all models failed.
    print("CRITICAL: All fallback models failed.")
    return ChatResponse(
        status="error", 
        final_agenda=f"An error occurred after trying all fallback models. Last error: {last_error}"
    )