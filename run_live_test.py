from ai_engineering_lab.live_extractor import extract_earnings_live

sample_text = """
Apple Inc. today announced financial results for its fiscal 2024 first quarter ended December 30, 2023. 
The Company posted quarterly revenue of $119.6 billion, up 2 percent year over year, and quarterly earnings per diluted share of $2.18, up 16 percent year over year.
"We are pleased to announce that our installed base of active devices has now surpassed 2.2 billion, reaching an all-time high across all products and geographic segments," said Tim Cook, Apple's CEO.
"During the quarter, we generated nearly $40 billion of operating cash flow, and returned almost $27 billion to our shareholders," said Luca Maestri, Apple's CFO.
We expect revenue to remain flat in Q2 2024 due to supply chain constraints.
"""

print("Sending request to Gemini API...")
# This will call Gemini and enforce our Pydantic schema
extraction = extract_earnings_live(sample_text)

print("\n--- EXTRACTION RESULTS ---")
print(f"Company: {extraction.company}")
print(f"Reporting Period: {extraction.reporting_period}")
print(f"Guidance: {extraction.guidance}")
print(f"Risks: {extraction.risks}")

print("\n--- METRICS ---")
for metric in extraction.metrics:
    print(f"- {metric.name}: {metric.value} {metric.unit}")
    print(f"  Evidence: '{metric.evidence}'\n")
