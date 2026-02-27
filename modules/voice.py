from gtts import gTTS
import os
import re

LANGUAGE_CODE_MAP = {
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


def preprocess_text_for_tts(text):
    """
    Preprocesses text to make it more suitable for text-to-speech.
    Converts ALL CAPS abbreviations and medicine names to Title Case.
    """
    # Convert TAB. to Tab
    text = re.sub(r'\bTAB\.\s+', 'Tab ', text)
    
    # Convert medicine names from ALL CAPS to Title Case
    # Pattern: Anything after "Tab " that is in ALL CAPS until a number or space-number
    def capitalize_medicine(match):
        medicine_name = match.group(1)
        # Convert to Title Case (first letter uppercase, rest lowercase)
        return 'Tab ' + ' '.join(word.capitalize() for word in medicine_name.split())
    
    text = re.sub(r'Tab\s+([A-Z\s]+?)\s+(\d+)', capitalize_medicine, text)
    
    # Convert SYP. to Syrup
    text = re.sub(r'\bSYP\.\s+', 'Syrup ', text)
    
    # Convert GEL to Gel
    text = re.sub(r'\bGEL\s+', 'Gel ', text)
    
    return text


def generate_voice_output(text, language, output_filename=None):
    """
    Converts text to speech in the specified language.
    
    Args:
        text: The text to convert to speech
        language: The language name (e.g., "Telugu", "Hindi")
        output_filename: Optional custom filename for the audio file
    
    Returns:
        The filename of the generated audio file
    """
    
    if language not in LANGUAGE_CODE_MAP:
        raise ValueError(f"Unsupported language: {language}")
    
    language_code = LANGUAGE_CODE_MAP[language]
    
    # Preprocess text for better TTS output
    processed_text = preprocess_text_for_tts(text)
    
    # Generate default filename if not provided
    if output_filename is None:
        output_filename = f"prescription_audio_{language}.mp3"
    
    try:
        # Create gTTS object
        tts = gTTS(text=processed_text, lang=language_code, slow=False)
        
        # Save the audio file
        tts.save(output_filename)
        
        return output_filename
    
    except Exception as e:
        raise Exception(f"Error generating voice output: {str(e)}")
