# agents/ingestion_agent.py

import os
import pandas as pd
from services.data_service import DataService


class IngestionAgent:
    def __init__(self):
        self.data_service = DataService()

    def run(self, state: dict):

        file_path = state.get("file_path")

        if not file_path:
            return {"status": "error", "message": "No file provided"}

        if not os.path.exists(file_path):
            return {"status": "error", "message": "File not found"}

        # ---------------------------
        # FILE METADATA
        # ---------------------------
        file_size = os.path.getsize(file_path)
        file_ext = os.path.splitext(file_path)[1].lower()

        if file_size > 10 * 1024 * 1024:
            return {"status": "error", "message": "File too large (>10MB)"}

        try:
            # ---------------------------
            # LOAD FILE (SMART LOADING)
            # ---------------------------
            if file_ext == ".csv":
                df = pd.read_csv(file_path)

            elif file_ext in [".xlsx", ".xls"]:
                try:
                    # 🔥 Try reading first sheet
                    df = pd.read_excel(file_path, engine="openpyxl")

                except ImportError:
                    return {
                        "status": "error",
                        "message": "Excel support missing. Run: pip install openpyxl"
                    }

                except Exception:
                    # 🔥 Handle multi-sheet fallback
                    excel_file = pd.ExcelFile(file_path)
                    first_sheet = excel_file.sheet_names[0]
                    df = excel_file.parse(first_sheet)

            else:
                return {"status": "error", "message": "Unsupported file type"}

        except Exception as e:
            return {"status": "error", "message": f"File read error: {str(e)}"}

        # ---------------------------
        # VALIDATION
        # ---------------------------
        if df.empty:
            return {"status": "error", "message": "File is empty"}

        # ---------------------------
        # MEMORY SAFETY (LARGE DATA)
        # ---------------------------
        if len(df) > 100000:
            df = df.sample(100000)
            print("⚠️ Large dataset detected → sampling applied")

        # ---------------------------
        # SUMMARY
        # ---------------------------
        summary = self.data_service.get_summary(df)

        # ---------------------------
        # 🔥 ENHANCED PREVIEW
        # ---------------------------
        preview = df.head(5).to_dict()

        # 🔥 Column classification (VERY USEFUL)
        column_types = {
            "numeric": list(df.select_dtypes(include=["number"]).columns),
            "categorical": list(df.select_dtypes(include=["object"]).columns),
            "datetime": list(df.select_dtypes(include=["datetime"]).columns),
        }

        print("📥 Ingestion Complete")

        return {
            "status": "success",
            "data": df,
            "meta": {
                "summary": summary,
                "preview": preview,
                "column_types": column_types,
                "file_info": {
                    "name": os.path.basename(file_path),
                    "size_kb": round(file_size / 1024, 2),
                    "type": file_ext
                }
            }
        }