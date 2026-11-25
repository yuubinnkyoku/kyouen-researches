#!/usr/bin/env python3
"""Freeze a stratified batch of untried S6 children for the final 15M-unknown S5."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s4-boundary-direct-20261012"
CURRENT = EXP / "output/current-exact-s5.cache"
FRONTIER = EXP / "output/frontier-after-ninth-batch.json"
HISTORY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/history.json"
GEOMETRY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
BUILD = EXP / "input/solver-build.json"
S5 = (1152921504607899649, 536870912)
DEFAULT_LIMIT = 1_000_000


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def freeze(path: Path, content: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != content:
            raise ValueError(f"refusing to overwrite frozen artifact: {path}")
    else:
        path.write_bytes(content)


def jbytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-number", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--budget", type=int, default=DEFAULT_LIMIT,
                        help="per-root S6 budget; advance UNKNOWN only to a new budget")
    parser.add_argument("--prior-run", type=Path, action="append", default=[])
    args = parser.parse_args()
    if args.batch_number < 1 or not 1 <= args.batch_size <= 16 or args.budget not in (1_000_000, 2_000_000, 15_000_000):
        raise ValueError("batch number/size/budget outside the documented K0374 comparison schedule")

    sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
    from s5_evidence_policy import quarantined_cache_keys
    sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
    from independent import Board
    board = Board(11)
    mask = S5[0] | (S5[1] << 64)
    if mask.bit_count() != 5 or board.canonical(mask) != mask:
        raise ValueError("final S5 root is not canonical")
    # Read the current S5 cache and require the one unresolved target root to be absent.
    cache = set()
    with CURRENT.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if not row or row[0].strip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"malformed current S5 cache row: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            key = (lo, hi)
            if stones != 5 or verdict not in (1, 2) or nodes < 0 or key in quarantined_cache_keys():
                raise ValueError(f"unsafe current S5 cache row: {row}")
            cache.add(key)
    if S5 in cache:
        raise ValueError("the selected S5 is already exact; do not run S6 split")

    s6_children = sorted((child & ((1 << 64) - 1), child >> 64) for child in board.children(mask))
    if len(s6_children) != len(set(s6_children)) or len(s6_children) != 98:
        raise ValueError(f"independent S6 boundary mismatch: expected 98 unique children, got {len(s6_children)}")
    history = {(r["stones"], *r["key"]): r for r in json.loads(HISTORY.read_text(encoding="utf-8"))}
    saved_exact = {}
    prior = []
    for key in s6_children:
        row = history.get((6, *key), {})
        verdict = int(row.get("verdict", 0))
        if verdict in (1, 2):
            saved_exact[key] = verdict
        observations = row.get("observations", [])
        for obs in observations:
            if obs.get("budget", 0) > 0:
                prior.append({"key": list(key), "budget": int(obs["budget"]),
                              "verdict": int(obs["verdict"]), "nodes": int(obs["nodes"])})
    saved_counts = Counter(saved_exact.values())
    if saved_counts[2]:
        raise ValueError("a saved S6 LOSS witness already proves this S5 LOSS; materialize that audited evidence")
    if saved_counts[1] == len(s6_children):
        raise ValueError("all S6 children already WIN; derive S5 WIN and reject this S4 candidate")

    prior_paths = [p if p.is_absolute() else ROOT / p for p in args.prior_run]
    prior_runs = [json.loads(p.read_text(encoding="utf-8")) for p in prior_paths]
    prior_records = [r for doc in prior_runs for r in doc.get("runs", [])]
    prior_by_key_budget = {(tuple(r["key"]), int(r["budget"])): r for r in prior_records}
    if len(prior_by_key_budget) != len(prior_records):
        raise ValueError("duplicate prior S6 root/budget in run manifests")

    resolved_win = set(saved_exact) | {tuple(r["key"]) for r in prior_records if r["verdict"] == "WIN"}
    resolved_loss = {tuple(k) for k, v in saved_exact.items() if v == 2} | {tuple(r["key"]) for r in prior_records if r["verdict"] == "LOSS"}
    if resolved_loss:
        raise ValueError("an exact S6 LOSS is already present; derive the S5 LOSS instead of more S6 work")
    # Exact children are resolved. Prior UNKNOWNs may be escalated only at a
    # distinct budget; a same-root/same-budget repeat was rejected above.
    attempted = {tuple(r["key"]) for r in prior_records}
    attempted.update(tuple(row["key"]) for row in prior if row["verdict"] in (1, 2))
    unresolved_prior = {tuple(r["key"]) for r in prior_records if r["verdict"] == "UNKNOWN"}
    unresolved_prior.update(tuple(row["key"]) for row in prior if row["verdict"] == 0)
    # A prior UNKNOWN at a smaller budget may coexist with a later exact result;
    # exact evidence supersedes it. Opposite exact values are rejected by the
    # per-root audit before they can be merged.
    available = []
    for key in s6_children:
        if key in resolved_win or key in resolved_loss:
            continue
        prior_for_key = [r for r in prior_records if tuple(r["key"]) == key]
        saved_prior = [r for r in prior if tuple(r["key"]) == key]
        had_unknown = any(r["verdict"] == "UNKNOWN" for r in prior_for_key) or any(r["verdict"] == 0 for r in saved_prior)
        if key in attempted and not (had_unknown and args.budget not in {int(r["budget"]) for r in prior_for_key + saved_prior}):
            continue
        if key in unresolved_prior and args.budget in {int(r["budget"]) for r in prior_for_key + saved_prior}:
            continue
        m = key[0] | (key[1] << 64)
        available.append({"key": key, "legal": board.legal(m).bit_count()})
    if not available:
        raise ValueError("no untried S6 children remain at this budget; inspect UNKNOWNs for one-step escalation")
    available.sort(key=lambda r: (r["legal"], r["key"]))
    count = min(args.batch_size, len(available))
    if count == 1:
        positions = [(len(available) - 1) // 2]
    else:
        positions = sorted(set(round(i * (len(available) - 1) / (count - 1)) for i in range(count)))
    picked = [available[i] for i in positions]

    build = json.loads(BUILD.read_text(encoding="utf-8"))
    solver = ROOT / build["binary_path"]
    if sha(solver) != build["binary_sha256"]:
        raise ValueError("pinned solver binary hash mismatch")
    start = (args.batch_number - 1) * 16
    selected = []
    for offset, row in enumerate(picked):
        seq = start + offset
        lo, hi = row["key"]
        input_path = EXP / f"input/s6-{seq:03}.csv"
        content = f"target,{seq},6,{lo},{hi},{row['legal']},0,1,0,0,0\n".encode("utf-8")
        freeze(input_path, content)
        selected.append({
            "sequence": seq, "key": list(row["key"]), "stones": 6, "is_or": 1,
            "legal": row["legal"], "budget": args.budget,
            "input_path": str(input_path.relative_to(ROOT)), "input_sha256": sha(input_path),
            "reason": "stratified legal-count quantile among untried S6 children; S6 OR at fixed-player view; exact LOSS witness closes parent S5 AND as LOSS",
        })
    selection = {
        "schema": "n11-s4-boundary-final-s5-s6-split-selection-v1",
        "source_main_commit": "1bdd30b71adaf8f476a98922f1b454bdd369feb3",
        "parent_s5": list(S5), "parent_s5_direct_budget": 15_000_000,
        "parent_s5_direct_unknown_nodes": 15_000_000,
        "s6_child_count": len(s6_children), "saved_s6_exact_counts": {"WIN": saved_counts[1], "LOSS": saved_counts[2]},
        "saved_s6_exact_keys": [{"key": list(k), "verdict": v} for k, v in sorted(saved_exact.items())],
        "prior_s6_raw_observation_count": len(prior), "prior_s6_unknown_by_budget": dict(sorted(Counter(str(r["budget"]) for r in prior if r["verdict"] == 0).items())),
        "exact_cache": {"path": str(CURRENT.relative_to(ROOT)), "sha256": sha(CURRENT), "rows": len(cache)},
        "geometry": {"path": str(ROOT.joinpath("research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py").relative_to(ROOT)),
                     "sha256": sha(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py")},
        "history": {"path": str(HISTORY.relative_to(ROOT)), "sha256": sha(HISTORY)},
        "frontier": {"path": str(FRONTIER.relative_to(ROOT)), "sha256": sha(FRONTIER)},
        "prior_run_manifest_sha256s": [sha(p) for p in prior_paths],
        "solver": {"binary_path": build["binary_path"], "binary_sha256": build["binary_sha256"],
                   "source_sha256": build["source_sha256"], "frozen_build_manifest": str((EXP / "input/solver-build.json").relative_to(ROOT)),
                   "mode": "fresh DFPN process per S6 child; no profile; exact-order=count", "budget": args.budget},
        "selection_rule": "K0374-style direct S6 split: reuse exact saved S6; probe untried S6 at one fixed per-root budget with legal-count coverage; do not repeat same root/budget; stop immediately on one S6 LOSS witness; escalate only unresolved roots to a different documented budget after first-pass yield review",
        "selected": selected,
    }
    word = {1:"first",2:"second",3:"third",4:"fourth",5:"fifth",6:"sixth",7:"seventh",8:"eighth",9:"ninth",10:"tenth",11:"eleventh",12:"twelfth",13:"thirteenth",14:"fourteenth",15:"fifteenth"}.get(args.batch_number)
    if word is None:
        raise ValueError("S6 batch number must be <= 10")
    path = EXP / f"input/s6-{word}-batch-selection.json"
    freeze(path, jbytes(selection))
    print(json.dumps({"selection": str(path.relative_to(ROOT)), "selection_sha256": sha(path),
                      "parent_s5": list(S5), "saved_s6": {"WIN": saved_counts[1], "LOSS": saved_counts[2]},
                      "untried_s6": len(available), "budget": args.budget,
                      "selected": [{"sequence": r["sequence"], "key": r["key"], "legal": r["legal"]} for r in selected]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
