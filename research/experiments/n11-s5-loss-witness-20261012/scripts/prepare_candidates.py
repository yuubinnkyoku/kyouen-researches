"""Freeze the geometry-only S6 candidate schedules before running DFPN."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board, mask_from_key  # noqa: E402


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def source_row(target: dict) -> dict:
    path = ROOT / target["source_csv"]
    if not path.is_file():
        raise FileNotFoundError(path)
    digest = sha256(path)
    if target.get("source_csv_sha256") and digest != target["source_csv_sha256"].lower():
        raise ValueError(f"source SHA mismatch for {target['id']}")
    rows = []
    with path.open(encoding="utf-8", newline="") as stream:
        for row in csv.reader(stream):
            if row and row[0] == "replay" and len(row) == 11:
                if (int(row[9]), int(row[10])) == (target["lo"], target["hi"]):
                    rows.append(row)
    if len(rows) != 1:
        raise ValueError(f"expected exactly one source row for {target['id']}, got {len(rows)}")
    row = rows[0]
    if (int(row[2]), int(row[3]), int(row[6]), int(row[7])) != (
            target["stones"], target["legal"], target["expected_verdict"], target["prior_nodes"]):
        raise ValueError(f"provenance values differ for {target['id']}: {row}")
    return {"path": target["source_csv"], "sha256": digest,
            "bytes": path.stat().st_size, "reported_seconds": int(row[8]),
            "nodes": int(row[7]), "verdict": int(row[6])}


def validate_independent_sources(targets: dict) -> None:
    expected_by_group = {}
    for target in targets["positions"]:
        expected_by_group.setdefault(target["s4_group"], set()).add(
            str((target["hi"] << 64) | target["lo"]))
    for source in targets["independent_certificate_sources"]:
        cert_path = ROOT / source["path"]
        receipt_path = ROOT / source["receipt_path"]
        if sha256(cert_path) != source["sha256"] or sha256(receipt_path) != source["receipt_sha256"]:
            raise ValueError(f"independent source SHA mismatch: {source['path']}")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        roots = receipt["roots"]
        actual = {str(int(root["root"])) for root in roots if int(root["verdict"]) == 2}
        if (len(roots) != source["roots"] or receipt["trusted_leaves"] != 0
                or actual != expected_by_group["latest-s4" if "current-s4" in source["path"] else "previous-s4"]):
            raise ValueError(f"independent proof receipt does not match selected roots: {receipt_path}")
    integration = targets["six_root_integration_receipt"]
    integration_path = ROOT / integration["path"]
    if sha256(integration_path) != integration["sha256"]:
        raise ValueError("six-root integration receipt SHA mismatch")
    audit = json.loads(integration_path.read_text(encoding="utf-8"))
    independent = audit["independent_verification"]
    actual_roots = {str(int(root["root"])) for root in independent["roots"]
                    if int(root["verdict"]) == 2}
    expected_roots = set().union(*expected_by_group.values())
    if (independent["certificate_sha256"] != integration["reported_certificate_sha256"]
            or independent["trusted_leaves"] != 0 or len(independent["roots"]) != 6
            or actual_roots != expected_roots):
        raise ValueError("six-root integration audit does not match fixed sample")


def make_schedule(targets: dict, board: Board) -> dict:
    budget = targets["budget_protocol"]
    roots = []
    seen = set()
    validate_independent_sources(targets)
    for target in targets["positions"]:
        root = mask_from_key(target["lo"], target["hi"], board.n)
        if root.bit_count() != target["stones"] or board.canonical(root) != root:
            raise ValueError(f"noncanonical or wrong-rank S5 root: {target['id']}")
        legal_count = board.legal(root).bit_count()
        if legal_count != target["legal"] or target["expected_verdict"] != 2:
            raise ValueError(f"target geometry/outcome mismatch: {target['id']}")
        if root in seen:
            raise ValueError(f"duplicate S5 target: {target['id']}")
        seen.add(root)
        source = source_row(target)
        children = []
        for child in sorted(board.children(root)):
            if child.bit_count() != 6 or board.canonical(child) != child:
                raise ValueError(f"bad canonical S6 child of {target['id']}")
            children.append({
                "key": str(child),
                "lo": child & ((1 << 64) - 1),
                "hi": child >> 64,
                "stones": 6,
                "legal": board.legal(child).bit_count(),
            })
        if not children:
            raise ValueError(f"S5 has no legal S6 child: {target['id']}")
        key_order = sorted(children, key=lambda c: int(c["key"]))
        legal_order = sorted(children, key=lambda c: (c["legal"], int(c["key"])))
        cap = budget["max_s6_candidates_per_parent"]
        roots.append({
            "target": target,
            "source_row": source,
            "canonical_s6_children": len(children),
            "all_s6_children_key_order": key_order,
            "key_order_screen": key_order[:cap],
            "legal_count_order_screen": legal_order[:cap],
        })
    return {
        "schema": "n11-s5-loss-witness-schedule-v1",
        "geometry_source": "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py",
        "geometry_source_sha256": sha256(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"),
        "targets_sha256": sha256(EXP / "input/targets.json"),
        "board_size": board.n,
        "selection_order": ["A direct S5 exact DFPN", "B first five S6 canonical keys ascending",
                            "C/D/E first five S6 by ascending legal move count, then canonical key"],
        "budget_protocol": budget,
        "roots": roots,
    }


def main() -> None:
    targets_path = EXP / "input/targets.json"
    output_path = EXP / "input/s6-candidate-schedule.json"
    targets = json.loads(targets_path.read_text(encoding="utf-8"))
    schedule = make_schedule(targets, Board(targets["board_size"]))
    payload = (json.dumps(schedule, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    if output_path.exists():
        if json.loads(output_path.read_text(encoding="utf-8")) != schedule:
            raise ValueError(f"fixed schedule differs from regenerated geometry: {output_path}")
    else:
        output_path.write_bytes(payload)
    print(json.dumps({"path": str(output_path.relative_to(ROOT)),
                      "sha256": sha256(output_path),
                      "roots": len(schedule["roots"]),
                      "canonical_s6_children": [r["canonical_s6_children"] for r in schedule["roots"]]},
                     sort_keys=True))


if __name__ == "__main__":
    main()
