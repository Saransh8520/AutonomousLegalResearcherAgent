import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def is_legal_query(query):
    prompt = f"""
You are a strict legal domain classifier.

Classify the following query strictly as:

LEGAL
or
NON_LEGAL

Only respond with exactly one word.
No explanation.

Query:
{query}
"""

    response = model.generate_content(prompt)

    result = response.text.strip().upper()

    # Strict equality check
    if result == "LEGAL":
        return True
    else:
        return False