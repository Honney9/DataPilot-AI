from fastapi import APIRouter, Query
from memory.session_memory import memory
import pandas as pd
import numpy as np

router = APIRouter(prefix="/insights")


@router.get("")
def get_insights(session_id: str = Query(...)):
    session = memory.get(session_id)

    if not session:
        return {"error": "Session not found"}

    state = session.get("state")

    if not state:
        return {"error": "No state found"}

    # ✅ FIX: Proper dataframe selection
    df = state.get("clean_data") if state.get("clean_data") is not None else state.get("data")

    if df is None:
        return {"error": "No data available"}

    # ---------------------------
    # NUMERIC DATA
    # ---------------------------
    numeric_df = df.select_dtypes(include=[np.number])

    # ---------------------------
    # 📊 SUMMARY STATS
    # ---------------------------
    stats = []
    for col in numeric_df.columns:
        stats.append({
            "column": col,
            "mean": float(numeric_df[col].mean()),
            "median": float(numeric_df[col].median()),
            "std": float(numeric_df[col].std()),
            "min": float(numeric_df[col].min()),
            "max": float(numeric_df[col].max())
        })

    # ---------------------------
    # 🔗 CORRELATIONS (FIXED)
    # ---------------------------
    correlations = []

    if len(numeric_df.columns) > 1:
        corr_matrix = numeric_df.corr()
        seen = set()

        for col in corr_matrix.columns:
            for idx in corr_matrix.index:

                # skip self-correlation
                if col == idx:
                    continue

                # avoid duplicate pairs
                pair_key = tuple(sorted([col, idx]))

                if pair_key in seen:
                    continue

                seen.add(pair_key)

                value = corr_matrix.loc[idx, col]

                # only meaningful correlations
                if abs(value) > 0.2:
                    correlations.append({
                        "a": idx,
                        "b": col,
                        "value": round(float(value), 2)
                    })

    # strongest first
    correlations = sorted(
        correlations,
        key=lambda x: abs(x["value"]),
        reverse=True
    )[:10]

    # ---------------------------
    # 📈 TRENDS (REAL LOGIC)
    # ---------------------------
    trends = []

    for col in numeric_df.columns:
        if numeric_df[col].nunique() > 10:
            trend = "increasing" if numeric_df[col].iloc[-1] > numeric_df[col].iloc[0] else "fluctuating"

            trends.append(f"{col} shows {trend} pattern")

    if not trends:
        trends.append("No strong trends detected")

    # ---------------------------
    # 🚨 OUTLIERS (IQR METHOD)
    # ---------------------------
    outliers = []

    for col in numeric_df.columns:
        Q1 = numeric_df[col].quantile(0.25)
        Q3 = numeric_df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outlier_count = ((numeric_df[col] < lower) | (numeric_df[col] > upper)).sum()

        if outlier_count > 0:
            outliers.append({
                "column": col,
                "count": int(outlier_count)
            })

    # ---------------------------
    # RESPONSE
    # ---------------------------
    return {
        "summary": {
            "rows": len(df),
            "columns": len(df.columns),
            "missing": int(df.isnull().sum().sum()),
            "duplicates": int(df.duplicated().sum())
        },
        "stats": stats,
        "correlations": correlations,
        "trends": trends,
        "outliers": outliers
    }