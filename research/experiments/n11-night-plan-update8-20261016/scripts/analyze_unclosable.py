"""Unrestricted re-analysis of the unclosable reply orbits of first move 49
(update8 cache), for the six orbits the seventh update reported as unclosable
plus any orbit the eighth update adds.

For every reply orbit, all 119 thirds and all fourth boundaries are rebuilt
from independent integer geometry (no stored witness pool during
classification).  Each fourth S4 is classified with the complete update8
exact+S5 verdict cache: FREE (some WIN child), DEAD (all children LOSS) or
OPEN (some unknown child).  A third is refuted exactly when it has a DEAD
fourth; the obstruction is genuine mathematics (the four-stone position is
first-player LOSS by the frozen registry), not a pool shortage.

For every non-refuted third a greedy witness cover is computed over ALL
canonical unknown fifth-stone children; the reply is rescued iff some third is
not refuted.  For each reported reply the third moves whose greedy cover is
within a small margin of the best are then optimised exactly (branch and bound
with a node cap, greedy fallback), which bounds the minimum witness count of
the small-scale covering problem.  The restricted pass is reproduced as well
and must agree with the eighth-update win-side output.

No solver search is involved; nothing here upgrades an UNKNOWN verdict.
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
RANK = ROOT / "research/experiments/n11-conflict-ranking-20261013/output/ranking.json"
S6DIR = ROOT / "research/experiments/n11-s6-terminal-loss-20261015"
NATIVE = ROOT / "research/experiments/n11-native-terminal-checker-20261013/output"
K0423 = ROOT / "research/experiments/n11-s5-s6-quotient-20261013/output"
ADAPTIVE = ROOT / "research/experiments/n11-adaptive-verify-20261013/output"
PROBE = ROOT / "research/experiments/n11-adaptive-probe-20261013/output"
NIGHT = {n: ROOT / f"research/experiments/n11-night-batch{n}-20261014/output"
         for n in (1, 2, 3, 4, 5)}

sys.path.insert(0, str(COST_CMP / "scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-s7-fifth-terminal-20261015"))
from independent import Board  # noqa: E402
from analyze_central_reply_frontier import load_exact_s5_cache, sha  # noqa: E402
from s4_win_polarity import classify_s4, verdict_of, FREE, OPEN, DEAD  # noqa: E402
from fifth_verify_standalone import canonical, points  # noqa: E402

RECEIPTS = {
    558600: (K0423, "pilot-558600-terminal-verification.json", "pilot-558600-terminal-dag.json.gz", 2),
    209644: (K0423, "pilot-209644-terminal-verification.json", "pilot-209644-terminal-dag.json.gz", 1),
    126899: (ADAPTIVE, "pilot-126899-receipt.json", "pilot-126899-terminal-dag.json.gz", 2),
    144095: (ADAPTIVE, "pilot-144095-receipt.json", "pilot-144095-terminal-dag.json.gz", 1),
    121263: (PROBE, "adaptive-121263-receipt.json", "adaptive-121263-terminal-dag.json.gz", 2),
    145001: (PROBE, "adaptive-145001-receipt.json", "adaptive-145001-terminal-dag.json.gz", 2),
    137694: (NIGHT[1], "night-a-137694-receipt.json", "night-a-137694-terminal-dag.json.gz", 2),
    143240: (NIGHT[1], "night-a-143240-receipt.json", "night-a-143240-terminal-dag.json.gz", 2),
    220231: (NIGHT[1], "night-a-220231-receipt.json", "night-a-220231-terminal-dag.json.gz", 2),
    126017: (NIGHT[1], "nightb10m-126017-receipt.json", "nightb10m-126017-terminal-dag.json.gz", 1),
    197665: (NIGHT[2], "nighta25m-197665-receipt.json", "nighta25m-197665-terminal-dag.json.gz", 1),
    206386: (NIGHT[3], "nighta25m-206386-receipt.json", "nighta25m-206386-terminal-dag.json.gz", 1),
    131631: (NIGHT[4], "nighta25m-131631-receipt.json", "nighta25m-131631-terminal-dag.json.gz", 1),
    162106: (NIGHT[5], "nighta25m-162106-receipt.json", "nighta25m-162106-terminal-dag.json.gz", 1),
    115540: (NATIVE, "pilot-115540-receipt.json", "pilot-115540-terminal-dag.json.gz", 2),
    144193: (NATIVE, "pilot-144193-receipt.json", "pilot-144193-terminal-dag.json.gz", 2),
    144311: (NATIVE, "pilot-144311-receipt.json", "pilot-144311-terminal-dag.json.gz", 1),
}
S6_ROOT = int("00000000040004001004000004010000", 16)
FIRST = 49
TARGET_REPLIES = (1, 2, 4, 15, 79, 101)
SHORTLIST_MARGIN = 3
SHORTLIST_CAP = 25
NODE_CAP = 400000


def key_of(mask: int) -> tuple[int, int]:
    return mask & ((1 << 64) - 1), mask >> 64


def greedy_cover(needs: list[frozenset[int]]) -> set[int]:
    uncovered = [s for s in needs if s]
    chosen: set[int] = set()
    while uncovered:
        freq: Counter = Counter()
        for s in uncovered:
            freq.update(s)
        best = max(freq, key=lambda e: (freq[e], e))
        chosen.add(best)
        uncovered = [s for s in uncovered if best not in s]
    return chosen


def exact_min_hitting_set(needs: list[frozenset[int]], greedy: list[int],
                          node_cap: int = NODE_CAP):
    """Minimum hitting set of ``needs`` (witnesses hitting every need set).

    Transposes the instance: the universe is the need indices and every
    candidate witness covers the needs that contain it.  The greedy cover is
    seeded as the incumbent, so a completed search proves the greedy cover
    optimal; a node-cap abort returns (greedy, False).
    """
    nonempty = [s for s in needs if s]
    if not nonempty:
        return [], True
    witness_to_needs: dict[int, list[int]] = {}
    for i, s in enumerate(nonempty):
        for w in s:
            witness_to_needs.setdefault(w, []).append(i)
    if len(witness_to_needs) > 3000:
        return greedy, False
    cands = sorted(witness_to_needs)
    covers = [tuple(witness_to_needs[w]) for w in cands]
    if len(cands) <= 400:
        froz = [frozenset(c) for c in covers]
        keep: list[int] = []
        for i in sorted(range(len(cands)), key=lambda i: -len(covers[i])):
            if not any(froz[i] <= froz[j] for j in keep):
                keep.append(i)
        cands = [cands[i] for i in keep]
        covers = [covers[i] for i in keep]
    idx_of = {w: i for i, w in enumerate(cands)}
    cand_of_need: dict[int, list[int]] = {}
    for j, cov in enumerate(covers):
        for e in cov:
            cand_of_need.setdefault(e, []).append(j)
    universe = frozenset(range(len(nonempty)))
    incumbent: list[int] = [idx_of[w] for w in greedy if w in idx_of]
    best: list[list[int]] = [incumbent]
    state = {"nodes": 0}

    def rec(uncovered: frozenset[int], chosen: list[int]) -> None:
        state["nodes"] += 1
        if state["nodes"] > node_cap:
            raise TimeoutError
        if not uncovered:
            if len(chosen) < len(best[0]):
                best[0] = list(chosen)
            return
        if not best or len(chosen) + 1 >= len(best[0]):
            return
        counts: Counter = Counter()
        for e in uncovered:
            for j in cand_of_need[e]:
                counts[j] += 1
        lower = len(uncovered) // max(counts.values())
        if len(chosen) + lower >= len(best[0]):
            return
        pivot = min(uncovered, key=lambda e: len(cand_of_need[e]))
        for j in sorted(cand_of_need[pivot], key=lambda j: -counts[j]):
            rec(uncovered - frozenset(covers[j]), chosen + [j])

    try:
        rec(universe, [])
    except TimeoutError:
        return greedy, False
    return sorted(cands[j] for j in best[0]), True


def main() -> None:
    started = time.time()
    win_path = EXP / "output/win-side-reanalysis8.json"
    win = json.loads(win_path.read_text())
    assert win["verification"]["passed"]
    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        central = json.load(stream)
    stored_file = json.loads(
        (COST_CMP / "output/win-witness-masks.json").read_text(encoding="utf-8"))
    stored_masks = {lo | (hi << 64) for lo, hi in stored_file["witness_masks"]}
    ranking = json.loads(RANK.read_text(encoding="utf-8"))
    conflict_candidates = {row["s5_index"] for row in ranking["rows"]}
    s5_index_of = {lo | hi << 64: i for i,
                   (lo, hi) in enumerate(central["s5_masks"])}

    board = Board(11)
    cache = load_exact_s5_cache(board)
    sources = {str(win_path.relative_to(ROOT).as_posix()): sha(win_path),
               str(GRAPH.relative_to(ROOT).as_posix()): sha(GRAPH)}
    for index, (directory, receipt_name, cert_name, expect) in RECEIPTS.items():
        receipt_path = directory / receipt_name
        cert_path = directory / cert_name
        receipt = json.loads(receipt_path.read_text())
        assert receipt["verdict"] == expect and receipt["trusted_leaves"] == 0, index
        assert sha(cert_path) == receipt["certificate_sha256"], index
        mask = central["s5_masks"][index][0] | central["s5_masks"][index][1] << 64
        cache[key_of(mask)] = {"verdict": expect}
        sources[str(receipt_path.relative_to(ROOT).as_posix())] = sha(receipt_path)
        sources[str(cert_path.relative_to(ROOT).as_posix())] = sha(cert_path)
    s6_cert = S6DIR / "s6-loss-optimized.cert"
    parents = {canonical(S6_ROOT ^ (1 << p)) for p in points(S6_ROOT)}
    for mask in parents:
        assert key_of(mask) not in cache
        cache[key_of(mask)] = {"verdict": 2}
    sources[str(s6_cert.relative_to(ROOT).as_posix())] = sha(s6_cert)
    allowed = stored_masks - {m for m in stored_masks if key_of(m) in cache}
    assert len(allowed) == win["allowed_witness_pool"] == 1929

    memo: dict[int, tuple[str, frozenset[int]]] = {}
    class_census: dict[int, tuple[int, int, int]] = {}

    def classify(mask: int):
        hit = memo.get(mask)
        if hit is None:
            children = board.children(mask)
            verdicts = [verdict_of(cache, key_of(c)) for c in children]
            kind = classify_s4(verdicts)
            unknown = frozenset(c for c, v in zip(children, verdicts) if v == 0)
            wins = verdicts.count(1)
            class_census[mask] = (len(children), wins, len(unknown))
            hit = (kind, unknown)
            memo[mask] = hit
        return hit

    def fourths_of(pair: int, t: int) -> list[int]:
        s3 = pair | (1 << t)
        return [board.canonical(s3 | (1 << u))
                for u in board.points(board.legal(s3))]

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
    assert len(orbit_reps) == 65

    # Pass 1: classify every third of every reply; no covers yet, only
    # viability (no DEAD fourth), restricted viability and the S4 census.
    pass1: dict[int, dict] = {}
    for pos, r in enumerate(orbit_reps):
        pair = (1 << FIRST) | (1 << r)
        touched: set[int] = set()
        viable = 0
        restricted_ok = 0
        refuted = []
        n_free_thirds = 0
        for t in sorted(board.points(board.legal(pair))):
            dead = []
            open_fourths = []
            for m in fourths_of(pair, t):
                touched.add(m)
                kind, unknown = classify(m)
                if kind == DEAD:
                    dead.append(m)
                elif kind == OPEN:
                    open_fourths.append(unknown)
            if dead:
                refuted.append(dict(third=t, dead_fourths=len(dead),
                                    example_dead_s4=dead[0]))
                continue
            viable += 1
            if not open_fourths:
                n_free_thirds += 1
                restricted_ok += 1
            elif all(unknown & allowed for unknown in open_fourths):
                restricted_ok += 1
        census = Counter()
        for m in touched:
            total, wins, unknown = class_census[m]
            census["S4_classes"] += 1
            census["S5_children"] += total
            census["S5_known_win"] += wins
            census["S5_unknown"] += unknown
        pass1[r] = dict(viable_thirds=viable, restricted_viable_thirds=restricted_ok,
                        refuted=refuted, free_thirds=n_free_thirds,
                        s5_child_census=dict(census))
        print(f"  reply {pos + 1}/65 (r={r}): viable {viable}, "
              f"restricted {restricted_ok}, free {n_free_thirds}, "
              f"dead fourths {sum(x['dead_fourths'] for x in refuted)}, "
              f"classes {len(memo)}", flush=True)

    win_rows = {row["reply"]: row for row in win["replies"]}
    restricted_closable = {r: pass1[r]["restricted_viable_thirds"] > 0 for r in orbit_reps}
    disagreements = [r for r in orbit_reps if restricted_closable[r] != win_rows[r]["closable"]]
    assert not disagreements, disagreements

    reported = [r for r in orbit_reps
                if r in TARGET_REPLIES or not restricted_closable[r]]

    # Pass 2 for the reported replies: greedy covers over all thirds, then
    # exact minimum covers over a shortlist of the best greedy thirds.
    reply_reports: dict[int, dict] = {}
    for r in reported:
        pair = (1 << FIRST) | (1 << r)
        sizes: dict[int, int] = {}
        greedy_witnesses: dict[int, list[int]] = {}
        restricted_sizes: dict[int, int] = {}
        for t in sorted(board.points(board.legal(pair))):
            needs_all = []
            needs_pool = []
            dead = False
            for m in fourths_of(pair, t):
                kind, unknown = classify(m)
                if kind == DEAD:
                    dead = True
                elif kind == OPEN:
                    needs_all.append(unknown)
                    needs_pool.append(unknown & allowed)
            if dead:
                continue
            if not needs_all:
                sizes[t] = 0
                greedy_witnesses[t] = []
                restricted_sizes[t] = 0
                continue
            cover = greedy_cover(needs_all)
            sizes[t] = len(cover)
            greedy_witnesses[t] = sorted(cover)
            if all(needs_pool):
                restricted_sizes[t] = len(greedy_cover(needs_pool))
        best_greedy = min(sizes.values()) if sizes else None
        shortlist = []
        if best_greedy is not None:
            for t, size in sorted(sizes.items()):
                if size <= best_greedy + SHORTLIST_MARGIN and len(shortlist) < SHORTLIST_CAP:
                    shortlist.append(t)
        exact_results = {}
        for t in shortlist:
            needs = [unknown for m in fourths_of(pair, t)
                     for kind, unknown in (classify(m),) if kind == OPEN]
            if not needs:
                exact_results[t] = dict(witnesses=[], count=0, exact=True)
                continue
            cover, exact = exact_min_hitting_set(needs, greedy_witnesses[t])
            exact_results[t] = dict(witnesses=sorted(cover), count=len(cover), exact=exact)
        chosen_third, chosen_info = (min(exact_results.items(),
                                         key=lambda kv: (kv[1]["count"], kv[0]))
                                     if exact_results else (None, None))
        witnesses = chosen_info["witnesses"] if chosen_info else []
        report = dict(
            reply=r,
            exact_cover_shortlist=bool(shortlist),
            classified_by=("pool-shortage" if sizes and not restricted_closable[r]
                           else ("fundamental-dead-refutation" if not sizes else "closed")),
            viable_thirds_unrestricted=len(sizes),
            viable_thirds_restricted=len(restricted_sizes),
            all_free_thirds=sum(1 for v in sizes.values() if v == 0),
            dead_fourths_total=sum(x["dead_fourths"] for x in pass1[r]["refuted"]),
            s5_child_census=pass1[r]["s5_child_census"],
            greedy_min_witness_count=best_greedy,
            restricted_min_witness_count=(min(restricted_sizes.values())
                                          if restricted_sizes else None),
            shortlist=shortlist,
            shortlist_results={str(t): dict(count=v["count"], exact=v["exact"],
                                            witnesses=v["witnesses"])
                               for t, v in sorted(exact_results.items())},
            chosen_third=chosen_third,
            min_witness_count=len(witnesses),
            exact_min_witness_count=any(v["exact"] for v in exact_results.values()),
            witnesses=witnesses,
            refuted_thirds=pass1[r]["refuted"],
        )
        reply_reports[r] = report
        print(f"  reply {r}: greedy min {best_greedy} over {len(sizes)} viable thirds; "
              f"shortlist {len(shortlist)} -> {len(witnesses)} witnesses "
              f"(third {chosen_third}, exact {report['exact_min_witness_count']})",
              flush=True)

    candidate_hits: Counter = Counter()
    candidate_in_pool: dict[int, bool] = {}
    candidate_index: dict[int, int | None] = {}
    for r in reported:
        for w in reply_reports[r]["witnesses"]:
            candidate_hits[w] += 1
            candidate_in_pool[w] = w in stored_masks
            candidate_index[w] = s5_index_of.get(w)
    for r in reported:
        reply_reports[r]["witnesses"] = [
            dict(mask=w, in_stored_pool=w in stored_masks,
                 graph_index=s5_index_of.get(w),
                 conflict_candidate=s5_index_of.get(w) in conflict_candidates,
                 used_in_other_replies=candidate_hits[w])
            for w in reply_reports[r]["witnesses"]]

    new_candidates = sorted(w for w in candidate_hits if w not in stored_masks)
    result = dict(
        schema="n11-night-unclosable-reanalysis-update8-v1",
        first=FIRST,
        source_sha256=sources,
        allowed_witness_pool=len(allowed),
        stored_witness_pool=len(stored_masks),
        cache_keys=len(cache),
        target_replies=list(TARGET_REPLIES),
        reported_replies=reported,
        shortlist_margin=SHORTLIST_MARGIN,
        shortlist_cap=SHORTLIST_CAP,
        summary=dict(
            replies_total=len(orbit_reps),
            restricted_closable=sum(restricted_closable.values()),
            unrestricted_closable=sum(1 for r in orbit_reps if pass1[r]["viable_thirds"]),
            newly_closed_by_unrestricted=[r for r in orbit_reps
                                          if pass1[r]["viable_thirds"]
                                          and not restricted_closable[r]],
            fundamental=[r for r in reported if not reply_reports[r]["witnesses"]
                         and not reply_reports[r]["shortlist"]],
            pool_shortage=[r for r in reported if reply_reports[r]["classified_by"]
                          == "pool-shortage"],
            exact_cover_replies=reported,
        ),
        replies={str(r): reply_reports[r] for r in reported},
        all_reply_outcomes={str(r): dict(
            restricted_closable=restricted_closable[r],
            unrestricted_closable=bool(pass1[r]["viable_thirds"]),
            viable_thirds_unrestricted=pass1[r]["viable_thirds"],
            all_free_thirds=pass1[r]["free_thirds"],
        ) for r in orbit_reps},
        witness_candidates={
            str(w): dict(in_stored_pool=candidate_in_pool[w],
                         graph_index=candidate_index[w],
                         conflict_candidate=(candidate_index[w] in conflict_candidates),
                         used_in_replies=candidate_hits[w],
                         new_outside_pool=w not in stored_masks)
            for w in sorted(candidate_hits)},
        new_witness_candidates=[str(w) for w in new_candidates],
        s4_classes_touched=len(memo),
        s4_kind_counts=dict(Counter(kind for kind, _ in memo.values())),
        verification=dict(passed=True, restricted_pass_matches_update8=True,
                          covers_checked=len(reported)),
        note=("classification uses the complete update8 verdict registry; DEAD "
              "refutations rest on verdicts already proven elsewhere (receipts or "
              "the frozen certificate), never on assumptions; witness masks are "
              "canonical unknown fifth-stone children and remain UNKNOWN until "
              "their own all-sixths WIN closure is proven; the exact minimum is "
              "computed over a shortlist of the best greedy thirds with a bounded "
              "node search (greedy fallback flagged per third)"),
        seconds=round(time.time() - started, 1),
    )
    target = EXP / "output/unclosable-reanalysis8.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True,
                                 indent=2) + "\n")
    print(json.dumps({k: result[k] for k in
                      ("summary", "s4_kind_counts", "new_witness_candidates",
                       "reported_replies", "seconds")}, ensure_ascii=False, indent=2))
    print(json.dumps({str(r): {k: reply_reports[r][k] for k in
                               ("classified_by", "viable_thirds_unrestricted",
                                "viable_thirds_restricted", "all_free_thirds",
                                "dead_fourths_total", "greedy_min_witness_count",
                                "min_witness_count", "exact_min_witness_count")}
                      for r in reported}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
