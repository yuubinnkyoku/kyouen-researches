#!/usr/bin/env python3
"""Record the 9b6362d4 reply27 audit checkpoint in K0355 and the resume log."""
from __future__ import annotations

import hashlib
import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
K = ROOT / "research/knowledge/items/K0355-n11-reply27-cache-recovery-frontier.md"
LOG = ROOT / "research/log/n11-resume-20261006.md"
INVENTORY = OUT / "post-9b6362d4-reply27-checkpoint-artifact-hashes-20261008.json"

ITEMS = [
    ("post-9b6362d4-build-reply27-artifact-inventory.py", "verifier", "Validates the prior checkpoint at its recorded Git source and inventories the refreshed audit."),
    ("post-9b6362d4-update-checkpoint-records.py", "verifier", "Updates K0355 and the dated reply27 resume log."),
    ("post-9b6362d4-rank1-10448351135499567104-0-raw-history-audit-15m.json", "verifier", "79 remaining s5 children: 2,585 CSVs scanned, no exact result or same-budget UNKNOWN, all dispatch-ready."),
    ("post-9b6362d4-rank1-10448351135499567104-0-saved-s6-summary.json", "verifier", "Hash-validated saved-s6 intersection for all 79 children; all UNKNOWN, no derivation or conflict."),
    ("post-9b6362d4-rank1-10448351135499567104-0-saved-s6-full.json.gz", "source", "Complete saved-s6 child-boundary audit details for the 79 remaining s5 parents."),
    ("post-9b6362d4-rank1-10448351135499567104-0-saved-s6-derived-s5.cache", "data", "No s5 verdicts derive from the saved-s6 intersection."),
    ("post-9b6362d4-rank1-10448351135499567104-0-probe8.csv", "data", "Eight-target low-legal-count schedule; order is scheduling only."),
    ("post-9b6362d4-rank1-10448351135499567104-0-probe8-manifest.json", "manifest", "Probe schedule bound to target, cache, raw/s6 audits, solver and runner hashes."),
    ("post-9b6362d4-rank1-10448351135499567104-0-probe8-raw-history-audit-15m.json", "verifier", "Exact eight-key raw-history audit with requested 15M budget recorded in the file."),
    ("post-9b6362d4-rank1-10448351135499567104-0-probe8-saved-s6-summary.json", "verifier", "Exact eight-key saved-s6 intersection; all UNKNOWN and no new exact result."),
    ("post-9b6362d4-rank1-10448351135499567104-0-probe8-saved-s6-full.json.gz", "source", "Complete saved-s6 child-boundary details for the scheduled eight parents."),
    ("post-9b6362d4-rank1-10448351135499567104-0-probe8-saved-s6-derived-s5.cache", "data", "No s5 verdicts derive from the scheduled eight saved-s6 boundaries."),
    ("post-9b6362d4-rank1-10448351135499567104-0-probe8-preflight.json", "verifier", "Latest-main fail-closed preflight: eight ready, zero blocked, zero conflicts."),
    ("post-9b6362d4-reply27-checkpoint-artifact-hashes-20261008.json", "manifest", "Prior and current checkpoint artifacts, current/historical source hashes, and 79-key preflight inventory."),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def block(name: str, value: str) -> str:
    wrapped = textwrap.fill(value, width=110, initial_indent="  ", subsequent_indent="  ",
                            break_long_words=False, break_on_hyphens=False)
    return f"{name}: >-\n{wrapped}"


def main() -> int:
    if not INVENTORY.is_file():
        raise SystemExit(f"missing checkpoint inventory: {INVENTORY}")
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    inventory_hash = sha256(INVENTORY)

    text = K.read_text(encoding="utf-8")
    rows = []
    for name, role, note in ITEMS:
        path = f"research/experiments/n11-boundary-recovery-20261006/output/{name}"
        if not (ROOT / path).is_file():
            raise SystemExit(f"missing artifact: {path}")
        marker = f"  - path: {path}\n"
        if marker not in text:
            rows.append(f'  - path: {path}\n    role: {role}\n    note: "{note}"')
    if rows:
        text, n = re.subn(r"(?m)^scope:", "\n".join(rows) + "\nscope:", text, count=1)
        if n != 1:
            raise SystemExit(f"expected one scope field, found {n}")

    scope = (
        "Finite reply27 frontier at main 9b6362d4 after fresh, hash-bound raw-history and saved-s6 audits "
        "for the 79 UNKNOWN children of class (10448351135499567104,0). The eight-key probe is prepared "
        "and preflighted but has not been dispatched. Existing exact verdicts and the previous checkpoint "
        "remain unchanged."
    )
    evidence = (
        "Fetched and fast-forwarded nine incoming main commits from aa90bb5b to 9b6362d4. The incoming "
        "reply27 changes make raw-history audits record their requested budget and reject legacy budgetless "
        "audits; prior raw evidence was preserved. After the update, uv sync --locked passed, the knowledge "
        "check reports 363 items with zero errors or warnings, the knowledge unittest suite passes 33 tests, "
        "the experiment tests pass 30 tests, and knowledge build generated six views plus README. The "
        "generated diff adds the new K0369 view and expected K0355 artifacts. Latest exact s5 cache remains "
        "4,871 rows (121 WIN, 4,750 LOSS, conflict 0; SHA-256 "
        "0653c02857e30102c18287bfc2c25e864b6e445238e469747b736c3e4a612516). All 3,384 s4 statuses remain "
        "29 LOSS / 218 WIN / 3,137 UNKNOWN; secured third moves 113/119, six remain; minimum additional "
        "classes 3 equals rational dual 3 (dual-tight), with 275 distinct UNKNOWN s5 in the optimized repair. "
        "The target class has 104 canonical children (25 LOSS / 0 WIN / 79 UNKNOWN). On the updated main, "
        "the 79-key raw-history audit scanned 2,585 CSV files at requested 15M budget: zero prior exact, "
        "same-budget UNKNOWN, cache hits, or conflicts; all 79 are dispatch-ready. The hash-validated "
        "40-source saved-s6 intersection covers the same 79 parents, all UNKNOWN, deriving zero verdicts "
        "with zero conflicts. The selected eight-key schedule was separately re-audited against the same "
        "cache and budget: 2,586 CSVs, eight ready, zero blocked, zero exact, zero conflicts; saved-s6 "
        "leaves all eight UNKNOWN. Main's fail-closed preflight passes. No solver was dispatched. The new "
        f"inventory covers {len(inventory['artifacts'])} artifacts, "
        f"{len(inventory['manifested_sources'])} current manifested sources and "
        f"{len(inventory['historical_sources_verified_at_aa90bb5b'])} historical sources verified at aa90bb5b, "
        f"with zero missing paths; SHA-256 {inventory_hash}. A scoped `.gitattributes` rule disables "
        "newline normalization inside this experiment output tree, preserving each raw/artifact byte hash "
        "in Git. The staged blob audit is recorded in the resume entry. {60,27} and the 11×11 empty board remain UNKNOWN."
    )
    replacement = block("scope", scope) + "\n" + block("evidence", evidence) + "\n"
    text, n = re.subn(r"(?ms)^scope:.*?^evidence:.*?(?=^---\s*$)", replacement, text, count=1)
    if n != 1:
        raise SystemExit(f"expected one scope/evidence block, found {n}")
    K.write_text(text, encoding="utf-8", newline="\n")

    heading = "## 2026-10-08 15:36 JST refreshed dual-tight 79-key audit and strict preflight"
    entry = f"""{heading}

At start, `HEAD == origin/main == aa90bb5b914ce9901f24663a4a012cd62b1daf9a`; `git fetch origin main` brought nine commits through `9b6362d4cc0f115608bc6c5586cfdb5b509ce521`. Their reply27 changes bind the requested budget into raw-history JSON and make the probe preparation/preflight fail closed. No solver process was present. Fast-forwarded `main` while preserving all uncommitted raw evidence and `.local` files.

The pre-existing current exact s5 cache remains 4,871 rows (121 WIN / 4,750 LOSS / conflict 0), SHA-256 `0653c02857e30102c18287bfc2c25e864b6e445238e469747b736c3e4a612516`. Recomputed status checkpoint remains 3,384 s4 classes: LOSS 29 / WIN 218 / UNKNOWN 3,137; secured 113/119, remaining 6; minimum additional cover 3 equals rational dual 3 (dual-tight); reoptimized repair union 275 UNKNOWN s5. Candidate `(10448351135499567104,0)` remains 25 LOSS / 0 WIN / 79 UNKNOWN among 104 canonical children.

Regenerated the 79-key raw-history audit with `--budget 15000000` on updated main. It scanned 2,585 CSVs across `research/experiments` and `.local/n11`, finding zero prior exact results, same-budget UNKNOWNs, cache hits or conflicts; all 79 are ready. Recomputed the complete saved-s6 intersection from the 40-source hash-validated corpus for the same 79 keys: all remain UNKNOWN, zero exact derivations/conflicts. Selected an eight-key low-legal-count schedule. Its separately regenerated raw audit scanned 2,586 CSVs with eight ready, zero blocked/exact/conflict; matching saved-s6 audit has eight UNKNOWN and no derived result. `verify_dual_tight_probe_preflight.py` passes with the current cache, exact schedule, and recorded 15M budget. This is scheduling only; the solver has not been dispatched.

`uv sync --locked`, knowledge check (363 items, zero errors/warnings), knowledge unittest (33 tests), experiment tests (30 tests), and knowledge build passed. The generated diff adds expected K0369 and K0355 views; README has no unexpected hand edit. Inventory `post-9b6362d4-reply27-checkpoint-artifact-hashes-20261008.json` records {len(inventory['artifacts'])} artifacts and {len(inventory['manifested_sources'])} current sources, while verifying historical source hashes against aa90bb5b where main changed them; missing paths: 0, SHA-256 `{inventory_hash}`. A scoped `.gitattributes` rule disables newline normalization in the experiment output tree; the staged blob check confirms every inventoried artifact matches its recorded byte-level SHA-256. `.local` and prior raw outputs remain preserved. `{{60,27}}` and the 11×11 empty board remain UNKNOWN.

Next: stage only the documented experiment outputs, K0355, resume log and generated views; run the final staged/generated/hash checks; push directly to `main`, fetch again, then rerun strict preflight before any dispatch.
"""
    log_text = LOG.read_text(encoding="utf-8")
    if heading in log_text:
        before, _, _ = log_text.partition(heading)
        log_text = before.rstrip() + "\n\n" + entry
    else:
        log_text = log_text.rstrip() + "\n\n" + entry
    LOG.write_text(log_text, encoding="utf-8", newline="\n")
    print(f"updated K0355 with {len(ITEMS)} current-checkpoint artifacts and appended resume log")


if __name__ == "__main__":
    raise SystemExit(main())
