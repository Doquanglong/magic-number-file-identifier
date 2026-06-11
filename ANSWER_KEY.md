# Magic Number File Type Identifier

A lightweight Python security tool that identifies a file's **true type** by
reading the bytes inside it — not by trusting the file extension.

---

## What Is This?

Every file on your computer has a name with an extension, like `photo.jpg` or
`report.pdf`. Most programs decide what a file is just by looking at that
extension. The problem? **The extension is just a label, and labels can lie.**

An attacker can take a malicious script called `malware.sh` and simply rename
it to `cute_cat.svg`. To the eye — and to many basic systems — it now looks
like a harmless image.

This tool ignores the name entirely. Instead, it reads the first few bytes of
the file, known as the **magic number** (or file signature), and compares them
against a database of known formats. These signature bytes are part of the
file's actual content, so renaming the file cannot fake them.

If the real content doesn't match the claimed extension, the tool raises a
warning that the file may be disguised.

---

## How It Works

Most file formats begin with a fixed sequence of bytes that acts like a
fingerprint:

| File Type | Magic Number (hex)      | Meaning             |
|-----------|-------------------------|---------------------|
| PNG       | `89 50 4E 47`           | "PNG" image         |
| PDF       | `25 50 44 46` (`%PDF`)  | PDF document        |
| GIF       | `47 49 46 38` (`GIF8`)  | GIF image           |
| Script    | `23 21` (`#!`)          | Shebang / script    |
| ZIP/Office| `50 4B 03 04` (`PK..`)  | ZIP-based archive   |

The tool follows four simple steps:

1. **Read the header** — opens the file in binary mode and reads only the first
   32 bytes (fast and safe, even on huge files).
2. **Match the signature** — compares those bytes against its table of known
   magic numbers.
3. **Compare to the extension** — checks the detected type against the
   extension written in the filename.
4. **Report and warn** — prints the real type, and if the extension doesn't
   match, flags the file as potentially disguised.

Importantly, the tool **reads** files but never **executes** them, so it is
safe to point at suspicious files.

---

## Why It Matters in Cybersecurity

Disguising a file's true type is a classic technique attackers use to sneak
malware past defenses and trick users into opening dangerous files. Detecting
the real type from content rather than the filename is a foundational concept
behind:

- **Antivirus and EDR tools** that scan files regardless of their name.
- **Email and upload filters** that block executables masquerading as images
  or documents.
- **Digital forensics**, where investigators must determine what a file truly
  is, not what it claims to be.

This project demonstrates the core idea behind those professional systems in a
clear, readable form — making it a strong introduction to **detection
engineering** and **blue-team defense** fundamentals.

---

## How to Use It

You only need **Python 3**. There are no external libraries to install — the
tool uses the Python standard library only.

Run it from the terminal, passing the path to any file:

```bash
python file_identifier.py <path_to_file>
```

### Example: a genuine file

```bash
python file_identifier.py document_real.pdf
```

Output:

```
==================================================
File:            document_real.pdf
First 16 bytes:  25 50 44 46 2d 31 2e 34 0a 31 20 30 20 6f 62 6a
Claimed ext:     .pdf
Detected type:   PDF document
True extension:  .pdf
==================================================
```

No warning — the content and the extension agree.

### Example: a disguised file

```bash
python file_identifier.py sunset.jpg
```

Output:

```
==================================================
File:            sunset.jpg
First 16 bytes:  23 21 2f 75 73 72 2f 62 69 6e 2f 65 6e 76 20 70
Claimed ext:     .jpg
Detected type:   Script (shebang)
True extension:  .sh

[!] WARNING: Extension does NOT match real file type!
    This file may be disguised.
==================================================
```

The file pretends to be a `.jpg` image, but its bytes reveal it is actually a
script — exactly the kind of disguise an attacker would use.

---

## The Challenge Mode

Included is a set of **8 test files** designed as a guessing game. Some are
genuine, and some are disguised. The goal is to run the tool on each one and
figure out which is which.

| File              | Claims to be | Status     |
|-------------------|--------------|------------|
| photo_real.png    | PNG image    | Try it!    |
| document_real.pdf | PDF document | Try it!    |
| notes_real.txt    | Text file    | Try it!    |
| sunset.jpg        | JPEG image   | Try it!    |
| logo.png          | PNG image    | Try it!    |
| backup.zip        | ZIP archive  | Try it!    |
| report.docx       | Word doc     | Try it!    |
| song.mp3          | MP3 audio    | Try it!    |

Run each file through the tool and record whether it's **real** or **fake**.
The full solution is in `ANSWER_KEY.md` — try to solve it before peeking!

To run the whole set at once:

```bash
for f in *; do python file_identifier.py "$f"; done
```

---

## Known Limitations

Being honest about a tool's boundaries is part of good security work:

- **Polyglot files** — a cleverly crafted file can be valid as two formats at
  once and may fool a simple signature check.
- **Shared signatures** — ZIP-based formats like `.docx`, `.xlsx`, and `.apk`
  all begin with the same `PK..` bytes, so they can't be told apart by header
  alone.
- **Plain text** — formats like `.py`, `.csv`, and `.txt` have no binary
  signature, so they are reported as plain text rather than a specific type.

These are normal trade-offs of signature-based detection and good starting
points for future improvements.

---

## Files in This Project

- `file_identifier.py` — the main tool
- Challenge files — 8 real and disguised test files
- `ANSWER_KEY.md` — solution to the challenge
- `README.md` — this file