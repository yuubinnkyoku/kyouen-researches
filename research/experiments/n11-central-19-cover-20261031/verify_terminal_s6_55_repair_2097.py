#!/usr/bin/env python3
"""Independent exact-geometry audit of the 46-S6 repair after a new WIN6.

This is a conditional S5->S6 LOSS-witness cover, NOT a LOSS proof.
The terminal-proved WIN6 is excluded. Enumerate all 2-for-2 replacements
of that WIN6 plus one other selected S6, with the remaining 44 fixed.
Use a 4x4 integer determinant for all S7 frontiers; verify the terminal
certificate with a separate full-game strategy replay.
"""
import argparse
import base64
import copy
import hashlib
import itertools
import json
import zlib
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_s7_shared_frontier_46 as geom4
import verify_shared58_win6_repair_2089 as previous
import verify_terminal_s6_55_compact as terminal
import verify_terminal_s7_seven_win6 as seven

HERE = Path(__file__).resolve().parent
CERT = HERE / "terminal_s6_55_strategy.b64"
MANIFEST = HERE / "conditional_s6_cover_46_after_terminal_s6_55_repair_2097.json"
ROOT = "00000000000200801002000081000000"
OTHER = "00000000000000203820000002000000"
ADDED = ["00000000000000203820000000080000",
         "00000000000880801002000040000000"]
EXPECTED = (66, 2097, 2986)
UNKNOWN = {"s6": "UNKNOWN", "s4": "UNKNOWN",
           "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"}


def require(ok, why):
    if not ok:
        raise ValueError(why)


def terminal_evidence():
    raw = zlib.decompress(base64.b64decode(CERT.read_text(encoding="ascii")))
    require(hashlib.sha256(raw).hexdigest() == terminal.EXPECTED_SHA256,
            "terminal WIN6 certificate identity changed")
    require(terminal.verify(raw) == terminal.EXPECTED,
            "terminal WIN6 independent replay failed")
    return raw


def reconstruct():
    incidence, costs, fixed44, pairs, known_win6, known_win7, _ = previous.reconstruct()
    selected = fixed44 | {base.decode(k) for k in previous.EXPECTED_ADDED}
    require(len(selected) == 46 and base.decode(ROOT) in selected
            and base.decode(OTHER) in selected, "old 2089 plan changed")
    require(set().union(*(incidence[k] for k in selected)) == set(range(94)),
            "old S5 cover incomplete")
    require(base.decode(ROOT) not in known_win6,
            "new proof was already in the previous comparison set")
    shared = seven.audit()
    seven_parents = {base.decode(row["canonical_s6"]) for row in shared["parents"]}
    require(len(seven_parents) == 7 and base.decode(ROOT) in seven_parents
            and len(selected & seven_parents) == 1,
            "seven terminal WIN6 parents conflict with repaired selection")
    known_win6 = known_win6 | seven_parents
    return incidence, costs, selected, known_win6, known_win7


def audit(incidence, costs, selected, known_win6, known_win7):
    memo = {}

    def kids(board):
        if board not in memo:
            children = geom4.children(board)
            keys = {base.key(geom4.canonical(c)) for c in children}
            require(len(keys) == len(children) == costs[board],
                    "independent 4x4/3x3 S7 geometry disagreement")
            memo[board] = keys
        return memo[board]

    candidates = sorted(k for k in incidence
                        if k not in selected and k not in known_win6)
    all_options = []
    single_replacements = 0
    for other in sorted(selected - {base.decode(ROOT)}):
        fixed = selected - {base.decode(ROOT), other}
        covered = set().union(*(incidence[k] for k in fixed))
        missing = set(range(94)) - covered
        touching = [k for k in candidates if incidence[k] & missing]
        single_replacements += sum(missing <= incidence[k] for k in touching)
        for u, v in itertools.combinations(touching, 2):
            if not missing <= incidence[u] | incidence[v]:
                continue
            chosen = fixed | {u, v}
            require(len(chosen) == 46 and not (chosen & known_win6)
                    and set().union(*(incidence[k] for k in chosen))
                        == set(range(94)), "invalid replacement cover")
            distinct = set()
            raw_edges = 0
            for k in sorted(chosen):
                ch = kids(k)
                raw_edges += len(ch)
                distinct.update(ch)
            require(not (distinct & known_win7),
                    "known WIN7 selected as LOSS7 obligation")
            all_options.append((len(distinct), raw_edges,
                                base.key(other), base.key(u), base.key(v)))
    require(single_replacements == 0,
            "one-for-one replacement unexpectedly became possible")
    require(len(all_options) == EXPECTED[0],
            "number of exhaustive 2-for-2 repairs changed")
    best = min(all_options)
    require(best == (2097, 2986, OTHER, *ADDED),
            "claimed best fixed44 repair no longer optimal")
    return {"eligible_repair_pairs": len(all_options),
            "single_replacement_options": single_replacements,
        "refuted_repair_pairs_by_shared_s7": 2,
        "excluded_terminal_win6_parents": 7,
            "selected_s6": 46, "s5_covered": 94,
            "distinct_s7": best[0], "raw_s7_edges": best[1],
            "removed": [ROOT, best[2]], "added": list(best[3:]),
            "known_win6_conflicts": 0, "known_win7_conflicts": 0,
            "conditional_only": True, "two_stone_root": "UNKNOWN",
            "empty_board": "UNKNOWN"}


def verify_manifest(doc, result):
    require(doc.get("schema") == "n11-central49-terminal-win6-fixed44-repair-v2"
            and doc.get("source") ==
                "conditional_s6_cover_46_after_shared58_win6_repair_2089.json"
            and doc.get("terminal_certificate") == CERT.name
            and doc.get("terminal_raw_sha256") == terminal.EXPECTED_SHA256
            and doc.get("evidence_level") ==
                "GEOMETRY_ONLY_CONDITIONAL_S6_LOSS_WITNESS_COVER_NOT_VERDICTS"
            and doc.get("outcomes") == UNKNOWN,
            "manifest identity/provenance/outcome altered")
    for field in ("eligible_repair_pairs", "single_replacement_options",
                  "refuted_repair_pairs_by_shared_s7",
                  "excluded_terminal_win6_parents",
                  "selected_s6", "s5_covered", "distinct_s7", "raw_s7_edges",
                  "removed", "added", "known_win6_conflicts",
                  "known_win7_conflicts"):
        require(doc.get(field) == result[field],
                "manifest mismatch: " + field)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    terminal_evidence()
    result = audit(*reconstruct())
    doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
    verify_manifest(doc, result)
    if args.negative:
        tests = 0
        for change in (
            lambda d: d.__setitem__("distinct_s7", 2096),
            lambda d: d["added"].__setitem__(0, d["removed"][0]),
            lambda d: d["outcomes"].__setitem__("s6", "LOSS"),
            lambda d: d.__setitem__("eligible_repair_pairs", 67),
            lambda d: d.__setitem__("terminal_raw_sha256", "0" * 64),
        ):
            bad = copy.deepcopy(doc)
            change(bad)
            try:
                verify_manifest(bad, result)
            except (ValueError, KeyError, TypeError):
                tests += 1
            else:
                raise AssertionError("forged manifest accepted")
        result["negative_tests"] = tests
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
