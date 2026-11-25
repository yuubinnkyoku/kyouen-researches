#!/usr/bin/env python3
"""Build stats.json for the cost73l certificate band from the extraction logs.

Reads the per-bit extraction driver stderr summaries (JSON lines with a "bit"
field) from logs/73l_certE.log, logs/73l_certF.log and logs/73l_cert61.log
(the bit 61 pilot foreground run re-captured), cross-checks each against the
extracted certificate file (size, md5, row count = lines - 2 header lines),
and writes output/class2-lane-cost73l-certificates/stats.json keyed by bit:
{bit: {root, md5, size, rows, nodes, fbt_drops, moves}}.
"""
import hashlib, json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parents[1]
EXP = HERE
WORK = HERE / "output" / "class2-lane-cost73l-certificates"
CHILD = "00000000000000c09002000000400000"
WIN_BITS = [1, 2, 3, 4, 6, 8, 9, 18, 21, 23, 25, 28, 29, 32, 34, 41, 42, 44,
            47, 53, 54, 61, 62, 64, 66, 80, 95, 105, 112, 113, 116, 119]
LOGS = ["logs/73l_certE.log", "logs/73l_certF.log", "logs/73l_cert61.log"]

summaries = {}
for lname in LOGS:
    p = EXP / lname
    if not p.exists():
        continue
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line.startswith("{") or '"bit"' not in line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "bit" in d and "sum" in d:
            summaries[int(d["bit"])] = d

assert sorted(summaries) == sorted(WIN_BITS), (
    sorted(set(WIN_BITS) - set(summaries)), sorted(set(summaries) - set(WIN_BITS)))

stats = {}
for b in WIN_BITS:
    s = summaries[b]
    assert s["fbt_drops"] == 0 and s["fatal"] is None, (b, s)
    root = "%032x" % (int(CHILD, 16) | (1 << b))
    cert = WORK / f"bit{b}.cert"
    data = cert.read_bytes()
    lines = data.decode().splitlines()
    assert lines[0] == "n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS"
    assert lines[1] == f"root {root}", (b, lines[1])
    rows = len(lines) - 2
    assert rows == s["nRows"], (b, rows, s["nRows"])
    assert len(data) == sum(len(l) + 1 for l in lines), b
    pm = s["perMove"]
    assert all(v["ok"] is True and v["capped"] is False for v in pm.values()), b
    assert sum(v["nodes"] for v in pm.values()) == s["sum"], b
    assert len(pm) == s["moves"], b
    stats[str(b)] = {
        "root": root,
        "md5": hashlib.md5(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
        "rows": rows,
        "nodes": s["sum"],
        "fbt_drops": s["fbt_drops"],
        "moves": s["moves"],
    }

out = WORK / "stats.json"
out.write_text(json.dumps(stats, indent=1, sort_keys=True) + "\n")
print(f"wrote {out} ({out.stat().st_size} bytes)")
print("bits:", len(stats), "total rows:", sum(v["rows"] for v in stats.values()),
      "total nodes:", sum(v["nodes"] for v in stats.values()),
      "total bytes:", sum(v["size"] for v in stats.values()))
