#!/usr/bin/env python3
"""counts_from_run.py <run.txt> <out.json> — parse blocking_duality stdout into JSON."""
import sys, json, re
txt = open(sys.argv[1]).read()
def parse(key):
    m = re.search(key + r"(.+)", txt).group(1).strip()
    return {int(a): int(b) for a, b in (e.split(":") for e in m.split())}
out = {
  "board": re.search(r"board (\S+)", txt).group(1),
  "n": int(re.search(r"n (\d+)", txt).group(1)),
  "l": int(re.search(r" l (\d+)", txt).group(1)),
  "s": int(re.search(r" s (\d+)", txt).group(1)),
  "t": int(re.search(r" t (\d+)", txt).group(1)),
  "maximal_safe": parse("maximal_safe"),
  "minimal_blocking": parse("minimal_blocking"),
  "complement_check_fail": int(re.search(r"complement_check_fail (\d+)", txt).group(1)),
}
json.dump(out, open(sys.argv[2], "w"), indent=1)
print(sys.argv[2], "written")
