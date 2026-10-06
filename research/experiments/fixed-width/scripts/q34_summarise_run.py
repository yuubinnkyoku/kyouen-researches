"""Summarise a q34 exclusion JSONL run and cross-check it against another run."""
import json
import sys


def load(path):
    rows = []
    for line in open(path):
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    rows.sort(key=lambda r: r["m"])
    return rows


def main():
    sound = load(sys.argv[1])
    other_path = sys.argv[2] if len(sys.argv) > 2 else None
    other = load(other_path) if other_path else None

    lengths = [r["m"] for r in sound]
    assert lengths == list(range(min(lengths), max(lengths) + 1)), "gap in lengths"
    print("sound lengths:", len(lengths), "range", min(lengths), "-", max(lengths))
    print("contiguous:", True)
    print("cover_exists true at:", [r["m"] for r in sound if any(r["cover_exists"])])
    print("total candidates tested:",
          sum(sum(r["candidates"]) for r in sound))
    print("lengths where prune1 alone removed everything:",
          [r["m"] for r in sound if not any(r["candidates"])])

    if other is None:
        return
    om = {r["m"]: r for r in other}
    same_verdict, same_cand, differ = [], [], []
    for r in sound:
        o = om.get(r["m"])
        if o is None:
            differ.append((r["m"], "absent"))
            continue
        if list(o["cover_exists"]) == list(r["cover_exists"]):
            same_verdict.append(r["m"])
        if list(o["candidates"]) == list(r["candidates"]):
            same_cand.append(r["m"])
        if list(o["cover_exists"]) != list(r["cover_exists"]):
            differ.append((r["m"], o["cover_exists"], r["cover_exists"]))
    print("common lengths:", len(set(om) & set(lengths)))
    print("identical verdict:", len(same_verdict))
    print("identical candidate counts:", len(same_cand))
    print("verdict differences:", differ)
    extra = {r["m"]: sum(r["candidates"]) - sum(om[r["m"]]["candidates"])
             for r in sound if r["m"] in om}
    print("candidates examined additionally by sound mode (total):", sum(extra.values()))
    print("largest per-length increases:",
          sorted(extra.items(), key=lambda kv: -kv[1])[:6])


if __name__ == "__main__":
    main()