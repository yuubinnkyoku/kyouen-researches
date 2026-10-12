#!/usr/bin/env python3
"""Rebuild and freeze a stratified cold-exact S5 batch before solver launch."""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s4-boundary-direct-20261012"
BASE_CACHE = ROOT / "research/experiments/n11-reply27-20more-20261011/output/merged-exact-s5.cache"
GEOMETRY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
HISTORY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/history.json"
HISTORY_SOURCES = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/history-sources.json"
TASKS = ROOT / "research/experiments/n11-reply27-20more-20261011/output/new-ranking/shared-s5-tasks.csv"
BUILD = ROOT / "research/experiments/n11-s5-loss-cost-drivers-20261012/input/child-profile-build.json"
INDEPENDENT = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
TARGET = (1297036692683752448, 0)
REQUIRED_THIRD = {100, 108}
LIMIT = 15_000_000

# Fixed before any run. Four currently live shared S5 and four single-parent
# S5 span legal counts 96..105 and include partial saved-S6-WIN evidence.
FIXED_KEYS = [
    (1152921504607899649, 536870912),
    (1152921504606851585, 536870912),
    (1152921504607896576, 536879104),
    (1152921504612090880, 536870912),
    (1297036692683752704, 0),
    (1297036692683785216, 0),
    (1297036692683752448, 8),
    (1152921513197831168, 536870912),
]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_cache(board):
    sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
    from s5_evidence_policy import quarantined_cache_keys

    quarantine = quarantined_cache_keys()
    values = {}
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as f:
        for line, row in enumerate(csv.reader(f), 1):
            if not row or row[0].strip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"invalid baseline cache row {line}: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            key = (lo, hi)
            if stones != 5 or verdict not in (1, 2) or nodes < 0:
                raise ValueError(f"invalid baseline S5 exact row {line}: {row}")
            if key in quarantine:
                raise ValueError(f"quarantined key in baseline cache: {key}")
            mask = lo | (hi << 64)
            if mask.bit_count() != 5 or board.canonical(mask) != mask:
                raise ValueError(f"noncanonical/non-S5 baseline key: {key}")
            board.legal(mask)  # rejects geometrically unsafe positions
            old = values.get(key)
            if old is not None and old != verdict:
                raise ValueError(f"baseline cache conflict for {key}: {old} vs {verdict}")
            values[key] = verdict
    return values, quarantine


def read_history_sources(board, s5_keys: set[tuple[int, int]], s6_keys: set[tuple[int, int]]):
    """Verify the frozen source inventory and rebuild raw history for this frontier."""
    manifest = json.loads(HISTORY_SOURCES.read_text(encoding="utf-8"))
    if manifest.get("scanned_files") != 11893 or manifest.get("matching_files") != len(manifest.get("sources", [])):
        raise ValueError("unexpected raw-history source inventory size")
    s5_records: dict[tuple[int, int], list[dict]] = defaultdict(list)
    s6_exact: dict[tuple[int, int], list[dict]] = defaultdict(list)
    file_count = actual_rows = total_bytes = 0
    for source in manifest["sources"]:
        raw_path = Path(source["path"])
        path = raw_path if raw_path.is_absolute() else ROOT / raw_path
        if not path.is_file():
            raise ValueError(f"missing raw-history source: {source['path']}")
        if sha(path) != source["sha256"]:
            raise ValueError(f"raw-history source hash mismatch: {source['path']}")
        file_count += 1
        total_bytes += path.stat().st_size
        with path.open(encoding="utf-8-sig", newline="") as f:
            for row_number, row in enumerate(csv.reader(f), 1):
                if not row or row[0] != "replay":
                    continue
                if len(row) != 11:
                    raise ValueError(f"malformed replay row: {source['path']}:{row_number}")
                actual_rows += 1
                sequence, stones, legal, is_or, budget, verdict, nodes, seconds, lo, hi = map(int, row[1:])
                key = (lo, hi)
                record = {
                    "source": source["path"], "row": row_number, "stones": stones,
                    "legal": legal, "is_or": is_or, "budget": budget,
                    "verdict": verdict, "nodes": nodes,
                }
                if stones == 5 and key in s5_keys:
                    if is_or != 0 or (lo | (hi << 64)).bit_count() != 5:
                        raise ValueError(f"bad S5 history polarity/key: {source['path']}:{row_number}")
                    s5_records[key].append(record)
                elif stones == 6 and key in s6_keys and verdict in (1, 2):
                    if is_or != 1 or (lo | (hi << 64)).bit_count() != 6:
                        raise ValueError(f"bad S6 history polarity/key: {source['path']}:{row_number}")
                    s6_exact[key].append(record)
    indexed_rows = sum(int(source.get("rows", 0)) for source in manifest["sources"])
    if file_count != 6951 or actual_rows < indexed_rows or indexed_rows != 18389:
        raise ValueError(f"raw-history source inventory is incomplete: files={file_count}, rows={actual_rows}/{indexed_rows}")
    return s5_records, s6_exact, {
        "scanned_files": manifest["scanned_files"], "verified_source_files": file_count,
        "manifest_indexed_rows": indexed_rows, "actual_replay_rows": actual_rows,
        "unindexed_raw_row_delta": actual_rows - indexed_rows,
        "verified_bytes": total_bytes,
        "raw_history_manifest_sha256": sha(HISTORY_SOURCES),
        "history_index_sha256": sha(HISTORY),
    }


def main() -> None:
    sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
    from independent import Board

    board = Board(11)
    with gzip.open(GEOMETRY, "rt", encoding="utf-8") as f:
        geometry = json.load(f)
    if len(geometry) != 3384:
        raise ValueError(f"expected 3,384 S4 classes, got {len(geometry)}")
    cache, quarantine = read_cache(board)
    if len(cache) != 5785 or Counter(cache.values()) != Counter({1: 159, 2: 5626}):
        raise ValueError(f"unexpected baseline cache counts: {Counter(cache.values())}")

    classes = {}
    parent_incidence: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    secured = set()
    class_counts = Counter()
    all_third = set()
    for item in geometry:
        parent = tuple(item["key"])
        mask = parent[0] | (parent[1] << 64)
        if mask.bit_count() != 4 or board.canonical(mask) != mask:
            raise ValueError(f"noncanonical S4 class: {parent}")
        children = {tuple(k) for k in item["children"]}
        generated = {
            (k & ((1 << 64) - 1), k >> 64)
            for k in board.children(mask)
        }
        if children != generated or len(children) != len(item["children"]):
            raise ValueError(f"independent S4 child-boundary mismatch: {parent}")
        verdicts = [cache.get(k, 0) for k in children]
        status = "WIN" if 1 in verdicts else ("LOSS" if verdicts and all(v == 2 for v in verdicts) else "UNKNOWN")
        class_counts[status] += 1
        classes[parent] = {"status": status, "children": children, "coverage": set(item["coverage"])}
        all_third.update(item["coverage"])
        if status == "LOSS":
            secured.update(item["coverage"])
    if len(classes) != 3384 or len(all_third) != 119 or sorted(all_third - secured) != [100, 108]:
        raise ValueError("baseline full-frontier / third-move coverage mismatch")
    if class_counts != Counter({"LOSS": 31, "WIN": 274, "UNKNOWN": 3079}):
        raise ValueError(f"unexpected baseline S4 class counts: {class_counts}")

    target = classes.get(TARGET)
    if target is None:
        raise ValueError("target S4 missing from geometry")
    target_mask = TARGET[0] | (TARGET[1] << 64)
    generated_target = {
        (k & ((1 << 64) - 1), k >> 64) for k in board.children(target_mask)
    }
    if target["children"] != generated_target or len(generated_target) != 106:
        raise ValueError("target S4 must have exactly 106 independently regenerated children")
    target_counts = Counter(cache.get(k, 0) for k in generated_target)
    if target_counts != Counter({2: 40, 0: 66}):
        raise ValueError(f"target S4 baseline boundary is not LOSS40/WIN0/UNKNOWN66: {target_counts}")

    # Rebuild the 61 relevant surviving S4 set and its active S5 sharing graph.
    active_classes = {
        parent for parent, info in classes.items()
        if info["status"] == "UNKNOWN" and REQUIRED_THIRD <= info["coverage"]
    }
    if len(active_classes) != 61 or TARGET not in active_classes:
        raise ValueError(f"expected 61 live classes covering both unresolved third moves; got {len(active_classes)}")
    for parent in active_classes:
        for child in classes[parent]["children"]:
            parent_incidence[child].append(parent)

    with TASKS.open(encoding="utf-8-sig", newline="") as f:
        tasks = {row["key"]: row for row in csv.DictReader(f)}
    unknown = sorted(k for k in generated_target if cache.get(k, 0) == 0)
    if len(unknown) != 66:
        raise ValueError("target unresolved child count changed")
    task_parents = {}
    for key in unknown:
        key_text = f"{key[0]}:{key[1]}"
        task = tasks.get(key_text)
        parents = sorted(parent_incidence[key])
        if task is None or int(task["live_parents"]) != len(parents):
            raise ValueError(f"live parent incidence mismatch for {key_text}")
        stated = sorted(json.loads(task["live_parent_keys"].replace("'", '"')))
        computed = sorted(f"{p[0]}:{p[1]}" for p in parents)
        if stated != computed:
            raise ValueError(f"live parent keys mismatch for {key_text}")
        task_parents[key] = parents
    shared = sum(len(task_parents[k]) > 1 for k in unknown)
    if shared != 45 or len(unknown) - shared != 21:
        raise ValueError(f"target shared/single boundary mismatch: {shared}/{len(unknown)-shared}")

    all_s6 = set()
    s6_by_s5 = {}
    for key in unknown:
        mask = key[0] | (key[1] << 64)
        s6 = {
            (child & ((1 << 64) - 1), child >> 64)
            for child in board.children(mask)
        }
        s6_by_s5[key] = s6
        all_s6.update(s6)
    s5_raw, s6_raw, raw_inventory = read_history_sources(board, set(unknown), all_s6)
    history = {tuple(row["key"]): row for row in json.loads(HISTORY.read_text(encoding="utf-8"))}

    # Cache/raw agreement is checked before selection. Exact cache rows are
    # trusted solver outcomes; unknown history never becomes an exact value.
    for key in generated_target:
        rows = [r for r in s5_raw.get(key, []) if r["verdict"] in (1, 2)]
        exact_seen = {r["verdict"] for r in rows}
        if len(exact_seen) > 1:
            raise ValueError(f"conflicting raw exact S5 verdicts for {key}")
        if exact_seen and cache.get(key, 0) not in exact_seen:
            raise ValueError(f"S5 cache/raw conflict for {key}")

    if any(r["verdict"] == 2 for key in unknown for s6 in s6_by_s5[key] for r in s6_raw.get(s6, [])):
        raise ValueError("an unresolved S5 has a saved exact S6 LOSS witness; reuse that evidence first")

    selected_reasons = {
        (1152921504607899649, 536870912): "shared; legal-count low stratum; reuse accounting includes two prior exact S6 WIN children, no S6 LOSS witness",
        (1152921504606851585, 536870912): "shared; legal-count low/middle stratum; no prior S5 raw and no exact S6 raw hit",
        (1152921504607896576, 536879104): "shared; legal-count middle stratum; no prior S5 raw and no exact S6 raw hit",
        (1152921504612090880, 536870912): "shared; legal-count high stratum (105); no prior S5 raw and no exact S6 raw hit",
        (1297036692683752704, 0): "single-parent; legal-count low stratum (96); no prior S5 raw and no exact S6 raw hit",
        (1297036692683785216, 0): "single-parent; legal-count low stratum (96); retain one partial saved S6 WIN case",
        (1297036692683752448, 8): "single-parent; legal-count middle stratum (100); no prior S5 raw and no exact S6 raw hit",
        (1152921513197831168, 536870912): "single-parent; legal-count high stratum (103); retain a partial saved S6 WIN case",
    }
    selected = []
    if len(set(FIXED_KEYS)) != 8:
        raise ValueError("fixed batch has duplicate roots")
    for i, key in enumerate(FIXED_KEYS):
        if key not in unknown:
            raise ValueError(f"fixed batch target is not currently UNKNOWN: {key}")
        rows = s5_raw.get(key, [])
        if rows:
            raise ValueError(f"fixed batch has prior raw S5 exploration; do not repeat: {key}")
        hist = history.get(key)
        if hist and hist.get("observations"):
            raise ValueError(f"history index has prior S5 observations; do not repeat: {key}")
        if key in quarantine:
            raise ValueError(f"fixed batch key is quarantined: {key}")
        parents = task_parents[key]
        is_shared = len(parents) > 1
        if i < 4 and not is_shared or i >= 4 and is_shared:
            raise ValueError(f"fixed batch sharing stratum changed: {key}")
        mask = key[0] | (key[1] << 64)
        if mask.bit_count() != 5 or board.canonical(mask) != mask:
            raise ValueError(f"selected S5 not canonical: {key}")
        board.legal(mask)
        exact_s6_keys = {}
        exact_s6_rows = [
            row for s6 in s6_by_s5[key] for row in s6_raw.get(s6, [])
            if row["verdict"] in (1, 2)
        ]
        for s6 in s6_by_s5[key]:
            verdicts = {row["verdict"] for row in s6_raw.get(s6, []) if row["verdict"] in (1, 2)}
            if len(verdicts) > 1:
                raise ValueError(f"conflicting saved exact S6 raw results for {s6}")
            if verdicts:
                exact_s6_keys[s6] = next(iter(verdicts))
        saved_counts = Counter(exact_s6_keys.values())
        hist_rows = s5_raw.get(key, [])
        max_unknown_budget = max((row["budget"] for row in hist_rows if row["verdict"] == 0), default=0)
        selected.append({
            "sequence": i, "key": list(key), "legal": board.legal(mask).bit_count(),
            "live_parent_count": len(parents), "live_parent_keys": [list(p) for p in parents],
            "sharing": "shared" if is_shared else "single",
            "historical_s5_rows": len(hist_rows), "historical_15m_unknown": max_unknown_budget >= LIMIT,
            "saved_s6_exact_children": len(exact_s6_keys),
            "saved_s6_loss_children": saved_counts[2], "saved_s6_win_children": saved_counts[1],
            "saved_s6_exact_rows": len(exact_s6_rows),
            "saved_s6_loss_rows": sum(r["verdict"] == 2 for r in exact_s6_rows),
            "saved_s6_win_rows": sum(r["verdict"] == 1 for r in exact_s6_rows),
            "reason": selected_reasons[key],
        })

    build = json.loads(BUILD.read_text(encoding="utf-8"))
    solver = ROOT / build["binary_path"]
    source = ROOT / build["source_path"]
    if not solver.is_file() or sha(solver) != build["binary_sha256"]:
        raise ValueError("pinned current exact solver binary is missing or hash-mismatched")
    if not source.is_file() or sha(source) != build["source_sha256"]:
        raise ValueError("pinned current exact solver source is missing or hash-mismatched")

    manifest = {
        "schema": "n11-s4-direct-s5-first-batch-selection-v1",
        "source_main_commit": "1bdd30b71adaf8f476a98922f1b454bdd369feb3",
        "target_s4": list(TARGET), "target_s4_children": 106,
        "baseline_target_counts": {"LOSS": 40, "WIN": 0, "UNKNOWN": 66},
        "baseline_all_s4_counts": dict(class_counts),
        "baseline_secured_third_moves": sorted(secured),
        "baseline_remaining_third_moves": sorted(all_third - secured),
        "independent_geometry": {"path": str(GEOMETRY.relative_to(ROOT)), "sha256": sha(GEOMETRY),
                                 "source": str(INDEPENDENT.relative_to(ROOT)), "source_sha256": sha(INDEPENDENT),
                                 "all_3384_boundaries_regenerated": True},
        "baseline_cache": {"path": str(BASE_CACHE.relative_to(ROOT)), "sha256": sha(BASE_CACHE),
                           "frozen_copy": "research/experiments/n11-s4-boundary-direct-20261012/input/baseline-exact-s5.cache",
                           "rows": len(cache), "WIN": sum(v == 1 for v in cache.values()),
                           "LOSS": sum(v == 2 for v in cache.values()), "quarantine_rows": 0},
        "history": {**raw_inventory, "source_manifest_path": str(HISTORY_SOURCES.relative_to(ROOT)),
                    "history_index_path": str(HISTORY.relative_to(ROOT)),
                    "target_unknown_s5_raw_rows": sum(len(s5_raw.get(k, [])) for k in unknown),
                    "target_unknown_s5_15m_unknown_count": sum(any(r["verdict"] == 0 and r["budget"] >= LIMIT for r in s5_raw.get(k, [])) for k in unknown),
                    "target_unknown_s5_with_saved_s6_loss": 0,
                    "target_unknown_s5_with_partial_saved_s6_exact": sum(any(
                        row["verdict"] in (1, 2) for s6 in s6_by_s5[k] for row in s6_raw.get(s6, [])
                    ) for k in unknown)},
        "live_candidate_class_count": len(active_classes),
        "target_unknown_s5_shared": shared, "target_unknown_s5_single": len(unknown) - shared,
        "selection_rule": "fixed 4 shared + 4 single; legal-count range 96..105; no S5 raw history or >=15M UNKNOWN; include three cases with partial exact S6 WIN raw; no saved S6 LOSS witness exists",
        "solver": {"build_manifest": str(BUILD.relative_to(ROOT)),
                   "frozen_build_manifest": "research/experiments/n11-s4-boundary-direct-20261012/input/solver-build.json",
                   "build_manifest_sha256": sha(BUILD), "binary_sha256": build["binary_sha256"],
                   "source_sha256": build["source_sha256"],
                   "mode": "cold exact replay; one target per fresh process; profile off",
                   "flags": ["--n=11", "--memo=22", "--only=5", "--exact-order=count",
                             f"--exact-replay-budget={LIMIT}"],
                   "profile_regression": "research/experiments/n11-s5-loss-cost-drivers-20261012/output/profile-regression-v4/receipt.json"},
        "selected": selected,
    }

    input_dir = EXP / "input"
    input_dir.mkdir(parents=True, exist_ok=True)
    for source_path, frozen_path in (
        (BASE_CACHE, input_dir / "baseline-exact-s5.cache"),
        (BUILD, input_dir / "solver-build.json"),
    ):
        if frozen_path.exists():
            if sha(frozen_path) != sha(source_path):
                raise ValueError(f"frozen input already differs from source: {frozen_path}")
        else:
            frozen_path.write_bytes(source_path.read_bytes())
    for row in selected:
        i = row["sequence"]
        lo, hi = row["key"]
        input_path = input_dir / f"s5-{i:02}.csv"
        expected_input = f"target,{i},5,{lo},{hi},{row['legal']},0,0,0,0,0\n"
        if input_path.exists():
            if input_path.read_text(encoding="utf-8") != expected_input:
                raise ValueError(f"frozen target input already differs: {input_path}")
        else:
            input_path.write_text(expected_input, encoding="utf-8")
        row["input_path"] = str(input_path.relative_to(ROOT))
        row["input_sha256"] = sha(input_path)
    write_json(EXP / "input/first-batch-selection.json", manifest)
    print(json.dumps({
        "target_children": 106, "baseline": manifest["baseline_target_counts"],
        "history_files_verified": raw_inventory["verified_source_files"],
        "history_rows_scanned": raw_inventory["actual_replay_rows"],
        "shared_single": [shared, len(unknown) - shared],
        "selected": selected,
        "selection_sha256": sha(EXP / "input/first-batch-selection.json"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
