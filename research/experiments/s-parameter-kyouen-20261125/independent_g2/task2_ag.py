"""Tasks 2 & 4 (AG boards): exhaustive caps, maximal caps, subset
distinctness, full Grundy DP, and comparison with the published data files.

Usage: python task2_ag.py AG2q5|AG2q7
"""

from __future__ import annotations

import json
import sys
import time
from collections import Counter
from itertools import combinations
from math import comb

import g2common as C

PUB = {
    "AG2q5": {
        "name": "AG(2,5)",
        "board": C.BOARDS["AG(2,5)"],
        "max_size": 5,
        "subset_size": 4,
        "json_game": "AG2(5)_s2",
        "json_path": C.REPO / "research/experiments/s-parameter-kyouen-20261125/output/grundy_general.json",
        "stats_path": C.REPO / "research/experiments/s-parameter-kyouen-20261125/output/stats_ag2q5_s2.txt",
        "claim_max": 600,
        "claim_subsets": 3000,
        "claim_g2": 3000,
    },
    "AG2q7": {
        "name": "AG(2,7)",
        "board": C.BOARDS["AG(2,7)"],
        "max_size": 7,
        "subset_size": 5,
        "json_game": None,
        "json_path": None,
        "stats_path": None,
        "grundy_path": C.REPO / "research/experiments/pg2q7-cap-game-20261125/output/grundy_ag2q7_s2.txt",
        "claim_max": 2352,
        "claim_subsets": 49392,
        "claim_g2": 49392,
    },
}


def parse_grundy_txt(path):
    out = {"GRUNDY": {}, "SIZE": {}, "GSIZE": {}, "maximal": {}}
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "GRUNDY":
            out["GRUNDY"][int(parts[1])] = int(parts[2])
        elif parts[0] == "SIZE":
            out["SIZE"][int(parts[1])] = [int(x) for x in parts[2:]]
        elif parts[0] == "GSIZE":
            out["GSIZE"][(int(parts[1]), int(parts[2]))] = int(parts[3])
    return out


def main():
    key = sys.argv[1]
    cfg = PUB[key]
    t0 = time.time()
    n, blocks = C.load_board(cfg["board"])
    print(f"{cfg['name']}: n={n}, b={len(blocks)}", flush=True)

    by_size = C.enumerate_all_caps(n, blocks)
    size_counts = {s: len(v) for s, v in enumerate(by_size) if v}
    total_caps = sum(size_counts.values())
    print("enumeration:", size_counts, "total", total_caps, f"({time.time()-t0:.1f}s)", flush=True)

    g, maximal, _, max_size = C.grundy_all(n, blocks, by_size)
    print("DP done", f"({time.time()-t0:.1f}s)", "max_size", max_size,
          "maximal", dict(sorted(maximal.items())), flush=True)
    dist = Counter(g.values())
    per_size_g = Counter((mask.bit_count(), v) for mask, v in g.items())

    # maximal caps of the odd size claimed by K1336
    size = cfg["max_size"]
    lmasks = C.line_masks(blocks)
    max_caps = [m for m in by_size[size] if C.addable_mask(m, n, lmasks) == 0]
    assert all(g[m] == 0 for m in max_caps)

    # (subset_size)-subsets of maximal odd caps, with a real hash set
    subs = set()
    duplicates = 0
    pts_of = [C.bits(M) for M in max_caps]
    for pts in pts_of:
        for comb_pts in combinations(pts, cfg["subset_size"]):
            X = C.mask_of(comb_pts)
            if X in subs:
                duplicates += 1
            subs.add(X)
    expected_sub_count = len(max_caps) * comb(size, cfg["subset_size"])

    g2 = {m for m, v in g.items() if v == 2}
    g2_sizes = Counter(m.bit_count() for m in g2)
    g2_is_exactly_subsets = g2 == subs
    g2_size_is_subset_size = set(g2_sizes) == {cfg["subset_size"]}

    # every (size-1)-subset must itself be a cap (sanity) and be a key of g
    caps_ok = all(m in g for m in subs)

    # maximal-extension profile of the maximal caps themselves is trivial;
    # extension profile of each subset is reported by task 3.

    result = {
        "board": cfg["name"],
        "n": n,
        "b": len(blocks),
        "size_counts": size_counts,
        "total_caps": total_caps,
        "maximal_by_size": dict(sorted(maximal.items())),
        "max_size": max_size,
        "grundy_dist": dict(sorted(dist.items())),
        "grundy_by_size": {f"{s},{k}": v for (s, k), v in sorted(per_size_g.items())},
        "maximal_odd_caps": {
            "size": size,
            "count": len(max_caps),
            "claimed": cfg["claim_max"],
            "all_terminal": all(C.addable_mask(m, n, lmasks) == 0 for m in max_caps),
        },
        "subsets": {
            "subset_size": cfg["subset_size"],
            "generated": expected_sub_count,
            "distinct": len(subs),
            "duplicates": duplicates,
            "claimed": cfg["claim_subsets"],
            "all_are_caps": caps_ok,
        },
        "g2": {
            "count": len(g2),
            "claimed": cfg["claim_g2"],
            "sizes": dict(sorted(g2_sizes.items())),
            "equals_all_subsets": g2_is_exactly_subsets,
            "all_size_subset_size": g2_size_is_subset_size,
        },
        "seconds": round(time.time() - t0, 2),
    }

    # --- comparison with published data -------------------------------------
    comparison = {}
    if cfg.get("json_path") and cfg["json_path"].exists():
        data = json.loads(cfg["json_path"].read_text(encoding="utf-8"))
        game = next(x for x in data["games"] if x["name"] == cfg["json_game"])
        comparison["json_size_counts"] = {
            "published": game["size_counts"],
            "ours": {str(k): v for k, v in size_counts.items()},
            "match": {str(k): v for k, v in size_counts.items()} == game["size_counts"],
        }
        comparison["json_maximal_by_size"] = {
            "published": game["maximal_by_size"],
            "ours": {str(k): v for k, v in maximal.items()},
            "match": {str(k): v for k, v in maximal.items()} == game["maximal_by_size"],
        }
        comparison["json_grundy_dist"] = {
            "published": game["grundy_dist"],
            "ours": {str(k): v for k, v in dist.items()},
            "match": {str(k): v for k, v in dist.items()} == game["grundy_dist"],
        }
        comparison["json_root_grundy"] = {"published": game["root_grundy"], "ours": g[0]}
    if cfg.get("grundy_path") and cfg["grundy_path"].exists():
        pub = parse_grundy_txt(cfg["grundy_path"])
        comparison["txt_grundy"] = {
            "published": pub["GRUNDY"],
            "ours": {k: dist.get(k, 0) for k in sorted(pub["GRUNDY"])},
            "match": {k: dist.get(k, 0) for k in sorted(pub["GRUNDY"])} == pub["GRUNDY"],
        }
        pub_sizes = {k: v[0] for k, v in pub["SIZE"].items()}
        comparison["txt_size_total"] = {
            "published": pub_sizes,
            "ours": size_counts,
            "match": {k: size_counts.get(k, 0) for k in sorted(pub_sizes)} == pub_sizes,
        }
        comparison["txt_gsize"] = {
            "published": {f"{s},{gg}": v for (s, gg), v in pub["GSIZE"].items()},
            "ours": {f"{s},{gg}": v for (s, gg), v in per_size_g.items()
                     if (s, gg) in pub["GSIZE"]},
            "match": all(per_size_g.get(key2, 0) == v
                         for key2, v in pub["GSIZE"].items()),
        }
        # The SIZE lines of grundy_ag2q7_s2.txt are:
        #   SIZE k  total  maximal  G0
        pub_max = {k: v[1] for k, v in pub["SIZE"].items()}
        pub_g0 = {k: v[2] for k, v in pub["SIZE"].items()}
        our_g0 = {s: per_size_g.get((s, 0), 0) for s in size_counts}
        comparison["txt_maximal_column"] = {
            "published": pub_max,
            "ours": {**{s: 0 for s in size_counts}, **dict(maximal)},
            "match": all(maximal.get(k, 0) == v for k, v in pub_max.items()),
        }
        comparison["txt_g0_column"] = {
            "published": pub_g0,
            "ours": our_g0,
            "match": all(our_g0.get(k, 0) == v for k, v in pub_g0.items()),
        }
        comparison["txt_maximal_col"] = {
            "published": pub["SIZE"],
            "note": "SIZE lines: size, total, maximal, G0 (validated above)",
        }
    result["comparison"] = comparison

    (C.OUT / f"task2_{key}.json").write_text(json.dumps(result, indent=1), encoding="utf-8")

    print()
    print("maximal caps of size", size, ":", len(max_caps), "(claim", cfg["claim_max"], ")")
    print("subsets:", expected_sub_count, "distinct:", len(subs), "duplicates:", duplicates)
    print("G=2:", len(g2), "sizes:", dict(g2_sizes), "equals subsets:", g2_is_exactly_subsets)
    print("grundy dist:", dict(sorted(dist.items())))
    print("maximal by size:", dict(sorted(maximal.items())))
    print("comparison:", json.dumps(comparison, indent=1)[:4000])
    print(f"total {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
