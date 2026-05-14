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
You are a senior data analyst.

Create a PROFESSIONAL, DETAILED, STRUCTURED report.

STRICT RULES:
- NO markdown symbols (no ##, no *)
- Use clear plain text
- Be data-driven (use numbers from analysis)
- Be specific, not generic
- Write like a real business report

OUTPUT FORMAT (STRICT):

TITLE: AI Data Analysis Report

SECTION: Overview
<detailed paragraph>

SECTION: Data Quality
<missing values, duplicates, issues>

SECTION: Statistical Summary
<mean, median, std insights>

SECTION: Key Findings
<data-driven observations>

SECTION: Insights
<patterns, correlations explained>

SECTION: Recommendations
<actionable business suggestions>

DATA ANALYSIS:
{analysis}

INSIGHTS:
{insights}
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
        import re

        title = "AI Data Analysis Report"
        sections = []

        # Extract title
        title_match = re.search(r"TITLE:\s*(.*)", text)
        if title_match:
            title = title_match.group(1).strip()

        # Extract sections
        section_matches = re.findall(
            r"SECTION:\s*(.*?)\n(.*?)(?=SECTION:|$)",
            text,
            re.DOTALL
        )

        for sec_title, sec_body in section_matches:
            sections.append({
                "title": sec_title.strip(),
                "body": sec_body.strip()
            })

        return title, sections