# routes/chat.py

from fastapi import APIRouter
from pydantic import BaseModel
from memory.session_memory import memory
from agents.query_agent import QueryAgent

router = APIRouter(prefix="/chat")


class ChatRequest(BaseModel):
    message: str
    session_id: str

@router.post("")
def chat(req: ChatRequest):

    session = memory.get(req.session_id)
    state = session.get("state")

    agent = QueryAgent()

    # ✅ inject query into real state
    state["user_query"] = req.message

    result = agent.run(state)

    return {
        "reply": result.get("data")
    }