"""Collects every successful witness into witnesses.txt.

Sources, in this order:
  - wit_d*.txt records written directly by search.cpp (probe waves)
  - wit_x*.txt records written directly by search.cpp (targeted waves)
  - JSON status lines with ok:true in probe_logs*/ logs (covers runs whose
    output file was /dev/null; the witness list in the status line is the
    same list the program would have appended)

Records are deduplicated exactly and sorted by (d, m).  The output is the
input for both verifiers.
"""
import glob
import json
import sys


def read_records(path):
    records = []
    with open(path) as fh:
        tokens = fh.read().split()
    i = 0
    while i < len(tokens):
        d, m = int(tokens[i]), int(tokens[i + 1])
        i += 2
        points = [int(x) for x in tokens[i:i + m]]
        i += m
        records.append((d, m, tuple(points)))
    return records


def main():
    records = set()
    for pattern in ("wit_d*.txt", "wit_x*.txt"):
        for path in sorted(glob.glob(pattern)):
            records.update(read_records(path))
    for path in sorted(glob.glob("probe_logs*/*.log")):
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if not line.startswith("{"):
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if obj.get("ok") and "witness" in obj:
                    records.add((obj["d"], obj["m"], tuple(obj["witness"])))
    ordered = sorted(records)
    with open("witnesses.txt", "w") as out:
        for d, m, points in ordered:
            out.write(f"{d} {m}\n")
            out.write(" ".join(str(x) for x in points) + "\n")
    print(f"wrote {len(ordered)} records "
          f"({len({(d, m) for d, m, _ in ordered})} distinct (d,m) pairs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
