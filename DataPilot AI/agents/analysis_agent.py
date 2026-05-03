# agents/analysis_agent.py

from services.llm_service import LLMService
from utils.parser import safe_parse
from tools.data_tools import summarize_df


class AnalysisAgent:
    def __init__(self):
        self.llm = LLMService()

    def run(self, state: dict):

        if not state.get("cleaning"):
            return {"status": "error", "message": "No cleaned data"}

        clean_data = state["cleaning"]
        df = clean_data["data"]

        # 🔥 Better summary
        summary = summarize_df(df)

        prompt = f"""
        You are a senior data analyst.

        DATA SUMMARY:
        {summary}

        TASK:
        Perform EDA.

        INSTRUCTIONS:
        - Identify trends
        - Detect correlations
        - Highlight anomalies
        - DO NOT hallucinate

        OUTPUT FORMAT (STRICT JSON):
        {{
            "key_trends": [],
            "correlations": [],
            "anomalies": []
        }}
        """

        response = self.llm.generate(prompt, task="reasoning")

        parsed = safe_parse(response)

        print("📊 Analysis Done")

        return {
            "status": "success",
            "data": parsed,
            "meta": {
                "summary_used": summary
            }
        }