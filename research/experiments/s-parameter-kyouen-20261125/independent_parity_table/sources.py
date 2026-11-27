"""Parsers for the published data sources cited by K1358."""
import json
from pathlib import Path


def parse_grundy_txt(path):
    """Parse the C engine's grundy_*.txt / stats_*.txt format."""
    out = {"SIZE": {}, "GRUNDY": {}, "GSIZE": {}}
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        t = raw.split()
        if not t:
            continue
        if t[0] == "POINTS":
            out["points"] = int(t[1])
        elif t[0] == "CIRCLES":
            out["circles"] = int(t[1])
        elif t[0] == "SAFE":
            out["safe"] = int(t[1])
        elif t[0] == "ROOT":
            out["root_grundy"] = int(t[1])
            out["root_misere_win"] = int(t[2])
        elif t[0] == "SIZE":
            out["SIZE"][int(t[1])] = {"total": int(t[2]),
                                      "maximal": int(t[3]),
                                      "g0": int(t[4])}
        elif t[0] == "GRUNDY":
            out["GRUNDY"][int(t[1])] = int(t[2])
        elif t[0] == "GSIZE":
            out["GSIZE"][(int(t[1]), int(t[2]))] = int(t[3])
        # FIRSTMOVE / PROBE / PROBE_CHILDREN ignored
    return out


def parse_grundy_general(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {g["name"]: g for g in data["games"]}


def parse_census_pg2q9(path):
    out = {"SIZE": {}}
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        t = raw.split()
        if not t:
            continue
        if t[0] == "N":
            out["points"] = int(t[1])
            out["circles"] = int(t[3])
            out["safe"] = int(t[5])
        elif t[0] == "SIZE":
            out["SIZE"][int(t[1])] = {"total": int(t[2]),
                                      "maximal": int(t[3])}
    return out


def parse_spectrum(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


# K1352 (knowledge item) full PG(2,9) s=2 Grundy classification.
# Not among the K1358 artifact list, but it is the only source for "max G = 2".
K1352_PG2Q9 = {
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

# K1357 (knowledge item) maximal counts for the two s=3 projective boards.
K1357_MAXIMAL = {
    "PG2q3_s3": {7: 234, 9: 13},
    "PG2q4_s3": {7: 360, 9: 11480},
}
