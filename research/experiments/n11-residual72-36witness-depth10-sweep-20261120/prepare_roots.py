#!/usr/bin/env python3
"""Rebuild the 36-root sweep input from the pinned K1075 witness_full record."""
import collections, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SOURCE = REPO / "research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json"
EXPECTED = "49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa"

raw = SOURCE.read_bytes()
actual = hashlib.sha256(raw).hexdigest()
assert actual == EXPECTED, (actual, EXPECTED)
data = json.loads(raw)


def points(mask):
    return [p for p in range(121) if (mask >> p) & 1]


def transform(mask, t):
    out = 0
    for p in points(mask):
        x, y = p % 11, p // 11
        if t == 0: X, Y = x, y
        elif t == 1: X, Y = 10 - y, x
        elif t == 2: X, Y = 10 - x, 10 - y
        elif t == 3: X, Y = y, 10 - x
        elif t == 4: X, Y = 10 - x, y
        elif t == 5: X, Y = x, 10 - y
        elif t == 6: X, Y = y, x
        else: X, Y = 10 - y, 10 - x
        out |= 1 << (11 * Y + X)
    return out


def canon(mask):
    return min(transform(mask, t) for t in range(8))


def hx(mask):
    return f"{mask:032x}"

residual = set(data["base_state"]["residual_row_hex"])
witness = data["witness_full"]
assert len(residual) == 72
assert len(witness) == 36
roots = []
row_use = collections.Counter()
seen = set()
for entry in witness:
    root_hex = entry["root"]
    root = int(root_hex, 16)
    assert len(root_hex) == 32
    assert root_hex not in seen
    seen.add(root_hex)
    assert root.bit_count() == 7
    assert canon(root) == root
    assert entry["safe"] is True
    rows = sorted(entry["rows"])
    assert sorted(entry["covered"]) == rows
    assert len(rows) == 2
    lo = root & -root
    bit = lo.bit_length() - 1
    child = root - lo
    deletion_orbit = {hx(canon(root ^ (1 << p))) for p in points(root)}
    assert set(rows) <= deletion_orbit, (root_hex, deletion_orbit, rows)
    assert all(int(r, 16).bit_count() == 6 and canon(int(r, 16)) == int(r, 16) for r in rows)
    for row in rows:
        row_use[row] += 1
    roots.append({
        "root": root_hex,
        "child": hx(child),
        "bit": bit,
        "pcount": 7,
        "rows": rows,
        "safe": True,
    })
assert set(row_use) == residual
assert all(row_use[r] == 1 for r in residual)
assert sum(row_use.values()) == 72
roots.sort(key=lambda x: x["root"])
(HERE / "roots.json").write_text(json.dumps(roots, indent=1) + "\n", encoding="utf-8")
(HERE / "residual72.json").write_text(json.dumps(sorted(residual), indent=1) + "\n", encoding="utf-8")
print(json.dumps({
    "source_sha256": actual,
    "roots": len(roots),
    "residual_rows": len(residual),
    "covered_memberships": sum(row_use.values()),
    "stranded_rows": len(residual - set(row_use)),
    "duplicate_coverage_rows": sum(1 for n in row_use.values() if n != 1),
    "roots_sha256": hashlib.sha256((HERE / "roots.json").read_bytes()).hexdigest(),
    "residual_sha256": hashlib.sha256((HERE / "residual72.json").read_bytes()).hexdigest(),
}, indent=2))
