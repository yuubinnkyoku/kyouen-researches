#!/usr/bin/env python3
"""Independent terminal verification of a new N11 original-first S8 LOSS.

The certificate lists one terminal-proved S10 LOSS witness for EVERY legal
canonical S9 child of the S8 root. Both solvers start with empty memo tables.
No frozen verdict cache, S8/S9 verdict, or incomplete df-pn result is used.
"""
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
ROOT = "000000100010a0011000000001004000"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# The first module uses the 3x3 integer circle determinant, the second
# an independently implemented 4x4 Bareiss determinant.
SOURCE = load("n11_s8_shared_source", EXP / "n11-s9-neighbor23-terminal-20261026" / "verify.py")
THREE, FOUR = SOURCE.THREE, SOURCE.FOUR


def read_certificate():
    lines = (HERE / "certificate.tsv").read_text(encoding="ascii").splitlines()
    need(lines[:3] == [
        "# n11-s8-loss-shared-target-v1",
        "# root " + ROOT,
        "# s9 s10_loss legal_s10_classes",
    ], "certificate header changed")
    need(len(lines) == 30, "certificate row count changed")
    rows = []
    for line in lines[3:]:
        cells = line.split()
        need(len(cells) == 3, "malformed certificate row")
        a, b, n = cells
        need(all(len(h) == 32 and set(h) <= set("0123456789abcdef")
                 for h in (a, b)), "malformed position key")
        need(n.isdecimal(), "malformed legal child count")
        rows.append((int(a, 16), int(b, 16), int(n)))
    need([r[0] for r in rows] == sorted({r[0] for r in rows}),
         "duplicate/unsorted S9 obligations")
    return rows


def boundary(rows, terminal=True):
    need(len(rows) == 27, "missing S9 obligation")
    root = int(ROOT, 16)
    witnesses = set()
    for geom in (THREE, FOUR):
        need(geom.safe(root) and geom.canonical(root) == root and
             root.bit_count() == 8, "invalid S8 root")
        children9 = SOURCE.children(geom, root)
        need(len(children9) == 27 and children9 == {r[0] for r in rows},
             "S8 universal S9 boundary incomplete")
        for s9, s10, count in rows:
            need(s9.bit_count() == 9 and geom.safe(s9) and
                 geom.canonical(s9) == s9, "invalid S9 obligation")
            actual10 = SOURCE.children(geom, s9)
            need(len(actual10) == count and s10 in actual10,
                 "illegal S10 witness or changed S9 boundary")
            need(s10.bit_count() == 10 and geom.safe(s10) and
                 geom.canonical(s10) == s10, "invalid S10 witness")
            witnesses.add(s10)
    need(len(witnesses) == 24, "distinct LOSS leaf boundary changed")
    if terminal:
        independent = []
        for geom in (THREE, FOUR):
            solve = SOURCE.terminal_solver(geom)
            counts = []
            for leaf in sorted(witnesses):
                outcome, new_states = solve(leaf)
                need(outcome is False, f"S10 LOSS witness refuted: {leaf:032x}")
                counts.append(new_states)
            independent.append(counts)
        need(independent[0] == independent[1],
             "independent per-leaf terminal search mismatch")
    parents7 = {THREE.canonical(root ^ (1 << p))
                for p in THREE.points(root)}
    need(len(parents7) == 8, "unexpected S7 parent orbit count")
    return {"s8_loss_root": ROOT, "s9_obligations": len(rows),
            "distinct_s10_loss_witnesses": len(witnesses),
            "s7_loss_witness_parents": [f"{p:032x}" for p in sorted(parents7)],
            "terminal_verified": terminal, "empty_board": "UNKNOWN"}


def verify(negative=False):
    rows = read_certificate()
    result = boundary(rows)
    if negative:
        tests = [
            rows[:-1],
            [rows[0]] + rows[:-1],
            [(rows[0][0], rows[0][0], rows[0][2])] + rows[1:],
            [(rows[0][0], rows[0][1], rows[0][2] + 1)] + rows[1:],
            [(rows[1][0], rows[0][1], rows[0][2])] + rows[1:],
        ]
        for bad in tests:
            try:
                boundary(bad, terminal=False)
            except ValueError:
                continue
            raise ValueError("tampered S8 LOSS certificate accepted")
    print(result)
    if negative:
        print("PASS five S8 LOSS certificate mutation rejections")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--negative", action="store_true")
    verify(ap.parse_args().negative)
