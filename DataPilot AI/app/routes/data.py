# routes/data.py

from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
from memory.session_memory import memory
import numpy as np
import pandas as pd
import os

router = APIRouter(prefix="/data")


@router.get("/raw")
def get_raw_data(session_id: str):

    state = memory.get_state(session_id)

    if not state:
        return {"columns": [], "rows": [], "total_rows": 0}

    df = state.get("data")

    if df is None:
        return {"columns": [], "rows": [], "total_rows": 0}

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.astype(object).where(pd.notnull(df), None)

    return {
        "columns": [
            {"name": col, "type": str(df[col].dtype), "missing": int(df[col].isnull().sum())}
            for col in df.columns
        ],
        "rows": df.head(100).to_dict(orient="records"),
        "total_rows": len(df)
    }


@router.get("/preview")
def get_cleaned_data(session_id: str):

    state = memory.get_state(session_id)

    if not state:
        return {"columns": [], "rows": [], "total_rows": 0}

    # ✅ USE CLEANED DATA
    cleaning = state.get("cleaning")

    if not cleaning:
        return {"error": "No cleaned data found"}

    df = cleaning["data"]

    if df is None:
        return {"error": "No cleaned data found"}

    # Safety formatting (not cleaning)
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.astype(object).where(pd.notnull(df), None)

    return {
        "columns": [
            {
                "name": col,
                "type": str(df[col].dtype),
                "missing": int(df[col].isnull().sum())
            }
            for col in df.columns
        ],
        "rows": df.head(100).to_dict(orient="records"),
        "total_rows": len(df)
    }

@router.get("/download")
def download_cleaned(session_id: str):

    state = memory.get_state(session_id)

    if not state:
        return {"error": "No session"}

    cleaning = state.get("cleaning")

    if not cleaning:
        return {"error": "No cleaned data"}

    file_path = cleaning["meta"].get("processed_path")

    if not file_path or not os.path.exists(file_path):
        return {"error": "File not found"}

    return FileResponse(
        path=file_path,
        filename="cleaned_data.csv",
        media_type="text/csv"
    )
