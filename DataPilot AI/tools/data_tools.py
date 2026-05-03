def summarize_df(df):
    return {
        "columns": list(df.columns),
        "shape": df.shape,
        "missing": df.isnull().sum().to_dict(),
        "sample": df.head(3).to_dict()
    }