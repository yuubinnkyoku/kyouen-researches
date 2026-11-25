#!/usr/bin/env python3
"""Verify that the @@TRANSCRIPTION blocks inside audit_frontier.py are
byte-identical to the pinned published bytes.

Pins (published y=18 universal verifier, part2 edition,
research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/verify_y18_universal.py,
whole-file SHA-256 8ddd0c2f24213e658705a403ede55d185aab59e7b7d47bd68679d9b3b0b6072a):
  engine  block SHA-256 e5abe0536489ebe75f2af87a43e5bf38ad1d76c27ef849c931c9162f269bc59a
  cand17  block SHA-256 44f1ce4e5a30fd930566a91b2d191c3397b8c3210fd5e7ee3721e6084cb34cb4
  cand18  block SHA-256 caf13e8015d51948389f4417d52f38c7d445a4d58fa0225318191968a3967c05

Usage: python3 scripts/check_blocks.py  (run from the experiment dir).
Fails closed (rc=1) on any mismatch.
"""
import hashlib
import sys
from pathlib import Path

PINS = {
    "ENGINE": "e5abe0536489ebe75f2af87a43e5bf38ad1d76c27ef849c931c9162f269bc59a",
    "CAND17": "44f1ce4e5a30fd930566a91b2d191c3397b8c3210fd5e7ee3721e6084cb34cb4",
    "CAND18": "caf13e8015d51948389f4417d52f38c7d445a4d58fa0225318191968a3967c05",
}
SRC = ("ENGINE", "CAND17", "CAND18")


def extract(text, tag):
    start = "# @@TRANSCRIPTION-%s-START@@" % tag
    end = "# @@TRANSCRIPTION-%s-END@@" % tag
    i = text.index(start)
    j = text.index(end) + len(end)
    return text[i:j] + "\n"


def main():
    here = Path(__file__).resolve().parent.parent
    src = (here / "audit_frontier.py").read_text()
    ok = True
    for tag in SRC:
        block = extract(src, tag)
        got = hashlib.sha256(block.encode()).hexdigest()
        want = PINS[tag]
        status = "OK" if got == want else "MISMATCH"
        print(f"{tag}: {status} got={got}")
        ok = ok and (got == want)
    print("check_blocks:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
