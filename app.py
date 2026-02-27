import json
import os
import sys
from modules.extractor import extract_prescription
from modules.translate import translate_summary

DEFAULT_IMAGE_PATH = "samples/sample2.jpeg"
DEFAULT_LANGUAGE = "Telugu"

def main():
    # Usage: python app.py [image_path] [language]
    image_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_IMAGE_PATH
    language = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_LANGUAGE

    # Check if file exists before processing
    if not os.path.exists(image_path):
        print(f"Error: File not found at {image_path}")
        return

    print(f"\n{'='*80}")
    print(f"Processing prescription: {image_path}...")
    print(f"{'='*80}\n")

    try:
        # Call the extractor
        result = extract_prescription(image_path)

        # Print structured data
        print(f"\n{'─'*80}")
        print("💊 STRUCTURED MEDICINE DATA")
        print(f"{'─'*80}\n")
        
        for idx, med in enumerate(result["structured_data"], 1):
            print(f"{idx}. {med['medicine_name']}")
            print(f"   Dosage: {med['dosage_pattern']} | Frequency: {med['frequency']} | Duration: {med['duration']}")
            print(f"   Food: {med['food_instruction']} | Confidence: {med['confidence_note']}")
            if med['special_notes'] != "unclear":
                print(f"   Notes: {med['special_notes']}")
            print()
        
        # Print patient summary
        print(f"{'─'*80}")
        print("📝 PATIENT SUMMARY (ENGLISH)")
        print(f"{'─'*80}\n")
        patient_summary = result.get("patient_summary", "")
        print(patient_summary)
        
        # Print translated summary
        print(f"\n{'─'*80}")
        print(f"🌍 TRANSLATED SUMMARY ({language.upper()})")
        print(f"{'─'*80}\n")
        translated_summary = translate_summary(patient_summary, language)
        print(translated_summary)
        
        print(f"\n{'='*80}\n")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
