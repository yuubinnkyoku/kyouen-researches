#!/usr/bin/env python3
"""Verify that the appendix table embedded in REPORT.md equals out/samples_table.md."""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
tab = [l.rstrip() for l in open(os.path.join(HERE, "out", "samples_table.md")) if l.startswith("|")]
rep = open(os.path.join(HERE, "REPORT.md")).read().splitlines()
start = next(i for i, l in enumerate(rep) if l.startswith("## Appendix"))
appendix = [l.rstrip() for l in rep[start:] if re.match(r"\|\s*(9|10|11|12|13)\s*\|", l)]
body = [l for l in tab if re.match(r"\|\s*(9|10|11|12|13)\s*\|", l)]


def norm(s):
    return (s.replace("non-dodecad", "nondodecad")
             .replace("non-maximal", "nonmaximal").strip())


print("report appendix rows:", len(appendix), " table rows:", len(body))
if [norm(x) for x in appendix] == [norm(x) for x in body]:
    print("MATCH")
else:
    for a, b in zip(appendix, body):
        if norm(a) != norm(b):
            print("DIFF\n  report:", norm(a), "\n  table :", norm(b))
