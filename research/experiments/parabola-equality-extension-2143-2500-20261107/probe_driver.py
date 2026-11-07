"""Parabola equality probe with file-based IO.

Same reduction as ``parabola-equality-extension-20261016/scripts/probe_parabola.py``
(safe sets of size h+2 are exactly {0,d,p-d} plus one element of each other pair;
safety is the signed NAE3/4 + origin CNF of K0334).  The difference is that the
generator and cadical write to files instead of pipes, so the driver also runs
under a job runner that does not allow orphaned pipe handles.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/experiments/structural-lemmas-2026-10-02/checks"))
from parabola_half_bound import clauses_for_pair  # noqa: E402
from quadratic_modular_barrier import prime  # noqa: E402

TMP = Path(tempfile.gettempdir()) / "kyouen-parabola"
TMP.mkdir(parents=True, exist_ok=True)


def to_wsl(path: Path) -> str:
    p = Path(path).resolve()
    return "/mnt/" + p.drive.rstrip(":").lower() + str(p)[len(p.drive):].replace("\\", "/")


def run_gen(gen: str, p: int) -> list[tuple[int, int, int, int]]:
    out = TMP / f"edges_{p}.txt"
    with out.open("w", encoding="ascii") as f:
        subprocess.run([gen, str(p)], stdout=f, stderr=subprocess.DEVNULL,
                       check=True, stdin=subprocess.DEVNULL)
    return [tuple(map(int, line.split())) for line in out.read_text(encoding="ascii").splitlines()]


def cadical(cnf_text: str, tag: str, timeout: int = 60):
    cnf = TMP / f"_probe_{tag}.cnf"
    cnf.write_text(cnf_text, encoding="ascii")
    log = TMP / f"_probe_{tag}.log"
    try:
        with log.open("w", encoding="ascii") as f:
            subprocess.run(["wsl", "-d", "Ubuntu", "-u", "root", "--", "bash", "-c",
                            f"timeout {timeout} cadical --quiet {to_wsl(cnf)} < /dev/null"],
                           stdout=f, stderr=subprocess.STDOUT,
                           stdin=subprocess.DEVNULL, timeout=timeout + 60)
    except subprocess.TimeoutExpired:
        return None, set()
    text = log.read_text(encoding="ascii", errors="replace")
    if "s UNKNOWN" in text or "s SATISFIABLE" not in text and "s UNSATISFIABLE" not in text:
        return None, set()
    sat = "s SATISFIABLE" in text
    model: set[int] = set()
    if sat:
        for line in text.splitlines():
            if line.startswith("v "):
                for x in line[2:].split():
                    if x != "0":
                        v = int(x)
                        if v > 0:
                            model.add(v)
    return sat, model


def probe(p: int, gen: str, max_doubles: int, timeout_s: int = 60) -> dict:
    edges = run_gen(gen, p)
    h = (p - 1) // 2
    tried = []
    unknown = []
    for d in list(range(h, 0, -1))[:max_doubles]:
        clauses = clauses_for_pair(p, edges, d)
        body = "".join(" ".join(map(str, c)) + " 0\n" for c in clauses)
        cnf = f"p cnf {h} {len(clauses)}\n" + body
        sat, upper = cadical(cnf, f"{p}_{d}", timeout=timeout_s)
        tried.append(d)
        if sat is None:
            unknown.append(d)
            continue
        if sat:
            params = sorted([0, d, p - d] + [p - i if i in upper else i
                                             for i in range(1, h + 1) if i != d])
            selected = set(params)
            safe = (len(params) == h + 2 and len(set(params)) == h + 2
                    and not any(set(e) <= selected for e in edges))
            return {"p": p, "attained": True, "double_pair": d,
                    "parameters": params, "size": len(params), "want": h + 2,
                    "safe_by_edges": safe, "forbidden_edges": len(edges),
                    "clauses": len(clauses), "doubles_tried": tried}
    return {"p": p, "attained": False, "forbidden_edges": len(edges),
            "want": h + 2, "doubles_tried": tried,
            "unknown_timeouts": unknown, "status": "not_found_within_budget"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--generator", required=True)
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--end", type=int, required=True)
    ap.add_argument("--max-doubles", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=60)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    records = json.loads(out.read_text(encoding="utf-8")) if out.exists() else []
    done = {r["p"] for r in records}
    for p in range(args.start | 1, args.end + 1, 2):
        if not prime(p) or p in done:
            continue
        t0 = time.time()
        rec = probe(p, args.generator, args.max_doubles, args.timeout)
        rec["seconds"] = round(time.time() - t0, 2)
        records.append(rec)
        records.sort(key=lambda r: r["p"])
        out.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"p={p} attained={rec['attained']} d={rec.get('double_pair')} "
              f"size={rec.get('size')} sec={rec['seconds']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
