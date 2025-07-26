
# codename.py — Random Project Codename Generator

**Generate memorable, fun codenames for your projects, servers, releases, or teams.**
Choose your style: classic Adjective Noun, Ubuntu animal, or military “Operation”–all in one simple Python script.

---

## ✨ Features

* **Adjective Noun combos:** *Clever Otter, Wandering Nebula, Ancient Lantern...*
* **Ubuntu style:** Alliterative, animal-inspired names (e.g. *Brilliant Badger, Wily Wombat*)
* **Military style:** “Operation” codenames (*Operation Silent Arrow*)
* **Single noun mode:** Just a big, bold word
* **JSON output:** For piping into other tools
* **Custom wordlists:** Just edit `adjectives.txt`, `nouns.txt`, or add `animals.txt`
* **Batch output:** Generate lots of names at once (`--count`)
* **No dependencies:** Pure Python, runs anywhere

## Inspiration

What started as a silly text munging exercise has proven to be a happy little app that I run all the time just for fun. 
With the --count argument, you can run it as many times as you like. It's bound to spit out something good eventually.


---

## 🛠 Usage

```sh
python3 codename.py                   # Random "Adjective Noun" pair
python3 codename.py --ubuntu          # Ubuntu-style: adj & animal share first letter
python3 codename.py --military        # Military-style: Operation [Adj] Noun
python3 codename.py --noun            # Just a noun
python3 codename.py --json            # Output JSON-formatted result
python3 codename.py --count 5         # Get five names at once
```
\* **NOTE** The wordlists in use by codename are taken from the system dictionary and may potentially create offensive
combinations. In other words, it's exactly as offensive as the dictionary! 

---

## Examples

```sh
$ python3 codename.py
Glorious Turnip

$ python3 codename.py --ubuntu
Jumpy Jackal

$ python3 codename.py --military
Operation Phantom Ocelot

$ python3 codename.py --noun
Nebula

$ python3 codename.py --json
{"adjective": "quiet", "noun": "mirage"}
```

---

## Wordlists

* **adjectives.txt** — Adjectives, one per line (required)
* **nouns.txt** — Nouns, one per line (required)
* **animals.txt** — Animal names (optional, for Ubuntu mode)

*The script expects these files to be next to `codename.py`. Add your own words to customize!*


### Wordlist Generators (for the curious)

Codename ships with ready‑to‑use `adjectives.txt`, `nouns.txt`, and `animals.txt`,  
but if you want to see how they were built (or rebuild them yourself), check out the scripts in [`/scripts`](scripts):

- `generate_wordlists.py` → builds adjectives and nouns  
- `generate_animals.py` → builds the animal list for Ubuntu‑style names  

They’re **developer tools** — not needed to run Codename — and they’ll prompt before overwriting the included files.  

👉 Read more about how they work in [**Operation Wordlists**](https://adminjitsu.com/posts/operation-wordlists/) — a deep dive into using Python + NLTK to craft the lists behind the names.


---

## License

MIT License — see [LICENSE](./LICENSE)

---

## About

**codename.py** was written for fun and utility by [Kevin Joiner](https://github.com/your-github) in 2025.
Why settle for generic names like “project2” or “server-b” when you could have *Gallant Phoenix* or *Operation Turquoise Spider*?

Pull requests, extra wordlists, and creative forks welcome!

---

*May your codenames always be memorable and mildly mysterious.*

