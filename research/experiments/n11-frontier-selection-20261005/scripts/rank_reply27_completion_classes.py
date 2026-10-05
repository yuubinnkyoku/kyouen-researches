#!/usr/bin/env python3
"""Rank current reply=27 repair classes for full exact completion.

This is a scheduling diagnostic.  It rebuilds the 3,384 canonical s4 classes,
loads the compact exact cache used by reply27_selected31_repair.py plus any
persisted adaptive-round caches, and ranks the *currently selected* repair
classes by how much exact s5 work remains before the class can become LOSS.

No UNKNOWN class is promoted here.  A class is only a completion target until
all of its remaining canonical s5 children are proved LOSS; one WIN child
invalidates it.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import reply27_selected31_repair as R  # noqa: E402


def load_cache(path: Path):
    out = {}
    with path.open(newline="", encoding="utf-8") as fp:
        for row in csv.reader(fp):
            if not row or row[0].startswith("#"):
                continue
            if row[0] != "s5verdict":
                continue
            key = (int(row[1]), int(row[2]))
            val = int(row[4])
            if val not in (1, 2):
                raise SystemExit(f"invalid verdict {val}: {key}")
            old = out.get(key)
            if old is not None and old != val:
                raise SystemExit(f"CONFLICT {key}: {old} vs {val}")
            out[key] = val
    return out


def merge(dst, src):
    for key, val in src.items():
        old = dst.get(key)
        if old is not None and old != val:
            raise SystemExit(f"CONFLICT {key}: {old} vs {val}")
        dst[key] = val


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repair-json", type=Path, required=True)
    ap.add_argument("--extra-s5-cache", type=Path, action="append", default=[])
    ap.add_argument("--targets-out", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    selected_doc = json.loads(R.SELECTED.read_text(encoding="utf-8"))
    verdict_doc = json.loads(R.VERDICTS.read_text(encoding="utf-8"))
    selected0 = {tuple(x) for x in selected_doc["classes"]}
    status0 = {
        tuple(map(int, row["key"])): row["status"]
        for row in verdict_doc["classes"]
    }
    if set(status0) != selected0:
        raise SystemExit("selected verdict manifest mismatch")

    verts, groups, coverage, children = R.build_geometry()
    derived = {}
    for key, st in status0.items():
        if st == "LOSS":
            for ch in children[key]:
                derived[ch] = 2
    merge(derived, load_cache(R.HARD9))
    for p in args.extra_s5_cache:
        merge(derived, load_cache(p))

    # Reclassify globally under the compact exact cache plus the manual selected
    # WIN exclusions.
    manual_win = {k for k, st in status0.items() if st == "WIN"}
    loss_classes = set()
    win_classes = set(manual_win)
    for key, ss in children.items():
        vals = [derived.get(ch, 0) for ch in ss]
        if 1 in vals:
            win_classes.add(key)
        elif vals and all(v == 2 for v in vals):
            loss_classes.add(key)
    if loss_classes & win_classes:
        raise SystemExit("class verdict conflict")

    secured = set()
    for key in loss_classes:
        secured.update(coverage[key])

    repair = json.loads(args.repair_json.read_text(encoding="utf-8"))
    selected = [
        tuple(map(int, row["key"]))
        for row in repair["additive_optimum"]["selected"]
    ]

    rows = []
    for key in selected:
        ss = children[key]
        vals = {ch: derived.get(ch, 0) for ch in ss}
        if any(v == 1 for v in vals.values()):
            raise SystemExit(f"selected repair class already WIN: {key}")
        unknown = [ch for ch, v in vals.items() if v == 0]
        known_loss = sum(v == 2 for v in vals.values())
        gain = coverage[key] - secured
        ranked_unknown = sorted(
            unknown,
            key=lambda ch: (R.legal_count_key(ch), ch[1], ch[0]),
        )
        rows.append({
            "key": list(key),
            "coverage": sorted(coverage[key]),
            "new_vertices": sorted(gain),
            "new_vertex_count": len(gain),
            "all_s5": len(ss),
            "known_loss_s5": known_loss,
            "unknown_s5": len(unknown),
            "known_loss_fraction": known_loss / len(ss) if ss else 1.0,
            "unknown_per_new_vertex": (
                len(unknown) / len(gain) if gain else float("inf")
            ),
            "min_unknown_legal": (
                R.legal_count_key(ranked_unknown[0]) if ranked_unknown else 0
            ),
            "max_unknown_legal": (
                max((R.legal_count_key(ch) for ch in ranked_unknown), default=0)
            ),
            "_unknown": ranked_unknown,
        })

    rows.sort(
        key=lambda row: (
            row["unknown_per_new_vertex"],
            row["unknown_s5"],
            -row["known_loss_fraction"],
            -row["new_vertex_count"],
            row["key"],
        )
    )

    clean = []
    for rank, row in enumerate(rows, 1):
        q = dict(row)
        q.pop("_unknown")
        q["rank"] = rank
        clean.append(q)

    best = rows[0] if rows else None
    out = {
        "root": [R.FIRST, R.R2],
        "derived_cache_entries": len(derived),
        "loss_classes": len(loss_classes),
        "win_forbidden_classes": len(win_classes),
        "secured_vertices": len(secured),
        "repair_classes": len(rows),
        "ranking_rule": (
            "unknown_s5/new_vertices, then unknown_s5, then known-loss fraction"
        ),
        "ranking": clean,
    }

    if args.targets_out and best is not None:
        args.targets_out.parent.mkdir(parents=True, exist_ok=True)
        with args.targets_out.open("w", encoding="utf-8") as fp:
            for seq, key in enumerate(best["_unknown"]):
                fp.write(R.exact_replay_row("reply27-class-completion", seq, key))
        out["best_target"] = {
            "key": best["key"],
            "unknown_s5": best["unknown_s5"],
            "new_vertices": best["new_vertices"],
            "targets_out": str(args.targets_out),
        }

    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    print("REPLY27_COMPLETION_RANK_OK")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
