# agents/insight_agent.py

from services.llm_service import LLMService
from utils.parser import safe_parse


class InsightAgent:
    def __init__(self):
        self.llm = LLMService()

    def run(self, state: dict):

        if not state.get("analysis"):
            return {"status": "error", "message": "No analysis data"}

        analysis = state["analysis"]["data"]

        prompt = f"""
        You are a business intelligence expert.

        ANALYSIS:
        {analysis}

        TASK:
        Generate actionable insights.

        INSTRUCTIONS:
        - Focus on cause-effect relationships
        - Avoid generic statements
        - Be specific and data-driven

        OUTPUT FORMAT (STRICT JSON):
        {{
            "insights": [
                {{
                    "observation": "",
                    "explanation": "",
                    "impact": ""
                }}
            ]
        }}
        """

        response = self.llm.generate(prompt, task="reasoning")
        parsed = safe_parse(response)

        print("🧠 Insights Generated")

        return {
            "status": "success",
            "data": parsed,
            "meta": {
                "raw": response,
            }
        }