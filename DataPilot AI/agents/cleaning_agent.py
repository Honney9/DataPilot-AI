# agents/cleaning_agent.py

from services.llm_service import LLMService
from utils.parser import safe_parse
from tools.data_tools import summarize_df
from services.data_service import DataService
import pandas as pd
import os
import uuid


class CleaningAgent:
    def __init__(self):
        self.llm = LLMService()
        self.data_service = DataService()

    def run(self, state: dict):

        # ---------------------------
        # VALIDATION
        # ---------------------------
        if not state.get("ingestion"):
            return {"status": "error", "message": "No ingestion data"}

        raw_data = state["ingestion"]

        if raw_data.get("status") != "success":
            return {"status": "error", "message": "Ingestion failed"}

        df = raw_data["data"]

        # ---------------------------
        # SUMMARY FOR LLM
        # ---------------------------
        summary = summarize_df(df)

        prompt = f"""
        You are a data cleaning expert.

        DATA SUMMARY:
        {summary}

        INSTRUCTIONS:
        - Suggest cleaning steps
        - Identify missing values
        - Detect duplicates
        - Suggest column fixes
        - DO NOT hallucinate

        OUTPUT FORMAT (STRICT JSON):
        {{
            "cleaning_steps": [],
            "issues_found": []
        }}
        """

        response = self.llm.generate(prompt, task="reasoning")
        parsed = safe_parse(response)

        # ---------------------------
        # 🔥 ACTUAL CLEANING LOGIC
        # ---------------------------

        df_cleaned = df.copy()
        

        # ---------------------------
        # 1. Remove duplicates
        # ---------------------------
        df_cleaned = df_cleaned.drop_duplicates()

        # ---------------------------
        # 2. Fix datatypes
        # ---------------------------
        for col in df_cleaned.columns:
            try:
                df_cleaned[col] = pd.to_numeric(df_cleaned[col])
            except:
                pass

        # ---------------------------
        # 3. Handle missing values (SMART)
        # ---------------------------
        for col in df_cleaned.columns:
            if df_cleaned[col].dtype in ["float64", "int64"]:
                df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
            else:
                if not df_cleaned[col].mode().empty:
                    df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0])
                else:
                    df_cleaned[col] = df_cleaned[col].fillna("Unknown")

        # ---------------------------
        # 4. Outlier handling (IQR)
        # ---------------------------
        for col in df_cleaned.select_dtypes(include=["int64", "float64"]).columns:
            q1 = df_cleaned[col].quantile(0.25)
            q3 = df_cleaned[col].quantile(0.75)
            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            df_cleaned[col] = df_cleaned[col].clip(lower, upper)

        # ---------------------------
        # 5. Clean strings
        # ---------------------------
        for col in df_cleaned.select_dtypes(include=["object"]).columns:
            df_cleaned[col] = df_cleaned[col].astype(str).str.strip().str.lower()

        # ---------------------------
        # 6. Date parsing
        # ---------------------------
        for col in df_cleaned.columns:
            if "date" in col.lower():
                df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors="coerce")

        # ---------------------------
        # 7. Drop highly empty columns
        # ---------------------------
        threshold = len(df_cleaned) * 0.5
        df_cleaned = df_cleaned.dropna(axis=1, thresh=threshold)

        # ---------------------------
        # 8. Normalize column names
        # ---------------------------
        df_cleaned.columns = [
            col.strip().lower().replace(" ", "_")
            for col in df_cleaned.columns
        ]
        
        state["clean_data"] = df_cleaned

        # ---------------------------
        # SAVE FILE (UNIQUE NAME)
        # ---------------------------
        file_id = str(uuid.uuid4())[:8]
        filename = f"cleaned_{file_id}.csv"

        processed_path = self.data_service.save_processed(df_cleaned, filename)

        print("🧹 Cleaning Done")

        return {
            "status": "success",
            "data": df_cleaned,
            "meta": {
                "llm_output": parsed,
                "rows": len(df_cleaned),
                "columns": list(df_cleaned.columns),
                "processed_path": processed_path
            }
        }