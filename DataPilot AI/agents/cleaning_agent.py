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

        # 1. Remove duplicates
        df_cleaned = df_cleaned.drop_duplicates()

        # 2. Handle missing values
        for col in df_cleaned.columns:
            if df_cleaned[col].dtype in ["float64", "int64"]:
                df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
            else:
                df_cleaned[col] = df_cleaned[col].fillna("Unknown")

        # 3. Standardize column names
        df_cleaned.columns = [col.strip().lower().replace(" ", "_") for col in df_cleaned.columns]

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