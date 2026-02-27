import os
import json
from dotenv import load_dotenv
from google import genai
from PIL import Image

_client = None


PROMPT = """
You are a medical prescription processing AI.

Analyze the prescription image carefully and extract ALL medicines.

For EACH medicine extract:

- medicine_name (exact as written)
- dosage_pattern (example: 1-0-1 or 2 puffs)
- frequency (convert OD, BD, TDS only if clearly written)
- duration
- food_instruction
- special_notes
- confidence_note (High / Medium / Low based on clarity)

RULES:
- Do NOT guess missing information.
- If unclear, write "unclear".
- Do NOT modify dosage.
- Do NOT invent medicines.
- Extract every medicine listed.

After structured extraction, generate a patient-friendly summary in EXACT format:
Start with: "You have been prescribed the following medicines:"
Then create a numbered list with this exact format for each medicine:
[Number]. [MEDICINE_NAME]: [Clear instruction with dosage, timing, food instruction, and duration]

Format example:
1. TAB. SOMPRAZ 40MG: Take 1 tablet before morning meal and 1 tablet before night meal, every day for 1 month.
2. SYP. DOLCID SYP: Take 15 ML before food at 9 AM and 15 ML before food at 9 PM, every day for 1 month.
3. GEL NANOFASST: Apply once in the morning and once in the night to the affected area, as needed, until your next visit.

For each medicine:
- Use "Take [X] tablet(s)" or "Take [X] ML" or "Apply"
- Mention the dosage pattern clearly (e.g., "1 tablet", "15 ML")
- Include timing if available (e.g., "at 9 AM", "at 10 PM")
- Include food instruction (e.g., "before food", "after food")
- Include frequency and duration

Return ONLY valid JSON in this format:

{
  "structured_data": [
    {
      "medicine_name": "",
      "dosage_pattern": "",
      "frequency": "",
      "duration": "",
      "food_instruction": "",
      "special_notes": "",
      "confidence_note": ""
    }
  ],
  "patient_summary": ""
}
"""


def extract_prescription(image_path):
    """
    Takes image path and returns structured JSON + summary.
    """
    global _client

    if _client is None:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("API key not found. Check your .env file.")

        _client = genai.Client(api_key=api_key)

    img = Image.open(image_path)

    response = _client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[PROMPT, img],
        config={
            "temperature": 0.1,
            "max_output_tokens": 4096,
        }
    )

    raw_text = response.text.strip()

    # Sometimes Gemini wraps output in ```json
    if raw_text.startswith("```"):
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        parsed_json = json.loads(raw_text)
    except json.JSONDecodeError:
        # Fallback: extract outermost JSON object if model added extra text.
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("Model did not return valid JSON.")
        parsed_json = json.loads(raw_text[start : end + 1])

    return parsed_json

