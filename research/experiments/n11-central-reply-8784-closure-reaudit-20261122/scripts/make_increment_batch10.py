#!/usr/bin/env python3
"""Batch 10 (class 8784, Part X) -> 52-LOSS increment generator (fail-closed).

Sources the published batch-10 raw outputs (p1/p2 per key, chunk commits
7b8790ab / 736a4f11 / 354524de) and the published input/batch-keys.json
(sha256 a1401ee2...), then validates every row fail-closed:

* the pinned-replica rule gate line (`forbidden quadruples: 95670`) present
  in every raw file (both passes),
* the row schema `replay,<id>,<stones>,<legal>,<is_or>,<budget>,<result>,
  <nodes>,<wall>,<lo>,<hi>` with stones==5, is_or==0, budget==15,000,000,
* (budget,result,nodes) identical across the two passes (2-pass node-exact),
* result==2 (LOSS) for every row (batch 10 has no WIN, no exhaustion),
* legal and (lo,hi) matching the published batch-keys.json row.

Emits `s5verdict,<lo>,<hi>,5,2,<nodes>` rows in probe_order. Any violation
aborts rc=1 with NO output (fail-closed). Nodes are bookkeeping, never
verdicts; no coverage/closure/root claim; 11x11 remains UNKNOWN.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

QUADS = "# forbidden quadruples: 95670"
BUDGET = 15000000
SCHEMA = "n11-centralreply-closure-class8784-batch-input-v1"


def fail(msg: str):
    print(f"GATE FAILED: {msg}", file=sys.stderr)
    raise SystemExit(1)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_raw(path: Path, key_id: str, pass_name: str) -> dict:
    text = path.read_text(encoding="utf-8")
    if QUADS not in text:
        fail(f"rule gate line missing in {key_id} {pass_name}")
    line = next((l for l in text.splitlines() if l.startswith("replay,")), None)
    if line is None:
        fail(f"no replay row in {key_id} {pass_name}")
    f = line.split(",")
    if len(f) != 11:
        fail(f"bad field count in {key_id} {pass_name}: {line}")
    if f[0] != "replay":
        fail(f"bad prefix in {key_id} {pass_name}")
    try:
        return {
            "stones": int(f[2]), "legal": int(f[3]), "is_or": int(f[4]),
            "budget": int(f[5]), "result": int(f[6]), "nodes": int(f[7]),
            "lo": f[9], "hi": f[10],
        }
    except ValueError as e:
        fail(f"non-numeric field in {key_id} {pass_name}: {e}")


def main():
    if len(sys.argv) != 4:
        print("usage: make_increment_batch10.py <raw_dir> <batch_keys.json> <out.cache>")
        raise SystemExit(2)
    raw_dir = Path(sys.argv[1])
    keys_path = Path(sys.argv[2])
    out_path = Path(sys.argv[3])

    keys = json.loads(keys_path.read_text(encoding="utf-8"))
    if keys.get("schema") != SCHEMA:
        fail(f"batch-keys schema {keys.get('schema')!r} != {SCHEMA!r}")
    if keys.get("class_index") != 8784:
        fail(f"class_index {keys.get('class_index')} != 8784")
    if keys.get("budget") != BUDGET:
        fail(f"budget {keys.get('budget')} != {BUDGET}")
    rows_in = keys["keys"]
    if len(rows_in) != 52:
        fail(f"key count {len(rows_in)} != 52")

    orders = [k["probe_order"] for k in rows_in]
    if orders != sorted(orders) or len(set(orders)) != 52:
        fail("probe_order not strictly ascending/unique")

    lines = [
        "# n11 central-reply closure batch 10 increment (2026-11-22)",
        "# 52 rows: batch 10 class 8784 exact-S5 probe, experiment",
        "#   n11-centralreply-closure-class8784-batch10-20261122: 52/52 keys 2-pass",
        "#   node-exact LOSS verdicts at budget 15M, fresh cold, no WIN-HALT, no",
        "#   mismatch, no exhaustion. Consumed via fail-closed merge only (Part Y).",
    ]
    for k in rows_in:
        kid = k["key_id"]
        p1 = parse_raw(raw_dir / f"{kid}.p1.out", kid, "p1")
        p2 = parse_raw(raw_dir / f"{kid}.p2.out", kid, "p2")
        for tag, r in (("p1", p1), ("p2", p2)):
            if r["stones"] != 5:
                fail(f"{kid} {tag}: stones {r['stones']} != 5")
            if r["is_or"] != 0:
                fail(f"{kid} {tag}: is_or {r['is_or']} != 0")
            if r["budget"] != BUDGET:
                fail(f"{kid} {tag}: budget {r['budget']} != {BUDGET}")
            if r["legal"] != k["legal"]:
                fail(f"{kid} {tag}: legal {r['legal']} != keys {k['legal']}")
            if r["lo"] != str(k["lo"]) or r["hi"] != str(k["hi"]):
                fail(f"{kid} {tag}: key ({r['lo']}:{r['hi']}) != keys ({k['lo']}:{k['hi']})")
        if (p1["budget"], p1["result"], p1["nodes"]) != (p2["budget"], p2["result"], p2["nodes"]):
            fail(f"{kid}: 2-pass mismatch {p1} vs {p2}")
        if p1["result"] != 2:
            fail(f"{kid}: result {p1['result']} != 2 (LOSS); WIN/exhausted rows are never increment rows")
        lines.append(f"s5verdict,{k['lo']},{k['hi']},5,2,{p1['nodes']}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    keys_sha = sha256_file(keys_path)
    print(f"INCREMENT rows=52 out={out_path} sha256={sha256_file(out_path)}")
    print(f"keys_json_sha256={keys_sha} (expected a1401ee2769f3943f993527dd4934ce82e99c6d55ee27a13cf74b1b417148ebf)")
    if keys_sha != "a1401ee2769f3943f993527dd4934ce82e99c6d55ee27a13cf74b1b417148ebf":
        fail("batch-keys.json sha drift")


if __name__ == "__main__":
    main()
