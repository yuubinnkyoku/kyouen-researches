"""Independent verification of the PG(2,4) s=3 game spectrum (K1355 claim).

Board given in the parent experiment.  All output stays under independent/.
Python standard library only.
"""
import itertools
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOARD = HERE.parent.parent / "projective-blocking-kyouen-20261125" / "output" / "board_pg2q4.txt"
FULL = (1 << 21) - 1

CLAIM = {  # claimed: k -> (grundy, count)
    0: (1, 1), 1: (0, 21), 2: (1, 210), 3: (0, 1330), 4: (1, 5040),
    5: (0, 16128), 6: (1, 35952), 7: (0, 50976), 8: (1, 37620), 9: (0, 10120),
}
CLAIM_TOTAL = 157398
CLAIM_G0 = 78575
CLAIM_G1 = 78823


def read_board(path):
    rows = path.read_text().splitlines()
    n, nb = map(int, rows[0].split())
    blocks = []
    for row in rows[1:]:
        vals = list(map(int, row.split()))
        assert vals[0] == 5
        blocks.append(sum(1 << p for p in vals[1:]))
    assert len(blocks) == nb
    return n, blocks


def build_pc(n, blocks):
    pc = [[] for _ in range(n)]
    for c, m in enumerate(blocks):
        for p in range(n):
            if (m >> p) & 1:
                pc[p].append(c)
    return pc


def check_pg(n, blocks):
    problems = []
    if n != 21 or len(blocks) != 21:
        problems.append("wrong point/line count")
    if any(m.bit_count() != 5 for m in blocks):
        problems.append("line size != 5")
    if len(set(blocks)) != 21:
        problems.append("duplicate lines")
    pair = Counter()
    for m in blocks:
        pts = [p for p in range(n) if (m >> p) & 1]
        for a, b in itertools.combinations(pts, 2):
            pair[(a, b)] += 1
    if len(pair) != n * (n - 1) // 2 or any(v != 1 for v in pair.values()):
        problems.append("pair not on exactly one line")
    return problems


def enumerate_safe(n, blocks, pc):
    """Every safe set exactly once; increasing-point DFS."""
    sys.setrecursionlimit(10000)
    counts = [0] * len(blocks)
    order = []

    def dfs(mask, start):
        order.append(mask)
        for p in range(start, n):
            ok = True
            for c in pc[p]:
                if counts[c] >= 3:
                    ok = False
                    break
            if not ok:
                continue
            for c in pc[p]:
                counts[c] += 1
            dfs(mask | (1 << p), p + 1)
            for c in pc[p]:
                counts[c] -= 1

    dfs(0, 0)
    return order


def grundy_bottom_up(order):
    by_size = defaultdict(list)
    for m in order:
        by_size[m.bit_count()].append(m)
    g = {}
    for k in range(max(by_size), -1, -1):
        for m in by_size[k]:
            opts = set()
            avail = FULL & ~m
            while avail:
                b = avail & -avail
                nm = m | b
                if nm in g:
                    opts.add(g[nm])
                avail ^= b
            v = 0
            while v in opts:
                v += 1
            g[m] = v
    return by_size, g


def cone(n, blocks, pc, base):
    """All safe supersets of base, with their full local Grundy values."""
    counts = [0] * len(blocks)
    for p in range(n):
        if (base >> p) & 1:
            for c in pc[p]:
                counts[c] += 1
    order = []

    def dfs(mask, start):
        order.append(mask)
        for p in range(start, n):
            if (base >> p) & 1:
                continue
            if any(counts[c] >= 3 for c in pc[p]):
                continue
            for c in pc[p]:
                counts[c] += 1
            dfs(mask | (1 << p), p + 1)
            for c in pc[p]:
                counts[c] -= 1

    dfs(base, 0)
    g = {}
    for m in sorted(order, key=lambda x: -x.bit_count()):
        opts = set()
        avail = FULL & ~m
        while avail:
            b = avail & -avail
            nm = m | b
            if nm in g:
                opts.add(g[nm])
            avail ^= b
        v = 0
        while v in opts:
            v += 1
        g[m] = v
    return order, g


def full_upset_grundy(mask, safe, memo):
    """Independent memoised DP over the full upset of mask."""
    if mask in memo:
        return memo[mask]
    opts = set()
    avail = FULL & ~mask
    while avail:
        b = avail & -avail
        nm = mask | b
        if nm in safe:
            opts.add(full_upset_grundy(nm, safe, memo))
        avail ^= b
    v = 0
    while v in opts:
        v += 1
    memo[mask] = v
    return v


def main():
    out = {}
    n, blocks = read_board(BOARD)
    pc = build_pc(n, blocks)
    out["board_problems"] = check_pg(n, blocks)

    # ---------- exhaustive brute force over all subsets of size <= 10 ----------
    brute = Counter()
    for mask in range(1 << 21):
        k = mask.bit_count()
        if k > 10:
            continue
        ok = True
        for b in blocks:
            if (mask & b).bit_count() > 3:
                ok = False
                break
        if ok:
            brute[k] += 1
    out["brute_force_counts_0_10"] = {str(k): brute[k] for k in range(11)}
    out["brute_total_le9"] = sum(brute[k] for k in range(10))
    out["brute_size10"] = brute[10]

    # ---------- full DFS enumeration + Grundy DP ----------
    order = enumerate_safe(n, blocks, pc)
    by_size, g = grundy_bottom_up(order)
    true_counts = {k: len(v) for k, v in sorted(by_size.items())}
    out["true_counts"] = {str(k): true_counts[k] for k in sorted(true_counts)}
    out["true_total"] = len(order)
    gdist = {k: dict(Counter(g[m] for m in v)) for k, v in sorted(by_size.items())}
    out["grundy_distribution"] = {str(k): {str(x): c for x, c in sorted(gdist[k].items())} for k in gdist}
    out["uniform_grundy_per_size"] = all(len(d) == 1 for d in gdist.values())
    out["max_safe_size"] = max(by_size)
    out["dfs_vs_bruteforce_0_9"] = all(true_counts.get(k, 0) == brute[k] for k in range(10))

    # terminal counts per size
    terminal = {}
    for k, masks in by_size.items():
        cnt = 0
        for m in masks:
            has = False
            avail = FULL & ~m
            while avail:
                b = avail & -avail
                if (m | b) in g:
                    has = True
                    break
                avail ^= b
            if not has:
                cnt += 1
        terminal[k] = cnt
    out["terminal_counts"] = {str(k): terminal[k] for k in sorted(terminal)}

    true_g0 = sum(true_counts[k] for k in true_counts if k % 2 == 1)
    true_g1 = sum(true_counts[k] for k in true_counts if k % 2 == 0)
    out["true_G0"] = true_g0
    out["true_G1"] = true_g1
    out["true_total_check"] = true_g0 + true_g1

    # ---------- the two cones ----------
    tri = (1 << 0) | (1 << 1) | (1 << 5)
    col = (1 << 0) | (1 << 1) | (1 << 2)
    cones = {}
    for name, base in [("triangle", tri), ("collinear", col)]:
        ordc, gc = cone(n, blocks, pc, base)
        Tc = Counter(m.bit_count() for m in ordc)
        Gc = defaultdict(Counter)
        for m in ordc:
            Gc[m.bit_count()][gc[m]] += 1
        # cross-check against full enumeration
        via_full = Counter()
        for m in order:
            if (m & base) == base:
                via_full[m.bit_count()] += 1
        cones[name] = {
            "base": [p for p in range(n) if (base >> p) & 1],
            "base_grundy": gc[base],
            "size": len(ordc),
            "T": {str(k): Tc[k] for k in sorted(Tc)},
            "T_grundy": {str(k): {str(x): c for x, c in sorted(Gc[k].items())} for k in sorted(Gc)},
            "via_full_enumeration": {str(k): via_full[k] for k in sorted(via_full)},
            "dfs_matches_full": all(Tc[k] == via_full[k] for k in set(Tc) | set(via_full)),
        }
    out["cones"] = cones

    # ---------- double counting ----------
    T = {int(k): v for k, v in cones["triangle"]["T"].items()}
    U = {int(k): v for k, v in cones["collinear"]["T"].items()}
    Tg = {int(k): {int(x): c for x, c in v.items()} for k, v in cones["triangle"]["T_grundy"].items()}
    Ug = {int(k): {int(x): c for x, c in v.items()} for k, v in cones["collinear"]["T_grundy"].items()}
    N3 = 1120
    formula = {}
    for m in range(3, 10):
        C = math.comb(m, 3)
        claim_num = N3 * T[m]
        claim_val = claim_num // C
        claim_int = claim_num % C == 0
        corr_num = N3 * T[m] + 210 * U[m]
        corr_val = corr_num // C
        corr_int = corr_num % C == 0
        formula[m] = {
            "C(m,3)": C,
            "T_m": T[m],
            "U_m": U[m],
            "claim_1120*T_m": claim_num,
            "claim_integer": claim_int,
            "claim_N_m": claim_val,
            "claim_N_m_plus_k3_210": claim_val + (210 if m == 3 else 0),
            "corrected_numerator": corr_num,
            "corrected_integer": corr_int,
            "corrected_N_m": corr_val,
            "true_N_m": true_counts[m],
            "corrected_matches_true": corr_val == true_counts[m],
            "claim_matches_true": (claim_val + (210 if m == 3 else 0)) == true_counts[m],
            "deficit": true_counts[m] - (claim_val + (210 if m == 3 else 0)),
        }
    out["double_counting"] = formula
    out["claim_table"] = {str(k): {"G": v[0], "N": v[1]} for k, v in CLAIM.items()}
    out["claim_table_matches_formula"] = all(
        CLAIM[m] == (0 if m % 2 else 1, formula[m]["claim_N_m_plus_k3_210"]) for m in range(3, 10)
    )
    # g-resolved corrected identity
    gsplit = {}
    for m in range(3, 10):
        C = math.comb(m, 3)
        rows = {}
        for gg in sorted(set(Tg[m]) | set(Ug[m]) | {CLAIM[m][0]}):
            num = N3 * Tg[m].get(gg, 0) + 210 * Ug[m].get(gg, 0)
            rows[str(gg)] = {
                "T_m_g": Tg[m].get(gg, 0),
                "U_m_g": Ug[m].get(gg, 0),
                "numerator": num,
                "integer": num % C == 0,
                "N_m_g": num // C,
                "true_N_m_g": gdist[m].get(gg, 0),
                "matches": num // C == gdist[m].get(gg, 0),
            }
        gsplit[str(m)] = rows
    out["grundy_resolved_identity"] = gsplit

    # ---------- 3-caps ----------
    triples = list(itertools.combinations(range(n), 3))

    def collinear(t):
        a, b, c = t
        for bl in blocks:
            if ((bl >> a) & 1) and ((bl >> b) & 1):
                return bool((bl >> c) & 1)
        raise AssertionError

    col_t = [t for t in triples if collinear(t)]
    ncol_t = [t for t in triples if not collinear(t)]
    out["three_caps"] = {
        "total": len(triples),
        "collinear": len(col_t),
        "collinear_formula_21*C(5,3)": 21 * math.comb(5, 3),
        "noncollinear": len(ncol_t),
        "noncollinear_formula": len(triples) - len(col_t),
        "all_safe": all(
            all(((sum(1 << p for p in t) & bl).bit_count() <= 3) for bl in blocks) for t in triples
        ),
        "all_grundy_zero": all(g[sum(1 << p for p in t)] == 0 for t in triples),
    }

    # ---------- sample 10 caps per size, full upset DP ----------
    rng = random.Random(20261128)
    safe_set = set(order)
    samples = {}
    all_ok = True
    for k in range(10):
        pool = sorted(by_size[k])
        picks = rng.sample(pool, min(10, len(pool)))
        rows = []
        for m in picks:
            memo = {}
            gv = full_upset_grundy(m, safe_set, memo)
            claimed_g = CLAIM[k][0]
            row = {
                "points": [p for p in range(n) if (m >> p) & 1],
                "G": gv,
                "claimed_G": claimed_g,
                "G_matches_claim": gv == claimed_g,
                "G_matches_full_DP": gv == g[m],
                "states": len(memo),
            }
            rows.append(row)
            if not (row["G_matches_claim"] and row["G_matches_full_DP"]):
                all_ok = False
        samples[str(k)] = rows
    out["samples"] = samples
    out["samples_all_pass"] = all_ok

    # ---------- mex chain for k=0,1,2 ----------
    empty = 0
    chain = {}
    chain["G_empty"] = g[empty]
    chain["G_singletons"] = sorted({g[1 << p] for p in range(n)})
    chain["empty_options_grundy_set"] = sorted({g[1 << p] for p in range(n)})
    chain["empty_mex_check"] = g[empty] == (0 if 0 not in {g[1 << p] for p in range(n)} else 1)
    # all 2-sets
    two = by_size[2]
    chain["G_2sets_set"] = sorted({g[m] for m in two})
    chain["all_2sets_have_option"] = all(
        any(((m | (1 << p)) in g) for p in range(n) if not ((m >> p) & 1)) for m in two
    )
    chain["two_set_options_grundy_set"] = sorted({
        g[m | (1 << p)] for m in two for p in range(n)
        if not ((m >> p) & 1) and (m | (1 << p)) in g
    })
    three = by_size[3]
    chain["G_3sets_set"] = sorted({g[m] for m in three})
    chain["all_3sets_have_option"] = all(
        any(((m | (1 << p)) in g) for p in range(n) if not ((m >> p) & 1)) for m in three
    )
    chain["three_set_options_grundy_set"] = sorted({
        g[m | (1 << p)] for m in three for p in range(n)
        if not ((m >> p) & 1) and (m | (1 << p)) in g
    })
    chain["G_empty_mex_chain_ok"] = (
        chain["G_empty"] == 1 and chain["G_singletons"] == [0]
        and chain["G_2sets_set"] == [1] and chain["two_set_options_grundy_set"] == [0]
        and chain["G_3sets_set"] == [0] and chain["three_set_options_grundy_set"] == [1]
    )
    out["mex_chain"] = chain

    # ---------- claim comparison ----------
    comp = {}
    for k in range(10):
        comp[str(k)] = {
            "claim_G": CLAIM[k][0],
            "true_G": sorted(gdist[k]),
            "G_agree": CLAIM[k][0] in gdist[k],
            "claim_N": CLAIM[k][1],
            "true_N": true_counts[k],
            "N_agree": CLAIM[k][1] == true_counts[k],
        }
    out["claim_comparison"] = comp
    out["claim_total_agree"] = CLAIM_TOTAL == len(order)
    out["claim_G0_agree"] = CLAIM_G0 == true_g0
    out["claim_G1_agree"] = CLAIM_G1 == true_g1
    out["claim_G_values_agree"] = all(CLAIM[k][0] in gdist[k] for k in range(10))

    print("board problems:", out["board_problems"])
    print("brute-force counts 0..10:", [brute[k] for k in range(11)])
    print("DFS counts 0..9:", [true_counts[k] for k in range(10)], "total", len(order))
    print("grundy distribution:", out["grundy_distribution"])
    print("terminal counts:", out["terminal_counts"])
    print("true G0/G1:", true_g0, true_g1)
    print("cones:", json.dumps(out["cones"], indent=1)[:4000])
    print("double counting:")
    for m in range(3, 10):
        f = formula[m]
        print(f"  m={m}: T={f['T_m']} U={f['U_m']} claim={f['claim_N_m']}(+k3={f['claim_N_m_plus_k3_210']}) "
              f"corrected={f['corrected_N_m']} true={f['true_N_m']} deficit={f['deficit']}")
    print("claim table matches flawed formula:", out["claim_table_matches_formula"])
    print("claim comparisons:")
    for k in range(10):
        c = comp[str(k)]
        print(f"  k={k}: claim G={c['claim_G']} true G={c['true_G']} G_agree={c['G_agree']} "
              f"claim N={c['claim_N']} true N={c['true_N']} N_agree={c['N_agree']}")
    print("totals: claim", CLAIM_TOTAL, CLAIM_G0, CLAIM_G1, "| true", len(order), true_g0, true_g1)
    print("samples all pass:", all_ok)
    print("mex chain:", {k: v for k, v in chain.items() if k.startswith("G_") or k.endswith("ok")})

    (HERE / "game_out.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
