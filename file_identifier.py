#!/usr/bin/env python3

import sys
import os

# ---------------------------------------------------------------------------
# Signature database.
# Each entry: (offset, signature_bytes, friendly_name, real_extension)
#   offset    -> how many bytes from the start the signature begins
#   signature -> the exact bytes that mark this file type
# ---------------------------------------------------------------------------
SIGNATURES = [
    (0, b"\x89PNG\r\n\x1a\n",         "PNG image",            ".png"),
    (0, b"\xFF\xD8\xFF",              "JPEG image",           ".jpg"),
    (0, b"GIF87a",                   "GIF image",            ".gif"),
    (0, b"GIF89a",                   "GIF image",            ".gif"),
    (0, b"BM",                       "BMP image",            ".bmp"),
    (0, b"%PDF",                     "PDF document",         ".pdf"),
    (0, b"PK\x03\x04",               "ZIP / Office / APK",   ".zip"),
    (0, b"PK\x05\x06",               "ZIP (empty archive)",  ".zip"),
    (0, b"Rar!\x1a\x07\x00",         "RAR archive",          ".rar"),
    (0, b"\x1f\x8b",                 "GZIP archive",         ".gz"),
    (0, b"7z\xbc\xaf\x27\x1c",       "7-Zip archive",        ".7z"),
    (0, b"\x7fELF",                  "ELF executable (Linux)", ".elf"),
    (0, b"MZ",                       "Windows executable",   ".exe"),
    (0, b"#!",                       "Script (shebang)",     ".sh"),
    (0, b"\xCA\xFE\xBA\xBE",         "Java class file",      ".class"),
    (0, b"ID3",                      "MP3 audio",            ".mp3"),
    (0, b"OggS",                     "OGG media",            ".ogg"),
    (0, b"fLaC",                     "FLAC audio",           ".flac"),
    (0, b"RIFF",                     "RIFF (WAV/AVI)",       ".wav"),
    (4, b"ftyp",                     "MP4 / MOV video",      ".mp4"),
    (0, b"<?xml",                    "XML / possibly SVG",   ".xml"),
    (0, b"<svg",                     "SVG image",            ".svg"),
    (0, b"\x25\x21PS",               "PostScript",           ".ps"),
]


def read_header(path, num_bytes=32):
    """Read the first few bytes of a file."""
    with open(path, "rb") as f:
        return f.read(num_bytes)


def identify(header):
    """Compare the header against known signatures."""
    for offset, signature, name, ext in SIGNATURES:
        chunk = header[offset:offset + len(signature)]
        if chunk == signature:
            return name, ext
    return None, None


def looks_like_text(header):
    """Rough check: if all bytes are printable, it's probably plain text."""
    try:
        text = header.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return all(c.isprintable() or c in "\r\n\t " for c in text)


def main():
    if len(sys.argv) != 2:
        print("Usage: python file_identifier.py <path_to_file>")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.isfile(path):
        print(f"[!] Not a file: {path}")
        sys.exit(1)

    header = read_header(path)
    hex_preview = header[:16].hex(" ")

    name, real_ext = identify(header)
    claimed_ext = os.path.splitext(path)[1].lower()

    print("=" * 50)
    print(f"File:            {path}")
    print(f"First 16 bytes:  {hex_preview}")
    print(f"Claimed ext:     {claimed_ext or '(none)'}")

    if name:
        print(f"Detected type:   {name}")
        print(f"True extension:  {real_ext}")

        if claimed_ext and claimed_ext != real_ext:
            print("\n[!] WARNING: Extension does NOT match real file type!")
            print("    This file may be disguised.")
    elif looks_like_text(header):
        print("Detected type:   Plain text (no binary signature)")
    else:
        print("Detected type:   Unknown / no known signature")

    print("=" * 50)


if __name__ == "__main__":
    main()
