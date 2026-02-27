import json
import sys
from modules.translate import translate_summary
from modules.voice import generate_voice_output
from modules.history import (
    add_prescription_to_history,
    display_history,
    display_statistics,
    display_downloadable_files,
    generate_accuracy_chart
)

# Sample prescription data (simulating API response)
sample_prescription = {
    "structured_data": [
        {
            "medicine_name": "TAB. SOMPRAZ 40MG",
            "dosage_pattern": "1-0-1",
            "frequency": "every day",
            "duration": "1 month",
            "food_instruction": "before food",
            "special_notes": "Take 1 before morning meal, 1 before night meal",
            "confidence_note": "High"
        },
        {
            "medicine_name": "TAB. DILNIP T 40MG",
            "dosage_pattern": "1-0-0",
            "frequency": "every day",
            "duration": "1 month",
            "food_instruction": "after food",
            "special_notes": "Take 1 after morning meal at 9 AM",
            "confidence_note": "High"
        },
        {
            "medicine_name": "TAB. ROZAVEL EZ",
            "dosage_pattern": "0-0-1",
            "frequency": "every day",
            "duration": "1 month",
            "food_instruction": "after food",
            "special_notes": "Take 1 after night meal at 9 PM",
            "confidence_note": "High"
        },
        {
            "medicine_name": "TAB. MYOSPAS",
            "dosage_pattern": "1-0-1",
            "frequency": "every day",
            "duration": "3 days",
            "food_instruction": "after food",
            "special_notes": "Take 1 after morning meal at 10 AM, 1 after night meal at 10 PM",
            "confidence_note": "High"
        },
        {
            "medicine_name": "SYP. DOLCID SYP",
            "dosage_pattern": "1-0-1",
            "frequency": "every day",
            "duration": "1 month",
            "food_instruction": "before food",
            "special_notes": "Take 15 ML before morning meal at 9 AM, 15 ML before night meal at 9 PM",
            "confidence_note": "High"
        },
        {
            "medicine_name": "TAB. D-RISE 60K",
            "dosage_pattern": "0-0-1",
            "frequency": "monthly",
            "duration": "8 weeks",
            "food_instruction": "after food",
            "special_notes": "Take 1 after night meal at 9 PM",
            "confidence_note": "High"
        },
        {
            "medicine_name": "GEL NANOFASST",
            "dosage_pattern": "1-0-1",
            "frequency": "as needed",
            "duration": "Till Next Visit",
            "food_instruction": "unclear",
            "special_notes": "Apply in the morning for affected area, in the night for affected area (SOS)",
            "confidence_note": "High"
        }
    ],
    "patient_summary": """You have been prescribed the following medicines:
1. TAB. SOMPRAZ 40MG: Take 1 tablet before morning meal and 1 tablet before night meal, every day for 1 month.
2. TAB. DILNIP T 40MG: Take 1 tablet after morning meal at 9 AM, every day for 1 month.
3. TAB. ROZAVEL EZ: Take 1 tablet after night meal at 9 PM, every day for 1 month.
4. TAB. MYOSPAS: Take 1 tablet after morning meal at 10 AM and 1 tablet after night meal at 10 PM, every day for 3 days.
5. SYP. DOLCID SYP: Take 15 ML before morning meal at 9 AM and 15 ML before night meal at 9 PM, every day for 1 month.
6. TAB. D-RISE 60K: Take 1 tablet after night meal at 9 PM, monthly for 8 weeks.
7. GEL NANOFASST: Apply once in the morning and once in the night to the affected area, as needed, until your next visit."""
}

def test_workflow(language="Telugu"):
    
    print(f"\n{'='*80}")
    print(f"PRESCRIPTION PROCESSING - TEST WORKFLOW")
    print(f"Language: {language}")
    print(f"{'='*80}\n")
    
    # Display structured data
    print(f"{'─'*80}")
    print("💊 STRUCTURED MEDICINE DATA")
    print(f"{'─'*80}\n")
    
    for idx, med in enumerate(sample_prescription["structured_data"], 1):
        print(f"{idx}. {med['medicine_name']}")
        print(f"   Dosage: {med['dosage_pattern']} | Frequency: {med['frequency']} | Duration: {med['duration']}")
        print(f"   Food: {med['food_instruction']} | Confidence: {med['confidence_note']}")
        if med['special_notes'] != "unclear":
            print(f"   Notes: {med['special_notes']}")
        print()
    
    # Display patient summary
    print(f"{'─'*80}")
    print("📝 PATIENT SUMMARY (ENGLISH)")
    print(f"{'─'*80}\n")
    patient_summary = sample_prescription.get("patient_summary", "")
    print(patient_summary)
    
    # Translate summary
    print(f"\n{'─'*80}")
    print(f"🌍 TRANSLATED SUMMARY ({language.upper()})")
    print(f"{'─'*80}\n")
    try:
        translated_summary = translate_summary(patient_summary, language)
        print(translated_summary)
    except Exception as e:
        print(f"Error translating: {e}")
        return
    
    # Generate voice output
    print(f"\n{'─'*80}")
    print(f"🎤 GENERATING AUDIO OUTPUT ({language.upper()})")
    print(f"{'─'*80}\n")
    try:
        audio_filename = generate_voice_output(translated_summary, language)
        print(f"✅ Audio file generated successfully!")
        print(f"📁 Filename: {audio_filename}")
        print(f"🔊 You can now listen to this file using any audio player")
        import os
        file_size = os.path.getsize(audio_filename)
        print(f"📊 File size: {file_size:,} bytes ({file_size/1024:.2f} KB)")
        
        # Save to history
        prescription_record = add_prescription_to_history(
            "sample_prescription.jpg",
            language,
            sample_prescription["structured_data"],
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

if __name__ == "__main__":
    # Handle special commands
    if len(sys.argv) > 1:
        if sys.argv[1] == "--history":
            display_history()
            sys.exit()
        elif sys.argv[1] == "--stats":
            display_statistics()
            sys.exit()
        elif sys.argv[1] == "--files":
            display_downloadable_files()
            sys.exit()
        elif sys.argv[1] == "--chart":
            chart_file = generate_accuracy_chart()
            if chart_file:
                print(f"\n✅ Accuracy chart saved: {chart_file}\n")
            sys.exit()
        else:
            language = sys.argv[1]
    else:
        language = "Telugu"
    
    test_workflow(language)
