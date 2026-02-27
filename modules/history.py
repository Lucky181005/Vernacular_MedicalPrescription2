import json
import os
import shutil
from datetime import datetime
import matplotlib.pyplot as plt
from tabulate import tabulate

HISTORY_FILE = "prescription_history.json"
AUDIO_FOLDER = "audio_files"
CHART_FOLDER = "charts"


def ensure_folders():
    """Create necessary folders if they don't exist."""
    if not os.path.exists(AUDIO_FOLDER):
        os.makedirs(AUDIO_FOLDER)
    if not os.path.exists(CHART_FOLDER):
        os.makedirs(CHART_FOLDER)


def load_history():
    """Load prescription history from JSON file."""
    ensure_folders()
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"prescriptions": []}


def save_history(history):
    """Save prescription history to JSON file."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def add_prescription_to_history(image_path, language, medicines_data, audio_filename):
    """
    Add a new prescription to history.
    
    Args:
        image_path: Path to the prescription image
        language: Language of translation
        medicines_data: List of medicine dictionaries
        audio_filename: Path to the generated audio file
    """
    ensure_folders()
    
    history = load_history()
    
    # Calculate average confidence
    confidences = []
    for med in medicines_data:
        if med['confidence_note'].lower() == 'high':
            confidences.append(100)
        elif med['confidence_note'].lower() == 'medium':
            confidences.append(75)
        else:
            confidences.append(50)
    
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    
    # Move audio file to organized folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    organized_audio_path = os.path.join(AUDIO_FOLDER, f"{timestamp}_{language}.mp3")
    
    if os.path.exists(audio_filename):
        shutil.copy(audio_filename, organized_audio_path)
    
    # Create prescription record
    prescription_record = {
        "id": timestamp,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "image_file": os.path.basename(image_path),
        "language": language,
        "medicine_count": len(medicines_data),
        "medicines": [
            {
                "name": med['medicine_name'],
                "dosage": med['dosage_pattern'],
                "frequency": med['frequency'],
                "duration": med['duration'],
                "confidence": med['confidence_note']
            }
            for med in medicines_data
        ],
        "accuracy_score": round(avg_confidence, 2),
        "audio_file": organized_audio_path,
        "audio_available": os.path.exists(organized_audio_path)
    }
    
    history["prescriptions"].append(prescription_record)
    save_history(history)
    
    return prescription_record


def display_history():
    """Display prescription history in a formatted table."""
    history = load_history()
    prescriptions = history.get("prescriptions", [])
    
    if not prescriptions:
        print("\n" + "="*80)
        print("📋 PRESCRIPTION HISTORY")
        print("="*80)
        print("\nNo prescriptions found in history.\n")
        return
    
    print("\n" + "="*80)
    print("📋 PRESCRIPTION HISTORY")
    print("="*80 + "\n")
    
    # Prepare table data
    table_data = []
    for i, rx in enumerate(prescriptions[-10:], 1):  # Show last 10
        table_data.append([
            i,
            rx['id'],
            rx['date'],
            rx['language'],
            rx['medicine_count'],
            f"{rx['accuracy_score']}%",
            "✓" if rx['audio_available'] else "✗"
        ])
    
    headers = ["#", "ID", "Date", "Language", "Medicines", "Accuracy", "Audio"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print()


def show_prescription_details(prescription_id):
    """Show detailed information about a specific prescription."""
    history = load_history()
    prescriptions = history.get("prescriptions", [])
    
    for rx in prescriptions:
        if rx['id'] == prescription_id:
            print(f"\n{'='*80}")
            print(f"📋 PRESCRIPTION DETAILS - {prescription_id}")
            print(f"{'='*80}\n")
            
            print(f"Date: {rx['date']}")
            print(f"Image: {rx['image_file']}")
            print(f"Language: {rx['language']}")
            print(f"Accuracy Score: {rx['accuracy_score']}%")
            print(f"Audio File: {rx['audio_file']}")
            print(f"Audio Available: {'Yes' if rx['audio_available'] else 'No'}")
            
            print(f"\n{'─'*80}")
            print("MEDICINES:")
            print(f"{'─'*80}\n")
            
            for i, med in enumerate(rx['medicines'], 1):
                print(f"{i}. {med['name']}")
                print(f"   Dosage: {med['dosage']} | Frequency: {med['frequency']} | Duration: {med['duration']}")
                print(f"   Confidence: {med['confidence']}\n")
            
            print(f"{'='*80}\n")
            return
    
    print(f"Prescription {prescription_id} not found.")


def generate_accuracy_chart():
    """Generate accuracy chart from prescription history."""
    ensure_folders()
    history = load_history()
    prescriptions = history.get("prescriptions", [])
    
    if not prescriptions:
        print("No prescriptions to display in chart.")
        return None
    
    # Prepare data
    ids = [p['id'][-8:] for p in prescriptions[-15:]]  # Last 15, show last 8 chars of ID
    accuracy_scores = [p['accuracy_score'] for p in prescriptions[-15:]]
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Subplot 1: Line chart of accuracy over time
    ax1.plot(ids, accuracy_scores, marker='o', linewidth=2, markersize=8, color='#667eea')
    ax1.fill_between(range(len(ids)), accuracy_scores, alpha=0.3, color='#667eea')
    ax1.set_xlabel('Prescription ID', fontsize=10)
    ax1.set_ylabel('Accuracy Score (%)', fontsize=10)
    ax1.set_title('Prescription Accuracy Over Time', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 105)
    ax1.tick_params(axis='x', rotation=45)
    
    # Subplot 2: Average accuracy by confidence level
    confidence_counts = {"High": 0, "Medium": 0, "Low": 0}
    confidence_scores = {"High": [], "Medium": [], "Low": []}
    
    for p in prescriptions:
        for med in p['medicines']:
            confidence = med['confidence']
            confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1
            if confidence == "High":
                confidence_scores["High"].append(100)
            elif confidence == "Medium":
                confidence_scores["Medium"].append(75)
            else:
                confidence_scores["Low"].append(50)
    
    colors = ['#28a745', '#ffc107', '#dc3545']
    ax2.bar(confidence_counts.keys(), 
            [len(confidence_scores["High"]), len(confidence_scores["Medium"]), len(confidence_scores["Low"])],
            color=colors)
    ax2.set_ylabel('Number of Medicines', fontsize=10)
    ax2.set_title('Medicine Extraction Confidence Distribution', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Save chart
    chart_filename = os.path.join(CHART_FOLDER, f"accuracy_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    plt.tight_layout()
    plt.savefig(chart_filename, dpi=100, bbox_inches='tight')
    plt.close()
    
    return chart_filename


def list_downloadable_audio():
    """List all downloadable audio files."""
    ensure_folders()
    
    audio_files = []
    if os.path.exists(AUDIO_FOLDER):
        for file in os.listdir(AUDIO_FOLDER):
            if file.endswith('.mp3'):
                filepath = os.path.join(AUDIO_FOLDER, file)
                size_kb = os.path.getsize(filepath) / 1024
                audio_files.append({
                    'filename': file,
                    'path': filepath,
                    'size_kb': round(size_kb, 2)
                })
    
    return audio_files


def display_downloadable_files():
    """Display all downloadable audio files."""
    audio_files = list_downloadable_audio()
    
    if not audio_files:
        print("\n📁 No audio files available for download.\n")
        return
    
    print(f"\n{'='*80}")
    print("📁 DOWNLOADABLE AUDIO FILES")
    print(f"{'='*80}\n")
    
    table_data = []
    for i, audio in enumerate(audio_files, 1):
        table_data.append([
            i,
            audio['filename'],
            f"{audio['size_kb']} KB",
            audio['path']
        ])
    
    headers = ["#", "Filename", "Size", "Path"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print(f"\nTotal files: {len(audio_files)}\n")


def get_history_statistics():
    """Get overall statistics from prescription history."""
    history = load_history()
    prescriptions = history.get("prescriptions", [])
    
    if not prescriptions:
        return None
    
    total_prescriptions = len(prescriptions)
    total_medicines = sum(p['medicine_count'] for p in prescriptions)
    avg_accuracy = sum(p['accuracy_score'] for p in prescriptions) / total_prescriptions
    languages_used = set(p['language'] for p in prescriptions)
    
    return {
        "total_prescriptions": total_prescriptions,
        "total_medicines": total_medicines,
        "average_accuracy": round(avg_accuracy, 2),
        "languages_used": list(languages_used),
        "audio_files": sum(1 for p in prescriptions if p['audio_available'])
    }


def display_statistics():
    """Display overall statistics."""
    stats = get_history_statistics()
    
    if not stats:
        print("\n📊 No statistics available yet.\n")
        return
    
    print(f"\n{'='*80}")
    print("📊 OVERALL STATISTICS")
    print(f"{'='*80}\n")
    print(f"Total Prescriptions: {stats['total_prescriptions']}")
    print(f"Total Medicines: {stats['total_medicines']}")
    print(f"Average Accuracy: {stats['average_accuracy']}%")
    print(f"Languages Used: {', '.join(stats['languages_used'])}")
    print(f"Audio Files: {stats['audio_files']}")
    print(f"\n{'='*80}\n")
