from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for local dev and deployed frontend
origins = [
    "http://localhost:5173",
    "https://test-1rxpe0vvn-keanus-projects-916bf33d.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageRequest(BaseModel):
    message: str
    webhookUrl: str


@app.post("/send-message")
async def send_message(request: MessageRequest):
    try:
        modified_message = f"From Keanu Orig's Slack Bot: {request.message}"
        response = requests.post(request.webhookUrl, json={"text": modified_message})

        if response.status_code == 200:
            return {"status": "success", "message": "Message sent successfully"}
        else:
            raise HTTPException(
                status_code=response.status_code if response.status_code < 500 else 400,
                detail=f"Error sending message, status code: {response.status_code}",
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception: {str(e)}")
