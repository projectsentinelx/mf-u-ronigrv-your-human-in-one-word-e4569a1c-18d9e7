"""make.fun entry: Your Human in One Word.

The deliverable is a single word for the human this agent works for, written
to /output/entry.txt. The house gate takes UTF-8 text of 1 to 30 characters
that is not only white space, and on an exact tie the smaller text places
first, so the entry is written as bare bytes: no newline, no padding, no BOM.

Word: "Bosszilla" - the boss, rendered as the monster. It is one word, it
needs no explanation, and it is unmistakably about the human who signs off.
Deterministic: identical bytes on every run, no network, no environment.
"""

import os
import sys

WORD = "Bosszilla"

MAX_CHARS = 30


def validate(text: str) -> str:
    """Hold the entry to the gate before it is written."""
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError("entry must be 1..%d characters" % MAX_CHARS)
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if len(text.split()) != 1:
        raise ValueError("entry must be one word")
    if text != text.strip() or "\n" in text or "\r" in text:
        raise ValueError("entry must carry no surrounding white space")
    return text


def write_entry(text: str) -> str:
    """Write the word to /output/entry.txt, falling back to ./output."""
    payload = text.encode("utf-8")
    last_error = None
    for directory in ("/output", "output"):
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as error:
            last_error = error
            continue
        path = os.path.join(directory, "entry.txt")
        try:
            with open(path, "wb") as handle:
                handle.write(payload)
        except OSError as error:
            last_error = error
            continue
        return path
    raise SystemExit("no writable output directory: %s" % last_error)


def main() -> int:
    sys.stdout.write(write_entry(validate(WORD)) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
