"""Audit saved witnesses with the standalone independent C++ checker."""
from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent


def audit(verifier: str, source: str, output: str, filtered: bool) -> dict:
    witnesses = json.loads((HERE / source).read_text(encoding="utf-8"))
    lines = []
    for witness in witnesses:
        p = witness["p"]
        parameters = witness["parameters"]
        assert len(parameters) == (p+3)//2
        assert len(set(parameters)) == len(parameters)
        assert parameters == sorted(parameters)
        lines.append(f"{p} {len(parameters)} " + " ".join(map(str,parameters)))
    command = [verifier] + (["--modular-filter"] if filtered else [])
    raw = subprocess.check_output(command, input="\n".join(lines)+"\n", text=True)
    fields = ["p", "points", "covered_quadruples", "integer_quadruples_checked"]
    records = [dict(zip(fields,map(int,line.split()))) for line in raw.splitlines()]
    assert len(records) == len(witnesses)
    for witness,record in zip(witnesses,records):
        assert record["p"] == witness["p"]
        assert record["points"] == len(witness["parameters"])
        assert record["covered_quadruples"] == comb(record["points"],4)
        if not filtered:
            assert record["integer_quadruples_checked"] == record["covered_quadruples"]
    method = ("generic 4x4 Leibniz determinant, exhaustive modulo-sum candidate filter proved in proof.md"
              if filtered else "generic 4x4 Leibniz __int128 determinant; no modular filter")
    result = {"method": method, "records": records}
    if not filtered:
        result["total_quadruples"] = sum(r["covered_quadruples"] for r in records)
    (HERE / output).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verifier", required=True)
    args = parser.parse_args()
    recovered = audit(args.verifier, "recovered-witnesses.json",
                      "recovered-independent-audit.json", False)
    probes = audit(args.verifier, "density-probe-witnesses.json",
                   "density-probe-independent-audit.json", True)
    print("Recovered primes:", len(recovered["records"]),
          "direct integer quadruples:", recovered["total_quadruples"])
    print("Density probes:", len(probes["records"]),
          "direct integer candidates:", sum(r["integer_quadruples_checked"] for r in probes["records"]),
          "quadruples covered:", sum(r["covered_quadruples"] for r in probes["records"]))


if __name__ == "__main__":
    main()
