#!/usr/bin/env python3
"""Independently audit S6 split raws and exact AND propagation to their S5 parent."""
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
HISTORY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/history.json"
S5 = (1152921504607899649, 536870912)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_replay(path: Path) -> dict:
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if row and row[0] == "replay":
                rows.append(row)
    if len(rows) != 1 or len(rows[0]) != 11:
        raise ValueError(f"expected one replay row in {path}")
    row = rows[0]
    return {"row_sequence": int(row[1]), "stones": int(row[2]), "legal": int(row[3]),
            "is_or": int(row[4]), "budget": int(row[5]), "verdict_code": int(row[6]),
            "nodes": int(row[7]), "seconds": float(row[8]), "key": [int(row[9]), int(row[10])]}


def audit_saved_history(history: list, selection: dict, children: dict, board,
                        raw_overrides: dict[tuple[int, int], dict] | None = None) -> list[dict]:
    rows = {(r["stones"], tuple(r["key"])): r for r in history}
    sources = []
    used_overrides = set()
    for entry in selection["saved_s6_exact_keys"]:
        key = tuple(entry["key"])
        record = rows.get((6, key))
        if not record or record["verdict"] != entry["verdict"] or record["verdict"] not in (1, 2):
            raise ValueError(f"saved exact S6 history mismatch for {key}")
        observations = [o for o in record.get("observations", []) if o.get("verdict") == record["verdict"]]
        if not observations:
            raise ValueError(f"saved exact S6 lacks matching raw observation: {key}")
        obs = observations[0]
        historical_path = obs["path"]
        override = (raw_overrides or {}).get(key)
        if override:
            if override["historical_path"].replace("\\", "/") != historical_path.replace("\\", "/"):
                raise ValueError(f"saved S6 raw override does not match history path for {key}")
            raw = resolve(Path(override["raw_path"]))
            if sha(raw) != override["raw_sha256"]:
                raise ValueError(f"saved S6 raw override SHA-256 mismatch for {key}: {raw}")
            original = resolve(Path(historical_path))
            if original.is_file() and sha(original) != sha(raw):
                raise ValueError(f"saved S6 raw override is not byte-identical to history source for {key}")
            used_overrides.add(key)
        else:
            raw = resolve(Path(historical_path))
        if not raw.is_file():
            raise FileNotFoundError(f"saved exact S6 source missing: {raw}")
        allrows = []
        with raw.open(encoding="utf-8-sig", newline="") as f:
            for line_no, row in enumerate(csv.reader(f), 1):
                if row and row[0] == "replay":
                    allrows.append((line_no, row))
        matching = [(line, row) for line, row in allrows
                    if len(row) == 11 and (int(row[9]), int(row[10])) == key]
        if len(matching) != 1:
            raise ValueError(f"saved raw does not have unique S6 key {key}: {raw}")
        line, row = matching[0]
        parsed = {"stones": int(row[2]), "legal": int(row[3]), "is_or": int(row[4]),
                  "budget": int(row[5]), "verdict": int(row[6]), "nodes": int(row[7]),
                  "key": [int(row[9]), int(row[10])], "line": line}
        mask = key[0] | (key[1] << 64)
        legal = board.legal(mask).bit_count()
        if (line != obs["row"] or tuple(key) not in children or board.canonical(mask) != mask
                or parsed["stones"] != 6 or parsed["is_or"] != 1 or parsed["legal"] != legal
                or parsed["legal"] != obs["legal"] or parsed["budget"] != obs["budget"]
                or parsed["verdict"] != record["verdict"] or parsed["nodes"] != obs["nodes"]):
            raise ValueError(f"saved S6 raw/history/geometry mismatch for {key}: {parsed}")
        sources.append({"key": list(key), "verdict": "WIN" if record["verdict"] == 1 else "LOSS",
                        "legal": legal, "budget": obs["budget"], "nodes": obs["nodes"],
                        "historical_raw_path": historical_path,
                        "raw_path": override["raw_path"] if override else historical_path,
                        "raw_line": line, "raw_sha256": sha(raw)})
    if raw_overrides and used_overrides != set(raw_overrides):
        raise ValueError(f"unused saved S6 raw overrides: {sorted(set(raw_overrides) - used_overrides)}")
    return sources


def read_cache(path: Path) -> set[tuple[int, int]]:
    keys = set()
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"malformed current exact S5 cache row: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            if stones != 5 or verdict not in (1, 2) or nodes < 0:
                raise ValueError(f"invalid current cache row: {row}")
            keys.add((lo, hi))
    return keys


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selection", type=Path, required=True)
    ap.add_argument("--run-manifest", type=Path, required=True)
    ap.add_argument("--worker-cache", type=Path)
    ap.add_argument("--receipt", type=Path)
    ap.add_argument("--saved-raw-overrides", type=Path,
                    help="Optional path/hash-verified relocations for saved raw files recorded outside Git")
    args = ap.parse_args()
    selection_path, run_path = resolve(args.selection), resolve(args.run_manifest)
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    run = json.loads(run_path.read_text(encoding="utf-8"))
    if run.get("selection_sha256") != sha(selection_path):
        raise ValueError("run manifest is not bound to the frozen S6 selection")
    override_path = resolve(args.saved_raw_overrides) if args.saved_raw_overrides else None
    override_doc = None
    raw_overrides = None
    if override_path:
        override_doc = json.loads(override_path.read_text(encoding="utf-8"))
        if override_doc.get("schema") != "n11-reply27-saved-s6-raw-relocations-v1":
            raise ValueError("unexpected saved S6 raw relocation manifest schema")
        if override_doc.get("source_history_sha256") != selection["history"]["sha256"]:
            raise ValueError("raw relocation manifest is not bound to the frozen saved-history hash")
        raw_overrides = {}
        for row in override_doc.get("relocations", []):
            key = tuple(row["key"])
            if key in raw_overrides:
                raise ValueError(f"duplicate saved S6 raw relocation key: {key}")
            raw_overrides[key] = row
    build = json.loads(resolve(Path(selection["solver"]["frozen_build_manifest"])).read_text(encoding="utf-8"))
    binary = resolve(Path(build["binary_path"]))
    if (sha(binary) != selection["solver"]["binary_sha256"]
            or run.get("solver_binary_sha256") != sha(binary)
            or selection["solver"]["source_sha256"] != build["source_sha256"]):
        raise ValueError("pinned S6 solver build provenance mismatch")
    if override_doc:
        history = [
            {"stones": 6, "key": row["key"], "verdict": row["verdict"],
             "observations": [{"budget": row["budget"], "legal": row["legal"],
                               "nodes": row["nodes"], "path": row["historical_path"],
                               "row": row["row"], "verdict": row["verdict"]}]}
            for row in override_doc["relocations"]
        ]
    else:
        if sha(HISTORY) != selection["history"]["sha256"]:
            raise ValueError("saved S6 history changed after selection")
        history = json.loads(HISTORY.read_text(encoding="utf-8"))

    sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
    from independent import Board
    board = Board(11)
    parent_mask = S5[0] | (S5[1] << 64)
    if parent_mask.bit_count() != 5 or board.canonical(parent_mask) != parent_mask:
        raise ValueError("selected S5 parent is not canonical")
    children = {}
    for child in board.children(parent_mask):
        key = (child & ((1 << 64) - 1), child >> 64)
        if key in children:
            raise ValueError(f"duplicate independently generated S6 child: {key}")
        if board.canonical(child) != child or child.bit_count() != 6:
            raise ValueError(f"unsafe/noncanonical S6 child: {key}")
        children[key] = board.legal(child).bit_count()
    if len(children) != 98 or len(children) != selection["s6_child_count"]:
        raise ValueError(f"independent S6 boundary count mismatch: {len(children)}")

    saved_sources = audit_saved_history(history, selection, children, board, raw_overrides)
    saved = {tuple(s["key"]): (1 if s["verdict"] == "WIN" else 2) for s in saved_sources}
    selected = {int(t["sequence"]): t for t in selection["selected"]}
    runs = {int(r["sequence"]): r for r in run.get("runs", [])}
    if len(runs) != len(run.get("runs", [])) or not set(runs) <= set(selected):
        raise ValueError("run manifest has duplicate or unselected S6 sequence")
    if not selected:
        raise ValueError("empty S6 selection")
    stop_loss = next((seq for seq in sorted(runs) if runs[seq]["verdict"] == "LOSS"), None)
    expected_sequences = [s for s in sorted(selected) if stop_loss is None or s <= stop_loss]
    if sorted(runs) != expected_sequences:
        raise ValueError(f"runner sequence does not match completion/stop rule: {sorted(runs)} != {expected_sequences}")
    if stop_loss is not None and run.get("stop_reason", "").find("proves parent S5 LOSS") < 0:
        raise ValueError("runner did not stop and record the first S6 LOSS witness")

    outcomes = dict(saved)
    result_records = []
    for seq in sorted(runs):
        target, record = selected[seq], runs[seq]
        key = tuple(target["key"])
        raw, log = resolve(Path(record["raw_path"])), resolve(Path(record["log_path"]))
        if key not in children or children[key] != target["legal"]:
            raise ValueError(f"selected S6 is outside the independent parent boundary: {key}")
        if not raw.is_file() or not log.is_file() or sha(raw) != record["raw_sha256"] or sha(log) != record["log_sha256"]:
            raise ValueError(f"raw/log SHA-256 mismatch for S6 sequence {seq}")
        parsed = read_replay(raw)
        mask = key[0] | (key[1] << 64)
        verdict = {0: "UNKNOWN", 1: "WIN", 2: "LOSS"}.get(parsed["verdict_code"])
        if (board.canonical(mask) != mask or mask.bit_count() != 6
                or parsed["row_sequence"] != 0 or parsed["key"] != list(key)
                or parsed["stones"] != 6 or parsed["is_or"] != 1
                or parsed["legal"] != board.legal(mask).bit_count()
                or parsed["legal"] != target["legal"] or parsed["budget"] != target["budget"]
                or parsed["nodes"] > target["budget"] or parsed["nodes"] != record["nodes"]
                or verdict != record["verdict"] or record["budget"] != target["budget"]):
            raise ValueError(f"S6 raw/geometry/fixed-polarity/manifest mismatch at {seq}: {parsed}")
        if key in outcomes and outcomes[key] != parsed["verdict_code"] and parsed["verdict_code"] in (1, 2):
            raise ValueError(f"saved and new exact S6 evidence conflict for {key}")
        if parsed["verdict_code"] in (1, 2):
            outcomes[key] = parsed["verdict_code"]
        result_records.append({"sequence": seq, "key": list(key), "legal": target["legal"],
                               "budget": target["budget"], "verdict": verdict, "nodes": parsed["nodes"],
                               "elapsed_seconds": record["elapsed_seconds"],
                               "raw_path": record["raw_path"], "raw_sha256": sha(raw),
                               "log_path": record["log_path"], "log_sha256": sha(log)})

    # The direct S5 AND root is LOSS iff any S6 child is LOSS, WIN iff all 98 are WIN.
    loss_witnesses = [list(k) for k, verdict in sorted(outcomes.items()) if verdict == 2 and k in children]
    win_count = sum(outcomes.get(k) == 1 for k in children)
    unknown_count = len(children) - win_count - len(loss_witnesses)
    parent_outcome = "LOSS" if loss_witnesses else "WIN" if win_count == len(children) else "UNKNOWN"
    cache_keys = read_cache(EXP / "output/current-exact-s5.cache")
    if S5 in cache_keys:
        raise ValueError("parent S5 is already exact in current cache; reconcile before deriving again")
    worker_path = resolve(args.worker_cache) if args.worker_cache else EXP / "output/s6-derived-s5-worker.cache"
    cache_code = {"WIN": 1, "LOSS": 2}.get(parent_outcome)
    cache_text = "# exact-only S5 derived from independently audited complete S6 boundary; UNKNOWN omitted\n"
    if cache_code is not None:
        cache_text += f"s5verdict,{S5[0]},{S5[1]},5,{cache_code},0\n"
    worker_path.parent.mkdir(parents=True, exist_ok=True)
    if worker_path.exists() and worker_path.read_text(encoding="utf-8") != cache_text:
        raise ValueError("derived S5 worker cache already exists with different content")
    if not worker_path.exists():
        worker_path.write_text(cache_text, encoding="utf-8", newline="")

    receipt = {
        "schema": "n11-s4-final-s5-s6-split-audit-v1",
        "selection_path": str(selection_path.relative_to(ROOT)), "selection_sha256": sha(selection_path),
        "run_manifest_path": str(run_path.relative_to(ROOT)), "run_manifest_sha256": sha(run_path),
        "solver_binary_sha256": sha(binary), "solver_source_sha256": build["source_sha256"],
        "parent_s5": list(S5), "parent_s5_polarity": "AND (is_or=0)",
        "independently_generated_s6_children": len(children),
        "saved_s6_exact_counts": {"WIN": sum(v == 1 for v in saved.values()), "LOSS": sum(v == 2 for v in saved.values())},
        "saved_s6_raw_sources": saved_sources,
        "saved_s6_raw_relocation_manifest": str(override_path.relative_to(ROOT)) if override_path else None,
        "saved_s6_raw_relocation_manifest_sha256": sha(override_path) if override_path else None,
        "new_s6_counts": {"WIN": sum(r["verdict"] == "WIN" for r in result_records),
                           "LOSS": sum(r["verdict"] == "LOSS" for r in result_records),
                           "UNKNOWN": sum(r["verdict"] == "UNKNOWN" for r in result_records)},
        "new_s6_nodes": sum(r["nodes"] for r in result_records),
        "new_s6_elapsed_seconds": sum(r["elapsed_seconds"] for r in result_records),
        "new_s6_results": result_records,
        "boundary_exact_counts": {"WIN": win_count, "LOSS": len(loss_witnesses), "unresolved": unknown_count},
        "loss_witnesses": loss_witnesses,
        "derived_parent_s5_outcome": parent_outcome,
        "derivation": "S5 is fixed-player AND: one exact S6 LOSS proves S5 LOSS; all 98 exact S6 WIN prove S5 WIN; otherwise UNKNOWN",
        "worker_cache_path": str(worker_path.relative_to(ROOT)), "worker_cache_sha256": sha(worker_path),
        "trust": "fresh and saved S6 outcomes are solver-trusted exact leaves; independent integer geometry validates canonical/legal boundaries and AND propagation; not terminal-only minimax proof",
    }
    receipt_path = resolve(args.receipt) if args.receipt else EXP / "output" / selection_path.name.replace("-selection.json", "-audit.json")
    encoded = (json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if receipt_path.exists() and receipt_path.read_bytes() != encoded:
        raise ValueError("existing S6 audit receipt differs; refusing overwrite")
    if not receipt_path.exists():
        receipt_path.write_bytes(encoded)
    print(json.dumps({k: v for k, v in receipt.items() if k not in ("saved_s6_raw_sources", "new_s6_results")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
