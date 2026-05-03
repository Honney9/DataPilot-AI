# routes/data.py

from fastapi import APIRouter, Query
from memory.session_memory import memory
import numpy as np
import pandas as pd

router = APIRouter(prefix="/data")


@router.get("/raw")
def get_raw_data(session_id: str = Query(...)):

    session = memory.get(session_id)
    if not session:
        return {"columns": [], "rows": [], "total_rows": 0}

    state = session.get("state")
    if not state:
        return {"columns": [], "rows": [], "total_rows": 0}

    df = state.get("data")
    if df is None:
        return {"columns": [], "rows": [], "total_rows": 0}

    # 🔥 FIX (same as preview)
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

    state = memory.get_state(session_id)   # ✅ correct

    if not state:
        return {"columns": [], "rows": [], "total_rows": 0}

    df = state.get("data")
    if df is None:
        return {"columns": [], "rows": [], "total_rows": 0}

    df_clean = df.drop_duplicates()

    df_clean = df_clean.replace([np.inf, -np.inf], np.nan)
    df_clean = df_clean.astype(object).where(df_clean.notnull(), None)

    return {
        "columns": [
            {
                "name": col,
                "type": str(df_clean[col].dtype),
                "missing": int(df_clean[col].isnull().sum())
            }
            for col in df_clean.columns
        ],
        "rows": df_clean.head(100).to_dict(orient="records"),
        "total_rows": len(df_clean)
    }
