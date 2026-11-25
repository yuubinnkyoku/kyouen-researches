#!/usr/bin/env python3
"""Independent second verification of the 36-root three-ply D4 frontier census.

Uses only Python stdlib. Geometry is computed from 3D cross products on the
integer paraboloid lift (x^2+y^2, x, y), not the JS cofactor/Leibniz routines.
No original JS is imported or executed.
"""
import hashlib
import itertools
import json
import resource
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CAND = ROOT / "research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json"
PUBLISHED = ROOT / "research/experiments/n11-residual72-36root-three-ply-frontier-20261120/output/36-root-three-ply-frontier-20261120.json"
OUT = Path(__file__).resolve().parents[1] / "output" / "independent-second-verification-20261120.json"
CAND_SHA = "49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa"
PUBLISHED_SHA = "94fdb0c6e3503f1e9d19aaaf345f4478157c5a44374f10642c52325f346c2023"
AUDIT_HEAD = "da4b167811aec6d2405d5222759a6086e435ac1e"

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

START = time.perf_counter()
candidate_bytes = CAND.read_bytes()
published_bytes = PUBLISHED.read_bytes()
need(hashlib.sha256(candidate_bytes).hexdigest() == CAND_SHA, "K1075 source SHA-256 mismatch")
need(hashlib.sha256(published_bytes).hexdigest() == PUBLISHED_SHA, "published frontier SHA-256 mismatch")
candidate = json.loads(candidate_bytes)
published = json.loads(published_bytes)
roots = candidate["witness_full"]
residual = {int(x, 16) for x in candidate["base_state"]["residual_row_hex"]}
need(len(roots) == 36 and len(residual) == 72, "input root/residual cardinality mismatch")

N = 121
ALL = (1 << N) - 1
ROWS = []
for p in range(N):
    x, y = p % 11, p // 11
    ROWS.append((x*x + y*y, x, y))

def cross(u, v):
    return (
        u[1]*v[2] - u[2]*v[1],
        u[2]*v[0] - u[0]*v[2],
        u[0]*v[1] - u[1]*v[0],
    )

def sub(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def det4(a, b, c, d):
    A, B, C, D = ROWS[a], ROWS[b], ROWS[c], ROWS[d]
    return dot(cross(sub(B, A), sub(C, A)), sub(D, A))

# Eight D4 actions are authored as coordinate maps, independently of the
# original script's swap/reflection loop.
D4 = []
for transform in (
    lambda x, y: (x, y),
    lambda x, y: (10-y, x),
    lambda x, y: (10-x, 10-y),
    lambda x, y: (y, 10-x),
    lambda x, y: (10-x, y),
    lambda x, y: (x, 10-y),
    lambda x, y: (y, x),
    lambda x, y: (10-y, 10-x),
):
    D4.append([transform(p % 11, p // 11)[0] + 11*transform(p % 11, p // 11)[1] for p in range(N)])

def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low

def transform_mask(mask, table):
    out = 0
    for p in bits(mask):
        out |= 1 << table[p]
    return out

def canonical(mask):
    best = None
    for table in D4:
        image = transform_mask(mask, table)
        if best is None or image < best:
            best = image
    return best

triple_cache = {}
point_checks = 0

def triple_mask(a, b, c):
    global point_checks
    key = tuple(sorted((a, b, c)))
    found = triple_cache.get(key)
    if found is not None:
        return found
    A, B, C = ROWS[key[0]], ROWS[key[1]], ROWS[key[2]]
    normal = cross(sub(B, A), sub(C, A))
    mask = 0
    for q, Q in enumerate(ROWS):
        if dot(normal, sub(Q, A)) == 0:
            mask |= 1 << q
    point_checks += N
    triple_cache[key] = mask
    return mask

def popcount(mask):
    return mask.bit_count()

def format_mask(mask):
    return format(mask, "032x")

owners = {}
pair_counts = [[0]*36 for _ in range(36)]
per_root = []
root_quadruples = 0
total9 = total_raw10 = total_d4 = within_total = terminal9_total = 0
all_third_moves = 0

for index, item in enumerate(roots):
    root_hex = item["root"]
    root = int(root_hex, 16)
    stones = list(bits(root))
    need(len(stones) == 7, f"root {index} is not 7-stone")
    need(canonical(root) == root, f"root {index} is not D4-canonical")
    need(item["safe"] is True, f"root {index} source safe flag false")
    for a, b, c, d in itertools.combinations(stones, 4):
        root_quadruples += 1
        need(det4(a, b, c, d) != 0, f"root {index} has unsafe quadruple")

    # Independently rederive the 6-stone rows from all D4 images and one
    # deletion, then intersect with the pinned 72-row residual.
    removal_rows = set()
    for table in D4:
        image = transform_mask(root, table)
        for q in bits(image):
            removal_rows.add(canonical(image ^ (1 << q)))
    derived_rows = sorted(format_mask(x) for x in removal_rows if x in residual)
    recorded_rows = sorted(item["rows"])
    need(derived_rows == recorded_rows, f"root {index} residual-row incidence mismatch")
    need(sorted(item["covered"]) == recorded_rows, f"root {index} covered/rows mismatch")

    base_forbidden = 0
    for a, b, c in itertools.combinations(stones, 3):
        base_forbidden |= triple_mask(a, b, c)
    first_mask = ALL & ~(base_forbidden | root)
    first_moves = list(bits(first_mask))

    n9 = raw10 = d4_memberships = within = third_moves = terminal9 = 0
    min3, max3 = 999, -1
    for p in first_moves:
        bit_p = 1 << p
        st8 = stones + [p]
        ep = base_forbidden
        for a, b in itertools.combinations(stones, 2):
            ep |= triple_mask(a, b, p)
        occupied8 = root | bit_p
        legal_second = ALL & ~(ep | occupied8)
        for q in bits(legal_second):
            if q <= p:
                continue
            n9 += 1
            bit_q = 1 << q
            eq = ep
            for a, b in itertools.combinations(st8, 2):
                eq |= triple_mask(a, b, q)
            occupied9 = occupied8 | bit_q
            replies = ALL & ~(eq | occupied9)
            count3 = popcount(replies)
            third_moves += count3
            min3 = min(min3, count3)
            max3 = max(max3, count3)
            if count3 == 0:
                terminal9 += 1
            later = replies >> (q + 1)
            while later:
                low = later & -later
                r = q + 1 + low.bit_length() - 1
                later ^= low
                raw10 += 1
                state = root | bit_p | bit_q | (1 << r)
                key = canonical(state)
                previous = owners.get(key)
                root_bit = 1 << index
                if previous is None:
                    owners[key] = root_bit
                    d4_memberships += 1
                elif previous & root_bit:
                    within += 1
                else:
                    for j in range(index):
                        if previous & (1 << j):
                            pair_counts[j][index] += 1
                    owners[key] = previous | root_bit
                    d4_memberships += 1

    need(third_moves == 3*raw10, f"root {index} third/raw identity failed")
    per_root.append({
        "rank": index+1,
        "root": root_hex,
        "rows": recorded_rows,
        "worker": index % 4,
        "first": len(first_moves),
        "n9": n9,
        "third": third_moves,
        "raw10": raw10,
        "d4": d4_memberships,
        "within": within,
        "terminal9": terminal9,
        "min3": min3,
        "max3": max3,
    })
    total9 += n9
    total_raw10 += raw10
    total_d4 += d4_memberships
    within_total += within
    terminal9_total += terminal9
    all_third_moves += third_moves

multiplicity_histogram = {}
duplicate_memberships = 0
max_multiplicity = 0
for owner_mask in owners.values():
    multiplicity = popcount(owner_mask)
    multiplicity_histogram[str(multiplicity)] = multiplicity_histogram.get(str(multiplicity), 0) + 1
    if multiplicity > 1:
        duplicate_memberships += multiplicity - 1
    max_multiplicity = max(max_multiplicity, multiplicity)

overlaps = []
same_worker = cross_worker = pairwise_total = 0
for i in range(36):
    for j in range(i+1, 36):
        shared = pair_counts[i][j]
        if shared:
            overlaps.append({
                "a": roots[i]["root"],
                "b": roots[j]["root"],
                "shared": shared,
                "workerA": i % 4,
                "workerB": j % 4,
            })
            pairwise_total += shared
            if i % 4 == j % 4:
                same_worker += shared
            else:
                cross_worker += shared
overlaps.sort(key=lambda x: (-x["shared"], x["a"], x["b"]))

worker_stats = []
for worker in range(4):
    rows = [x for x in per_root if x["worker"] == worker]
    worker_stats.append({
        "worker": worker,
        "roots": len(rows),
        "n9": sum(x["n9"] for x in rows),
        "raw10": sum(x["raw10"] for x in rows),
        "d4": sum(x["d4"] for x in rows),
        "within": sum(x["within"] for x in rows),
    })

summary = {
    "roots": 36,
    "first_moves_min": min(x["first"] for x in per_root),
    "first_moves_max": max(x["first"] for x in per_root),
    "unique_9stone_positions": total9,
    "all_legal_third_moves": all_third_moves,
    "raw_10stone_positions": total_raw10,
    "per_root_d4_memberships": total_d4,
    "within_root_d4_merges": within_total,
    "global_unique_d4_classes": len(owners),
    "cross_root_duplicate_memberships": duplicate_memberships,
    "cross_root_duplicate_rate_percent": round(100*duplicate_memberships/total_d4, 6),
    "pairwise_overlap_total": pairwise_total,
    "overlapping_root_pairs": len(overlaps),
    "multiplicity_histogram": multiplicity_histogram,
    "max_root_multiplicity": max_multiplicity,
    "terminal_9stone_positions": terminal9_total,
    "min_legal_third_moves": min(x["min3"] for x in per_root),
    "max_legal_third_moves": max(x["max3"] for x in per_root),
    "same_worker_pairwise_overlap": same_worker,
    "cross_worker_pairwise_overlap": cross_worker,
    "cross_worker_share_percent": round(100*cross_worker/(same_worker+cross_worker), 6),
}

checks = []
def gate(name, condition, detail=""):
    checks.append({"name": name, "pass": bool(condition), "detail": str(detail)[:240]})

gate("K1075 source SHA-256", hashlib.sha256(candidate_bytes).hexdigest() == CAND_SHA)
gate("published frontier SHA-256", hashlib.sha256(published_bytes).hexdigest() == PUBLISHED_SHA)
gate("36 roots / 72 residual rows", len(roots) == 36 and len(residual) == 72)
gate("all 36 roots safe, 7-stone, D4-canonical", root_quadruples == 1260)
gate("all 36 root-to-row incidences independently rederived", all(sorted(roots[i]["rows"]) == per_root[i]["rows"] for i in range(36)))
gate("9-stone count", total9 == published["summary"]["unique_9stone_positions"])
gate("raw 10-stone count", total_raw10 == published["summary"]["raw_10stone_positions"])
gate("D4 membership count", total_d4 == published["summary"]["per_root_d4_memberships"])
gate("within-root D4 merges", within_total == published["summary"]["within_root_d4_merges"])
gate("global D4 class count", len(owners) == published["summary"]["global_unique_d4_classes"])
gate("cross-root duplicate memberships", duplicate_memberships == published["summary"]["cross_root_duplicate_memberships"])
gate("pairwise overlap count and total", len(overlaps) == published["summary"]["overlapping_root_pairs"] and pairwise_total == published["summary"]["pairwise_overlap_total"])
gate("full multiplicity histogram", multiplicity_histogram == published["summary"]["multiplicity_histogram"])
gate("full per-root table", per_root == published["per_root"])
gate("full 221-pair overlap table", overlaps == published["pairwise_overlap"])
gate("four-worker aggregate table", worker_stats == published["worker_stats"])
gate("all legal third moves / terminal count", all_third_moves == published["summary"]["all_legal_third_moves"] and terminal9_total == 0)
gate("cross-worker overlap split", same_worker == 1242 and cross_worker == 4193)
gate("third-move identity", all(x["third"] == 3*x["raw10"] for x in per_root))

record = {
    "schema": "n11-residual72-36root-three-ply-frontier-independent-second-verification-20261120-v1",
    "date": "2026-11-20",
    "status": "second-verified" if all(x["pass"] for x in checks) else "gate-failed",
    "audited_main_head": AUDIT_HEAD,
    "inputs": {
        "candidate_supply_path": "research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json",
        "candidate_supply_sha256": CAND_SHA,
        "frontier_census_path": "research/experiments/n11-residual72-36root-three-ply-frontier-20261120/output/36-root-three-ply-frontier-20261120.json",
        "frontier_census_sha256": PUBLISHED_SHA,
    },
    "method": {
        "implementation": "independent Python 3.13 stdlib",
        "geometry": "integer cross product and dot product on lifted points (x^2+y^2,x,y), equivalent to exact 4x4 determinant zero test",
        "symmetry": "eight coordinate maps written directly; canonical representative is minimum 121-bit integer mask",
        "enumeration": "independent triple-forbidden masks, then exhaustive sorted first/second/third additions",
        "original_script_imported": False,
        "point_checks": point_checks,
        "unique_triples": len(triple_cache),
        "root_quadruples": root_quadruples,
    },
    "summary": summary,
    "worker_stats": worker_stats,
    "per_root": per_root,
    "pairwise_overlap": overlaps,
    "checks": checks,
    "check_count": len(checks),
    "all_pass": all(x["pass"] for x in checks),
    "interpretation_guard": [
        "This verifies geometric state overlap only, not DFPN node cost or transposition-table hit rate.",
        "A shared D4 class does not imply identical search depth, bounds, or reusable proof state.",
        "REFUTED-D10 is not a LOSS proof.",
        "The 36 roots are candidate roots, not WIN certificates.",
        "The standard 11x11 empty board and two-stone roots remain UNKNOWN."
    ],
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({
    "status": record["status"],
    "check_count": record["check_count"],
    "all_pass": record["all_pass"],
    "summary": summary,
    "point_checks": point_checks,
    "unique_triples": len(triple_cache),
    "elapsed_seconds": round(time.perf_counter()-START, 3) if "START" in globals() else None,
    "maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
}, ensure_ascii=False))


