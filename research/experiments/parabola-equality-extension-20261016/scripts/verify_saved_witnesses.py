"""Feed probe witnesses to the independent generic-4x4 verifier."""
import json
import subprocess
import sys
from pathlib import Path

records = json.loads(Path(sys.argv[1]).read_text())
lines = []
for r in records:
    assert r["attained"] and r["safe_by_edges"], r
    lines.append(f'{r["p"]} {r["size"]} ' + " ".join(map(str, r["parameters"])))
inp = "\n".join(lines) + "\n"
out = subprocess.run([sys.argv[2], "--modular-filter"], input=inp,
                     capture_output=True, text=True)
print(out.stdout.strip())
if out.returncode != 0:
    print("VERIFIER FAILED rc=", out.returncode)
    print(out.stderr[-500:])
    sys.exit(1)
rows = [l.split() for l in out.stdout.strip().splitlines()]
print(f"records={len(records)} verified={len(rows)}")
assert len(rows) == len(records)
print("ALL PASS")
