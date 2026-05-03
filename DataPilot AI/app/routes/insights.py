# routes/insights.py

from fastapi import APIRouter, Query
from memory.session_memory import memory

router = APIRouter(prefix="/insights")


@router.get("")
def get_insights(session_id: str = Query(...)):
    session = memory.get(session_id)

    if not session:
        return {"error": "Session not found"}

    state = session.get("state")
    if not state or "data" not in state:
        return {"error": "No data found"}

    df = state["data"]

    return {
        "summary": {
            "rows": len(df),
            "columns": len(df.columns),
            "missing": int(df.isnull().sum().sum()),
            "duplicates": int(df.duplicated().sum())
        },
        "stats": [],
        "correlations": [],
        "trends": ["Basic dataset loaded"],
        "outliers": []
    }