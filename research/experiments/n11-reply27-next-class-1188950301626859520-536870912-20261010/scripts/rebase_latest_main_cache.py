"""Reconcile this experiment's direct S5 losses with the latest main cache."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board  # noqa: E402
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from s5_evidence_policy import quarantined_cache_keys  # noqa: E402

S4 = (1188950301626859520, 536870912)
LOCAL_LOSSES = {
    4: ((1152921504606851072, 537001986), 90, 4_519_790, "fourth"),
    5: ((1188950301626859520, 536870976), 90, 8_361_840, "fifth"),
    7: ((10412322338481635328, 536870912), 91, 2_569_967, "seventh"),
    8: ((1189091039115214848, 536870912), 92, 4_808_557, "eighth"),
    9: ((1765411053930283008, 536870912), 92, 4_785_007, "ninth"),
    10: ((1152921504606851072, 570425346), 93, 6_730_471, "tenth"),
}
UPSTREAM_LOSSES = [
    ((1152921504606851072, 536870946), 98,
     "first-15m-s5-1152921504606851072-536870946", 3_651_923),
    ((1188950301626860544, 536870912), 99,
     "second-15m-s5-1188950301626860544-536870912", 5_040_200),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def parse_cache(path: Path) -> tuple[str, dict[tuple[int, int], int]]:
    header = "# s5 verdict cache: n=11 schema=1"
    values: dict[tuple[int, int], int] = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line:
            continue
        if line.startswith("#"):
            header = line
            continue
        f = line.split(",")
        if len(f) != 6 or f[0] != "s5verdict" or int(f[3]) != 5:
            raise SystemExit(f"malformed cache row {rel(path)}:{line_no}")
        key, verdict = (int(f[1]), int(f[2])), int(f[4])
        if verdict not in (1, 2) or key in values and values[key] != verdict:
            raise SystemExit(f"invalid/conflicting cache row {rel(path)}:{line_no}")
        values[key] = verdict
    return header, values


def replay(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        rows = [row for row in csv.reader(stream) if row and row[0] == "replay"]
    if len(rows) != 1 or len(rows[0]) != 11:
        raise SystemExit(f"expected one replay row in {rel(path)}")
    return rows[0]


def main() -> None:
    base_path = ROOT / "research/experiments/n11-two-target-design-20261010/output/merged-exact-s5.cache"
    original_base_path = OUT / "current-exact-s5-after-probe-3.cache"
    local_final_path = OUT / "current-exact-s5-after-probe-9.cache"
    output_path = OUT / "current-exact-s5-after-probe-9-rebased-main.cache"
    receipt_path = OUT / "latest-main-cache-rebase.json"

    base_header, main_cache = parse_cache(base_path)
    _, original_base = parse_cache(original_base_path)
    _, local_final = parse_cache(local_final_path)
    local_delta = {key: value for key, value in local_final.items() if key not in original_base}
    main_delta = {key: value for key, value in main_cache.items() if key not in original_base}
    if len(original_base) != 5741 or len(local_final) != 5747 or len(local_delta) != 6:
        raise SystemExit("unexpected old-main continuation cache/delta")
    if len(main_cache) != 5743 or len(main_delta) != 2:
        raise SystemExit("unexpected current main cache/delta")
    if any(value != 2 for value in [*local_delta.values(), *main_delta.values()]):
        raise SystemExit("all incoming delta rows must be exact LOSS")
    if local_delta.keys() & main_delta.keys():
        raise SystemExit("same-key delta overlap requires explicit reconciliation")
    if set(original_base) - set(main_cache) or any(main_cache[key] != value for key, value in original_base.items()):
        raise SystemExit("latest main cache does not preserve the prior checkpoint base")

    upstream_audit_path = ROOT / "research/experiments/n11-two-target-design-20261010/output/probe-audit.json"
    upstream_audit = json.loads(upstream_audit_path.read_text(encoding="utf-8"))
    expected_upstream_keys = {item[0] for item in UPSTREAM_LOSSES}
    if (set(main_delta) != expected_upstream_keys
            or upstream_audit["merged_cache_sha256"] != sha(base_path)
            or upstream_audit["merged_cache_rows"] != len(main_cache)
            or upstream_audit["baseline_cache_sha256"] != sha(original_base_path)
            or upstream_audit["new_raw_exact"] != 2
            or upstream_audit["new_loss_s4_classes"] != 0
            or upstream_audit["new_win_s4_classes"] != 0):
        raise SystemExit("latest-main probe audit does not bind the exact cache and two LOSS rows")

    main_checkpoint = "f3c0c8ec265e034a3e69c03e6eee6d5d9a4a8e43"
    ancestry = subprocess.run(["git", "merge-base", "--is-ancestor", main_checkpoint, "HEAD"], cwd=ROOT)
    if ancestry.returncode != 0:
        raise SystemExit("main checkpoint f3c0c8ec is not an ancestor of HEAD")

    board = Board(11)
    parent_mask = S4[0] | (S4[1] << 64)
    children = set(board.children(parent_mask))
    geometry = json.loads((OUT / "geometric-cache-preflight.json").read_text(encoding="utf-8"))
    geometric_keys = {tuple(item["key"]) for item in geometry["s5_children"]}
    if len(children) != 109 or geometric_keys != {
            (mask & ((1 << 64) - 1), mask >> 64) for mask in children}:
        raise SystemExit("stored complete boundary differs from independent Board regeneration")

    evidence = []
    for suffix, (key, legal, nodes, word) in LOCAL_LOSSES.items():
        raw = OUT / f"probe-15m-{word}.csv"
        row = replay(raw)
        actual = tuple(map(int, (row[2], row[3], row[4], row[5], row[6], row[7], row[9], row[10])))
        if actual != (5, legal, 0, 15_000_000, 2, nodes, *key):
            raise SystemExit(f"local raw LOSS mismatch for {key}: {row}")
        receipt_path_local = OUT / f"merge-receipt-{word}.json"
        receipt = json.loads(receipt_path_local.read_text(encoding="utf-8"))
        if receipt["merged_verdict"] != "LOSS" or tuple(receipt["merged_key"]) != key:
            raise SystemExit(f"local merge receipt mismatch for {key}")
        mask = key[0] | (key[1] << 64)
        if (mask not in children or board.canonical(mask) != mask or mask.bit_count() != 5
                or board.legal(mask).bit_count() != legal):
            raise SystemExit(f"local direct LOSS fails independent S4/S5 geometry: {key}")
        evidence.append({"source": "local-continuation", "key": list(key), "legal_count": legal,
                         "raw": rel(raw), "raw_sha256": sha(raw),
                         "merge_receipt": rel(receipt_path_local), "nodes": nodes})

    upstream_exp = ROOT / "research/experiments/n11-two-target-design-20261010/output/raw"
    for key, legal, stem, nodes in UPSTREAM_LOSSES:
        raw = upstream_exp / f"{stem}.out.csv"
        input_path = upstream_exp / f"{stem}.input.csv"
        row = replay(raw)
        actual = tuple(map(int, (row[2], row[3], row[4], row[5], row[6], row[7], row[9], row[10])))
        if actual != (5, legal, 0, 15_000_000, 2, nodes, *key):
            raise SystemExit(f"latest-main raw LOSS mismatch for {key}: {row}")
        with input_path.open(newline="", encoding="utf-8-sig") as stream:
            input_row = next(csv.reader(stream))
        if tuple(map(int, (input_row[2], input_row[3], input_row[4], input_row[5]))) != (5, key[0], key[1], legal):
            raise SystemExit(f"latest-main input mismatch for {key}: {input_row}")
        mask = key[0] | (key[1] << 64)
        if (mask not in children or board.canonical(mask) != mask or mask.bit_count() != 5
                or board.legal(mask).bit_count() != legal):
            raise SystemExit(f"latest-main direct LOSS fails independent geometry: {key}")
        if main_cache.get(key) != 2:
            raise SystemExit(f"latest-main direct LOSS missing from main cache: {key}")
        evidence.append({"source": "f3c0c8ec-main", "key": list(key), "legal_count": legal,
                         "input": rel(input_path), "input_sha256": sha(input_path),
                         "raw": rel(raw), "raw_sha256": sha(raw), "nodes": nodes})

    quarantine = quarantined_cache_keys()
    merged = dict(main_cache)
    for key, verdict in local_delta.items():
        if key in quarantine or key in merged and merged[key] != verdict:
            raise SystemExit(f"quarantine or cache conflict on local delta {key}")
        if key in merged:
            raise SystemExit(f"unexpected duplicate local delta key {key}")
        merged[key] = verdict
    if set(merged) & quarantine:
        raise SystemExit("active quarantined key entered rebased cache")
    if len(merged) != 5749 or Counter(merged.values()) != Counter({1: 158, 2: 5591}):
        raise SystemExit("unexpected rebased cache size/verdict counts")

    if output_path.exists():
        _, existing_output = parse_cache(output_path)
        if existing_output != merged:
            raise SystemExit("existing partial rebase cache differs from the audited union")
    else:
        with output_path.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(base_header + "\n")
            for (lo, hi), verdict in sorted(merged.items()):
                stream.write(f"s5verdict,{lo},{hi},5,{verdict},0\n")
    target_counts = Counter(merged[key] if key in merged else 0 for key in geometric_keys)
    boundary = {"LOSS": target_counts[2], "WIN": target_counts[1], "UNKNOWN": target_counts[0]}
    if boundary != {"LOSS": 22, "WIN": 0, "UNKNOWN": 87}:
        raise SystemExit(f"unexpected rebased target boundary: {boundary}")
    receipt = {
        "schema": "n11-reply27-latest-main-cache-rebase-v1",
        "main_commit": main_checkpoint,
        "base_cache": {"path": rel(base_path), "sha256": sha(base_path), "rows": len(main_cache),
                       "verdict_counts": {"WIN": 158, "LOSS": 5585}},
        "base_cache_source_audit": {"path": rel(upstream_audit_path), "sha256": sha(upstream_audit_path),
                                     "new_exact_losses": upstream_audit["new_raw_exact"],
                                     "new_s4_loss_classes": upstream_audit["new_loss_s4_classes"]},
        "old_checkpoint_cache": {"path": rel(original_base_path), "sha256": sha(original_base_path),
                                 "rows": len(original_base)},
        "old_main_continuation_cache": {"path": rel(local_final_path), "sha256": sha(local_final_path),
                                        "rows": len(local_final), "new_exact_loss_delta": len(local_delta)},
        "latest_main_delta": [{"key": list(key), "verdict": "LOSS"} for key in sorted(main_delta)],
        "merged_evidence": evidence,
        "independent_geometry": {"source": "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py",
                                 "complete_s5_boundary": len(geometric_keys), "canonical_legal_edges_checked": 8},
        "quarantine_registry_sha256": sha(ROOT / "results/n11-s5-evidence-quarantine.json"),
        "conflicts": 0,
        "rebased_cache": {"path": rel(output_path), "sha256": sha(output_path), "rows": len(merged),
                          "verdict_counts": {"WIN": 158, "LOSS": 5591},
                          "target_s4_boundary": boundary},
    }
    if receipt_path.exists():
        previous = json.loads(receipt_path.read_text(encoding="utf-8"))
        if previous != receipt:
            raise SystemExit("existing rebase receipt differs from the audited latest-main union")
    else:
        receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"main_commit": main_checkpoint, "rows": len(merged), "target_boundary": boundary,
                      "cache_sha256": sha(output_path), "receipt_sha256": sha(receipt_path)}, sort_keys=True))


if __name__ == "__main__":
    main()
