"""Task 4: compare the independent decomposition with the reference output
output/grundy_ag2q7_s2.txt (and the GSIZE lines in the separate stats file),
and check all size-by-size arithmetic stated in claim K1338.

Reference file semantics (from scripts/grundy_s_stats.c):
  SIZE <k> <count> <maximal> <grundy0>
  GRUNDY <g> <count>
  GSIZE <k> <g> <count>            (stats variant only; check_size uses it)
  ROOT <normal grundy> <misere win bit>
  FIRSTMOVE <g> <count-moves-to-options-of-grundy-g>
"""

import hashlib
import json
from pathlib import Path

from boardlib import BOARD_PATH, HERE, REFERENCE_PATH, STATS_PATH

enum = json.loads((HERE / "summary_enum.json").read_text(encoding="utf-8"))
gr = json.loads((HERE / "summary_grundy.json").read_text(encoding="utf-8"))

checks = []


def check(name, cond, expected=None, actual=None, detail=""):
    checks.append({
        "name": name, "pass": bool(cond),
        "expected": expected, "actual": actual, "detail": detail,
    })
    return cond


def parse_ref(path):
    scalars = {}
    sizes = {}
    grundy = {}
    gsize = {}
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        parts = raw.split()
        if not parts:
            continue
        if parts[0] == "SIZE":
            sizes[int(parts[1])] = tuple(int(x) for x in parts[2:5])
        elif parts[0] == "GRUNDY":
            grundy[int(parts[1])] = int(parts[2])
        elif parts[0] == "GSIZE":
            gsize[(int(parts[1]), int(parts[2]))] = int(parts[3])
        else:
            scalars[parts[0]] = tuple(int(x) for x in parts[1:])
    return scalars, sizes, grundy, gsize


scalars, ref_sizes, ref_grundy, ref_gsize = parse_ref(REFERENCE_PATH)
stats_scalars, stats_sizes, stats_grundy, stats_gsize = parse_ref(STATS_PATH)

total = gr["total_caps"]
dist = {int(k): {int(g): c for g, c in v.items()}
        for k, v in gr["distribution_by_size"].items()}
counts = {int(k): v for k, v in enum["counts_by_size"].items()}
maximal = {int(k): v for k, v in enum["maximal_by_size"].items()}
six = enum["six_cap_classes"]
five = enum["five_caps"]
seven = enum["seven_caps"]
eight = enum["eight_caps"]
totals = {int(g): c for g, c in gr["grundy_totals"].items()}

# ------------------------------------------------------------- scalars / totals
check("reference POINTS=49", scalars.get("POINTS") == (49,), (49,), scalars.get("POINTS"))
check("reference CIRCLES=56", scalars.get("CIRCLES") == (56,), (56,), scalars.get("CIRCLES"))
check("reference SAFE = independent total", scalars.get("SAFE") == (total,), total, scalars.get("SAFE"))
check("sum of GRUNDY counts = SAFE", sum(ref_grundy.values()) == total, total, sum(ref_grundy.values()))
check("independent distribution sums to total",
      sum(sum(v.values()) for v in dist.values()) == total, total,
      sum(sum(v.values()) for v in dist.values()))
check("reference GRUNDY histogram equals independent",
      ref_grundy == totals, totals, ref_grundy)
check("root Grundy = 0", gr["root_grundy"] == 0, 0, gr["root_grundy"])
check("ROOT normal value = 0", scalars.get("ROOT", (None,))[0] == 0, 0, scalars.get("ROOT"))
check("FIRSTMOVE 1 49 (all 49 first moves have G=1)",
      scalars.get("FIRSTMOVE") == (1, 49), (1, 49), scalars.get("FIRSTMOVE"))
check("independent size-1 G=1 count = 49", dist[1].get(1) == 49, 49, dist[1].get(1))

# ----------------------------------------------------------------- SIZE lines
check("reference SIZE sizes = 0..8", sorted(ref_sizes) == list(range(9)),
      list(range(9)), sorted(ref_sizes))
for k in sorted(ref_sizes):
    cnt, mx, g0 = ref_sizes[k]
    check(f"SIZE {k}: count {cnt}", cnt == counts.get(k), counts.get(k), cnt)
    check(f"SIZE {k}: maximal {mx}", mx == maximal.get(k), maximal.get(k), mx)
    check(f"SIZE {k}: grundy0 {g0}", g0 == dist.get(k, {}).get(0, 0),
          dist.get(k, {}).get(0, 0), g0)

# ---------------------------------------------------------------- GSIZE lines
if stats_gsize:
    ind_gsize = {f"{k},{g}": c for k, d in dist.items() for g, c in d.items()}
    stats_gsize_s = {f"{k[0]},{k[1]}": v for k, v in stats_gsize.items()}
    check("stats GSIZE lines equal independent distribution",
          stats_gsize_s == ind_gsize, ind_gsize, stats_gsize_s)
    check("stats file scalars agree with reference",
          stats_scalars.get("SAFE") == scalars.get("SAFE"), scalars.get("SAFE"),
          stats_scalars.get("SAFE"))
else:
    check("stats GSIZE lines present", False, "non-empty", "missing")

# ---------------------------------------------------- claim K1338 arithmetic
check("6-caps total = 460,992", counts[6] == 460992, 460992, counts[6])
check("6-caps: maximal + only8 + only7 + mixed = total",
      six["maximal"] + six["only8"] + six["only7"] + six["mixed"] == six["total"],
      six["total"], six["maximal"] + six["only8"] + six["only7"] + six["mixed"])
check("6-caps: maximal = 271,656", six["maximal"] == 271656, 271656, six["maximal"])
check("6-caps: only8 = 172,872", six["only8"] == 172872, 172872, six["only8"])
check("6-caps: only7 = 16,464", six["only7"] == 16464, 16464, six["only7"])
check("6-caps: mixed = 0", six["mixed"] == 0, 0, six["mixed"])
check("only7 = 7 * maximal 7-caps", six["only7"] == 7 * seven["maximal"],
      7 * seven["maximal"], six["only7"])
check("only8 = 28 * 8-caps", six["only8"] == 28 * eight["total"],
      28 * eight["total"], six["only8"])
check("only8 count = 6-subsets incidence of 8-caps",
      six["only8"] == eight["incidence_6subsets"], eight["incidence_6subsets"], six["only8"])
check("only7 count = 6-subsets incidence of maximal 7-caps",
      six["only7"] == seven["incidence_6subsets"], seven["incidence_6subsets"], six["only7"])
check("6-caps G=0 count = maximal + only8",
      dist[6].get(0) == six["maximal"] + six["only8"],
      six["maximal"] + six["only8"], dist[6].get(0))
check("6-caps G=1 count = only7", dist[6].get(1) == six["only7"], six["only7"], dist[6].get(1))
check("6-caps have no G>=2", set(dist[6]) <= {0, 1}, "{0,1}", sorted(dist[6]))

check("5-caps total = 444,528", counts[5] == 444528, 444528, counts[5])
check("5-caps G=2 = 49,392", dist[5].get(2) == 49392, 49392, dist[5].get(2))
check("5-caps G=1 = 395,136", dist[5].get(1) == 395136, 395136, dist[5].get(1))
check("5-caps G=1 + G=2 = total", dist[5].get(1, 0) + dist[5].get(2, 0) == counts[5],
      counts[5], dist[5].get(1, 0) + dist[5].get(2, 0))
check("5-caps G=2 = 21 * maximal 7-caps", dist[5].get(2) == 21 * seven["maximal"],
      21 * seven["maximal"], dist[5].get(2))
check("all 5-caps have a maximal 6-child",
      five["with_maximal_6_child"] == five["total"], five["total"],
      five["with_maximal_6_child"])
check("5-caps with only7-child = 49,392", five["with_only7_child"] == 49392,
      49392, five["with_only7_child"])
check("5-caps without only7-child = 395,136", five["without_only7_child"] == 395136,
      395136, five["without_only7_child"])
check("G=2 set equals 5-subsets of maximal 7-caps",
      gr["five_caps"]["g2_equals_five_subsets_of_maximal7"] is True,
      True, gr["five_caps"]["g2_equals_five_subsets_of_maximal7"])

check("7-caps G=0 = 2,352 (maximal)", dist[7].get(0) == 2352, 2352, dist[7].get(0))
check("7-caps G=1 = 49,392", dist[7].get(1) == 49392, 49392, dist[7].get(1))
check("8-caps all maximal", eight["total"] == eight["maximal"], eight["total"], eight["maximal"])
check("8-caps all G=0", dist[8] == {0: 6174}, {0: 6174}, dist[8])

# --------------------------------------------------------------- grand totals
check("G=0 total = 581,827", totals.get(0) == 581827, 581827, totals.get(0))
check("G=1 total = 477,505", totals.get(1) == 477505, 477505, totals.get(1))
check("G=2 total = 49,392", totals.get(2) == 49392, 49392, totals.get(2))
check("no Grundy value >=3", max(totals) <= 2, "<=2", sorted(totals))
check("grand total = 1,108,724", total == 1108724, 1108724, total)
check("G totals add to grand total",
      totals.get(0, 0) + totals.get(1, 0) + totals.get(2, 0) == total,
      total, totals.get(0, 0) + totals.get(1, 0) + totals.get(2, 0))
check("G=0 total from per-size distribution",
      sum(d.get(0, 0) for d in dist.values()) == 581827,
      581827, sum(d.get(0, 0) for d in dist.values()))
check("G=1 total from per-size distribution",
      sum(d.get(1, 0) for d in dist.values()) == 477505,
      477505, sum(d.get(1, 0) for d in dist.values()))
check("G=2 total from per-size distribution",
      sum(d.get(2, 0) for d in dist.values()) == 49392,
      49392, sum(d.get(2, 0) for d in dist.values()))

# hashes for reproducibility
hashes = {}
for p in (BOARD_PATH, REFERENCE_PATH, STATS_PATH):
    hashes[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()

result = {
    "pass": all(c["pass"] for c in checks),
    "n_checks": len(checks),
    "n_failed": sum(1 for c in checks if not c["pass"]),
    "checks": checks,
    "file_sha256": hashes,
    "reference_scalars": scalars,
    "reference_sizes": {str(k): v for k, v in ref_sizes.items()},
    "reference_grundy": ref_grundy,
    "stats_gsize_lines": {f"{k[0]},{k[1]}": v for k, v in stats_gsize.items()},
}
(HERE / "summary_totals.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

for c in checks:
    if not c["pass"]:
        print("FAIL:", c)
print(f"{len(checks) - result['n_failed']}/{len(checks)} checks PASS; overall {'PASS' if result['pass'] else 'FAIL'}")
raise SystemExit(0 if result["pass"] else 1)
