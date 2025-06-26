# api/zuno_bot1.py

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from api.zuno_api import generate_answer
import requests

app = FastAPI()
API_KEY = "nexzgrowveryfast"

@app.get("/")
def home():
    return {"message": "Hi, I'm Zuno. How can I help you?"}

class Query(BaseModel):
    question: str

def is_valid_answer(answer: str) -> bool:
    if not answer or len(answer.strip()) < 15:
        return False

    answer = answer.strip()
    answer_lower = answer.lower()

    bad_phrases = [
        "i don't know", "not sure", "no idea",
        "can't say", "unsure", "undefined", "sorry"
    ]
    if any(phrase in answer_lower for phrase in bad_phrases):
        return False

    if not answer.endswith("."):
        return False

    incomplete_endings = ["and", "or", "but", "to", "such as", "like", "for example"]
    if any(answer_lower.endswith(ending) for ending in incomplete_endings):
        return False

    return True

@app.post("/zuno/ask")
async def unified_zuno_chat(query: Query, x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    zuno_response = generate_answer(query.question)

    if is_valid_answer(zuno_response):
        return {"response": zuno_response}

    # Fallback to Rasa
    try:
        rrasa_response = requests.post(
    "https://rasa-zuno.onrender.com/webhooks/rest/webhook",
    json={"sender": "user", "message": query.question},
    timeout=3
    )
        messages = [m.get("text") for m in rasa_response.json() if "text" in m]
        if messages:
            return {"response": messages[0]}
    except Exception as e:
        print("Rasa fallback failed:", str(e))

    return {"response": "I'm not sure about that. Can you ask differently?"}
