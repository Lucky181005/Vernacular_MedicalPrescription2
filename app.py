import json
import os
import sys
from modules.extractor import extract_prescription
from modules.translate import translate_summary
from modules.voice import generate_voice_output
from modules.history import (
    add_prescription_to_history, 
    display_history, 
    display_downloadable_files, 
    generate_accuracy_chart,
    display_statistics,
    show_prescription_details
)

DEFAULT_IMAGE_PATH = "samples/sample2.jpeg"
DEFAULT_LANGUAGE = "Telugu"

def main():
    # Usage: python app.py [image_path] [language]
    # Or: python app.py --history
    # Or: python app.py --files
    # Or: python app.py --chart
    # Or: python app.py --stats
    
    if len(sys.argv) > 1 and sys.argv[1] == "--history":
        display_history()
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == "--files":
        display_downloadable_files()
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == "--chart":
        chart_file = generate_accuracy_chart()
        if chart_file:
            print(f"✅ Accuracy chart generated: {chart_file}")
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == "--stats":
        display_statistics()
        return
    
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
        
        # Generate voice output
        print(f"\n{'─'*80}")
        print(f"🎤 GENERATING AUDIO OUTPUT ({language.upper()})")
        print(f"{'─'*80}\n")
        try:
            audio_filename = generate_voice_output(translated_summary, language)
            print(f"✅ Audio file generated successfully!")
            print(f"📁 Filename: {audio_filename}")
            print(f"🔊 You can now listen to this file using any audio player")
            
            # Save to history
            prescription_record = add_prescription_to_history(
                image_path,
                language,
                result["structured_data"],
                audio_filename
            )
            
            print(f"\n{'─'*80}")
            print("✅ PRESCRIPTION SAVED TO HISTORY")
            print(f"{'─'*80}\n")
            print(f"Prescription ID: {prescription_record['id']}")
            print(f"Accuracy Score: {prescription_record['accuracy_score']}%")
            print(f"Audio saved: {prescription_record['audio_file']}")
            
        except Exception as e:
            print(f"⚠️  Could not generate audio: {e}")
        
        print(f"\n{'='*80}\n")

    except Exception as e:
        print(f"An error occurred: {e}")


def show_menu():
    """Display available commands."""
    print(f"\n{'='*80}")
    print("📱 PRESCRIPTION PROCESSING SYSTEM - COMMANDS")
    print(f"{'='*80}\n")
    print("Process Prescription:")
    print("  python app.py <image_path> <language>")
    print("  Example: python app.py samples/sample2.jpeg Telugu\n")
    print("View History:")
    print("  python app.py --history           # View all prescriptions")
    print("  python app.py --stats             # View overall statistics")
    print("  python app.py --chart             # Generate accuracy chart\n")
    print("Download Files:")
    print("  python app.py --files             # List downloadable audio files\n")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        show_menu()
    else:
        main()
