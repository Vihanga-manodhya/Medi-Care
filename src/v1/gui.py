# File: src/gui.py (MODERN THEME - REVISED)
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font
from PIL import Image, ImageTk
import os
import sys
import threading
import json 

# Import the functions from your existing pipeline files
from preprocess import preprocess_image
from ocr import extract_text_with_ocr
from ner import extract_structured_data
from ner_data import DRUG_INFO

# --- AI API Configuration ---
AI_API_KEY = "YOUR_AI_API_KEY"

class TextRedirector:
    """A class to redirect stdout to a tkinter text widget."""
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        """Writes text to the widget and auto-scrolls."""
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)
        self.widget.update_idletasks()

    def flush(self):
        """This function is required for the stream interface."""
        pass

class PrescriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prescription Reader AI")
        self.root.geometry("1000x700")
        
        self.root.configure(bg="#1c1c1c")
        
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = font.Font(family="Arial", size=12, weight="bold")
        self.text_font = font.Font(family="Consolas", size=11)
        self.heading_font = font.Font(family="Helvetica", size=14, weight="bold")
        
        self.black = "#1c1c1c"
        self.red = "#e53935"
        self.white = "#ffffff"
        self.gray = "#424242"
        self.light_gray = "#b0b0b0"

        self.image_path = None
        self.medications = []

        title_frame = tk.Frame(self.root, bg=self.black, pady=10)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="AI Prescription Reader", font=self.title_font, fg=self.red, bg=self.black)
        title_label.pack()

        main_frame = tk.Frame(self.root, bg=self.black, padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame, bg=self.black)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        button_frame = tk.Frame(left_frame, bg=self.black)
        button_frame.pack(pady=10)

        self.load_button = tk.Button(button_frame, text="Load Prescription Image", command=self.load_image, bg=self.gray, fg=self.white, activebackground=self.red, activeforeground=self.white, font=self.button_font, borderwidth=0, padx=15, pady=8)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.process_button = tk.Button(button_frame, text="Extract Information", command=self.process_image, state=tk.DISABLED, bg=self.gray, fg=self.white, activebackground=self.red, activeforeground=self.white, font=self.button_font, borderwidth=0, padx=15, pady=8)
        self.process_button.pack(side=tk.LEFT, padx=5)

        self.image_label = tk.Label(left_frame, text="No Image Loaded", bg=self.gray, fg=self.light_gray, font=self.heading_font, relief="flat", borderwidth=0)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        right_frame = tk.Frame(main_frame, bg=self.black)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        med_list_label = tk.Label(right_frame, text="Detected Medications", font=self.heading_font, fg=self.red, bg=self.black)
        med_list_label.pack(anchor="w", pady=(0, 5))
        
        self.med_listbox = tk.Listbox(right_frame, bg=self.gray, fg=self.light_gray, selectbackground=self.red, selectforeground=self.white, font=self.text_font, relief="flat", borderwidth=0)
        self.med_listbox.pack(fill=tk.X)
        self.med_listbox.bind("<<ListboxSelect>>", self.show_medication_details)

        ai_button_frame = tk.Frame(right_frame, bg=self.black)
        ai_button_frame.pack(fill=tk.X, pady=10)

        self.ai_details_button = tk.Button(ai_button_frame, text="Get Details in Sinhala (AI)", command=self.get_drug_details_sinhala, state=tk.DISABLED, bg=self.red, fg=self.white, activebackground=self.gray, activeforeground=self.white, font=self.button_font, borderwidth=0, padx=15, pady=8)
        self.ai_details_button.pack(side=tk.LEFT, padx=5)

        med_details_label = tk.Label(right_frame, text="Medication Details", font=self.heading_font, fg=self.red, bg=self.black)
        med_details_label.pack(anchor="w", pady=(0, 5))

        self.details_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=50, height=15, bg=self.black, fg=self.light_gray, insertbackground=self.red, selectbackground=self.red, font=self.text_font, relief="flat", borderwidth=0)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
        sys.stdout = TextRedirector(self.details_text)
        
        print("--- AI Prescription Reader Initialized ---")
        print("Please load a prescription image to begin.")

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not path:
            return
        
        self.image_path = path
        
        img = Image.open(self.image_path)
        img.thumbnail((500, 600))
        photo = ImageTk.PhotoImage(img)
        
        self.image_label.config(image=photo, text="", bg=self.black)
        self.image_label.image = photo
        
        self.process_button.config(state=tk.NORMAL)
        self.ai_details_button.config(state=tk.DISABLED)
        self.med_listbox.delete(0, tk.END)
        
        self.details_text.delete(1.0, tk.END)
        print(f"Image loaded: {os.path.basename(self.image_path)}\n")
        print("Ready to extract information...")

    def process_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please load an image first.")
            return

        self.med_listbox.delete(0, tk.END)
        self.details_text.delete(1.0, tk.END)
        print("--- Starting Pipeline ---")

        try:
            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # UNCOMMENTED: These lines now run the actual pipeline on your image
            preprocessed_img = preprocess_image(self.image_path, output_dir)
            raw_text = extract_text_with_ocr(preprocessed_img)
            
            # This is the line that was hardcoded, it is now removed
            # raw_text = """..."""

            final_data = extract_structured_data(raw_text, output_dir)

            if not final_data:
                self.details_text.insert(tk.END, "No structured data could be extracted.")
            else:
                self.display_medications(final_data)

        except Exception as e:
            print(f"\n\n--- A PIPELINE ERROR OCCURRED ---")
            messagebox.showerror("Pipeline Error", f"An error occurred: {e}")
            
    def display_medications(self, data):
        self.medications = data.get("medications", [])
        if self.medications:
            print("--- FINAL STRUCTURED DATA ---")
            for med in self.medications:
                drug_name = med.get('drug_name', 'Unknown Drug')
                self.med_listbox.insert(tk.END, drug_name)
                print(f"  • {drug_name}")
            self.ai_details_button.config(state=tk.NORMAL)
        else:
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, "No medication details extracted.")

    def show_medication_details(self, event):
        selected_index = self.med_listbox.curselection()
        if not selected_index:
            return

        med = self.medications[selected_index[0]]
        
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, "--- Detailed Medication Information ---\n\n")
        
        drug = med.get('drug_name', 'N/A')
        strength = med.get('strength', 'N/A')
        form = med.get('form', 'N/A')
        instructions = med.get('instructions', 'N/A')
        
        self.details_text.insert(tk.END, f"💊 Drug Name: {drug}\n")
        self.details_text.insert(tk.END, f"💪 Strength: {strength}\n")
        self.details_text.insert(tk.END, f"📦 Form: {form}\n")
        self.details_text.insert(tk.END, f"📝 Instructions: {instructions}\n")
    
    def get_drug_details_sinhala(self):
        selected_index = self.med_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Select Drug", "Please select a medication from the list first.")
            return

        drug = self.medications[selected_index[0]].get('drug_name', 'Unknown Drug')
        
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, f"Searching for details on '{drug}' in Sinhala...\n")
        
        threading.Thread(target=self._fetch_sinhala_details, args=(drug,)).start()

    def _fetch_sinhala_details(self, drug_name):
        drug_info = DRUG_INFO.get(drug_name.lower())
        
        if drug_info and drug_info.get("sinhala_details"):
            sinhala_text = drug_info["sinhala_details"]
        else:
            sinhala_text = f"සමාවෙන්න, '{drug_name}' පිළිබඳ තොරතුරු දැනට ලබාගත නොහැක."

        self.root.after(0, self.update_details_text, sinhala_text)

    def update_details_text(self, text):
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, text)

if __name__ == '__main__':
    root = tk.Tk()
    app = PrescriptionApp(root)
    root.mainloop()