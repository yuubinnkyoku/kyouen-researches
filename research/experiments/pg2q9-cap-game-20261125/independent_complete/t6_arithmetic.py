"""Task 5: arithmetic of the claimed size/Grundy table and census comparison."""

from __future__ import annotations

import json
import math

import pg

CLAIM_N = {
    0: 1,
    1: 91,
    2: 4095,
    3: 110565,
    4: 1769040,
    5: 14859936,
    6: 52009776,
    7: 51554880,
    8: 7960680,
    9: 589680,
    10: 58968,
}
CLAIM_MAX = {
    0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
    6: 707616, 7: 2021760, 8: 5307120, 9: 0, 10: 58968,
}
CLAIM_G = {
    0: {0: 1},
    1: {1: 91},
    2: {0: 4095},
    3: {1: 110565},
    4: {0: 1769040},
    5: {1: 14859936},
    6: {0: 37857456, 2: 14152320},
    7: {0: 2021760, 1: 49533120},
    8: {0: 7960680},
    9: {1: 589680},
    10: {0: 58968},
}


def parse_census(path=pg.CENSUS_PATH):
    lines = path.read_text(encoding="utf-8").splitlines()
    head = lines[0].split()
    assert head[0] == "N" and head[2] == "B"
    n, b, safe = int(head[1]), int(head[3]), int(head[5])
    sizes = {}
    maximal = {}
    for ln in lines[1:]:
        parts = ln.split()
        assert parts[0] == "SIZE"
        k, total, mx = int(parts[1]), int(parts[2]), int(parts[3])
        sizes[k] = total
        maximal[k] = mx
    return {"n": n, "b": b, "safe": safe, "sizes": sizes, "maximal": maximal}


def main():
    census = parse_census()
    out = {"census": census}

    # 1. census vs claim table
    assert census["sizes"] == CLAIM_N, (census["sizes"], CLAIM_N)
    assert census["maximal"] == CLAIM_MAX, (census["maximal"], CLAIM_MAX)
    assert census["safe"] == sum(CLAIM_N.values()) == 128917712
    assert sum(CLAIM_MAX.values()) == 8095464

    # 2. k=6 and k=7 splits
    split6 = CLAIM_G[6]
    split7 = CLAIM_G[7]
    assert sum(split6.values()) == CLAIM_N[6] == 52009776
    assert sum(split7.values()) == CLAIM_N[7] == 51554880
    assert split6[0] + split6[2] == 52009776
    assert split7[0] + split7[1] == 51554880
    assert split7[0] == CLAIM_MAX[7]
    assert split6[2] == 14152320

    # 3. totals
    total = sum(CLAIM_N.values())
    assert total == 128917712

    # 4. parity rule for k = 0..5 and 8..10
    parity = {}
    for k in list(range(0, 6)) + [8, 9, 10]:
        vals = CLAIM_G[k]
        assert len(vals) == 1, (k, vals)
        g = next(iter(vals))
        expect = (10 - k) % 2
        parity[k] = {"G": g, "formula": expect, "ok": g == expect}
        assert g == expect, (k, g, expect)

    # 5. compare with the frame-derived global distribution (if available)
    frame_path = pg.HERE / "out" / "t2_frame_census.json"
    frame_derived = None
    if frame_path.exists():
        data = json.loads(frame_path.read_text(encoding="utf-8"))
        frame_derived = {}
        for k, d in data["global_grundy"].items():
            frame_derived[int(k)] = {int(g): c for g, c in d.items()}
        # k=0..3 are not covered by the frame double counting
        for k in range(4, 11):
            assert frame_derived[k] == CLAIM_G[k], (k, frame_derived[k], CLAIM_G[k])

    # 6. conic identities, using the verified counts
    conics = CLAIM_N[10]
    conic_identities = {
        "conics=10caps": conics == 58968,
        "9caps=10*conics": CLAIM_N[9] == 10 * conics,
        "nonmax8=C(10,8)*conics": CLAIM_N[8] - CLAIM_MAX[8]
        == math.comb(10, 8) * conics,
        "8caps=max8+nonmax8": CLAIM_N[8]
        == CLAIM_MAX[8] + math.comb(10, 8) * conics,
        "conic5=conics*C(10,5)": CLAIM_N[5] == conics * math.comb(10, 5),
        "conic6=conics*C(10,6)": conics * math.comb(10, 6)
        == 12383280,
    }
    assert all(conic_identities.values()), conic_identities

    # 7. frame double-counting factors used in the census derivation
    factors = {}
    N4 = CLAIM_N[4]
    for k in range(4, 11):
        factors[k] = {
            "C(k,4)": math.comb(k, 4),
            "N_k*C(k,4) % N4": (CLAIM_N[k] * math.comb(k, 4)) % N4,
        }
        assert factors[k]["N_k*C(k,4) % N4"] == 0

    # 8. average upset sizes of a j-cap (j = 1..4): exact because PGL is
    # transitive on 1-, 2-, 3-, 4-caps.
    upset = {}
    denominators = {1: CLAIM_N[1], 2: CLAIM_N[2], 3: CLAIM_N[3], 4: CLAIM_N[4]}
    for j in (1, 2, 3, 4):
        total_pairs = sum(
            math.comb(k, j) * CLAIM_N[k] for k in CLAIM_N if k >= j
        )
        assert total_pairs % denominators[j] == 0
        upset[j] = total_pairs // denominators[j]
    assert upset == {1: 9057592, 2: 554122, 3: 31681, 4: 1868}

    out.update(
        {
            "claim_N": {str(k): v for k, v in CLAIM_N.items()},
            "claim_max": {str(k): v for k, v in CLAIM_MAX.items()},
            "claim_G": {
                str(k): {str(g): c for g, c in v.items()}
                for k, v in CLAIM_G.items()
            },
            "split6": {str(k): v for k, v in split6.items()},
            "split7": {str(k): v for k, v in split7.items()},
            "total": total,
            "maximal_total": sum(CLAIM_MAX.values()),
            "parity": {str(k): v for k, v in parity.items()},
            "frame_derived_global_grundy": (
                {str(k): {str(g): c for g, c in v.items()}
                 for k, v in frame_derived.items()}
                if frame_derived else None
            ),
            "conic_identities": conic_identities,
            "upset_sizes": {str(k): v for k, v in upset.items()},
            "double_counting_factors": {
                str(k): {kk: vv for kk, vv in v.items()}
                for k, v in factors.items()
            },
        }
    )
    (pg.HERE / "out").mkdir(exist_ok=True)
    (pg.HERE / "out" / "t6_arithmetic.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8"
    )
    print("census sizes:", census["sizes"])
    print("census maximal:", census["maximal"])
    print("k=6 split:", split6)
    print("k=7 split:", split7)
    print("total:", total, "maximal total:", sum(CLAIM_MAX.values()))
    print("parity:", parity)
    print("conic identities:", conic_identities)
    print("upset sizes F1..F4:", upset)
    print("frame-derived global table matches claim:",
          frame_derived is not None)


if __name__ == "__main__":
    main()
