# File: src/ner.py
import re

def extract_structured_data(raw_text, output_dir):
    """
    Uses Regular Expressions (Regex) to parse OCR text from a specific format
    and translates medical abbreviations.
    """
    print("[INFO] Structuring data with Regex and abbreviation mapping...")

    # Dictionary to map medical shorthand to full text
    abbreviations = {
        "BID": "twice a day",
        "TID": "three times a day",
        "QD": "once a day",
        "QID": "four times a day",
        "PRN": "as needed"
    }

    # --- Extract Patient and Doctor ---
    patient_name = "Not Found"
    # Search for a pattern like "name Vola Smith ace 24"
    match = re.search(r"name (.*?) ace", raw_text, re.IGNORECASE)
    if match:
        patient_name = match.group(1).strip()

    prescriber = "Not Found"
    # Search for a pattern like "De Steve: dalinson"
    match = re.search(r"De Steve: (.*)", raw_text, re.IGNORECASE)
    if match:
        prescriber = match.group(1).strip()

    # --- Extract Medications ---
    medications = []
    # Regex to find lines with drug names, dosage, and frequency shorthand
    # Example line: "Betsloe 100mg - 1 tab BID"
    med_pattern = re.compile(r"(\w+\s?\w*)\s+(\d+\s?m[g|l]).*?(\bBID\b|\bTID\b|\bQD\b|\bQID\b)", re.IGNORECASE)
    
    found_meds = med_pattern.findall(raw_text)
    
    for med in found_meds:
        drug_name = med[0].strip()
        strength = med[1].strip()
        freq_abbr = med[2].upper() # Ensure abbreviation is uppercase for dictionary lookup
        
        # Translate the abbreviation to full text, default to the abbreviation if not found
        full_instructions = abbreviations.get(freq_abbr, freq_abbr)
        
        medications.append({
            "drug_name": drug_name,
            "strength": strength,
            "form": "Tablet",  # Assuming 'Tablet' as a default form
            "instructions": f"Take 1 tablet {full_instructions}"
        })

    # --- Final structured data ---
    final_data = {
        "patient_name": patient_name,
        "prescriber": prescriber,
        "medications": medications
    }

    return final_data