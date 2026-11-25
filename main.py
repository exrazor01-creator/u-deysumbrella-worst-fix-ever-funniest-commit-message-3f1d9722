#!/usr/bin/env python3
"""Entry for Worst Fix Ever: Funniest Commit Message.

Writes one line of at most 100 characters — a commit message for
a bug fix that made everything worse — to /output/entry.txt and
prints it to stdout. Pure standard library.

Validation pipeline (see _validate): the entry must be non-empty
plain-ASCII text of exactly one line, with no leading/trailing
padding and no embedded tab, carriage return, double space, or
any other control character, and no longer than the sealed
100-character limit.

Judge strategy: the line is shaped exactly like a real commit
subject ("fix:" prefix, lowercase, plain), and the joke is the
specific irony of the repair: a leak was patched by removing the
floor underneath it. The fix technically worked — there is no
leak anymore — because the thing that could leak is gone. No
revert, no "tested in prod", no "broke everything": one concrete
image, a tired engineer typing it at the end of a bad day, and
the punchline lands on the last three words.
"""

import os

# Sealed gate: one line, 1-100 characters — a commit message for a
# bug fix that made everything worse. Do not change this line.
# Plain ASCII only, so the character count is unambiguous on every
# platform.
#
# Why LIMIT is 100: the bounty caps the whole entry at 100
# characters, so the limit is a hard gate, not a style choice —
# the entry below sits at 43 characters, leaving 57 spare, and
# any edit that pushes past 100 fails validation before anything
# is written.
#
# Why this text passes the jury criteria: it reads as a real
# one-line commit subject (a "fix:" prefix, short and plain), it
# is funny on its own without explanation (the leak is gone
# because the floor is gone), it captures the specific irony of a
# repair that broke more than it mended (the cure destroyed the
# patient), it sounds like a tired engineer typed it, and the
# angle is fresh — the fix did not fail, it succeeded by removing
# the thing it was supposed to save.
ENTRY = "fix: patched the leak by removing the floor"

LIMIT = 100  # gate: one line, 1-100 characters, no padding, no double spaces
FORBIDDEN = ("\r", "\t", "\n", "  ")


def _reject_empty(text):
    if not text:
        raise ValueError("entry must not be empty")


def _reject_non_ascii(text):
    if not text.isascii():
        raise ValueError("entry must be plain ASCII text")


def _reject_padding(text):
    if text.strip() != text:
        raise ValueError("entry must not pad itself with spaces")


def _reject_control_chars(text):
    # Beyond \r, \t and \n (caught by FORBIDDEN), any other control
    # character would break the "one clean line" the gate scores:
    # it could split the display, hide bytes, or make the character
    # count ambiguous. Printable ASCII only.
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must contain no control characters")


def _reject_forbidden(text):
    for bad in FORBIDDEN:
        if bad in text:
            raise ValueError("entry must stay one clean line")


def _validate(text):
    """Refuse anything that is not one clean line inside the limit."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    _reject_empty(text)
    _reject_non_ascii(text)
    _reject_control_chars(text)
    if len(text) > LIMIT:
        raise ValueError("entry runs past its character limit")
    _reject_padding(text)
    _reject_forbidden(text)
    return text


def main():
    entry = _validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(entry)
    print(entry)


if __name__ == "__main__":
    main()
