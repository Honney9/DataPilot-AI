# tools/viz_tools.py

import matplotlib.pyplot as plt
import seaborn as sns
import os


def generate_smart_charts(df):

    os.makedirs("outputs/charts", exist_ok=True)
    chart_paths = []

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    categorical_cols = df.select_dtypes(include=["object"]).columns

    # ---------------------------
    # 1. NUMERIC DISTRIBUTION
    # ---------------------------
    for col in numeric_cols[:2]:
        plt.figure(figsize=(10, 5))
        sns.histplot(df[col], kde=True)
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.xticks(rotation=30)

        path = f"outputs/charts/{col}_hist.png"
        plt.tight_layout()
        plt.savefig(path)
        plt.close()

        chart_paths.append(path)

    # ---------------------------
    # 2. CATEGORICAL COUNT
    # ---------------------------
    for col in categorical_cols[:2]:

        # avoid too many labels
        if df[col].nunique() > 20:
            continue

        plt.figure(figsize=(12, 6))
        sns.countplot(x=df[col])

        plt.title(f"{col} Distribution")
        plt.xlabel(col)
        plt.ylabel("Count")
        plt.xticks(rotation=45)

        path = f"outputs/charts/{col}_count.png"
        plt.tight_layout()
        plt.savefig(path)
        plt.close()

        chart_paths.append(path)

    # ---------------------------
    # 3. SCATTER (if possible)
    # ---------------------------
    if len(numeric_cols) >= 2:
        x, y = numeric_cols[:2]

        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=df[x], y=df[y])

        plt.title(f"{x} vs {y}")
        plt.xlabel(x)
        plt.ylabel(y)

        path = f"outputs/charts/{x}_{y}_scatter.png"
        plt.tight_layout()
        plt.savefig(path)
        plt.close()

        chart_paths.append(path)

    return chart_paths