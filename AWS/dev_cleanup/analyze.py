import pandas as pd

df = pd.read_excel('data.xlsx')

for column in df.columns:
    top5 = df[column].value_counts().head(5)
    print(f"Top 5 elements in column '{column}':\n{top5}\n")
