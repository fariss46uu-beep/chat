from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os

app = FastAPI()

# CORS FIX - Ye sabse important hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def load_knowledge():
    try:
        with open("knowledge.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "No business data yet."

knowledge_data = load_knowledge()

@app.get("/")
def home():
    return {"status": "Chatbot Ready", "knowledge": "loaded"}

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_msg = body.get("message", "")

    prompt = f"""
    Tum is business ke assistant ho. Sirf neeche diye gaye data se jawab do.
    Business Data:
    {knowledge_data}

    User ka sawal: {user_msg}
    Agar data me jawab na ho to politely kaho ke WhatsApp pe rabta karein.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"reply": response.choices[0].message.content}