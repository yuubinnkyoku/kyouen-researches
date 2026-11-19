#!/usr/bin/env python3
# Fail-closed assembly of the K1075 residual-72 36-root sweep.
import collections, hashlib, json, sys
from pathlib import Path

D = Path(__file__).resolve().parent
roots = json.loads((D / "roots.json").read_text())
residual = set(json.loads((D / "residual72.json").read_text()))
recs = []
for w in range(4):
    p = D / "output" / f"probe-records-w{w}.jsonl"
    if p.exists():
        recs.extend(json.loads(line) for line in p.read_text().splitlines() if line.strip())


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


gates = []
def gate(name, ok, detail):
    gates.append({"name": name, "pass": bool(ok), "detail": detail})
    if not ok:
        print("GATE FAIL:", name, detail)
        sys.exit(1)

by_root = {r["root"]: r for r in roots}
roots_sha = hashlib.sha256((D / "roots.json").read_bytes()).hexdigest()
residual_sha = hashlib.sha256((D / "residual72.json").read_bytes()).hexdigest()
runner_raw = (D / "runner_v17.ts").read_bytes()
runner_blob = hashlib.sha1(b"blob " + str(len(runner_raw)).encode() + b"\0" + runner_raw).hexdigest()
ok_recs = [r for r in recs if r.get("result") is not None and r.get("error") is None]
gate("roots-pin", roots_sha == "3904041ea40c4e7c419d437046358eac7b91d169782e8d64abac0c9b044f160f", {"sha256": roots_sha})
gate("residual72-pin", residual_sha == "78e3ee7a8092dbca23fa3bf41491fdc666ba73a2e62c23f3da7570430bf28f9b", {"sha256": residual_sha})
gate("runner-v17-blob-pin", runner_blob == "c132cc6425eee3feaeef1d697dd74f968cfedb59", {"git_blob": runner_blob})
gate("no-error-records", len(ok_recs) == len(recs), {"records": len(recs), "ok": len(ok_recs)})
keys = collections.Counter((r["root"], r["ordering"]) for r in ok_recs)
gate("partition-72", len(keys) == 72 and set(k[0] for k in keys) == set(by_root),
     {"unique_keys": len(keys), "roots": len(set(k[0] for k in keys))})
per_root = collections.defaultdict(dict)
dups = collections.defaultdict(list)
for r in ok_recs:
    per_root[r["root"]][r["ordering"]] = r
    dups[(r["root"], r["ordering"])].append(r["result"])
mism = sum(1 for vals in dups.values() if len(vals) > 1 and
           not all(v["nodes"] == vals[0]["nodes"] and v["loss"] == vals[0]["loss"]
                   and v["capped"] == vals[0]["capped"] for v in vals))
gate("duplicate-agreement", mism == 0,
     {"duplicate_keys": sum(1 for v in dups.values() if len(v) > 1), "mismatches": mism})
gate("both-orders", all(set(per_root[r]) == {"andclose1", "andclose0"} for r in by_root),
     {"roots": len(by_root)})
cap_bad = [(r["root"], r["ordering"]) for r in ok_recs if r["result"].get("capped")]
gate("uncapped", not cap_bad, {"capped": len(cap_bad)})
pil_bad = [r["root"] for r in ok_recs if not (r.get("control") and
           r["control"].get("control") == "pilot_d6" and
           r["control"].get("loss") is False and r["control"].get("nodes") == 3402)]
gate("pilot-d6", not pil_bad, {"expected_nodes": 3402, "failures": len(pil_bad)})
conflicts, cls = [], {}
total_nodes, max_probe = 0, None
for root in sorted(by_root):
    r1 = per_root[root]["andclose1"]["result"]
    r0 = per_root[root]["andclose0"]["result"]
    total_nodes += r1["nodes"] + r0["nodes"]
    for r in (r1, r0):
        if max_probe is None or r["nodes"] > max_probe["nodes"]:
            max_probe = {"root": root, **r}
    if r1["loss"] != r0["loss"]:
        conflicts.append(root)
        cls[root] = "ORDER-CONFLICT"
    else:
        cls[root] = "WIN7-D10" if r1["loss"] is True else "REFUTED-D10"
gate("order-consistency", not conflicts, {"conflicts": conflicts})

row_use = collections.Counter()
anatomy_bad = []
for root_hex, item in by_root.items():
    root = int(root_hex, 16)
    if (root.bit_count() != 7 or canon(root) != root or item.get("safe") is not True
        or hx(root - (root & -root)) != item["child"]
        or (root & -root).bit_length() - 1 != item["bit"]
        or item.get("pcount") != 7 or len(item["rows"]) != 2
        or any(int(row, 16).bit_count() != 6 or canon(int(row, 16)) != int(row, 16) for row in item["rows"])):
        anatomy_bad.append(root_hex)
        continue
    deleted = {hx(canon(root ^ (1 << p))) for p in points(root)}
    if not set(item["rows"]) <= deleted:
        anatomy_bad.append(root_hex)
    for row in item["rows"]:
        row_use[row] += 1
gate("root-anatomy", not anatomy_bad,
     {"roots": len(by_root), "bad": anatomy_bad[:5], "bad_count": len(anatomy_bad)})
gate("covered-rows-equal-residual72", set(row_use) == residual and all(row_use[r] == 1 for r in residual),
     {"covered": len(row_use), "residual": len(residual),
      "duplicate_or_missing": sum(1 for r in residual if row_use[r] != 1)})
gate("perfect-matching-36", len(roots) == 36 and sum(len(x["rows"]) for x in roots) == 72,
     {"roots": len(roots), "memberships": sum(len(x["rows"]) for x in roots)})

dist = collections.Counter(cls.values())
out = {
  "schema": "n11-residual72-36freshwitness-depth10-sweep-20261120-v1",
  "date": "2026-11-20",
  "protocol": {"runner": "class4_child1_runner_v17.ts git blob c132cc6425eee3feaeef1d697dd74f968cfedb59",
               "depth": 10, "cap": 30000000,
               "orderings": ["andclose1", "andclose0"],
               "pilot_d6_control": {"loss": False, "nodes": 3402},
               "child_rule": "RAW integer hex, child = root - lowest set bit; canon_hex forbidden"},
  "inputs": {"main_commit": "412d75b93d14752f528c4fa4c6b5d472a4ca5ac8",
             "k1075_sha256": "49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa",
             "roots_sha256": roots_sha,
             "residual72_sha256": residual_sha, "runner_git_blob": runner_blob},
  "classification": {root: cls[root] for root in sorted(by_root)},
  "summary": {"roots": 36, "probes": 72, "win": dist.get("WIN7-D10", 0),
              "refuted": dist.get("REFUTED-D10", 0), "capped": 0,
              "order_conflicts": len(conflicts), "total_nodes": total_nodes,
              "max_probe": max_probe, "avg_nodes_per_probe": total_nodes // 72},
  "gates": gates,
  "interpretation_guard": [
    "REFUTED-D10 is not a LOSS proof; it means no first-mover win within depth 10 under runner v17.",
    "WIN7-D10 roots are certificate extraction candidates only; rows are closed only after certificate verification and receipt fold.",
    "This sweep is row-coverage candidate bookkeeping and says nothing about the game-theoretic values of rows, two-stone roots, or the empty board.",
    "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
  ]
}
blob = json.dumps(out, indent=1, sort_keys=True) + "\n"
(D / "output" / "residual72-36freshwitness-depth10-sweep-20261120.json").write_text(blob, encoding="utf-8")
print("all gates pass:", all(g["pass"] for g in gates))
print(json.dumps(out["summary"], indent=1))
print("sha256:", hashlib.sha256(blob.encode()).hexdigest())
