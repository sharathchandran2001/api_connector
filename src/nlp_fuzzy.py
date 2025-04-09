from rapidfuzz import process, fuzz

RULES = ["rule123", "rule456", "performance_test", "integration_check"]

def extract_rule(text: str) -> str:
    match, score, _ = process.extractOne(text, RULES, scorer=fuzz.WRatio)
    return match
