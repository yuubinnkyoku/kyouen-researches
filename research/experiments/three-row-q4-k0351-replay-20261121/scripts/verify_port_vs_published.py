#!/usr/bin/env python3
"""Compare the Node port sweep against the published (pinned) K0351 output.

Gate criteria per width m:
  G1 three_sets equal
  G2 cover_exists equal
  G3 candidates counter exact match (both kinds)
  G4 witnesses equal (null-ness; coordinates when present)
  G5 port must not report a cover the published run excluded, and vice versa

Usage: python3 verify_port_vs_published.py SWEEP.jsonl [SWEEP2.jsonl ...] > out.json
"""
import json
import sys

PUBLISHED = "q34_exact_threshold.json"


def main():
    pub = json.load(open(PUBLISHED, encoding="utf-8"))
    pub_cases = {c["m"]: c for c in pub["cases"]}
    port = {}
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                if rec["m"] in port:
                    raise SystemExit(f"duplicate width {rec['m']} across sweep files")
                port[rec["m"]] = rec

    rows, all_ok = [], True
    for m in sorted(port):
        p, q = port[m], pub_cases.get(m)
        checks = {}
        if q is None:
            checks["published_record"] = False
        else:
            checks = {
                "three_sets": p["three_sets"] == q["three_sets"],
                "cover_exists": p["cover_exists"] == q["cover_exists"],
                "candidates_exact": p["candidates"] == q["candidates"],
                "witnesses_equal": p["witnesses"] == q["witnesses"],
            }
        ok = all(checks.values())
        all_ok = all_ok and ok
        rows.append({
            "m": m,
            "port_candidates": p["candidates"],
            "port_cover_exists": p["cover_exists"],
            "port_three_sets": p["three_sets"],
            "checks": checks,
            "ok": ok,
        })

    out = {
        "published_threshold_file": PUBLISHED,
        "published_exact_threshold": pub["exact_threshold"],
        "published_analytic_tail": pub["analytic_tail"],
        "widths_checked": len(rows),
        "widths_ok": sum(1 for r in rows if r["ok"]),
        "all_ok": all_ok,
        "rows": rows,
    }
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
