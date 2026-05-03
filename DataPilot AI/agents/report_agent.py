# agents/report_agent.py

from services.llm_service import LLMService
from tools.report_tools import generate_pdf
from datetime import datetime


class ReportAgent:
    def __init__(self):
        self.llm = LLMService()

    def run(self, state: dict, session_id: str):
        print("🚀 ReportAgent started")
        print("STATE KEYS:", state.keys())

        df = state.get("data")

        if df is None:
            return {"status": "error", "message": "No dataset found"}

        # ✅ ALWAYS BUILD ANALYSIS FROM DATA (NO DEPENDENCY)
        analysis = f"""
Dataset Summary:
- Rows: {len(df)}
- Columns: {len(df.columns)}
- Column Names: {list(df.columns)}
- Missing Values: {df.isnull().sum().sum()}
"""

        # ✅ SIMPLE INSIGHTS (can upgrade later)
        insights = "Initial analysis completed. Patterns will be derived from dataset."

        print("🧠 Calling LLM...")

        prompt = f"""
You are a senior data analyst creating a professional report.

DATA ANALYSIS:
{analysis}

INSIGHTS:
{insights}

TASK:
Generate a structured, high-quality report.

STRICT FORMAT:

TITLE: AI Data Analysis Report

SECTION: Overview
Write a clear summary of the dataset.

SECTION: Data Quality
Explain missing values, issues.

SECTION: Key Findings
Highlight important patterns.

SECTION: Insights
Explain trends and relationships.

SECTION: Recommendations
Give actionable suggestions.

RULES:
- Be specific
- No generic text
- Use data context
"""

        # ✅ CALL LLM
        response = self.llm.generate(prompt, task="heavy")

        print("===== RAW LLM OUTPUT =====")
        print(response)
        print("==========================")

        # ✅ PARSE OUTPUT
        title, sections = self.parse_report(response)

        # fallback if parsing fails
        if not sections:
            sections = [{
                "title": "Overview",
                "body": response
            }]

        report = {
            "title": title,
            "generated_at": datetime.utcnow().isoformat(),
            "sections": sections
        }

        # ✅ GENERATE PDF
        pdf_path = generate_pdf(report, session_id)

        print("📄 Report Generated")

        return {
            "status": "success",
            "data": report,
            "meta": {
                "pdf_path": pdf_path
            }
        }

    def parse_report(self, text):
        title = "AI Data Analysis Report"
        sections = []

        parts = text.split("SECTION:")

        for part in parts:
            part = part.strip()

            if part.startswith("TITLE:"):
                title = part.replace("TITLE:", "").strip()

            elif part:
                lines = part.split("\n")
                sec_title = lines[0].strip()
                body = "\n".join(lines[1:]).strip()

                if sec_title and body:
                    sections.append({
                        "title": sec_title,
                        "body": body
                    })

        return title, sections