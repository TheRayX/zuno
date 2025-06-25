# api/zuno_bot1.py

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from api.zuno_api import generate_answer
import requests

app = FastAPI()

API_KEY = "nexzgrowveryfast"

# ✅ Show initial message
@app.get("/")
def home():
    return {"message": "Hi, I'm Zuno. How can I help you?"}


class Query(BaseModel):
    question: str

# ✅ Check if Zuno’s answer is valid
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

    # Must end with a period
    if not answer.endswith("."):
        return False

    # No vague endings
    incomplete_endings = ["and", "or", "but", "to", "such as", "like", "for example"]
    if any(answer_lower.endswith(ending) for ending in incomplete_endings):
        return False

    return True

# ✅ Unified Zuno + Rasa chat route
@app.post("/zuno/ask")
async def unified_zuno_chat(query: Query, x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # ✅ Primary: Zuno
    zuno_response = generate_answer(query.question)

    if is_valid_answer(zuno_response):
        return {"response": zuno_response}

    # 🔁 Fallback: Rasa (running locally on port 5005)
    rasa_response = requests.post(
        "http://localhost:5005/webhooks/rest/webhook",
        json={"sender": "user", "message": query.question}
    )

    messages = [m.get("text") for m in rasa_response.json() if "text" in m]
    if messages:
        return {"response": messages[0]}
    else:
        return {"response": "I'm not sure about that. Can you ask differently?"}
