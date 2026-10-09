#!/usr/bin/env python3
"""Union independently geometry-checked saved-S6 source audits fail-closed."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts"
sys.path.insert(0, str(SCRIPTS))
import audit_saved_s6_targets as s6_audit  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", action="append", type=Path, required=True,
                        help="previously hash-validated, geometry-checked saved-S6 source audit; repeatable")
    parser.add_argument("--scan-root", action="append", type=Path, default=[],
                        help="also scan raw .csv/.out solver files for S6 replay rows; repeatable")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise SystemExit(f"refusing to overwrite existing audit: {args.out}")
    if len(args.audit) < 2:
        raise SystemExit("at least two source audits are required")

    source_by_path: dict[str, dict] = {}
    result_by_key: dict[tuple[int, int], dict] = {}
    input_receipts = []
    for audit_path in args.audit:
        doc = json.loads(audit_path.read_text(encoding="utf-8"))
        if (doc.get("run_status") != "ok"
                or doc.get("source_hashes_validated") is not True
                or doc.get("s6", {}).get("all_s6_exact_rows_geometry_checked") is not True):
            raise SystemExit(f"input audit lacks complete hash/geometry attestation: {audit_path}")
        if len(doc.get("sources", [])) != doc.get("source_file_count"):
            raise SystemExit(f"input source count does not match manifest: {audit_path}")

        exact, _ = s6_audit.read_saved_exact_s6(doc)
        counts = Counter(str(item["verdict"]) for item in exact.values())
        input_receipts.append({
            "path": rel(audit_path),
            "sha256": sha256(audit_path),
            "source_file_count": len(doc["sources"]),
            "unique_canonical_s6_keys": len(exact),
            "unique_verdict_counts": dict(sorted(counts.items())),
        })

        for source in doc["sources"]:
            path = source.get("path", "").replace("\\", "/")
            if not path or type(source.get("s6_replay_rows")) is not int:
                raise SystemExit(f"malformed saved-S6 source entry in {audit_path}: {source}")
            item = {"path": path, "sha256": source.get("sha256"),
                    "s6_replay_rows": source["s6_replay_rows"]}
            previous = source_by_path.get(path)
            if previous is not None and previous != item:
                raise SystemExit(f"source manifest disagreement for {path}: {previous} vs {item}")
            source_by_path[path] = item

        for key, row in exact.items():
            previous = result_by_key.get(key)
            old_verdict = previous["verdict"] if previous else 0
            new_verdict = row["verdict"]
            if old_verdict in (1, 2) and new_verdict in (1, 2) and old_verdict != new_verdict:
                raise SystemExit(f"exact S6 verdict conflict for {key}: {old_verdict} vs {new_verdict}")
            if previous is None:
                result_by_key[key] = {"verdict": new_verdict}
            elif old_verdict == 0 and new_verdict in (1, 2):
                result_by_key[key]["verdict"] = new_verdict

    scan_roots = []
    scanned_files = 0
    s6_source_files = 0
    s6_replay_rows = 0
    discovered_sources = []
    for root in args.scan_root:
        if not root.is_dir():
            raise SystemExit(f"raw S6 scan root does not exist: {root}")
        files = sorted(path for path in root.rglob("*")
                       if path.is_file() and path.suffix.lower() in {".csv", ".out"})
        root_s6_files = 0
        root_s6_rows = 0
        for path in files:
            scanned_files += 1
            path_text = rel(path)
            previous_source = source_by_path.get(path_text)
            row_count = 0
            row_results: list[tuple[tuple[int, int], int]] = []
            with path.open(newline="", encoding="utf-8-sig") as stream:
                for row_num, row in enumerate(csv.reader(stream), 1):
                    if not row or row[0].lstrip().startswith("#") or row[0] != "replay":
                        continue
                    if len(row) < 3 or not row[2].isdigit() or int(row[2]) != 6:
                        continue
                    if len(row) != 11 or int(row[4]) != 1:
                        raise SystemExit(f"invalid raw S6 replay row {path}:{row_num}: {row}")
                    verdict, nodes = int(row[6]), int(row[7])
                    if verdict not in (0, 1, 2) or nodes < 0:
                        raise SystemExit(f"invalid raw S6 verdict/nodes {path}:{row_num}: {row}")
                    if previous_source is None:
                        raw_key = (int(row[9]), int(row[10]))
                        raw_points = s6_audit.points(raw_key)
                        if len(raw_points) != 6 or s6_audit.has_forbidden_quad(raw_points):
                            raise SystemExit(f"unsafe raw S6 replay key {path}:{row_num}: {raw_key}")
                        canonical = tuple(s6_audit.d4_canonical_key(raw_points))
                        if not s6_audit.safe_canonical(canonical, 6):
                            raise SystemExit(f"unsafe canonical S6 key {path}:{row_num}: {canonical}")
                        if int(row[3]) != len(s6_audit.legal_after(set(raw_points))):
                            raise SystemExit(f"raw S6 legal-count mismatch {path}:{row_num}: {row}")
                        row_results.append((canonical, verdict))
                    row_count += 1
            if not row_count:
                continue
            root_s6_files += 1
            root_s6_rows += row_count
            s6_source_files += 1
            s6_replay_rows += row_count
            source = {"path": path_text, "sha256": sha256(path),
                      "s6_replay_rows": row_count}
            if previous_source is not None and previous_source != source:
                raise SystemExit(f"raw S6 source differs from audited manifest: {path_text}")
            if previous_source is None:
                source_by_path[path_text] = source
                discovered_sources.append(path_text)
            for key, verdict in row_results:
                previous = result_by_key.get(key)
                old_verdict = previous["verdict"] if previous else 0
                if old_verdict in (1, 2) and verdict in (1, 2) and old_verdict != verdict:
                    raise SystemExit(f"exact S6 verdict conflict during raw scan for {key}: {old_verdict} vs {verdict}")
                if previous is None:
                    result_by_key[key] = {"verdict": verdict}
                elif old_verdict == 0 and verdict in (1, 2):
                    result_by_key[key]["verdict"] = verdict
        scan_roots.append({"path": rel(root), "files_examined": len(files),
                           "s6_source_files": root_s6_files,
                           "s6_replay_rows": root_s6_rows})

    counts = Counter(str(item["verdict"]) for item in result_by_key.values())
    exact_counts = {key: counts[key] for key in ("1", "2") if counts[key]}
    result = {
        "schema": "n11-saved-s6-source-audit-union-v1",
        "run_status": "ok",
        "source_hashes_validated": True,
        "source_file_count": len(source_by_path),
        "sources": [source_by_path[key] for key in sorted(source_by_path)],
        "s6": {
            "unique_canonical_keys": len(result_by_key),
            "unique_win_keys": counts["1"],
            "unique_loss_keys": counts["2"],
            "unknown_unique_keys": counts["0"],
            "verdict_counts_by_unique_key": exact_counts,
            "all_s6_exact_rows_geometry_checked": True,
            "attestation_basis": "Every input source audit passed hash validation and geometry/legal checks; source rows were rehydrated and canonicalized by audit_saved_s6_targets.read_saved_exact_s6. Exact WIN/LOSS conflicts were rejected.",
        },
        "union_provenance": {
            "method": "deduplicate source paths from independently validated source audits, verify each source hash and row count again, and union canonical verdicts; exact conflicts fail closed",
            "input_audits": input_receipts,
            "builder": {"path": rel(Path(__file__).resolve()),
                        "sha256": sha256(Path(__file__).resolve())},
            "rehydration_auditor": {
                "path": rel(SCRIPTS / "audit_saved_s6_targets.py"),
                "sha256": sha256(SCRIPTS / "audit_saved_s6_targets.py"),
            },
            "raw_source_scan": {
                "roots": scan_roots,
                "files_examined": scanned_files,
                "s6_source_files": s6_source_files,
                "s6_replay_rows": s6_replay_rows,
                "sources_not_in_input_audit_manifests": discovered_sources,
                "validation": "Input-manifest sources were rehydrated through the hash- and geometry-checking saved-S6 auditor. The raw scan checked their source hashes and row counts; any source absent from all input manifests was additionally checked row-by-row for legal count, safety, D4 canonical form, verdict, and node count before being added.",
            },
        },
    }
    # Re-run the production source rehydrator against the union summary before saving it.
    s6_audit.read_saved_exact_s6(result)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8", newline="\n")
    print(json.dumps({"sources": len(source_by_path),
                      "unique_s6_keys": len(result_by_key),
                      "verdict_counts": dict(sorted(counts.items())),
                      "exact_conflicts": 0, "out": rel(args.out)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
