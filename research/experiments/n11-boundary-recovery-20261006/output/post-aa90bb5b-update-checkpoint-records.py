#!/usr/bin/env python3
"""Update K0355 and the reply27 resume log for this checkpoint."""
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

ITEMS = [
    ("post-aa90bb5b-collect-s6-descent-evidence.py", "verifier", "Archives and audits the exact 83-child s6 descent."),
    ("post-aa90bb5b-augment-saved-s6-source-audit.py", "verifier", "Adds the new hash-attested s6 rows to the validated saved-s6 source union."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-descent-parent.csv", "data", "Single unresolved s5 parent sent to complete canonical s6 boundary."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-descent-raw-all.csv", "source", "83 exact s6 replay rows covering the complete canonical boundary."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-descent-exact-s6.cache", "data", "Exact s6 cache, 83 WIN and zero LOSS."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-descent-derived-s5.cache", "data", "Single exact s5 WIN derived from the complete all-WIN s6 boundary."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-descent-runner-summary.json", "data", "Complete-boundary solver run summary and node count."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-descent-receipt.json", "manifest", "Collection receipt for the complete s6 boundary."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-descent-sources.json", "manifest", "Hash-bound source and per-child raw evidence manifest."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-win-geometry-audit.json", "verifier", "Independent complete s5/s6 geometry and reverse-incidence audit."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-updated-class-boundary-audit.json", "verifier", "All 102 canonical s5 children verify the s4 class as WIN."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-merged-s5.cache", "data", "Merged exact s5 cache after the s6-derived witness."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-merge-receipt.json", "manifest", "Exact cache merge receipt with zero conflicts."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-cardinality.json", "data", "Recomputed all-class cardinality and rational dual."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-selected31-repair.json", "data", "Reoptimized repair and distinct UNKNOWN s5 union."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-dual-tight-ranking.json", "data", "Dual-tight next-class ranking after exact cache merge."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-next-target-unknowns.csv", "data", "Ranked class UNKNOWN s5 targets."),
    ("post-aa90bb5b-augmented-saved-s6-source-audit.json", "manifest", "40-source saved-s6 union including the new exact descent."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-next-raw-history-audit.json", "verifier", "Raw replay and same-budget audit for the initial 95-key target."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-next-augmented-saved-s6-summary.json", "verifier", "Saved-s6 intersection for the 95 candidate s5 parents."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-next-augmented-saved-s6-full.json.gz", "source", "Full saved-s6 child-boundary details for the candidate parents."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-ready.csv", "data", "Audited eight-key probe schedule."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-ready-manifest.json", "manifest", "Schedule and input source hashes."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-ready-preflight.json", "verifier", "Fail-closed preflight for the exact eight-key schedule."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-raw-all.csv", "source", "Eight exact s5 LOSS replay rows, 29,685,506 nodes."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-new-exact-s5.cache", "data", "Exact s5 LOSS delta from the first eight-key batch."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-merged-s5.cache", "data", "Exact cache after the first eight-key batch."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-merge-receipt.json", "manifest", "First batch exact cache merge receipt."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-sources.json", "manifest", "First batch source/raw hashes and per-target results."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-class-boundary-audit.json", "verifier", "Full canonical s5 boundary after the first batch."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-cardinality.json", "data", "All-class exact status and cover after the first batch."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-repair.json", "data", "Repair optimization after the first batch."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-dual-tight-ranking.json", "data", "Re-ranked repair classes after the first batch."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-next-raw-history-audit.json", "verifier", "Fresh raw-history audit for the remaining 87 candidate keys."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-next-augmented-saved-s6-summary.json", "verifier", "Saved-s6 audit for the remaining 87 candidate keys."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-ready.csv", "data", "Second audited eight-key probe schedule."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-ready-manifest.json", "manifest", "Second schedule and source hashes."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-ready-preflight.json", "verifier", "Fail-closed preflight for the second exact eight-key schedule."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-raw-all.csv", "source", "Second batch exact s5 LOSS replay rows, 27,060,139 nodes."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-new-exact-s5.cache", "data", "Exact s5 LOSS delta from the second batch."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-merged-s5.cache", "data", "Current exact s5 cache after both batches."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-merge-receipt.json", "manifest", "Second batch exact cache merge receipt."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-sources.json", "manifest", "Second batch source/raw hashes and per-target results."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-class-boundary-audit.json", "verifier", "Full canonical 104-child class boundary: 25 LOSS / 0 WIN / 79 UNKNOWN."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-cardinality.json", "data", "All-class cardinality and LP dual after both batches."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-repair.json", "data", "Reoptimized repair after both batches."),
    ("post-aa90bb5b-rank1-1297036692682702976-128-s6-probe8-collected-probe8-2-collected-dual-tight-ranking.json", "data", "Ranked next target after both batches."),
    ("post-aa90bb5b-build-reply27-artifact-inventory.py", "verifier", "Checkpoint inventory builder."),
    ("post-aa90bb5b-update-checkpoint-records.py", "verifier", "Updates K0355 and the dated reply27 resume log."),
    ("post-aa90bb5b-reply27-checkpoint-artifact-hashes-20261008.json", "manifest", "204 artifact files and 2,702 manifested sources; no missing or mismatched hashes."),
]


def main() -> None:
    text = K.read_text(encoding="utf-8")
    already_added = "post-aa90bb5b-reply27-checkpoint-artifact-hashes-20261008.json" in text
    rows = []
    for name, role, note in ITEMS:
        path = f"research/experiments/n11-boundary-recovery-20261006/output/{name}"
        if not (ROOT / path).is_file():
            raise SystemExit(f"missing artifact: {path}")
        rows.append(f'  - path: {path}\n    role: {role}\n    note: "{note}"')
    if not already_added:
        text, n = re.subn(r"(?m)^scope:", "\n".join(rows) + "\nscope:", text, count=1)
        if n != 1:
            raise SystemExit(f"expected one scope field, found {n}")

    inventory_path = OUT / "post-aa90bb5b-reply27-checkpoint-artifact-hashes-20261008.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory_hash = hashlib.sha256(inventory_path.read_bytes()).hexdigest()
    artifact_count = len(inventory["artifacts"])
    source_count = len(inventory["manifested_sources"])

    scope = (
        "Finite reply27 frontier after the fully exact s6-WIN boundary for class "
        "(1297036692682702976,128) and two bounded all-LOSS probes for class "
        "(10448351135499567104,0). The current exact s5 cache has 4,871 rows; all 3,384 s4 "
        "statuses are recomputed. The latest class remains UNKNOWN with 79 unknown s5 children."
    )
    evidence = """At main aa90bb5b914ce9901f24663a4a012cd62b1daf9a, class (1297036692682702976,128) received a bounded 8-key probe (7 exact LOSS, 1 UNKNOWN; 30,969,417 nodes). The UNKNOWN s5 parent (3602879701896396928,128) was taken to its independently rebuilt complete canonical s6 boundary: all 83 children were exact WIN (23,967,140 nodes), deriving that s5 as WIN. Geometry and reverse-incidence audit verifies the witness and the enclosing s4 class WIN; its full 102-child boundary is 14 LOSS / 1 WIN / 87 UNKNOWN, and no remaining siblings were explored. The exact s5 WIN witness changes three reachable reply27 parent classes to WIN. No s6 LOSS or reverse-propagated LOSS was produced. The refreshed 40-source saved-s6 union has 2,973 unique canonical s6 keys (2,780 WIN, 147 LOSS, 46 UNKNOWN-only; conflict 0). The next dual-tight target (10448351135499567104,0) has 104 canonical s5 children. Its first two audited 8-key probes returned 16 exact LOSS in 56,745,645 nodes, no WIN or UNKNOWN. Its complete class boundary is 25 LOSS / 0 WIN / 79 UNKNOWN. The merged exact s5 cache has 4,871 rows (WIN 121 / LOSS 4,750 / conflict 0), SHA-256 0653c02857e30102c18287bfc2c25e864b6e445238e469747b736c3e4a612516. Across all 3,384 s4 classes: LOSS 29 / WIN 218 / UNKNOWN 3,137; secured third moves 113/119 and six remain. Minimum additional class cover and rational LP dual are both 3 (dual-tight); reoptimized repair has 3 classes and 275 distinct UNKNOWN s5 children. The latest rank-1 target remains (10448351135499567104,0), with 79 UNKNOWN s5 children; its current raw-history and saved-s6 intersection must be refreshed before the next dispatch. {60,27} and the 11×11 empty board remain UNKNOWN."""

    evidence += (
        f" Checkpoint inventory post-aa90bb5b-reply27-checkpoint-artifact-hashes-20261008.json "
        f"covers {artifact_count} artifacts and {source_count} manifested sources, with zero missing or "
        f"mismatched hashes; SHA-256 {inventory_hash}."
    )

    def block(name: str, value: str) -> str:
        wrapped = textwrap.fill(value, width=110, initial_indent="  ", subsequent_indent="  ",
                                break_long_words=False, break_on_hyphens=False)
        return f"{name}: >-\n{wrapped}"

    replacement = block("scope", scope) + "\n" + block("evidence", evidence) + "\n"
    text, n = re.subn(
        r"(?ms)^scope:.*?^evidence:.*?(?=^---\s*$)",
        replacement,
        text,
        count=1,
    )
    if n != 1:
        raise SystemExit(f"expected one scope/evidence block, found {n}")
    K.write_text(text, encoding="utf-8", newline="\n")

    section = "## 2026-10-08 15:20 JST reply27 s6-WIN recovery and dual-tight LOSS probes"
    log_text = LOG.read_text(encoding="utf-8")
    entry = f"""## 2026-10-08 15:20 JST reply27 s6-WIN recovery and dual-tight LOSS probes

At start, `HEAD == origin/main == aa90bb5b914ce9901f24663a4a012cd62b1daf9a`; fetch succeeded with no incoming main changes. The eight-key probe for `(1297036692682702976,128)` returned seven exact LOSS and one UNKNOWN (30,969,417 nodes). The UNKNOWN parent `(3602879701896396928,128)` had a complete canonical s6 boundary of 83/83 exact WIN (23,967,140 nodes). The saved raw rows, exact s6 cache, derived s5 WIN, and geometry audit confirm all-WIN recurrence and legal parent incidence. Full s4 boundary is 14 LOSS / 1 WIN / 87 UNKNOWN; remaining siblings were stopped. No exact s6 LOSS or reverse-propagated LOSS occurred. Its exact s5 WIN witness also changes three reachable reply27 parent classes to WIN.

The refreshed saved-s6 source union validates 40 raw sources and 2,973 unique canonical s6 keys (2,780 WIN / 147 LOSS / 46 UNKNOWN-only; conflict 0). The current rank-1 candidate `(10448351135499567104,0)` had 104 canonical children. Two separately scheduled and audited eight-key probes each produced eight exact LOSS, totaling 16 LOSS and 56,745,645 nodes; no WIN/UNKNOWN occurred. Geometry rebuilt all 104 children as 25 LOSS / 0 WIN / 79 UNKNOWN, so the class remains UNKNOWN.

Exact s5 cache: 4,871 entries (WIN 121 / LOSS 4,750 / conflict 0), SHA-256 `0653c02857e30102c18287bfc2c25e864b6e445238e469747b736c3e4a612516`. Recomputed all 3,384 s4 classes: LOSS 29 / WIN 218 / UNKNOWN 3,137. Secured vertices 113/119; remaining 6. Integer minimum cover 3 equals rational dual 3 (dual-tight). Reoptimized repair: 3 classes, 275 distinct UNKNOWN s5.

Next rank-1 remains `(10448351135499567104,0)` with 79 UNKNOWN s5 children. Refresh raw-history and saved-s6 audits for these 79 before dispatch. Checkpoint inventory `post-aa90bb5b-reply27-checkpoint-artifact-hashes-20261008.json` covers {artifact_count} artifacts and {source_count} manifested sources, with zero missing or hash mismatches; SHA-256 `{inventory_hash}`. `{{60,27}}` and the 11×11 empty board remain UNKNOWN.
"""
    if section in log_text:
        before, _, _ = log_text.partition(section)
        updated_log = before.rstrip() + "\n\n" + entry
    else:
        updated_log = log_text.rstrip() + "\n\n" + entry
    LOG.write_text(updated_log, encoding="utf-8", newline="\n")
    print(f"updated K0355 with {len(ITEMS)} artifacts and appended the reply27 checkpoint log")


if __name__ == "__main__":
    main()
