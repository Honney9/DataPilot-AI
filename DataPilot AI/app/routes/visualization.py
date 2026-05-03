from fastapi import APIRouter, Query, Body
from memory.session_memory import memory
import pandas as pd
import numpy as np

router = APIRouter(prefix="/visualizations")


@router.get("")
def get_visualizations(session_id: str = Query(...)):

    session = memory.get(session_id)
    if not session:
        return []

    state = session.get("state")
    if not state:
        return []

    df = state.get("data")
    if df is None:
        return []

    charts = []

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) >= 2:
        charts.append({
            "id": "chart1",
            "title": f"{numeric_cols[0]} vs {numeric_cols[1]}",
            "type": "scatter",
            "x": numeric_cols[0],
            "y": numeric_cols[1],
            "data": df[[numeric_cols[0], numeric_cols[1]]]
                .head(100)
                .replace([np.inf, -np.inf], None)
                .to_dict(orient="records")
        })

    return charts


@router.post("/custom")
def custom_visualization(session_id: str = Query(...), payload: dict = Body(...)):

    import numpy as np

    session = memory.get(session_id)
    state = session.get("state")
    df = state.get("data")

    x = payload.get("x")
    y = payload.get("y")
    chart_type = payload.get("type", "bar")

    if x not in df.columns or y not in df.columns:
        return {"error": "Invalid columns"}

    df = df[[x, y]].replace([np.inf, -np.inf], np.nan).dropna()

    x_is_num = pd.api.types.is_numeric_dtype(df[x])
    y_is_num = pd.api.types.is_numeric_dtype(df[y])

    # ✅ PIE → always aggregate counts
    if chart_type == "pie":
        grouped = df.groupby(x).size().reset_index(name="value")
        data = grouped.head(50)

        return {
            "id": f"{x}-{chart_type}",
            "title": f"{x} distribution",
            "type": "pie",
            "x": x,
            "y": "value",
            "data": data.to_dict(orient="records")
        }

    # ✅ categorical vs categorical
    if not x_is_num and not y_is_num:
        grouped = df.groupby([x, y]).size().reset_index(name="count")
        data = grouped.head(50)

        return {
            "id": f"{x}-{y}-{chart_type}",
            "title": f"{y} vs {x}",
            "type": chart_type,
            "x": x,
            "y": "count",
            "data": data.to_dict(orient="records")
        }

    # ✅ categorical vs numeric
    if not x_is_num and y_is_num:
        grouped = df.groupby(x)[y].mean().reset_index()
        data = grouped.head(50)

        return {
            "id": f"{x}-{y}-{chart_type}",
            "title": f"Avg {y} by {x}",
            "type": chart_type,
            "x": x,
            "y": y,
            "data": data.to_dict(orient="records")
        }

    # ✅ numeric vs numeric → scatter
    if x_is_num and y_is_num:
        data = df[[x, y]].head(100)

        return {
            "id": f"{x}-{y}-scatter",
            "title": f"{y} vs {x}",
            "type": "scatter",
            "x": x,
            "y": y,
            "data": data.to_dict(orient="records")
        }

    return {"error": "Unsupported combination"}