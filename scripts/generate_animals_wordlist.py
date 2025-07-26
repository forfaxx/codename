#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path

# === Paths ===
script_dir = Path(__file__).resolve().parent
possible_venvs = [script_dir / "venv", script_dir / ".venv"]

# Pick whichever venv folder exists, or default to creating ./venv
venv_dir = next((p for p in possible_venvs if p.exists()), possible_venvs[0])
python = venv_dir / "bin" / "python"

# === Offer to create venv ===
if not venv_dir.exists():
    consent = input(f"Virtual env not found in {venv_dir}. Create one and install NLTK? [y/N] ")
    if consent.lower() != 'y':
        print("🛑 Aborted. No virtual environment created.")
        sys.exit(1)

    print(f"🐍 Setting up {venv_dir.name}...")
    subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    subprocess.run([str(python), "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([str(python), "-m", "pip", "install", "nltk==3.8.1"], check=True)
    subprocess.run([str(python), "-c", (
        "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
    )], check=True)
    print("✅ Venv ready.")

# === Relaunch in venv if needed ===
if sys.executable != str(python):
    import os
    os.execv(str(python), [str(python)] + sys.argv)

# === Main logic ===
import nltk
from nltk.corpus import wordnet as wn

# === Overwrite warning ===
animals_path = script_dir / "animals.txt"
if animals_path.exists():
    resp = input("⚠️  This will overwrite animals.txt. Continue? [y/N] ")
    if resp.strip().lower() != "y":
        print("🛑 Aborted by user.")
        sys.exit(1)

print("🔍 Gathering animal names from WordNet...")

# === Ensure corpora are available ===
for corpus in ("wordnet", "omw-1.4"):
    try:
        nltk.data.find(f"corpora/{corpus}")
    except LookupError:
        resp = input(f"Missing NLTK corpus '{corpus}'. Download now? [y/N] ")
        if resp.lower() == 'y':
            nltk.download(corpus)
        else:
            print(f"🛑 Cannot continue without '{corpus}'. Exiting.")
            sys.exit(1)

# === Step 1: Get animal synsets ===
animal_synsets = list(wn.synset('animal.n.01').closure(lambda s: s.hyponyms()))

# === Step 2: Extract and clean lemma names ===
animal_names = set()
for syn in animal_synsets:
    for lemma in syn.lemmas():
        name = lemma.name().replace('_', ' ')
        if name.isalpha() and 3 <= len(name) <= 12:
            animal_names.add(name.lower())

# === Step 3: Save to file ===
with open(animals_path, "w") as f:
    f.write('\n'.join(sorted(animal_names)) + '\n')

print(f"✅ Saved {len(animal_names)} animal names to animals.txt")
