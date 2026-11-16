#!/usr/bin/env python3
"""Assemble the order-matrix JSONLs for the cost-76d/77e v17 re-check (2026-11-17).

Reads the 16 solo runs in o-order/ (v16/v17 x andclose 0/1 for 76d bits
112/99 and 77e bits 33/0, depth 10, cap 1e9, fresh engine per run) and
emits one JSONL line per configuration with explicit metadata. Also
cross-checks that each v16-andclose1 line reproduces the published raw
batch record for that bit (the original sweep configuration).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
ORD = HERE / "o-order"

CONFIGS = {
    "76d": {
        "child": "00000000040000003800080008000000",
        "bits": [112, 99],
        "raw": ["class2-lane-cost76d-raw-batch8-20261116.jsonl",
                "class2-lane-cost76d-raw-batch9-20261116.jsonl"],
        "dest": "class2-lane-cost76d-v17-ordermatrix-20261117.jsonl",
    },
    "77e": {
        "child": "00000000040000809002000000004000",
        "bits": [33, 0],
        "raw": ["class2-lane-cost77e-raw-batch1-20261116.jsonl",
                "class2-lane-cost77e-raw-batch4-20261116.jsonl"],
        "dest": "class2-lane-cost77e-v17-ordermatrix-20261117.jsonl",
    },
}


def load_bits(path):
    recs = {}
    for line in Path(path).read_text().splitlines():
        d = json.loads(line)
        if "bit" in d:
            recs[d["bit"]] = d
    return recs


def main():
    for row, spec in CONFIGS.items():
        raw = {}
        for r in spec["raw"]:
            raw.update(load_bits(OUT / r))
        lines = []
        checks = []
        for bit in spec["bits"]:
            for engine in ("v16", "v17"):
                for ac in (0, 1):
                    p = ORD / f"om-{row}-b{bit}-{engine}-a{ac}.jsonl"
                    rec = load_bits(p)[bit]
                    line = {
                        "row": f"cost-{row}",
                        "bit": bit,
                        "engine": engine,
                        "engine_blob": ("0a4a86f6828dc010c89ff17596054336a6b6091f"
                                        if engine == "v16"
                                        else "c132cc6425eee3feaeef1d697dd74f968cfedb59"),
                        "andclose_param": ac,
                        "depth": 10,
                        "cap": 1000000000,
                        "child": spec["child"],
                        "loss": rec["loss"],
                        "nodes": rec["nodes"],
                        "capped": rec["capped"],
                        "terminalStoneRange": rec["terminalStoneRange"],
                        "andclose_effective": rec["andclose"],
                    }
                    lines.append(line)
                    if engine == "v16" and ac == 1:
                        pub = raw[bit]
                        agree = (pub["loss"] == rec["loss"] and
                                 pub["nodes"] == rec["nodes"] and
                                 pub["terminalStoneRange"] == rec["terminalStoneRange"])
                        checks.append({"bit": bit, "reproduces_published_raw": agree})
        dest = OUT / spec["dest"]
        with open(dest, "w") as f:
            for line in lines:
                f.write(json.dumps(line, sort_keys=True) + "\n")
        verdicts = sorted({(l["bit"], l["loss"]) for l in lines})
        print(row, "configs:", len(lines), "verdicts:", verdicts,
              "v16-a1 reproduces published raw:", all(c["reproduces_published_raw"] for c in checks))
        if not all(c["reproduces_published_raw"] for c in checks):
            raise SystemExit(1)


if __name__ == "__main__":
    main()
