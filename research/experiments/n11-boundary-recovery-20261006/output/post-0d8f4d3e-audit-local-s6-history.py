#!/usr/bin/env python3
"""Rebind local S6 same-budget history scans to the current 11-parent cache."""
from __future__ import annotations
import csv, hashlib, json, subprocess, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
BASE = "post-0d8f4d3e-active-class-10448351135499550722-0"
TARGET_DIR = OUT / f"{BASE}-s6-history-parent-targets"
TARGET_MANIFEST = OUT / f"{BASE}-s6-history-targets-manifest.json"
SAVED_AUDIT = OUT / "post-1001d051-reconciliation-20261009-augmented-s6-source-audit.json"
SAVED_FULL = OUT / f"{BASE}-saved-s6-full.json.gz"
CACHE = OUT / f"{BASE}-merged-s5.cache"
AUDIT_SCRIPT = ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/audit_local_s6_boundary_history.py"
HISTORY_DIR = OUT / f"{BASE}-s6-history-audits"
PREFLIGHT = OUT / f"{BASE}-s6-history-preflight.json"

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    if HISTORY_DIR.exists() or PREFLIGHT.exists():
        raise SystemExit("refusing to overwrite local S6 history audit artifacts")
    targets = sorted(TARGET_DIR.glob("s5-*.csv"))
    if len(targets) != 11:
        raise SystemExit(f"expected 11 current parent target inputs, got {len(targets)}")
    HISTORY_DIR.mkdir()
    audits = []
    for target in targets:
        rows = [r for r in csv.reader(target.open(newline="", encoding="utf-8-sig"))
                if r and not r[0].lstrip().startswith("#")]
        if len(rows) != 1:
            raise SystemExit(f"expected exactly one parent row in {target}")
        key = (int(rows[0][3]), int(rows[0][4]))
        audit_path = HISTORY_DIR / f"s5-{key[0]}-{key[1]}.json"
        cmd = [sys.executable, str(AUDIT_SCRIPT), "--parent", str(target),
               "--saved-audit", str(SAVED_AUDIT), "--saved-full-detail", str(SAVED_FULL),
               "--s5-cache", str(CACHE), "--local-root", str(ROOT / ".local/n11"),
               "--budget", "2000000", "--out", str(audit_path)]
        completed = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
        if completed.returncode:
            raise SystemExit(f"local S6 history audit failed for {key}:\n{completed.stdout}\n{completed.stderr}")
        doc = json.loads(audit_path.read_text(encoding="utf-8"))
        if doc.get("conflicts") != 0 or doc["parent"].get("key") != list(key):
            raise SystemExit(f"invalid local history audit receipt for {key}")
        audits.append((key, target, audit_path, doc))

    unique = {}
    for parent, target, audit_path, doc in audits:
        for entry in doc["boundary_entries"]:
            key = tuple(entry["key"])
            status = entry["saved_status"]
            if key in unique and unique[key][0] != status:
                raise SystemExit(f"saved S6 status differs across parent audits for {key}")
            unique.setdefault(key, [status, [], []])[1].extend(entry.get("local_observations", []))
            unique[key][2].extend(entry.get("same_or_higher_budget_local_unknowns", []))
            unique[key][2].extend(entry.get("same_or_higher_budget_saved_unknowns", []))
    saved_counts = Counter(row[0] for row in unique.values())
    blocked_keys = sorted(key for key, (_, _, unknown_rows) in unique.items()
                          if any(r.get("verdict") == 0 and r.get("budget", 0) >= 2_000_000
                                 for r in unknown_rows))
    local_exact_new = []
    for key, (saved_status, observations, _) in unique.items():
        exact_local = {int(r["verdict"]) for r in observations if int(r["verdict"]) in (1, 2)}
        if len(exact_local) > 1:
            raise SystemExit(f"local exact S6 conflict for {key}: {sorted(exact_local)}")
        if exact_local and saved_status not in ("WIN", "LOSS"):
            local_exact_new.append([list(key), next(iter(exact_local))])
        if exact_local and saved_status in ("WIN", "LOSS"):
            expected = 1 if saved_status == "WIN" else 2
            if exact_local != {expected}:
                raise SystemExit(f"local/saved S6 conflict for {key}")
    if local_exact_new:
        raise SystemExit(f"local exact S6 outcomes need reuse/materialization before dispatch: {local_exact_new[:10]}")

    total_incidences = sum(doc["geometry"]["boundary_child_count"] for _, _, _, doc in audits)
    ready_keys = sorted(k for k, (status, _, unknown_rows) in unique.items()
                        if status not in ("WIN", "LOSS")
                        and not any(r.get("verdict") == 0 and r.get("budget", 0) >= 2_000_000
                                    for r in unknown_rows))
    per_parent = []
    for key, target, audit_path, doc in audits:
        per_parent.append({"key": list(key), "boundary_children": doc["geometry"]["boundary_child_count"],
                           "saved_counts": doc["boundary_saved_verdict_counts"],
                           "local_csvs_scanned": doc["local_history"]["csv_files_scanned"],
                           "local_boundary_rows": doc["local_history"]["boundary_rows"],
                           "same_or_higher_budget_unknowns": len(doc["same_or_higher_budget_unknown_keys"]),
                           "ready": doc["direct_dispatch_ready_count"],
                           "target": {"path": target.relative_to(ROOT).as_posix(), "sha256": sha(target)},
                           "audit": {"path": audit_path.relative_to(ROOT).as_posix(), "sha256": sha(audit_path)}})
    report = {
        "schema": "n11-reply27-local-s6-history-preflight-v1",
        "class_key": [10448351135499550722, 0],
        "requested_s6_budget": 2000000,
        "parent_count": len(audits),
        "parent_outcomes": {"UNKNOWN": len(audits)},
        "s6_boundary_union": len(unique),
        "parent_child_incidences": total_incidences,
        "saved_s6_verdict_counts_over_unique_union": dict(sorted(saved_counts.items())),
        "same_or_higher_budget_unknown_s6_keys": len(blocked_keys),
        "direct_dispatch_ready_unique_s6_keys": len(ready_keys),
        "local_new_exact_s6_rows_requiring_reuse": 0,
        "conflicts": 0,
        "ready_s6_keys": [list(k) for k in ready_keys],
        "sources": [{"path": p.relative_to(ROOT).as_posix(), "sha256": sha(p), "bytes": p.stat().st_size}
                    for p in [TARGET_MANIFEST, SAVED_AUDIT, SAVED_FULL, CACHE, AUDIT_SCRIPT, Path(__file__).resolve()]],
        "parents": per_parent,
        "claim": "Only saved exact S6 verdicts and validated local exact history are reused. Same-or-higher-budget UNKNOWN S6 keys are blocked; UNKNOWN is not propagated.",
    }
    PREFLIGHT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"s5_parents": len(audits), "s6_union": len(unique),
                      "parent_child_incidences": total_incidences,
                      "saved_s6": dict(sorted(saved_counts.items())),
                      "same_budget_unknown_s6": len(blocked_keys), "ready_s6": len(ready_keys),
                      "conflicts": 0, "preflight_sha256": sha(PREFLIGHT)}, sort_keys=True))

if __name__ == "__main__":
    main()
