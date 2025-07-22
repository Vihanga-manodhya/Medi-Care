# ===================================================================
# File: src/main.py (Corrected Version)
# Purpose: Main entry point. Includes a new function to create a more
#          complex sample image for testing the advanced NER.
# ===================================================================
import os
import json
from PIL import Image, ImageDraw, ImageFont

# Import our custom modules
from preprocess import preprocess_image
from ocr import extract_text_with_ocr
from ner import extract_structured_data

def create_advanced_dummy_image(path):
    """
    Creates a more complex sample prescription image.
    This serves as our new sample data.
    """
    print(f"'{os.path.basename(path)}' not found. Creating a new, advanced dummy image.")
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        # Use a common font, fall back to default if not found
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_body = ImageFont.truetype("arial.ttf", 20)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except IOError:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # --- Draw the new prescription ---
    draw.text((30, 20), "Central City Medical Group", fill='black', font=font_title)
    draw.line((30, 60, 770, 60), fill='black', width=2)
    
    draw.text((30, 80), "Patient Name: John Appleseed", fill='black', font=font_body)
    draw.text((550, 80), "Date: 09/06/2025", fill='black', font=font_body)
    
    draw.text((30, 140), "Rx:", fill='black', font=font_title)
    
    # Medication 1
    draw.text((50, 180), "Lisinopril 10mg Tablet", fill='black', font=font_body)
    draw.text((50, 210), "Sig: Take one tablet by mouth once daily in the morning.", fill='black', font=font_small)
    
    # Medication 2
    draw.text((50, 260), "Metformin 500mg Tablet", fill='black', font=font_body)
    draw.text((50, 290), "Take one tablet twice daily with meals (breakfast and dinner).", fill='black', font=font_small)

    # Medication 3
    draw.text((50, 340), "Albuterol Sulfate HFA Inhaler", fill='black', font=font_body)
    draw.text((50, 370), "Sig: Inhale 2 puffs every 4-6 hours as needed for shortness of breath.", fill='black', font=font_small)

    draw.text((30, 500), "Prescriber: Dr. Samantha Miller", fill='black', font=font_body)
    draw.line((400, 510, 750, 510), fill='black', width=1)
    draw.text((400, 520), "(Signature on File)", fill='gray', font=font_small)
    
    img.save(path)
    print(f"New dummy image saved to '{path}'")

def run_pipeline():
    """Main function to orchestrate the prescription reading process."""
    raw_image_dir = os.path.join("data", "raw")
    image_name = "sample_prescription.png"
    image_path = os.path.join(raw_image_dir, image_name)
    output_dir = "output"

    os.makedirs(raw_image_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # We use our new image creation function
    if not os.path.exists(image_path):
        create_advanced_dummy_image(image_path)

    print(f"--- Starting Advanced Pipeline for {image_path} ---")

    preprocessed_image = preprocess_image(image_path, output_dir)
    raw_text = extract_text_with_ocr(preprocessed_image)
    final_data = extract_structured_data(raw_text, output_dir)

    print("\n--- FINAL EXTRACTED STRUCTURED DATA ---")
    print(json.dumps(final_data, indent=2))
    print("--- PIPELINE COMPLETE ---")

if __name__ == '__main__':
    # If the old sample image exists, let's remove it to generate the new one.
    old_sample_path = os.path.join("data", "raw", "sample_prescription.png")
    if os.path.exists(old_sample_path):
        # This is a simple way to force the new image to be created.
        # We check the file size. A small file size is likely our old simple image.
        if os.path.getsize(old_sample_path) < 10000: # 10KB threshold
             print("Old sample image detected. Deleting it to create the new advanced one.")
             os.remove(old_sample_path)

    run_pipeline()
