import pandas as pd
import json

csv_file = "data/_bis_standards - Sheet1.csv"
json_file = "data/bis_standards.json"

df = pd.read_csv(csv_file)

data = df.to_dict(orient="records")

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("CSV converted to JSON successfully!")
print("Number of standards:", len(data))