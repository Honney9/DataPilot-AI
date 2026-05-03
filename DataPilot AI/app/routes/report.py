from fastapi import APIRouter, Query
from memory.session_memory import memory
from agents.report_agent import ReportAgent
from fastapi.responses import FileResponse
import os
from datetime import datetime

router = APIRouter(prefix="/report")

agent = ReportAgent()

@router.post("")
def generate_report(session_id: str = Query(...)):
    session = memory.get(session_id)
    state = session.get("state")

    if not state:
        return {"error": "No state found"}

    result = agent.run(state, session_id)

    if result["status"] != "success":
        return result

    report = result["data"]

    return {
        **report,
        "download_url": f"/report/download?session_id={session_id}"
    }

@router.get("/download")
def download_report(session_id: str):
    file_path = f"outputs/reports/{session_id}.pdf"

    if not os.path.exists(file_path):
        return {"error": "Report not found"}

    return FileResponse(file_path, filename="report.pdf")