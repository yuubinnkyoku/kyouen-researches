"""Extracts the frontier records: the maximum-m verified witness per d.

Input witnesses.txt (as built by collect_witnesses.py), output frontier.txt
in the same record format.  Every smaller safe size is implied by the
frontier witness because affine general position is hereditary downward:
any (d+1)-subset of a subset is a (d+1)-subset of the whole witness.
"""
import sys


def read_records(path):
    records = {}
    with open(path) as fh:
        tokens = fh.read().split()
    i = 0
    while i < len(tokens):
        d, m = int(tokens[i]), int(tokens[i + 1])
        i += 2
        points = [int(x) for x in tokens[i:i + m]]
        i += m
        if d not in records or m > records[d][0]:
            records[d] = (m, points)
    return records


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "witnesses.txt"
    dst = sys.argv[2] if len(sys.argv) > 2 else "frontier.txt"
    records = read_records(src)
    with open(dst, "w") as out:
        for d in sorted(records):
            m, points = records[d]
            out.write(f"{d} {m}\n")
            out.write(" ".join(str(x) for x in points) + "\n")
            print(f"d={d} max_m={m} excess={m - d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
