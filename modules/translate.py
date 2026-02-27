from deep_translator import GoogleTranslator

LANGUAGE_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Bengali": "bn",
    "Odia": "or",
    "Urdu": "ur",
    "Assamese": "as",
    "Nepali": "ne"
}

def translate_summary(summary_text, target_language):
    """
    Translates simplified English prescription summary
    into selected Indian language.
    """

    if target_language not in LANGUAGE_MAP:
        raise ValueError("Unsupported language")

    if target_language == "English":
        return summary_text

    translated_text = GoogleTranslator(
        source="auto",
        target=LANGUAGE_MAP[target_language]
    ).translate(summary_text)

    return translated_text
