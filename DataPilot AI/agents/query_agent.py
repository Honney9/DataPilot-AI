# agents/query_agent.py

from services.llm_service import LLMService


class QueryAgent:
    def __init__(self):
        self.llm = LLMService()

    def run(self, state: dict):

        print("💬 QueryAgent started")
        print("STATE KEYS:", state.keys())

        df = state.get("data")
        query = state.get("user_query")

        # ✅ Safety checks
        if df is None:
            return {
                "status": "error",
                "data": "No dataset available. Please upload a file first."
            }

        if not query:
            return {
                "status": "error",
                "data": "No query provided"
            }

        # ---------------------------
        # 🔥 SMART DATA CONTEXT
        # ---------------------------
        preview = df.head(10).to_dict(orient="records")
        columns = list(df.columns)

        analysis = state.get("analysis", {}).get("data", "")
        insights = state.get("insight", {}).get("data", "")

        # ---------------------------
        # PROMPT
        # ---------------------------
        prompt = f"""
    You are a data analyst.

    AVAILABLE COLUMNS:
    {columns}

    DATA SAMPLE:
    {preview}

    ANALYSIS:
    {analysis}

    INSIGHTS:
    {insights}

    USER QUESTION:
    {query}

    RULES:
    - Answer ONLY using the dataset
    - Do NOT hallucinate
    - If data is missing → say "Not enough data"
    - Be short and precise
    - If numeric → calculate correctly

    ANSWER:
    """

        response = self.llm.generate(prompt, task="fast")

        print("===== LLM RESPONSE =====")
        print(response)
        print("========================")

        return {
            "status": "success",
            "data": response.strip(),
            "meta": {
                "query": query
            }
        }