"""Certify that one (x, c, e) class at a given size is unsatisfiable, with DRAT.

Generalises ``certify_equality_failure.py``: the size and the class are
arguments, so the same pipeline certifies

  * size h+2 class (1,1,0)  -> A(p) <= h+1
  * size h+1 the three classes (1,0,0), (0,1,0), (1,1,1) -> A(p) <= h
  * any other class

The CNF is rebuilt from scratch (``search_shape_class.build``), the solver's
DRAT is checked with the fixed incremental checker, and a receipt records every
hash.  ``--solve-with cadical`` uses the pysat CaDiCaL build, which is what the
existing h+2 certificates used.

Usage: certify_class_unsat.py --p 3719 --size 1860 --x 1 --c 1 --e 1 [--budget N]
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from edges_gen import run_edges  # noqa: E402
from search_shape_class import build  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

OUT = HERE / "output"
TMP = Path(tempfile.gettempdir())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, required=True)
    ap.add_argument("--size", type=int, required=True)
    ap.add_argument("--x", type=int, required=True)
    ap.add_argument("--c", type=int, required=True)
    ap.add_argument("--e", type=int, required=True)
    ap.add_argument("--budget", type=int, default=20_000_000)
    ap.add_argument("--tag", default=None)
    args = ap.parse_args()
    p, h, size = args.p, (args.p - 1) // 2, args.size
    tag = args.tag or f"x{args.x}c{args.c}e{args.e}"
    dest = OUT / f"cert-{p}-{size}-{tag}"
    dest.mkdir(parents=True, exist_ok=True)
    checker_src = HERE / "drat_check_incremental.cpp"
    checker = TMP / "drat_inc_cert.exe"
    if not checker.exists():
        subprocess.run(["g++", "-O2", "-std=c++17", str(checker_src), "-o", str(checker)],
                       check=True)
    edges = run_edges(p)
    clauses, nv, kept = build(p, edges, args.x, args.c, args.e)
    print(f"p={p} h={h} size={size} class=({args.x},{args.c},{args.e}) "
          f"vars={nv} clauses={len(clauses)} kept={kept}", flush=True)
    cnf = dest / f"a{p}_{size}_{tag}.cnf"
    with cnf.open("w", encoding="ascii", newline="\n") as f:
        f.write(f"p cnf {nv} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")
    solver = Cadical195(bootstrap_with=clauses, with_proof=True)
    solver.conf_budget(args.budget)
    t0 = time.time()
    res = solver.solve_limited()
    proof = solver.get_proof() if res is False else None
    solver.delete()
    solve_s = time.time() - t0
    print(f"solve={res} secs={solve_s:.1f} proof_lines={len(proof) if proof else 0}",
          flush=True)
    record = {"p": p, "h": h, "size": size, "class": [args.x, args.c, args.e],
              "vars": nv, "clauses": len(clauses), "kept_edges": kept,
              "sat": res, "unknown": res is None, "solve_seconds": round(solve_s, 1),
              "cnf_sha256": sha256(cnf)}
    if proof:
        pf = dest / f"a{p}_{size}_{tag}.drat"
        pf.write_text("\n".join(proof) + "\n", encoding="ascii")
        t1 = time.time()
        chk = subprocess.run([str(checker), str(cnf), str(pf)], capture_output=True, text=True)
        check_s = time.time() - t1
        out = chk.stdout.strip().splitlines()
        record.update({"proof_lines": len(proof), "proof_sha256": sha256(pf),
                       "checker_rc": chk.returncode,
                       "checker_last_line": out[-1] if out else chk.stderr.strip()[:200],
                       "verified": chk.returncode == 0 and bool(out) and "VERIFIED" in out[-1],
                       "check_seconds": round(check_s, 1)})
        print(f"verified={record['verified']} check_secs={check_s:.1f}", flush=True)
        if record["verified"]:
            with gzip.open(dest / f"a{p}_{size}_{tag}.drat.gz", "wb", compresslevel=6) as g:
                g.write(pf.read_bytes())
            pf.unlink()
            record["conclusion"] = f"A({p}) <= {size - 1}"
    (dest / "receipt.json").write_text(json.dumps(record, indent=2) + "\n",
                                       encoding="utf-8", newline="\n")
    print("done", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
