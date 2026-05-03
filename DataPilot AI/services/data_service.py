# services/data_service.py

import pandas as pd
import os


class DataService:

    def load_file(self, file_path: str):
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".csv":
            return pd.read_csv(file_path)

        elif ext in [".xlsx", ".xls"]:
            return pd.read_excel(file_path)

        else:
            raise ValueError("Unsupported file type")

    def save_processed(self, df, filename="processed.csv"):
        os.makedirs("data/processed", exist_ok=True)

        path = f"data/processed/{filename}"
        df.to_csv(path, index=False)

        return path

    def get_summary(self, df):
        return {
            "columns": list(df.columns),
            "shape": df.shape,
            "missing": df.isnull().sum().to_dict()
        }