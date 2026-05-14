# routes/upload.py

from fastapi import APIRouter, UploadFile, File, Form
import os
import pandas as pd
import uuid

from memory.session_memory import memory
from agents.cleaning_agent import CleaningAgent   # ✅ ADD THIS

router = APIRouter(prefix="/upload")

cleaner = CleaningAgent()   # ✅ INIT


@router.post("")
async def upload_file(
    file: UploadFile = File(...),
    session_id: str = Form(None)
):

    os.makedirs("data/raw", exist_ok=True)

    file_path = f"data/raw/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # ---------------------------
    # LOAD DATA
    # ---------------------------
    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
    except Exception as e:
        return {"error": str(e)}

    # ---------------------------
    # SESSION ID
    # ---------------------------
    if not session_id:
        session_id = str(uuid.uuid4())

    # ---------------------------
    # 🔥 RUN CLEANING AGENT
    # ---------------------------
    cleaning_result = cleaner.run({
        "ingestion": {
            "status": "success",
            "data": df
        }
    })

    if cleaning_result["status"] != "success":
        return cleaning_result

    # cleaned_df = cleaning_result["data"]

    # ---------------------------
    # 🔥 STORE BOTH RAW + CLEAN
    # ---------------------------
    state = {
        "file_path": file_path,
        "data": df,
        "cleaning": cleaning_result,   # ✅ FULL RESULT
        "history": ["upload", "cleaning"]
    }

    memory.set_state(session_id, state)

    print("✅ Upload + Cleaning complete")

    return {
        "session_id": session_id,
        "filename": file.filename,
        "size": os.path.getsize(file_path),
        "rows": len(df),
        "columns": len(df.columns)
    }