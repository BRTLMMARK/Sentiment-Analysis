from fastapi import FastAPI
from typing import Dict
import requests
import csv

app = FastAPI()

# Google Sheets URLs
sheets = {
    "PHQ-9": "https://docs.google.com/spreadsheets/d/1D312sgbt_nOsT668iaUrccAzQ3oByUT0peXS8LYL5wg/export?format=csv",
    "ASQ": "https://docs.google.com/spreadsheets/d/1TiU8sv5cJg30ZL3fqPSmBwJJbB7h2xv1NNbKo4ZIydU/export?format=csv",
    "BAI": "https://docs.google.com/spreadsheets/d/1f7kaFuhCv6S_eX4EuIrlhZFDR7W5MhQpJSXHznlpJEk/export?format=csv",
}

# Mapping textual responses to numerical values
response_mapping = {
    "Not at all": 0,
    "Several Days": 1,
    "More than half the days": 2,
    "Nearly every day": 3,
}

# Interpretation logic
def get_interpretation(tool: str, score: int) -> str:
    if tool == "PHQ-9":
        if score <= 4:
            return "Minimal or none (0-4)"
        elif score <= 9:
            return "Mild (5-9)"
        elif score <= 14:
            return "Moderate (10-14)"
        elif score <= 19:
            return "Moderately severe (15-19)"
        else:
            return "Severe (20-27)"
    elif tool == "ASQ":
        if score <= 5:
            return "No Risk"
        elif score <= 10:
            return "Low Risk"
        elif score <= 15:
            return "Moderate Risk"
        elif score <= 20:
            return "High Risk"
        else:
            return "Critical Risk"
    elif tool == "BAI":
        if score <= 21:
            return "Low Anxiety (0-21)"
        elif score <= 35:
            return "Moderate Anxiety (22-35)"
        else:
            return "Severe Anxiety (36+)"
    return "Unknown"

@app.get("/results/{client_name}")
async def analyze_client(client_name: str) -> Dict[str, Dict[str, str]]:
    results = {}
    for tool, url in sheets.items():
        response = requests.get(url)
        response.raise_for_status()
        data = csv.reader(response.text.splitlines())
        header = next(data)

        for row in data:
            name = row[-1].strip()  # Name is in the last column
            if name.lower() == client_name.lower():
                responses = row[1:-2]  # Adjust columns based on CSV format
                total_score = sum(response_mapping.get(r.strip(), 0) for r in responses)
                results[tool] = {
                    "score": total_score,
                    "interpretation": get_interpretation(tool, total_score),
                }
    return results
