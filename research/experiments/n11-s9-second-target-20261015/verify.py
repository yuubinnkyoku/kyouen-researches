#!/usr/bin/env python3
"""Independent terminal-only S9 WIN and S9 LOSS witness verification."""
from pathlib import Path
import importlib.util
import argparse
import subprocess
import tempfile
if not __debug__:
    raise SystemExit("python -O forbidden")
ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
GEOM = ROOT / "research/experiments/n11-s7-fifth-terminal-20261015/fifth_verify_standalone.py"
CPP = ROOT / "research/experiments/n11-targeted-terminal-lift-20261015/scripts/solve_s10_candidates.cpp"
S9 = int("00000100910000001042100000000040", 16)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cpp", action="store_true")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("independent_geometry", GEOM)
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    rows = {}
    for line in (HERE / "terminal-leaves.tsv").read_text().splitlines():
        h, v, states, moves = line.split()
        assert h not in rows and v in ("WIN", "LOSS")
        rows[h] = (v, int(states), int(moves))
    assert len(rows) == 64
    assert sum(v == "LOSS" for v, _, _ in rows.values()) == 49
    assert g.safe(S9) and g.canonical(S9) == S9 and S9.bit_count() == 9
    children = {f"{m:032x}" for m in g.children(S9)}
    assert len(children) == 15 and children == {h for h, (v, _, _) in rows.items() if v == "WIN"}
    loss_parents = set()
    total_states = 0
    for h, (v, states, moves) in sorted(rows.items()):
        m = int(h, 16)
        assert m.bit_count() == 10 and g.safe(m) and g.canonical(m) == m
        loss, n, k = g.terminal_s10(m)
        assert ("LOSS" if loss else "WIN", n, k) == (v, states, moves), h
        total_states += states
        if loss:
            loss_parents.update(g.canonical(m ^ (1 << p)) for p in g.points(m))
    assert len(loss_parents) == 410 and S9 not in loss_parents
    s8parents = {g.canonical(S9 ^ (1 << p)) for p in g.points(S9)}
    assert len(s8parents) == 9 and all(g.safe(x) and x.bit_count() == 8 for x in s8parents)
    assert total_states == 7629
    if args.cpp:
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            (temp / "masks").write_text("".join(h + "\n" for h in sorted(rows)))
            subprocess.run(["g++", "-O3", "-std=c++20", str(CPP), "-o", str(temp / "solve")], check=True)
            subprocess.run([str(temp / "solve"), str(temp / "masks"), str(temp / "results")], check=True)
            actual = {}
            for line in (temp / "results").read_text().splitlines():
                h, v, states, moves = line.split()
                assert h not in actual
                actual[h] = (v, int(states), int(moves))
            assert actual == rows
    print("PASS: 64 terminal leaves; 49 LOSS, 15 WIN; 7629 states")
    print("PASS: S9 WIN with 15/15 children; 9 S8 WIN parents; 410 S9 LOSS parents")
    if args.cpp:
        print("PASS: independent C++ and Python exact results agree")

if __name__ == "__main__":
    main()
