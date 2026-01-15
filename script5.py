#!/usr/bin/env python3
"""
Folder 5 - Python test script (script5.py)
"""


def to_upper(text: str) -> str:
    return text.upper()


def word_count(text: str) -> int:
    return len(text.split())


if __name__ == "__main__":
    sample = "folder five python test file"
    print("Folder 5 - script5.py")
    print("Upper:", to_upper(sample))
    print("Word count:", word_count(sample))


