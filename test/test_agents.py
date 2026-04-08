from app.agents import process_request
from dotenv import load_dotenv

# Ensure environment variables are loaded for the API key
load_dotenv()

print("--- Initializing Agent Test ---")
prompt = "Prep me for tomorrow's engineering sync. Block 10:00 AM for me to review."
print(f"User Prompt: {prompt}\n")

print("Waiting for Gemini to execute tools and synthesize... (This might take a few seconds)")
response = process_request(prompt)

print("\n--- Final Agent Response ---")
print(f"Status: {response.status}")
print(f"Agenda:\n{response.final_agenda}")