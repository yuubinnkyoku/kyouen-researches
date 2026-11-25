"""WIN-side re-analysis for first move 49 after the three native receipts
(115540 LOSS, 144193 LOSS, 144311 WIN) and the two extra S6-certificate
parents (381858, 382619 LOSS).

Flow follows n11-night-plan-update7-20261015/scripts/update_win_side.py (itself
the sixth-update win-side script, and so on back to win_side.py +
win_witness_masks.py), with three changes:

* the exact-S5 cache gains the three native receipts plus every parent of the
  frozen six-stone terminal LOSS certificate (the seventh update used only the
  three plan-required parents; the fifth and sixth parents are added here);
* the stored 1,945-mask pool loses exactly the sixteen resolved receipt keys
  (558600 was never in the pool), leaving 1,929 allowed witnesses, so damage
  from the two removed LOSS witnesses and the new WIN is attributed per key;
* the frozen K0423-basis ranking rows of 115540 / 144193 / 144311 are
  reproduced branch by branch exactly like 162106 was in the seventh update.

Two measurements are produced, as before: pre-optimisation damage on the stored
chosen thirds, and full re-optimisation over all 65 reply orbits restricted to
the remaining stored pool.  No solver search is involved and no witness is
invented.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
COST_CMP = ROOT / "research/experiments/n11-proof-cost-comparison-20261012"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
PREV = ROOT / "research/experiments/n11-night-plan-update7-20261015/output"
RANK = ROOT / "research/experiments/n11-conflict-ranking-20261013/output"
S6DIR = ROOT / "research/experiments/n11-s6-terminal-loss-20261015"
NATIVE = ROOT / "research/experiments/n11-native-terminal-checker-20261013/output"
S6_CERT_SHA = "cb2e73c277c6fd526689db64b1d8c07ebd1ca1bd8c2a966e0757d22c4471ebf6"
S6_ROOT = int("00000000040004001004000004010000", 16)

sys.path.insert(0, str(COST_CMP / "scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-s7-fifth-terminal-20261015"))
from independent import Board  # noqa: E402
from analyze_central_reply_frontier import load_exact_s5_cache, sha  # noqa: E402
from s4_win_polarity import classify_s4, verdict_of, FREE, OPEN, DEAD, WIN  # noqa: E402
from win_side import greedy_witness_cover  # noqa: E402
from fifth_verify_standalone import canonical, points  # noqa: E402

K0423 = ROOT / "research/experiments/n11-s5-s6-quotient-20261013/output"
ADAPTIVE = ROOT / "research/experiments/n11-adaptive-verify-20261013/output"
PROBE = ROOT / "research/experiments/n11-adaptive-probe-20261013/output"
NIGHT1 = ROOT / "research/experiments/n11-night-batch1-20261014/output"
NIGHT2 = ROOT / "research/experiments/n11-night-batch2-20261014/output"
NIGHT3 = ROOT / "research/experiments/n11-night-batch3-20261014/output"
NIGHT4 = ROOT / "research/experiments/n11-night-batch4-20261014/output"
NIGHT5 = ROOT / "research/experiments/n11-night-batch5-20261014/output"
UPD8 = EXP / "output"

RECEIPTS = {
    558600: (K0423, "pilot-558600-terminal-verification.json", "pilot-558600-terminal-dag.json.gz"),
    209644: (K0423, "pilot-209644-terminal-verification.json", "pilot-209644-terminal-dag.json.gz"),
    126899: (ADAPTIVE, "pilot-126899-receipt.json", "pilot-126899-terminal-dag.json.gz"),
    144095: (ADAPTIVE, "pilot-144095-receipt.json", "pilot-144095-terminal-dag.json.gz"),
    121263: (PROBE, "adaptive-121263-receipt.json", "adaptive-121263-terminal-dag.json.gz"),
    145001: (PROBE, "adaptive-145001-receipt.json", "adaptive-145001-terminal-dag.json.gz"),
    137694: (NIGHT1, "night-a-137694-receipt.json", "night-a-137694-terminal-dag.json.gz"),
    143240: (NIGHT1, "night-a-143240-receipt.json", "night-a-143240-terminal-dag.json.gz"),
    220231: (NIGHT1, "night-a-220231-receipt.json", "night-a-220231-terminal-dag.json.gz"),
    126017: (NIGHT1, "nightb10m-126017-receipt.json", "nightb10m-126017-terminal-dag.json.gz"),
    197665: (NIGHT2, "nighta25m-197665-receipt.json", "nighta25m-197665-terminal-dag.json.gz"),
    206386: (NIGHT3, "nighta25m-206386-receipt.json", "nighta25m-206386-terminal-dag.json.gz"),
    131631: (NIGHT4, "nighta25m-131631-receipt.json", "nighta25m-131631-terminal-dag.json.gz"),
    162106: (NIGHT5, "nighta25m-162106-receipt.json", "nighta25m-162106-terminal-dag.json.gz"),
    115540: (NATIVE, "pilot-115540-receipt.json", "pilot-115540-terminal-dag.json.gz"),
    144193: (NATIVE, "pilot-144193-receipt.json", "pilot-144193-terminal-dag.json.gz"),
    144311: (NATIVE, "pilot-144311-receipt.json", "pilot-144311-terminal-dag.json.gz"),
    150871: (UPD8, "receipt-150871.json", "terminal-150871-dag.json.gz"),
}
EXPECTED = {558600: 2, 209644: 1, 126899: 2, 144095: 1, 121263: 2, 145001: 2,
            137694: 2, 143240: 2, 220231: 2, 126017: 1, 197665: 1, 206386: 1,
            131631: 1, 162106: 1, 115540: 2, 144193: 2, 144311: 1, 150871: 2}
S6_LOSSES = (381840, 402066, 550881)
S6_EXTRA = (381858, 382619)
NEW_WIN = (144311,)
NEW_LOSS = (115540, 144193, 150871)
FIRST = 49


def key_of(mask: int) -> tuple[int, int]:
    return mask & ((1 << 64) - 1), mask >> 64


def main() -> None:
    started = time.time()
    analysis_path = COST_CMP / "output/win-side-analysis.json"
    masks_path = COST_CMP / "output/win-witness-masks.json"
    analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
    assert analysis["schema"] == "n11-win-side-analysis-v2"
    stored_file = json.loads(masks_path.read_text(encoding="utf-8"))
    assert stored_file["passed"] and not stored_file["failures"]
    first_row = next(a for a in analysis["firsts"] if a["first"] == FIRST)
    prev_path = PREV / "win-side-reanalysis7.json"
    prev = json.loads(prev_path.read_text(encoding="utf-8"))
    assert prev["verification"]["passed"]

    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        central = json.load(stream)
    board = Board(11)
    cache = load_exact_s5_cache(board)
    s5_masks: dict[int, int] = {}
    sources = {
        str(analysis_path.relative_to(ROOT)): sha(analysis_path),
        str(masks_path.relative_to(ROOT)): sha(masks_path),
        str(GRAPH.relative_to(ROOT)): sha(GRAPH),
        str(prev_path.relative_to(ROOT)): sha(prev_path),
    }
    for index, (directory, receipt_name, cert_name) in RECEIPTS.items():
        receipt_path = directory / receipt_name
        cert_path = directory / cert_name
        receipt = json.loads(receipt_path.read_text())
        assert receipt["trusted_leaves"] == 0, index
        if "pruned_roundtrip_verified" in receipt:
            assert receipt["pruned_roundtrip_verified"], index
        assert sha(cert_path) == receipt["certificate_sha256"], index
        mask = central["s5_masks"][index][0] | central["s5_masks"][index][1] << 64
        assert str(mask) == str(receipt["root_mask"]), index
        assert receipt["verdict"] == EXPECTED[index], index
        cache[key_of(mask)] = {"verdict": receipt["verdict"]}
        s5_masks[index] = mask
        sources.update({str(p.relative_to(ROOT)): sha(p)
                        for p in (receipt_path, cert_path)})
    assert {i: cache[key_of(m)]["verdict"] for i, m in s5_masks.items()} == EXPECTED

    # Every canonical parent of the six-stone certificate root is a legal S5
    # whose LOSS follows directly; all of them join the cache this round.
    s6_cert = S6DIR / "s6-loss-optimized.cert"
    assert sha(s6_cert) == S6_CERT_SHA
    parents = {canonical(S6_ROOT ^ (1 << p)) for p in points(S6_ROOT)}
    assert len(parents) == 6
    s6_masks: dict[int, int] = {}
    for index in S6_LOSSES + S6_EXTRA:
        mask = central["s5_masks"][index][0] | central["s5_masks"][index][1] << 64
        assert mask in parents, index
        if index not in S6_LOSSES:
            assert key_of(mask) not in cache, index
        s6_masks[index] = mask
    unmapped_parents = parents - set(s6_masks.values())
    assert len(unmapped_parents) == 1, unmapped_parents
    for mask in parents:
        if key_of(mask) not in cache:
            cache[key_of(mask)] = {"verdict": 2}
    sources[str(s6_cert.relative_to(ROOT))] = sha(s6_cert)
    for extra in ("audit_joint_plan.py", "verify_s6_terminal.py"):
        extra_path = S6DIR / extra
        sources[str(extra_path.relative_to(ROOT))] = sha(extra_path)

    stored_masks = {lo | (hi << 64) for lo, hi in stored_file["witness_masks"]}
    assert len(stored_masks) == first_row["optimistic_witness_s5"] == 1945
    assert not (parents & stored_masks), "S6 loss mask in witness pool"
    removed = {m: ("resolved-WIN" if cache[key_of(m)]["verdict"] == 1 else "resolved-LOSS")
               for m in stored_masks if key_of(m) in cache}
    assert set(removed) == {s5_masks[i] for i in RECEIPTS if i != 558600}, removed
    assert len(removed) == 17, len(removed)
    allowed = stored_masks - set(removed)
    assert len(allowed) == 1928
    prev_allowed = stored_masks - {s5_masks[i] for i in RECEIPTS
                                   if i not in (115540, 144193, 144311, 150871)}
    assert len(prev_allowed) == 1932, len(prev_allowed)
    round_removed = {i: s5_masks[i] for i in NEW_LOSS + NEW_WIN}

    memo: dict[int, tuple[str, frozenset[int]]] = {}
    memo7: dict[int, tuple[str, frozenset[int]]] = {}

    def classify(index_mask: int):
        hit = memo.get(index_mask)
        if hit is None:
            children = board.children(index_mask)
            verdicts = [verdict_of(cache, key_of(c)) for c in children]
            kind = classify_s4(verdicts)
            unknown = frozenset(c for c, v in zip(children, verdicts) if v == 0)
            hit = (kind, unknown)
            memo[index_mask] = hit
        return hit

    # Pre-optimisation damage on the stored chosen thirds, with per-key
    # attribution against the seventh-update allowed pool.
    new_win_mask = s5_masks[NEW_WIN[0]]
    s6_parent_keys = {key_of(m) for m in parents}
    uncovered_branches = 0
    uncovered_classes: set[int] = set()
    replies_affected: list[int] = []
    dead_thirds_stored = 0
    dead_touching_extra_s6 = 0
    freed_branches_new_win = 0
    freed_branches_new_win_novel = 0
    damaged_by_key: Counter = Counter()
    for rep in first_row["replies"]:
        if not rep["closable"]:
            continue
        pair = (1 << FIRST) | (1 << rep["reply"])
        s3 = pair | (1 << rep["chosen_third"])
        fourths = board.points(board.legal(s3))
        damaged = 0
        for u in fourths:
            m = board.canonical(s3 | (1 << u))
            kind, unknown = classify(m)
            if kind == DEAD:
                dead_thirds_stored += 1
                if any(key_of(c) in s6_parent_keys for c in board.children(m)):
                    dead_touching_extra_s6 += 1
            elif kind == OPEN and not (unknown & allowed):
                damaged += 1
                uncovered_branches += 1
                uncovered_classes.add(m)
                lost = unknown & prev_allowed
                for index, mask in round_removed.items():
                    if mask in lost:
                        damaged_by_key[str(index)] += 1
            elif kind == FREE and new_win_mask in board.children(m):
                freed_branches_new_win += 1
                if not any(verdict_of(cache, key_of(c)) == WIN
                           for c in board.children(m) if c != new_win_mask):
                    freed_branches_new_win_novel += 1
        if damaged:
            replies_affected.append(rep["reply"])

    # Re-optimisation restricted to the stored witness pool.
    stab = [m for m in board.maps if m[FIRST] == (1 << FIRST)]
    seen: set[tuple] = set()
    orbit_reps: list[int] = []
    for r in range(121):
        if r == FIRST:
            continue
        orb = tuple(sorted(m[r] for m in stab))
        if orb in seen:
            continue
        seen.add(orb)
        orbit_reps.append(r)
    assert len(orbit_reps) == first_row["reply_orbits"] == 65

    reply_rows = []
    witness_union: set[int] = set()
    and_width = 0
    dead_disqualified_total = 0
    for pos, r in enumerate(orbit_reps):
        pair = (1 << FIRST) | (1 << r)
        thirds = board.points(board.legal(pair))
        assert len(thirds) == 119
        best = None
        n_viable = 0
        n_all_free = 0
        for t in thirds:
            s3 = pair | (1 << t)
            fourths = board.points(board.legal(s3))
            needs = []
            for u in fourths:
                m = board.canonical(s3 | (1 << u))
                kind, unknown = classify(m)
                if kind == DEAD:
                    dead_disqualified_total += 1
                    break
                if kind == OPEN:
                    need = unknown & allowed
                    if not need:
                        break
                    needs.append(need)
            else:
                n_viable += 1
                if not needs:
                    n_all_free += 1
                    cand = {"third": t, "fourths": len(fourths), "witnesses": []}
                else:
                    cand = {"third": t, "fourths": len(fourths),
                            "witnesses": sorted(greedy_witness_cover(needs))}
                if best is None or len(cand["witnesses"]) < len(best["witnesses"]):
                    best = cand
        if best is None:
            reply_rows.append({"reply": r, "closable": False})
        else:
            witness_union |= set(best["witnesses"])
            and_width += best["fourths"]
            reply_rows.append({"reply": r, "closable": True,
                               "all_free": n_all_free > 0,
                               "viable_thirds": n_viable,
                               "chosen_third": best["third"],
                               "chosen_fourths": best["fourths"],
                               "witness_count": len(best["witnesses"]),
                               "witness_masks": sorted(
                                   [m & ((1 << 64) - 1), m >> 64]
                                   for m in best["witnesses"])})
        print(f"  first {FIRST}: reply {pos + 1}/{len(orbit_reps)} (r={r}) "
              f"closable={best is not None} s4_touched={len(memo)}", flush=True)

    n_close = sum(1 for x in reply_rows if x["closable"])
    n_free = sum(1 for x in reply_rows if x.get("all_free"))
    baseline_free = {rep["reply"] for rep in first_row["replies"]
                     if rep["closable"] and rep.get("all_free")}
    prev_free = {row["reply"] for row in prev["replies"]
                 if row["closable"] and row.get("all_free")}
    newly_free_vs_prev = [x["reply"] for x in reply_rows
                          if x.get("all_free") and x["reply"] not in prev_free]
    newly_free_vs_initial = [x["reply"] for x in reply_rows
                             if x.get("all_free") and x["reply"] not in baseline_free]
    regressed_vs_prev = sorted(prev_free - {x["reply"] for x in reply_rows
                                            if x.get("all_free")})
    prev_closable = {row["reply"] for row in prev["replies"] if row["closable"]}
    now_closable = {x["reply"] for x in reply_rows if x["closable"]}
    reclosed_vs_prev = sorted(now_closable - prev_closable)
    newly_unclosable_vs_prev = sorted(prev_closable - now_closable)

    # Final verification of the re-optimised covers (win_witness_masks flow).
    failures: list[str] = []
    for row in reply_rows:
        if not row["closable"]:
            continue
        stored = {lo | (hi << 64) for lo, hi in row["witness_masks"]}
        for m in stored:
            if board.canonical(m) != m:
                failures.append(f"reply {row['reply']}: non-canonical witness")
            if key_of(m) in cache:
                failures.append(f"reply {row['reply']}: cached witness")
            if m not in allowed:
                failures.append(f"reply {row['reply']}: witness outside stored pool")
        pair = (1 << FIRST) | (1 << row["reply"])
        s3 = pair | (1 << row["chosen_third"])
        fourths = board.points(board.legal(s3))
        if len(fourths) != row["chosen_fourths"]:
            failures.append(f"reply {row['reply']}: fourth count drift")
            continue
        for u in fourths:
            m = board.canonical(s3 | (1 << u))
            kind, unknown = classify(m)
            if kind == DEAD:
                failures.append(f"reply {row['reply']}: dead S4 in chosen third")
            elif kind == OPEN and not (unknown & stored):
                failures.append(f"reply {row['reply']}: open S4 unwitnessed")
            elif kind != FREE and kind != OPEN:
                failures.append(f"reply {row['reply']}: unknown kind {kind}")

    # Reproduce the frozen K0423-basis ranking rows for the new facts.
    ranking = json.loads((RANK / "ranking.json").read_text(encoding="utf-8"))
    rank_rows = {row["s5_index"]: row for row in ranking["rows"]}
    tsv_lines = (RANK / "ranking.tsv").read_text().splitlines()
    tsv_header = tsv_lines[0].split("\t")
    tsv_by_index = {int(dict(zip(tsv_header, line.split("\t")))["s5_index"]):
                    dict(zip(tsv_header, line.split("\t"))) for line in tsv_lines[1:]}
    rank_cache = load_exact_s5_cache(board)
    for index in (558600, 209644):
        rank_cache[key_of(s5_masks[index])] = {"verdict": EXPECTED[index]}
    preds = {i: board.predecessors(s5_masks[i]) for i in NEW_LOSS + NEW_WIN}
    children_memo: dict[int, frozenset[int]] = {}
    cross = {}
    for i in NEW_LOSS + NEW_WIN:
        with_candidate = sole_witness_no_old_win = branches_no_old_win = 0
        replies_touched = set()
        for rep in first_row["replies"]:
            if not rep["closable"]:
                continue
            pair = (1 << FIRST) | (1 << rep["reply"])
            s3 = pair | (1 << rep["chosen_third"])
            stored = {lo | (hi << 64) for lo, hi in rep["witness_masks"]}
            for u in board.points(board.legal(s3)):
                m = board.canonical(s3 | (1 << u))
                if m not in preds[i]:
                    continue
                if m not in children_memo:
                    children_memo[m] = frozenset(board.children(m))
                children = children_memo[m]
                assert s5_masks[i] in children, (i, m)
                with_candidate += 1
                replies_touched.add(rep["reply"])
                old_win = any(rank_cache.get(key_of(c), {}).get("verdict") == 1
                              for c in children)
                if not old_win:
                    branches_no_old_win += 1
                if not old_win and children & stored == {s5_masks[i]}:
                    sole_witness_no_old_win += 1
        if i not in rank_rows:
            cross[str(i)] = dict(
                verdict=EXPECTED[i], ranking_absent=True,
                recomputed_new_free_branches=branches_no_old_win,
                recomputed_sole_stored_witness_branches=sole_witness_no_old_win,
                stored_chosen_third_branches_with_candidate=with_candidate,
                stored_chosen_third_replies_with_candidate=sorted(replies_touched),
                effect_now="witness removed from the allowed pool (LOSS)",
                note=("150871 has no frozen ranking row; only the win-side branch "
                      "incidence is recorded"))
            continue
        ref = rank_rows[i]
        ref_free = len(ref["fixed_win_cover"]["if_win_newly_free_branches"])
        ref_sole = len(ref["fixed_win_cover"]["if_loss_uncovered_branches"])
        tsv_row = tsv_by_index[i]
        assert branches_no_old_win == ref_free, (i, branches_no_old_win, ref_free)
        assert sole_witness_no_old_win == ref_sole, (i, sole_witness_no_old_win, ref_sole)
        assert int(tsv_row["if_win_new_free_win_branches"]) == ref_free, i
        assert int(tsv_row["if_loss_fixed_win_branches_uncovered"]) == ref_sole, i
        cross[str(i)] = dict(
            verdict=EXPECTED[i],
            ranking_tsv_row={k: int(tsv_row[k]) for k in
                             ("geometry_rank", "if_win_loss_choices_invalidated",
                              "if_loss_fixed_win_branches_uncovered",
                              "if_win_new_free_win_branches",
                              "if_win_greedy_loss_union", "if_win_greedy_delta")},
            ranking_if_win_new_free_branches=ref_free,
            recomputed_new_free_branches=branches_no_old_win,
            ranking_if_loss_uncovered_branches=ref_sole,
            recomputed_sole_stored_witness_branches=sole_witness_no_old_win,
            stored_chosen_third_branches_with_candidate=with_candidate,
            stored_chosen_third_replies_with_candidate=sorted(replies_touched),
            effect_now=("branch became FREE (WIN child)" if EXPECTED[i] == 1
                        else "witness removed from the allowed pool (LOSS)"),
        )

    result = {
        "schema": "n11-night-win-side-reanalysis-update8-v1",
        "first": FIRST,
        "source_sha256": sources,
        "cache_sha256": sha(ROOT / "research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache"),
        "polarity_module_sha256": sha(ROOT / "research/experiments/n11-proof-cost-comparison-20261012/scripts/s4_win_polarity.py"),
        "baseline": {k: first_row[k] for k in
                     ("reply_orbits", "closable_replies", "free_closable_replies",
                      "witness_replies", "and_width_fourths",
                      "optimistic_witness_s5", "unclosable_replies")},
        "previous_after": prev["after"],
        "stored_witness_pool": len(stored_masks),
        "removed_witnesses": [{"mask": [m & ((1 << 64) - 1), m >> 64], "reason": why}
                              for m, why in sorted(removed.items())],
        "allowed_witness_pool": len(allowed),
        "s6_derived_losses": {str(i): {"mask": f"{m:032x}", "certificate_sha256": S6_CERT_SHA}
                              for i, m in sorted(s6_masks.items())},
        "s6_extra_parents_layered": [str(i) for i in S6_EXTRA],
        "s6_unindexed_parent": [f"{m:032x}" for m in sorted(unmapped_parents)],
        "pre_optimisation": {
            "uncovered_branches": uncovered_branches,
            "uncovered_s4_classes": len(uncovered_classes),
            "replies_affected": sorted(replies_affected),
            "damaged_by_layered_key": dict(damaged_by_key),
            "dead_branches_in_stored_thirds": dead_thirds_stored,
            "dead_branches_touching_s6_parents": dead_touching_extra_s6,
            "freed_branches_by_new_win_in_stored_thirds": freed_branches_new_win,
            "freed_branches_by_new_win_only_in_stored_thirds":
                freed_branches_new_win_novel,
        },
        "after": {
            "closable_replies": n_close,
            "unclosable_replies": [x["reply"] for x in reply_rows if not x["closable"]],
            "free_closable_replies": n_free,
            "witness_replies": n_close - n_free,
            "and_width_fourths": and_width,
            "optimistic_witness_s5": len(witness_union),
            "unresolved_witness_s5": len(witness_union),
            "newly_free_replies_vs_previous": sorted(newly_free_vs_prev),
            "newly_free_replies_vs_initial": sorted(newly_free_vs_initial),
            "regressed_free_replies_vs_previous": regressed_vs_prev,
            "reclosed_replies_vs_previous": reclosed_vs_prev,
            "newly_unclosable_replies_vs_previous": newly_unclosable_vs_prev,
            "newly_closed_third_moves_vs_previous": len(reclosed_vs_prev),
            "newly_closed_reply_orbits_vs_previous": len(reclosed_vs_prev),
            "newly_closed_third_moves_vs_initial": len(newly_free_vs_initial),
            "newly_closed_reply_orbits_vs_initial": len(newly_free_vs_initial),
        },
        "dead_disqualified_thirds": dead_disqualified_total,
        "ranking_cross_check": cross,
        "s4_classes_touched": len(memo),
        "s4_kind_counts": dict(Counter(kind for kind, _ in memo.values())),
        "replies": reply_rows,
        "witness_masks": sorted([[m & ((1 << 64) - 1), m >> 64]
                                 for m in witness_union]),
        "verification": {"passed": not failures, "failures": failures,
                         "covers_checked": n_close},
        "note": ("witnesses are optimistic frontiers restricted to the stored "
                 "1,945-mask pool minus the seventeen now-resolved receipt keys "
                 "(558600 LOSS was never stored); the five indexed S6-certificate "
                 "parents and the unindexed sixth were never stored witnesses, so "
                 "they only remove unknown status; every remaining witness S5 "
                 "still needs its own all-sixths WIN closure, which is NOT proven "
                 "here. Dead S4s remain reusable LOSS-side assets."),
        "seconds": round(time.time() - started, 1),
    }
    target = EXP / "output/win-side-reanalysis8.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True,
                                 separators=(",", ":")) + "\n")
    print(json.dumps({k: result[k] for k in
                      ("stored_witness_pool", "allowed_witness_pool",
                       "pre_optimisation", "after", "dead_disqualified_thirds",
                       "verification", "seconds")},
                     ensure_ascii=False, indent=2))
    print(json.dumps(cross, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
