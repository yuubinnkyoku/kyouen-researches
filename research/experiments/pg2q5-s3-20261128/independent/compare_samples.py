#!/usr/bin/env python3
"""Compare the Python full-upset DP samples with the independent C values."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    with open(os.path.join(HERE, "out", "samples.json"), encoding="utf-8") as f:
        samples = json.load(f)
    probed = {}
    with open(os.path.join(HERE, "out", "indep_probe_run.txt"),
              encoding="utf-8") as f:
        for line in f:
            t = line.split()
            if t and t[0] == "PROBE4":
                probed[int(t[1])] = int(t[2])

    bad = []
    for s in samples:
        c = probed.get(s["mask"])
        if c != s["grundy"]:
            bad.append((s["size"], s["mask"], s["grundy"], c))
    from collections import Counter
    per_size = Counter(s["size"] for s in samples)
    res = {
        "samples": len(samples),
        "per_size": dict(sorted(per_size.items())),
        "mismatches": bad,
        "size4_samples": sum(1 for s in samples if s["size"] == 4),
        "size4_all_g2": all(s["grundy"] == 2
                            for s in samples if s["size"] == 4),
    }
    with open(os.path.join(HERE, "out", "sample_check.json"), "w",
              encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1))
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
