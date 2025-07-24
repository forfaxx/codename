#!/usr/bin/env python3
"""
codename.py — Generate random codenames for projects, machines, releases, etc.

USAGE:
  ./codename.py                    → Random "Adjective Noun" pair
  ./codename.py --ubuntu          → Ubuntu-style: adj & noun share first letter
  ./codename.py --military        → Military-style "Operation Foxtrot Hammer"
  ./codename.py --noun            → Just a single capitalized noun
  ./codename.py --json            → Output JSON-formatted object

Word lists should exist alongside the script:
  - adjectives.txt
  - nouns.txt
  - animals.txt (optional)

EXAMPLES:
  ❯ ./codename.py
  Fierce Tumbleweed

  ❯ ./codename.py --ubuntu
  Bold Bison

  ❯ ./codename.py --military
  Operation Night Lantern
"""

import random
import argparse
from pathlib import Path
from collections import defaultdict

# === Load word lists ===
script_dir = Path(__file__).resolve().parent
adjectives = (script_dir / "adjectives.txt").read_text().splitlines()
nouns = (script_dir / "nouns.txt").read_text().splitlines()

# Load animals if available
animal_nouns_path = script_dir / "animals.txt"
if animal_nouns_path.exists():
    animal_nouns = animal_nouns_path.read_text().splitlines()
else:
    print("⚠️  Warning: animals.txt not found. Ubuntu codenames may fallback to all nouns.")
    animal_nouns = []

# === Codename generators ===

def get_random_pair():
    return random.choice(adjectives), random.choice(nouns)

def get_ubuntu_pair():
    # the goal is to find an adjective and animal name that start with the same 
    # letter and capitalize them both
    adj_map = defaultdict(list)
    noun_map = defaultdict(list)

    # Group adjectives by first letter
    for adj in adjectives:
        if adj:
            adj_map[adj[0].lower()].append(adj)

    # Group nouns (prefer animals if available) by first letter
    target_nouns = animal_nouns if animal_nouns else nouns
    for noun in target_nouns:
        if noun:
            noun_map[noun[0].lower()].append(noun)

    # Find common starting letters between adjective and noun pools
    common_letters = list(set(adj_map.keys()) & set(noun_map.keys()))
    if not common_letters:
        return get_random_pair()

    letter = random.choice(common_letters)
    adj = random.choice(adj_map[letter])
    noun = random.choice(noun_map[letter])
    return adj, noun

def get_military_codename():
    noun = random.choice(nouns)
    if random.random() < 0.5:
        adj = random.choice(adjectives)
        return f"Operation {adj.capitalize()} {noun.capitalize()}"
    return f"Operation {noun.capitalize()}"

# === Main logic ===

def main():
    parser = argparse.ArgumentParser(description="Generate a codename.")
    parser.add_argument("--ubuntu", action="store_true", help="Ubuntu-style: adjective and animal share first letter.")
    parser.add_argument("--military", action="store_true", help="Military-style: Operation + noun or adj-noun.")
    parser.add_argument("--noun", action="store_true", help="Only a noun.")
    parser.add_argument("--json", action="store_true", help="Output JSON format.")
    parser.add_argument("--count", type=int, default=1, help="Number of names to generate.")
    args = parser.parse_args()

    for _ in range(args.count):
        if args.military:
            print(get_military_codename())
        elif args.noun:
            print(random.choice(nouns).capitalize())
        elif args.ubuntu:
            adj, noun = get_ubuntu_pair()
            print(f"{adj.capitalize()} {noun.capitalize()}")
        elif args.json:
            adj, noun = get_random_pair()
            print({"adjective": adj, "noun": noun})
        else:
            adj, noun = get_random_pair()
            print(f"{adj.capitalize()} {noun.capitalize()}")


if __name__ == "__main__":
    main()
