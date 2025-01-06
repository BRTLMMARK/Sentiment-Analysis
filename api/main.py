import requests
import csv
from collections import defaultdict

# Google Sheets URLs (CSV export links)
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
    "Mildly, but it didn't bother me much": 1,
    "Moderately - it wasn't pleasant at times": 2,
    "Severely - it bothered me a lot": 3,
}

# Interpretation levels for each tool
interpretation_levels = {
    "PHQ-9": [
        "Minimal or none (0-4)",
        "Mild (5-9)",
        "Moderate (10-14)",
        "Moderately severe (15-19)",
        "Severe (20-27)",
    ],
    "ASQ": ["No Risk", "Low Risk", "Moderate Risk", "High Risk", "Critical Risk"],
    "BAI": [
        "Low Anxiety (0-21)",
        "Moderate Anxiety (22-35)",
        "Severe Anxiety (36+)",
    ],
}

# Tool recommendations based on severe/critical scores
recommendation_map = {
    "PHQ-9": "Depression",
    "ASQ": "Self-Harm, Suicide",
    "BAI": "Anxiety",
}

# Function to calculate interpretations
def get_interpretation(tool, score):
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

# Fetch and process data for a specific client
def analyze_client(client_name):
    results = defaultdict(dict)  # Store scores and interpretations per respondent
    client_found = False  # Flag to check if client is found

    for tool, url in sheets.items():
        response = requests.get(url)
        response.raise_for_status()
        data = response.text.splitlines()

        reader = csv.reader(data)
        header = next(reader)  # Skip header row

        for row in reader:
            name = row[-1].strip()  # Name is in the last column
            if name.lower() == client_name.lower():
                client_found = True
                responses = row[1:-2]  # Adjust columns for tool responses
                total_score = sum(response_mapping.get(r.strip(), 0) for r in responses)
                interpretation = get_interpretation(tool, total_score)

                # Store results for the client
                results[tool] = {
                    "score": total_score,
                    "interpretation": interpretation,
                }

    if not client_found:
        print(f"Error: Client '{client_name}' not found.")
        return

    # Generate recommendations
    recommendations = [
        recommendation_map[tool]
        for tool, result in results.items()
        if "Severe" in result["interpretation"] or "Critical" in result["interpretation"]
    ]

    # Output results
    print(f"\nResults for {client_name}:")
    for tool, result in results.items():
        print(f"{tool}: Score = {result['score']}, Interpretation = {result['interpretation']}")

    print("\nRecommendations:")
    if recommendations:
        print(", ".join(recommendations))
    else:
        print("No additional tools needed.")

# Example usage
analyze_client("Mark Joseph Bartolome")  # Replace with the client's name
