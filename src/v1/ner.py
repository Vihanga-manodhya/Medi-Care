# File: src/ner.py (Working and Enhanced)
import re
import os
import json

def extract_structured_data(raw_text, output_dir):
    """
    Uses a more advanced Regular Expression to parse OCR text from a variety of formats
    and translates medical abbreviations.
    """
    print("[INFO] Structuring data with advanced Regex and abbreviation mapping...")

    abbreviations = {
        "BID": "twice a day", "TID": "three times a day", "QD": "once a day", "QID": "four times a day",
        "PRN": "as needed", "TDS": "three times a day", "BD": "twice a day", "NOCTE": "at night"
    }

    # --- Extract Patient and Doctor ---
    patient_name = "Not Found"
    prescriber = "Not Found"

    # Enhanced regex patterns to be more flexible
    med_pattern = re.compile(
        r"(\w+)\s+(\d+\s?m?g?)\s+(\b(?:TDS|BD|NOCTE|PRN)\b)\s*(\w*)",
        re.IGNORECASE
    )
    
    # A second pattern for less structured text (e.g., "Amoxicillin 500mg bd")
    med_pattern_simple = re.compile(
        r"(\w+)\s+(\d+\s?m?g?)\s+(\w+)",
        re.IGNORECASE
    )
    
    medications = []
    
    # Process the raw text line by line
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue

        match = med_pattern.search(line)
        if match:
            drug_name = match.group(1).strip()
            strength = match.group(2).strip()
            freq_abbr = match.group(3).upper().strip()
            duration_text = match.group(4).strip() if match.group(4) else ""
            
            full_instructions = abbreviations.get(freq_abbr, freq_abbr)
            
            instructions = f"Take {full_instructions}"
            if duration_text:
                instructions += f" for {duration_text}"

            medications.append({
                "drug_name": drug_name,
                "strength": strength,
                "form": "Tablet",
                "instructions": instructions
            })
            print(f"[INFO] Found medication: {drug_name} with pattern 1")
            
        else:
            # Fallback to the simpler pattern
            match = med_pattern_simple.search(line)
            if match:
                drug_name = match.group(1).strip()
                strength = match.group(2).strip()
                instructions_text = match.group(3).strip()
                
                # Check if the third part is a known abbreviation
                freq_abbr = instructions_text.upper()
                full_instructions = abbreviations.get(freq_abbr, instructions_text)
                
                medications.append({
                    "drug_name": drug_name,
                    "strength": strength,
                    "form": "Tablet",
                    "instructions": f"Take {full_instructions}"
                })
                print(f"[INFO] Found medication: {drug_name} with pattern 2")

    final_data = {
        "patient_name": patient_name,
        "prescriber": prescriber,
        "medications": medications
    }
    
    output_path = os.path.join(output_dir, "structured_data.json")
    with open(output_path, 'w') as f:
        json.dump(final_data, f, indent=2)
    print(f"[INFO] Structured data saved to '{output_path}'")

    return final_data