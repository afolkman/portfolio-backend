from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

# Create a fake client to test the FastAPI app
client = TestClient(app)

def test_read_main():
    # Simulate a user opening their browser and hitting the root endpoint
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Success! The FastAPI server is up and running."}

# We use the @patch decorator to intercept calls to the Gemini client and return a fake response
@patch('main.client.models.generate_content')
def test_chat_endpoint(mock_generate_content):
    # Set up the mock to return a fake response when called
    mock_generate_content.return_value.text = "This is a fake AI response."

    # Simulate a user sending a message to the chat endpoint
    response = client.post(
        "/api/chat", 
        json={"message": "Hello, AI!"}
    )
    
    # Check that the response is what we expect
    assert response.status_code == 200
    assert response.json() == {"reply": "This is a fake AI response."}

    # Verify that our app actually called the Gemini client's generate_content method with the correct parameters
    mock_generate_content.assert_called_once_with(
        model='gemini-2.5-flash',
        contents="Hello, AI!",
    )