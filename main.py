from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize the Gemini Client
client = genai.Client()

# Initialize the FastAPI app
app = FastAPI(
    title="Portfolio AI Backend",
    description="FastAPI backend powering my AI chatbot."
)

# Define the data format we expect from the frontend
class ChatRequest(BaseModel):
    message: str

# Root endpoint to verify the server is running
@app.get("/")
async def root():
    return {"message": "Success! The FastAPI server is up and running."}

# AI chat endpoint
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Send the user's message to Gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=request.message,
        )
        # Return the AI's response back to the user
        return {"reply": response.text}

    except Exception as e:
        return {"error": f"Something went wrong: {str(e)}"}