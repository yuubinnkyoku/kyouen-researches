#!/usr/bin/env python3
"""Cache-free terminal verification of a canonical 11x11 six-stone LOSS.

Run from repository root: python3 research/experiments/n11-s6-terminal-loss-20261015/verify_s6_terminal.py
All WIN/LOSS labels use the original first player's perspective.
"""
if not __debug__:
    raise SystemExit("Refusing python -O")
import base64
import hashlib
import sys
import zlib
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "n11-s7-fifth-terminal-20261015"))
from fifth_verify_standalone import canonical, children, points, safe, terminal_s10

ROOT = int("00000000040004001004000004010000", 16)
CERT_SHA256 = "cb2e73c277c6fd526689db64b1d8c07ebd1ca1bd8c2a966e0757d22c4471ebf6"
EXPECTED_S5 = {
    "00000000000000101001000010010000",
    "00000000000000401100400040000000",
    "00000000040000011004000004000000",
    "00000000040004000004000004010000",
    "00000000040004001000000004010000",
    "00000000040004001004000004000000",
}

def verify_leaf(mask):
    if mask.bit_count() != 10 or canonical(mask) != mask or not safe(mask):
        raise ValueError("invalid canonical 10-stone leaf")
    is_loss, states, _ = terminal_s10(mask)
    if not is_loss:
        raise ValueError(f"WIN/LOSS conflict for 10-stone leaf {mask:032x}")
    return states

def main():
    packed = (HERE / "s6-loss-optimized.cert.zlib.b64").read_text(encoding="ascii").strip()
    raw = zlib.decompress(base64.b64decode(packed, validate=True))
    if hashlib.sha256(raw).hexdigest() != CERT_SHA256:
        raise ValueError("certificate SHA-256 mismatch")
    lines = raw.decode("ascii").splitlines()
    if lines[:2] != ["# n11-S8-LOSS-global-terminal-v1", "BOARD 11"] or lines[-1] != "END":
        raise ValueError("certificate syntax")
    roots, leaves = [], []
    in_leaves = False
    for line in lines[2:-1]:
        fields = line.split()
        if len(fields) != 2 or len(fields[1]) != 32:
            raise ValueError("invalid record")
        tag, hexmask = fields
        mask = int(hexmask, 16)
        if tag == "ROOT" and not in_leaves:
            roots.append(mask)
        elif tag == "LEAF":
            in_leaves = True
            leaves.append(mask)
        else:
            raise ValueError("record order")
    if len(roots) != 29 or len(set(roots)) != 29 or len(leaves) != 483 or len(set(leaves)) != 483:
        raise ValueError("missing or duplicated certificate nodes")
    if ROOT.bit_count() != 6 or canonical(ROOT) != ROOT or not safe(ROOT):
        raise ValueError("invalid S6 root")
    s7_children = children(ROOT)
    if len(s7_children) != 49:
        raise ValueError("S6 boundary mismatch")
    s7_covered = set()
    s9_witnesses = set()
    for s10 in leaves:
        if s10.bit_count() != 10 or canonical(s10) != s10 or not safe(s10):
            raise ValueError("invalid S10 leaf")
        for p in points(s10):
            s9_witnesses.add(canonical(s10 ^ (1 << p)))
    edges = 0
    for s8 in roots:
        if s8.bit_count() != 8 or canonical(s8) != s8 or not safe(s8):
            raise ValueError("invalid S8 witness")
        for p in points(s8):
            s7_covered.add(canonical(s8 ^ (1 << p)))
        for s9 in children(s8):
            if s9 not in s9_witnesses:
                raise ValueError(f"uncovered S9 {s9:032x}")
            edges += 1
    if not s7_children <= s7_covered or edges != 1046:
        raise ValueError("incomplete S6/S8 proof boundary")
    parents = {f"{canonical(ROOT ^ (1 << p)):032x}" for p in points(ROOT)}
    if parents != EXPECTED_S5:
        raise ValueError("S5 parent set mismatch")
    with Pool(processes=4) as pool:
        total_states = sum(pool.imap_unordered(verify_leaf, leaves, chunksize=1))
    if total_states != 1_028_621:
        raise ValueError("terminal state count mismatch")
    print("PASS 6-stone fixed-first LOSS; 49 S7, 29 S8 witnesses, 1046 S9 edges,"
          " 483 terminal S10 LOSS, 1028621 states; 6 S5 LOSS parents")

if __name__ == "__main__":
    main()
