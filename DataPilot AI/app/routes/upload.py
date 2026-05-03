# routes/upload.py

from fastapi import APIRouter, UploadFile, File, Form
import os
import pandas as pd
import uuid

from memory.session_memory import memory

router = APIRouter(prefix="/upload")


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
    # SESSION HANDLING
    # ---------------------------
    if not session_id:
        session_id = str(uuid.uuid4())

    # 🔥 STORE FULL STATE (IMPORTANT)
    state = {
        "file_path": file_path,
        "data": df,
        "history": []
    }

    memory.set_state(session_id, state)

    return {
        "session_id": session_id,
        "filename": file.filename,
        "size": os.path.getsize(file_path),
        "rows": len(df),
        "columns": len(df.columns)
    }