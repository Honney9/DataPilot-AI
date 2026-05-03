# agents/visualization_agent.py

from tools.viz_tools import generate_smart_charts


class VisualizationAgent:
    def run(self, state: dict):

        if not state.get("cleaning"):
            return {"status": "error", "message": "No cleaned data"}

        df = state["cleaning"]["data"]

        # 🔥 RULE-BASED SMART CHARTS (NO LLM NEEDED)
        chart_paths = generate_smart_charts(df)

        print("📊 Smart Charts Generated")

        return {
            "status": "success",
            "data": None,
            "meta": {
                "chart_paths": chart_paths
            }
        }