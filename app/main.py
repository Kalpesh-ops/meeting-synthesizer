from fastapi import FastAPI, HTTPException
from app.models import ChatRequest, ChatResponse
from app.agents import process_request
from app.database import init_dummy_data

app = FastAPI(
    title="Multi-Agent Productivity Assistant API",
    description="Gen AI Academy APAC Hackathon Submission",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    """Fires when the Cloud Run container spins up."""
    print("Starting up server... Initializing AlloyDB dummy data if connected.")
    init_dummy_data()

@app.get("/")
def health_check():
    """Simple endpoint so Cloud Run knows the container is alive."""
    return {"status": "online", "message": "Multi-Agent System is Ready"}

@app.post("/api/assistant", response_model=ChatResponse)
def assistant_endpoint(request: ChatRequest):
    """The main endpoint the judges will test."""
    if not request.user_prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    print(f"Received API Request: {request.user_prompt}")
    response = process_request(request.user_prompt)
    return response