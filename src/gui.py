# File: src/gui.py
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os

# Import the functions from your existing pipeline files

from preprocess import preprocess_image
from ocr import extract_text_with_ocr
from ner import extract_structured_data

class PrescriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prescription Reader AI")
        self.root.geometry("800x600")

        self.image_path = None

        # --- GUI Layout ---
        
        # Top Frame for buttons
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack(fill=tk.X)

        self.load_button = tk.Button(top_frame, text="Load Prescription Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=10)

        self.process_button = tk.Button(top_frame, text="Extract Information", command=self.process_image, state=tk.DISABLED)
        self.process_button.pack(side=tk.LEFT, padx=10)

        # Main Frame for image and results
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Image display label
        self.image_label = tk.Label(main_frame, text="No Image Loaded", relief="solid", borderwidth=1)
        self.image_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Results display text area
        self.results_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=40)
        self.results_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.results_text.insert(tk.END, "Extracted data will appear here...")
        self.results_text.config(state=tk.DISABLED)

    def load_image(self):
        """Opens a file dialog to select an image."""
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not path:
            return
        
        self.image_path = path
        
        # Display the selected image
        img = Image.open(self.image_path)
        img.thumbnail((400, 500)) # Create a thumbnail for display
        photo = ImageTk.PhotoImage(img)
        
        self.image_label.config(image=photo, text="")
        self.image_label.image = photo
        
        self.process_button.config(state=tk.NORMAL) # Enable the process button
        
        # Clear previous results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Image loaded. Ready to extract information.")
        self.results_text.config(state=tk.DISABLED)

    def process_image(self):
        """Runs the full backend pipeline on the selected image."""
        if not self.image_path:
            messagebox.showerror("Error", "Please load an image first.")
            return

        try:
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Processing...\n\n1. Pre-processing image...")
            self.root.update_idletasks() # Refresh the GUI to show the message

            # --- Call your backend functions ---
            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            preprocessed_img = preprocess_image(self.image_path, output_dir)
            self.results_text.insert(tk.END, "\n2. Extracting text with OCR...")
            self.root.update_idletasks()

            raw_text = extract_text_with_ocr(preprocessed_img)
            self.results_text.insert(tk.END, "\n3. Structuring data with NER...")
            self.root.update_idletasks()

            final_data = extract_structured_data(raw_text, output_dir)
            
            # --- Display the final results ---
            self.display_results(final_data)

        except Exception as e:
            messagebox.showerror("Pipeline Error", f"An error occurred: {e}")
            self.results_text.insert(tk.END, f"\n\nAn error occurred:\n{e}")
        finally:
            self.results_text.config(state=tk.DISABLED)

    def display_results(self, data):
        """Formats and displays the structured data in the GUI."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "--- EXTRACTION COMPLETE ---\n\n")
        
        if data.get("patient_name"):
            self.results_text.insert(tk.END, f"👤 Patient: {data['patient_name']}\n")
        if data.get("prescriber"):
            self.results_text.insert(tk.END, f"✍️ Prescriber: {data['prescriber']}\n\n")
        
        self.results_text.insert(tk.END, "--- Medications ---\n")
        if data.get("medications"):
            for med in data["medications"]:
                drug = med.get('drug_name', 'N/A')
                strength = med.get('strength', '')
                form = med.get('form', '')
                instructions = med.get('instructions', 'N/A')
                self.results_text.insert(tk.END, f"• {drug} {strength} {form}\n")
                self.results_text.insert(tk.END, f"  Instructions: {instructions}\n\n")
        else:
            self.results_text.insert(tk.END, "No medication details extracted.\n(Note: This requires a custom-trained NER model for accuracy.)")
        
        self.results_text.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    app = PrescriptionApp(root)
    root.mainloop()