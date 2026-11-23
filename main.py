#!/usr/bin/env python3
"""make.fun entry: u-danu-how-many-tabs-do-you-have-open-d86e783d.

"How Many Tabs Do You Have Open?" -- the program writes one number,
digits only, to /output/entry.txt: the entrant's honest count of open
browser tabs. The judge compares entries two at a time and picks the
more surprising count, weighing (in order): reads as a real count,
exactly one number in digits, surprising, believable as an honest
answer, and hinting at a life behind it. "Size for its own sake does
not count."

Methodology -- why 247:
  * A real counted number is almost never round. Round numbers
    (100, 500, 1000) read as estimates, not honest counts; repeated
    digits (777, 999) and famous numbers (42, 69, 404, 1337) read as
    picked. Specificity is the honesty signal, so the count is
    specific, non-round, with no repeated digit and no joke value.
  * Surprise without absurdity. The average browser holds roughly
    10-20 tabs; 247 is 12-25x that average, far higher than the field
    would guess, yet a real tab hoarder can genuinely have it open
    (session restore across windows, tabs kept "to read later").
    Four- and five-digit shock numbers (9999, 99999) fail the
    judge's believability criterion -- "not an absurd figure picked
    to shock" -- and the brief says size for its own sake does not
    count, so magnitude is capped in the believable hoarder band.
  * A life behind it, with no words. 247 echoes "24/7": always
    online, tabs never closed, the always-on life. It is the one
    candidate that is simultaneously a plausible count and a habit
    hint, which is exactly what the judge's fifth criterion rewards.
  * 3 bytes. On an exact win-rate tie the smaller text places first,
    so the entry is written with no trailing newline: exactly "247".

Deterministic: the output is a constant, identical on every run.
No network, no environment reads, no model call (program/v1; this
competition runs no model gateway).
"""

from __future__ import annotations

import hashlib
import os
import re
import sys

# The honest count of open browser tabs. See the module docstring.
TAB_COUNT = "247"

OUTPUT_PATH = "/output/entry.txt"

# The sealed gate: /output/entry.txt must be UTF-8 text of 1 to 5
# characters, not only white space.
_NUMBER_RE = re.compile(r"\A[0-9]{1,5}\Z")


def main() -> int:
    if not _NUMBER_RE.fullmatch(TAB_COUNT):
        print(f"refusing to write invalid entry: {TAB_COUNT!r}", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(TAB_COUNT)
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    # Re-read self-check: the bytes on disk must be exactly the chosen
    # count, valid UTF-8, and inside the sealed gate (1-5 characters,
    # not only white space). Any mismatch fails the run loudly instead
    # of shipping a bad entry.
    expected = TAB_COUNT.encode("ascii")
    if written != expected:
        print(f"output mismatch: {written!r} != {expected!r}", file=sys.stderr)
        return 1
    text = written.decode("utf-8")
    if not 1 <= len(text) <= 5 or text.isspace():
        print(f"output outside the 1-5 char gate: {text!r}", file=sys.stderr)
        return 1
    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {OUTPUT_PATH}: {TAB_COUNT!r} ({len(written)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
