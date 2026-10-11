#!/usr/bin/env python3
"""Audit saved S5/S6 evidence and compare the K0374 hierarchical run."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EX = Path(__file__).resolve().parents[1]
DEFAULT_RAW = EX / "input/raw"
S6_EX = ROOT / "research/experiments/n11-s6-universal-closure-20261011"
DIRECT_EX = ROOT / "research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010"
CURRENT_EX = ROOT / "research/experiments/n11-reply27-20more-20261011"
CURRENT_S4 = (1297036692683752448, 0)
HARD_S5 = (1188950301626859520, 603979776)
STAGE_ORDER = [
    "s6-lowest3",
    "s6-stratified15",
    "s6-batch1",
    "s6-batch2",
    "s6-batch3",
    "s6-batch4",
    "s6-escalate-a",
    "s6-escalate-b",
]
BASE_STAGES = STAGE_ORDER[:6]
RESULTS = {0: "UNKNOWN", 1: "WIN", 2: "LOSS"}
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from independent import Board  # noqa: E402
from s5_evidence_policy import quarantined_cache_keys  # noqa: E402
from strategy import LOSS, UNKNOWN, WIN, choose_strategy, fixed_first_outcome  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_rows(path: Path, first_column: str) -> list[list[str]]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as stream:
        return [row for row in csv.reader(stream) if row and row[0] == first_column]


def read_inputs(path: Path, expected_stones: int) -> dict[tuple[int, int], dict[str, int]]:
    rows = read_csv_rows(path, "target")
    out: dict[tuple[int, int], dict[str, int]] = {}
    for row in rows:
        if len(row) != 11:
            raise ValueError(f"bad target row in {path}: {row}")
        stones, lo, hi, legal, is_or = int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[7])
        if stones != expected_stones or is_or != int(stones % 2 == 0):
            raise ValueError(f"wrong fixed-player layer in {path}: {row}")
        key = (lo, hi)
        if key in out:
            raise ValueError(f"duplicate input key in {path}: {key}")
        out[key] = {"legal": legal, "sequence": int(row[1])}
    return out


def read_replays(path: Path, expected_stones: int) -> list[dict[str, int]]:
    rows = read_csv_rows(path, "replay")
    out = []
    for row in rows:
        if len(row) != 11:
            raise ValueError(f"bad replay row in {path}: {row}")
        seq, stones, legal, is_or, budget, verdict, nodes, seconds, lo, hi = map(int, row[1:])
        if stones != expected_stones or is_or != int(stones % 2 == 0):
            raise ValueError(f"wrong fixed-player layer in {path}: {row}")
        if verdict not in RESULTS or not 0 <= nodes <= budget:
            raise ValueError(f"bad replay result or node count in {path}: {row}")
        if verdict == UNKNOWN and nodes != budget:
            raise ValueError(f"censored UNKNOWN did not consume its cap in {path}: {row}")
        out.append({
            "key_lo": lo,
            "key_hi": hi,
            "sequence": seq,
            "legal": legal,
            "budget": budget,
            "verdict": verdict,
            "nodes": nodes,
            "wall_seconds": seconds,
        })
    if not out:
        raise ValueError(f"no replay records in {path}")
    return out


def replay_footer_seconds(path: Path) -> int:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig") as stream:
        lines = stream.read().splitlines()
    for line in reversed(lines):
        if line.startswith("# replay_done "):
            marker = "wall_s="
            if marker not in line:
                break
            return int(line.rsplit(marker, 1)[1])
    raise ValueError(f"missing replay_done wall time in {path}")


def load_cache(path: Path) -> dict[tuple[int, int], int]:
    values: dict[tuple[int, int], int] = {}
    quarantined = quarantined_cache_keys()
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"malformed current S5 cache row: {row}")
            key, stones, verdict = (int(row[1]), int(row[2])), int(row[3]), int(row[4])
            if stones != 5 or verdict not in (WIN, LOSS) or key in quarantined:
                raise ValueError(f"invalid or quarantined current S5 cache entry: {row}")
            if key in values and values[key] != verdict:
                raise ValueError(f"conflicting current S5 cache entries: {key}")
            values[key] = verdict
    return values


def expected_raw_hashes() -> tuple[dict[str, str], dict[str, str]]:
    k0374 = read_json(S6_EX / "output/audit.json")
    s6 = {entry["path"]: entry["sha256"] for entry in k0374["raw_sources"]}
    direct_inventory = read_json(DIRECT_EX / "output/artifact-sha256.json")
    direct = {entry["path"]: entry["sha256"] for entry in direct_inventory["artifacts"]}
    return s6, direct


def validate_raw_copy(name: str, input_dir: Path, s6_hashes: dict[str, str], direct_hashes: dict[str, str]) -> dict[str, object]:
    copied = input_dir / name
    if not copied.is_file():
        raise ValueError(f"missing copied raw: {name}")
    raw_name = name.removesuffix(".gz")
    if raw_name == "s5-direct-15m.csv":
        source_rel = "research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/probe-15m-sixth.csv"
        expected = direct_hashes.get(source_rel)
        original = ROOT / source_rel
    else:
        source_rel = f"research/experiments/n11-s6-universal-closure-20261011/output/raw/{raw_name}"
        expected = s6_hashes.get(source_rel)
        original = ROOT / source_rel
    if expected is None:
        raise ValueError(f"source manifest has no hash for {source_rel}")
    stored_hash = sha256(copied)
    try:
        raw = gzip.decompress(copied.read_bytes())
    except OSError as exc:
        raise ValueError(f"invalid gzip raw copy: {name}") from exc
    raw_hash, source_hash = hashlib.sha256(raw).hexdigest(), sha256(original)
    if raw_hash != expected or source_hash != expected:
        raise ValueError(f"raw hash mismatch for {source_rel}")
    return {
        "source_path": source_rel,
        "copy_path": copied.relative_to(ROOT).as_posix(),
        "stored_bytes": copied.stat().st_size,
        "raw_bytes": len(raw),
        "raw_sha256": raw_hash,
        "stored_gzip_sha256": stored_hash,
    }


def _s4_current_status(board: Board) -> dict[str, object]:
    current_audit = read_json(CURRENT_EX / "output/audit.json")
    cache_path = CURRENT_EX / "output/merged-exact-s5.cache"
    if sha256(cache_path) != current_audit["s5_cache_sha256"]:
        raise ValueError("current S4 cache no longer matches the audited main artifact")
    if tuple(current_audit["root_s4_key"]) != CURRENT_S4:
        raise ValueError("unexpected current S4 root in latest tracked audit")

    parent_mask = CURRENT_S4[0] | (CURRENT_S4[1] << 64)
    if board.canonical(parent_mask) != parent_mask:
        raise ValueError("current S4 is not canonical")
    child_masks = set(board.children(parent_mask))
    if len(child_masks) != 106:
        raise ValueError(f"current S4 child count changed: {len(child_masks)}")
    cache = load_cache(cache_path)
    counts = Counter(RESULTS[cache.get((mask & ((1 << 64) - 1), mask >> 64), UNKNOWN)] for mask in child_masks)
    expected = current_audit["target_s4_after"]
    got = {name: counts[name] for name in ("LOSS", "WIN", "UNKNOWN")}
    if got != expected or got != {"LOSS": 40, "WIN": 0, "UNKNOWN": 66}:
        raise ValueError(f"current S4 boundary disagrees with audited cache: {got}")
    return {
        "key": list(CURRENT_S4),
        "complete_s5_children": len(child_masks),
        "outcomes": got,
        "cache_path": cache_path.relative_to(ROOT).as_posix(),
        "cache_sha256": sha256(cache_path),
        "current_audit_sha256": sha256(CURRENT_EX / "output/audit.json"),
        "derived_from_exact_cache_and_independent_geometry": True,
        "solver_dispatch_for_this_experiment": False,
    }


def build_report(input_dir: Path = DEFAULT_RAW) -> tuple[dict[str, object], dict[str, object]]:
    s6_hashes, direct_hashes = expected_raw_hashes()
    filenames = [f"{stage}.{suffix}.csv.gz" for stage in STAGE_ORDER for suffix in ("input", "out")]
    files = [validate_raw_copy(name, input_dir, s6_hashes, direct_hashes) for name in filenames]
    direct_file = validate_raw_copy("s5-direct-15m.csv.gz", input_dir, s6_hashes, direct_hashes)

    board = Board(11)
    parent_mask = HARD_S5[0] | (HARD_S5[1] << 64)
    if board.canonical(parent_mask) != parent_mask or len(board.points(parent_mask)) != 5:
        raise ValueError("benchmark S5 root is noncanonical or has the wrong stone count")
    child_masks = set(board.children(parent_mask))
    if len(child_masks) != 90 or board.legal(parent_mask).bit_count() != 90:
        raise ValueError("benchmark S5 does not have its audited 90-child boundary")
    canonical_children = {
        (mask & ((1 << 64) - 1), mask >> 64): mask for mask in child_masks
    }

    stage_records: dict[str, list[dict[str, int]]] = {}
    first_pass: dict[tuple[int, int], dict[str, int]] = {}
    initial_nodes = 0
    retry_nodes = 0
    group_wall_seconds = 0
    for stage in STAGE_ORDER:
        inputs = read_inputs(input_dir / f"{stage}.input.csv.gz", 6)
        rows = read_replays(input_dir / f"{stage}.out.csv.gz", 6)
        keys = {(r["key_lo"], r["key_hi"]) for r in rows}
        if keys != set(inputs):
            raise ValueError(f"input/output target mismatch in {stage}")
        if len(keys) != len(rows):
            raise ValueError(f"duplicate S6 rows in {stage}")
        for row in rows:
            key = (row["key_lo"], row["key_hi"])
            if key not in canonical_children:
                raise ValueError(f"non-child S6 raw row in {stage}: {key}")
            if row["legal"] != inputs[key]["legal"]:
                raise ValueError(f"legal-count mismatch in {stage}: {key}")
            mask = canonical_children[key]
            if board.canonical(mask) != mask or len(board.points(mask)) != 6:
                raise ValueError(f"unsafe or noncanonical S6 child in {stage}: {key}")
            if row["legal"] != board.legal(mask).bit_count():
                raise ValueError(f"independent legal-count mismatch in {stage}: {key}")
            if row["budget"] != (2_000_000 if stage == "s6-lowest3" else 15_000_000 if stage.startswith("s6-escalate") else 1_000_000):
                raise ValueError(f"unexpected S6 budget in {stage}: {key}")
            if stage in BASE_STAGES:
                if key in first_pass:
                    raise ValueError(f"duplicate initial S6 child: {key}")
                first_pass[key] = row
                initial_nodes += row["nodes"]
            else:
                retry_nodes += row["nodes"]
        group_wall_seconds += replay_footer_seconds(input_dir / f"{stage}.out.csv.gz")
        stage_records[stage] = rows

    if set(first_pass) != set(canonical_children):
        raise ValueError("saved first-pass S6 rows are not the complete canonical boundary")
    first_unknown = {key for key, row in first_pass.items() if row["verdict"] == UNKNOWN}
    first_win = {key for key, row in first_pass.items() if row["verdict"] == WIN}
    if len(first_unknown) != 5 or len(first_win) != 85 or any(row["verdict"] == LOSS for row in first_pass.values()):
        raise ValueError("unexpected first-pass S6 outcome split")
    retries = [row for stage in STAGE_ORDER[6:] for row in stage_records[stage]]
    retry_keys = {(row["key_lo"], row["key_hi"]) for row in retries}
    if retry_keys != first_unknown or len(retries) != 5 or any(row["verdict"] != WIN for row in retries):
        raise ValueError("15M escalations do not exactly close the five first-pass UNKNOWN children")

    final_s6 = {key: WIN for key in canonical_children}
    derived_s5 = fixed_first_outcome(5, list(final_s6.values()), len(canonical_children))
    if derived_s5 != WIN:
        raise ValueError("S5 fixed-player AND propagation failed")

    direct_rows = read_replays(input_dir / "s5-direct-15m.csv.gz", 5)
    if len(direct_rows) != 1:
        raise ValueError("expected one direct S5 replay")
    direct = direct_rows[0]
    if (direct["key_lo"], direct["key_hi"]) != HARD_S5 or direct["budget"] != 15_000_000 or direct["verdict"] != UNKNOWN or direct["nodes"] != 15_000_000:
        raise ValueError("direct S5 record does not match the 15M UNKNOWN baseline")
    direct_profile = {
        "budget_nodes": direct["budget"],
        "actual_nodes": direct["nodes"],
        "verdict": RESULTS[direct["verdict"]],
        "reported_row_wall_seconds": direct["wall_seconds"],
        "rss_bytes": None,
    }

    # Reconstruct an aggregate 15M-node S6 schedule prefix without claiming an
    # unobserved run outcome for the final interrupted child.
    remaining = 15_000_000
    prefix_spent = 0
    prefix_exact: dict[tuple[int, int], int] = {}
    prefix_completed_unknown = 0
    prefix_started = 0
    prefix_midrow_truncated = False
    for stage in BASE_STAGES:
        for row in stage_records[stage]:
            if remaining == 0:
                break
            prefix_started += 1
            key = (row["key_lo"], row["key_hi"])
            if row["nodes"] <= remaining:
                remaining -= row["nodes"]
                prefix_spent += row["nodes"]
                if row["verdict"] == UNKNOWN:
                    prefix_completed_unknown += 1
                else:
                    prefix_exact[key] = row["verdict"]
            else:
                prefix_spent += remaining
                remaining = 0
                prefix_midrow_truncated = True
                break
        if remaining == 0:
            break
    prefix_s5 = fixed_first_outcome(5, list(prefix_exact.values()), len(canonical_children))
    if prefix_s5 != UNKNOWN:
        raise ValueError("15M-node split prefix unexpectedly closes the complete S5 boundary")

    current_status = _s4_current_status(board)
    hard_root_in_current_boundary = HARD_S5 in {
        (mask & ((1 << 64) - 1), mask >> 64) for mask in board.children(CURRENT_S4[0] | (CURRENT_S4[1] << 64))
    }

    recovered = choose_strategy(
        goal="s5_win",
        expected_s6_children=90,
        direct_s5_verdict=direct["verdict"],
        direct_s5_attempted=True,
        saved_s6_verdicts={f"{lo}:{hi}": value for (lo, hi), value in final_s6.items()},
        s6_children=[f"{lo}:{hi}" for (lo, hi) in final_s6],
    )
    current_goal_plan = {
        "mode": "D",
        "action": "target_specific_s6_probe_after_raw_cache_preflight",
        "selected_s5_key": None,
        "dispatch": False,
        "reason": "the historical benchmark did not show a node-cost reduction, so no current S5 was selected",
        "outcome_probability_estimate": None,
    }

    k0374_audit_path = S6_EX / "output/audit.json"
    direct_inventory_path = DIRECT_EX / "output/artifact-sha256.json"
    current_audit_path = CURRENT_EX / "output/audit.json"
    provenance = {
        "source_manifests": [
            {"path": k0374_audit_path.relative_to(ROOT).as_posix(), "sha256": sha256(k0374_audit_path)},
            {"path": direct_inventory_path.relative_to(ROOT).as_posix(), "sha256": sha256(direct_inventory_path)},
            {"path": current_audit_path.relative_to(ROOT).as_posix(), "sha256": sha256(current_audit_path)},
        ],
        "copied_raw_files": files + [direct_file],
        "independent_geometry": {
            "path": "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py",
            "sha256": sha256(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"),
        },
        "s6_solver_source_sha256": read_json(k0374_audit_path)["source_cpp_sha256"],
        "s6_solver_binary_sha256": read_json(k0374_audit_path)["solver_binary_sha256"],
        "direct_solver_source_sha256_recorded": False,
        "direct_solver_binary_sha256_recorded": False,
        "historical_direct_runtime_environment_recorded_in_raw": False,
    }

    report = {
        "schema": "n11-s5-hierarchical-adaptive-audit-v1",
        "benchmark_s5": {"key": list(HARD_S5), "legal_s6_children": 90},
        "outcomes": {
            "direct_15m": direct_profile,
            "s6_initial": {"distinct_children": len(first_pass), "WIN": len(first_win), "LOSS": 0, "UNKNOWN": len(first_unknown), "nodes": initial_nodes},
            "s6_escalations": {"children": len(retries), "WIN": len(retries), "LOSS": 0, "UNKNOWN": 0, "nodes": retry_nodes},
            "s6_full_split": {"WIN": 90, "LOSS": 0, "UNKNOWN": 0, "total_nodes": initial_nodes + retry_nodes},
            "derived_s5": RESULTS[derived_s5],
            "solver_trust": "all exact S6 leaves are solver-trusted; no terminal-only S6 proof DAG was supplied",
        },
        "same_15m_node_cap": {
            "direct": {"nodes": direct["nodes"], "verdict": RESULTS[direct["verdict"]]},
            "split_prefix": {
                "nodes": prefix_spent,
                "completed_s6_children": len(prefix_exact),
                "completed_unknown_runs": prefix_completed_unknown,
                "started_rows": prefix_started,
                "final_row_censored": prefix_midrow_truncated,
                "derived_s5": RESULTS[prefix_s5],
                "remaining_s6_children_unobserved_or_unresolved": 90 - len(prefix_exact),
                "status": "UNKNOWN",
                "reconstruction_only": True,
            },
            "conclusion": "neither method resolved S5 at the 15M-node cap; the complete split used more nodes",
        },
        "resource_comparison": {
            "split_group_wall_seconds_rounded_sum": group_wall_seconds,
            "direct_reported_wall_seconds": direct["wall_seconds"],
            "wall_time_comparable": False,
            "reason_wall_time_not_comparable": "the split README records Debian i5-9400T; the direct raw does not identify its runtime host",
            "peak_rss_bytes": None,
            "peak_rss_comparison": "not recorded by the selected raw sources",
            "split_total_nodes": initial_nodes + retry_nodes,
            "direct_capped_nodes": direct["nodes"],
            "split_to_direct_node_ratio": round((initial_nodes + retry_nodes) / direct["nodes"], 6),
            "same_binary_hash_verified": False,
            "direct_solver_source_hash_recorded": False,
            "node_cost_reduction_demonstrated": False,
        },
        "strategy_router": {
            "historical_target": recovered,
            "current_s4_loss_goal": current_goal_plan,
            "selected_current_s5_key": None,
            "current_s4_dispatch": False,
            "current_s4_dispatch_reason": "the paired benchmark did not demonstrate lower node cost; no new S5 was selected or run",
            "current_s4": current_status,
            "historical_s5_is_child_of_current_s4": hard_root_in_current_boundary,
        },
        "provenance": provenance,
        "limits": [
            "The 15M split prefix is reconstructed from saved row costs and the documented batch order; it is not an additional solver run.",
            "Raw wall times and peak RSS do not form a controlled same-host comparison.",
            "The 90 S6 exact outcomes trust the saved solver results; they are not independent terminal-only minimax certificates.",
            "No UNKNOWN was promoted to exact and no solver-trusted outcome was called independently proven.",
        ],
    }
    manifest = {
        "schema": "n11-s5-hierarchical-adaptive-source-manifest-v1",
        "sources": provenance["source_manifests"],
        "copied_raw_files": files + [direct_file],
        "result_sha256": None,
    }
    return report, manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_RAW)
    parser.add_argument("--output-dir", type=Path, default=EX / "output")
    args = parser.parse_args()
    report, manifest = build_report(args.input_dir.resolve())
    args.output_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.output_dir / "strategy-audit.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    manifest["result_sha256"] = sha256(report_path)
    (args.output_dir / "source-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "report": report_path.relative_to(ROOT).as_posix(),
        "direct_15m": report["outcomes"]["direct_15m"],
        "split_nodes": report["outcomes"]["s6_full_split"]["total_nodes"],
        "same_budget_split": report["same_15m_node_cap"]["split_prefix"],
        "current_s4": report["strategy_router"]["current_s4"]["outcomes"],
        "node_cost_reduction_demonstrated": report["resource_comparison"]["node_cost_reduction_demonstrated"],
    }, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
