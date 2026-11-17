#!/usr/bin/env python3
"""Determinism re-extraction control for the cost73l certificates (2026-11-17).

Re-extracts a fixed sample of the 32 WIN7-D10 certificate roots in fresh
processes with the exact publication pipeline (MS=1<<23 extractor variant,
per-bit fresh process) and compares the re-extracted files byte-for-byte
(md5 + size + row count) with the original certificates. Writes
output/class2-lane-cost73l-certificates/det-reextraction.json in the schema
the manifest builder reads:
  {"all_byte_identical": bool, "bits": [...],
   "details": {"<bit>": {"size": int, "rows": int, "md5": str, "identical": bool}}}

Usage: reextract_cost73l_det_20261117.py <bit> [<bit> ...]
Run bits sequentially; each bit is a fresh extraction process. The JSON is
(over)written at the end of each successful bit so partial progress survives
a timeout; a bit mismatch aborts with exit 1.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent  # experiment dir
WORK = HERE / "output" / "class2-lane-cost73l-certificates"
CHILD = "00000000000000c09002000000400000"
DET_JSON = WORK / "det-reextraction.json"


def extract(bit: int, out: pathlib.Path) -> None:
    root = "%032x" % (int(CHILD, 16) | (1 << bit))
    cmd = (
        f"python3 {HERE}/scripts/legal_candidates.py {root} "
        f"| node --experimental-strip-types "
        f"{HERE}/scripts/cert_driver73l.ts {CHILD} {bit} {out}"
    )
    r = subprocess.run(["sh", "-c", cmd], cwd=HERE,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, timeout=3000)
    out_log = pathlib.Path(str(out) + ".log")
    out_log.write_text(r.stdout)
    if r.returncode != 0:
        raise RuntimeError(f"extraction failed bit {bit}: rc={r.returncode}")


def summarize(path: pathlib.Path) -> dict:
    data = path.read_bytes()
    rows = sum(1 for line in data.split(b"\n")[2:] if line.strip())
    return {"size": len(data), "rows": rows,
            "md5": hashlib.md5(data).hexdigest()}


def main() -> None:
    bits = [int(a) for a in sys.argv[1:]]
    assert bits, "usage: reextract_cost73l_det_20261117.py <bit> [<bit> ...]"
    state = json.loads(DET_JSON.read_text()) if DET_JSON.exists() \
        else {"all_byte_identical": True, "bits": [], "details": {}}
    for bit in bits:
        reext = WORK / f"bit{bit}.cert.reext"
        if reext.exists() and str(bit) in state["details"]:
            print(f"bit {bit}: already done, skipping")
            continue
        print(f"re-extracting bit {bit} ...", flush=True)
        extract(bit, reext)
        a = summarize(WORK / f"bit{bit}.cert")
        b = summarize(reext)
        identical = (a["size"] == b["size"] and a["md5"] == b["md5"]
                     and a["rows"] == b["rows"])
        print(f"bit {bit}: size {b['size']} rows {b['rows']} "
              f"md5 {b['md5']} identical={identical}", flush=True)
        state["details"][str(bit)] = {
            "size": b["size"], "rows": b["rows"], "md5": b["md5"],
            "identical": identical}
        if bit not in state["bits"]:
            state["bits"].append(bit)
        state["bits"] = sorted(state["bits"])
        state["all_byte_identical"] = all(
            v["identical"] for v in state["details"].values())
        DET_JSON.write_text(json.dumps(state, indent=1, sort_keys=True) + "\n")
        if not identical:
            sys.exit(f"DETERMINISM FAIL bit {bit}: original {a} vs reext {b}")
    print(json.dumps(state, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
