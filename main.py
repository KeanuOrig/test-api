from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()


class MessageRequest(BaseModel):
    message: str
    webhookUrl: str


@app.post("/send-message")
async def send_message(request: MessageRequest):
    try:
        response = requests.post(request.webhookUrl, json={"text": request.message})
        if response.status_code == 200:
            return {"status": "success", "message": "Message sent successfully"}
        else:
            return {
                "status": "error",
                "message": f"Error sending message, status code: {response.status_code}",
            }
    except Exception as e:
        return {"status": "error", "message": f"Exception: {str(e)}"}
