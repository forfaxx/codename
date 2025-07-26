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
        "import nltk; nltk.download('punkt'); nltk.download('words'); nltk.download('averaged_perceptron_tagger')"
    )], check=True)
    print("✅ Venv ready.")

# === Relaunch in venv if needed ===
if sys.executable != str(python):
    import os
    os.execv(str(python), [str(python)] + sys.argv)

# === Main logic ===
import nltk
from nltk.corpus import words, brown
from nltk import pos_tag
from collections import Counter

# === Overwrite warning ===
adjectives_path = script_dir / "adjectives.txt"
nouns_path = script_dir / "nouns.txt"

if adjectives_path.exists() or nouns_path.exists():
    resp = input("⚠️  This will overwrite adjectives.txt and nouns.txt. Continue? [y/N] ")
    if resp.strip().lower() != "y":
        print("🛑 Aborted by user.")
        sys.exit(1)

print("⚙️  Generating filtered wordlists...")

# === Ensure corpora are available ===
def ensure_corpus(name):
    try:
        nltk.data.find(f'corpora/{name}')
    except LookupError:
        resp = input(f"Missing NLTK corpus '{name}'. Download now? [y/N] ")
        if resp.lower() == 'y':
            nltk.download(name)
        else:
            print(f"🛑 Cannot continue without '{name}'. Exiting.")
            sys.exit(1)

for corpus in ('brown', 'words'):
    ensure_corpus(corpus)

# === Filter words ===
bad_suffixes = ("'s", "’s")
wordlist = [
    w for w in words.words()
    if w.isalpha()
    and not w.lower().endswith(bad_suffixes)
    and 4 <= len(w) <= 12
]

brown_counts = Counter(w.lower() for w in brown.words())
FREQ_THRESHOLD = 3
wordlist = [w for w in wordlist if brown_counts[w.lower()] > FREQ_THRESHOLD]

# === Tag words ===
adjectives, nouns = [], []
for i in range(0, len(wordlist), 1000):
    tagged = pos_tag(wordlist[i:i+1000])
    for word, tag in tagged:
        if tag.startswith('JJ'):
            adjectives.append(word)
        elif tag.startswith('NN'):
            nouns.append(word)

# === Write files ===
def write_list(path, items):
    words = sorted(set(w.lower() for w in items))
    with open(path, "w") as f:
        f.write('\n'.join(words) + '\n')

write_list(adjectives_path, adjectives)
write_list(nouns_path, nouns)

print(f"✅ Wrote {len(set(adjectives))} adjectives and {len(set(nouns))} nouns")
