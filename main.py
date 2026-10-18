from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        user_msg = request.message.strip()

        if not user_msg:
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty"
            )

        if not os.environ.get("GROQ_API_KEY"):
            raise RuntimeError("GROQ_API_KEY is missing")

        prompt = f"""
        Tum is business ke assistant ho.
        Sirf neeche diye gaye business data se jawab do.

        Business Data:
        {knowledge_data}

        User ka sawal: {user_msg}
        Agar jawab data mein nahi hai to politely kaho
        ke WhatsApp par rabta karein.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        return {"reply": response.choices[0].message.content}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("CHAT_ENDPOINT_FAILED")
        raise HTTPException(
            status_code=500,
            detail="Chat request failed. Check Vercel runtime logs."
        )
