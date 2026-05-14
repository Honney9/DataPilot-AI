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
        summary_stats = df.describe(include="all").to_dict()
        missing = df.isnull().sum().to_dict()
        columns = list(df.columns)

        analysis = state.get("analysis", {}).get("data", "")
        insights = state.get("insight", {}).get("data", "")

        # ---------------------------
        # PROMPT
        # ---------------------------
        prompt = f"""
    You are a senior data analyst.

    AVAILABLE COLUMNS:
    {columns}

    DATA SAMPLE:
    {preview}

    DATA SUMMARY:
    {summary_stats}

    MISSING VALUES:
    {missing}

    ANALYSIS:
    {analysis}

    INSIGHTS:
    {insights}

    USER QUESTION:
    {query}

    Return ONLY markdown in this structure:

    ## 📊 Overview
    (Explain dataset clearly)

    ## 📈 Key Statistics
    (Bullet points with real numbers, mean, ranges, distributions)

    ## 🔍 Patterns & Trends
    (Relationships, correlations, behavior patterns)

    ## 🧠 Insights
    (Deep reasoning, not obvious statements)

    ## ⚠️ Observations
    (Data issues, anomalies, missing values)

    ## ✅ Recommendations
    (Actionable suggestions based ONLY on data)

    ---------------------------
    RULES:
    - Use ONLY given dataset
    - DO NOT hallucinate
    - Be detailed but clear
    - Use numbers wherever possible
    - Avoid generic statements
    - Keep formatting clean (no random symbols like ## inside text)
    - Do NOT return anything outside markdown

    ANSWER:
    """

        response = self.llm.generate(prompt, task="reasoning")

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