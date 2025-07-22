import spacy
import random
from spacy.training.example import Example
from TRAIN_DATA import TRAIN_DATA # Import your data

# --- Model setup ---
model = None
output_dir = "models/prescription_ner_model" # Directory to save the trained model
n_iter = 100 # Number of training iterations

# --- Load or create a blank model ---
if model is not None:
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
else:
    nlp = spacy.blank("en") # Create a blank English model
    print("Created blank 'en' model")

# --- Add NER pipe to the model ---
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner", last=True)
else:
    ner = nlp.get_pipe("ner")

# --- Add new entity labels to the NER pipe ---
for _, annotations in TRAIN_DATA:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

# --- Training ---
optimizer = nlp.begin_training()
for itn in range(n_iter):
    random.shuffle(TRAIN_DATA)
    losses = {}
    for text, annotations in TRAIN_DATA:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example], drop=0.5, sgd=optimizer, losses=losses)
    print(f"Iteration {itn+1}/{n_iter}, Losses: {losses}")

# --- Save the trained model ---
nlp.to_disk(output_dir)
print(f"\nSaved trained model to {output_dir}")

# --- Test the trained model ---
print("\n--- Testing the trained model ---")
test_text = "I was prescribed Oxprelol 50mg, one tablet every day."
doc = nlp(test_text)
for ent in doc.ents:
    print(f"Entity: '{ent.text}', Label: '{ent.label_}'")