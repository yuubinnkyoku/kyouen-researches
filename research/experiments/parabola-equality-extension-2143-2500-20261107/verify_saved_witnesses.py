"""Feed the saved 2143..2500 witnesses to the independent generic-4x4 verifier.

The verifier (``frontier-geometry-2026-10-05/verify_witnesses.cpp``) enumerates
every selected triple and the unique fourth point allowed by the proven
quartic/Vandermonde congruence, then evaluates a generic 4x4 Leibniz
determinant.  It never imports the search-side 3x3 determinant.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

TMP = Path(tempfile.gettempdir()) / "kyouen-parabola"
TMP.mkdir(parents=True, exist_ok=True)


def main() -> int:
    witness_json, verifier, audit_out = sys.argv[1], sys.argv[2], sys.argv[3]
    all_records = json.loads(Path(witness_json).read_text(encoding="utf-8"))
    records = [r for r in all_records if r["attained"]]
    skipped = [r["p"] for r in all_records if not r["attained"]]
    assert records, "no witnesses"
    lines = []
    for rec in records:
        assert rec["safe_by_edges"], rec
        assert len(rec["parameters"]) == rec["size"] == rec["want"], rec
        lines.append(f'{rec["p"]} {rec["size"]} ' + " ".join(map(str, rec["parameters"])))
    inp = TMP / "witness_input.txt"
    inp.write_text("\n".join(lines) + "\n", encoding="ascii")
    out = Path(audit_out)
    with inp.open("r", encoding="ascii") as fin, out.open("w", encoding="ascii") as fout:
        proc = subprocess.run([verifier, "--modular-filter"], stdin=fin,
                              stdout=fout, stderr=subprocess.STDOUT)
    rows = [line.split() for line in out.read_text(encoding="ascii").splitlines() if line.strip()]
    print(f"records={len(records)} verified={len(rows)} rc={proc.returncode} skipped={skipped}")
    if proc.returncode != 0 or len(rows) != len(records):
        print("VERIFIER FAILED")
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
