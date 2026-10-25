"""Exact rooted six-section aggregation through dimension nine.

Optionally pass output logs from the independent integer and prime C++ checkers
as two positional arguments to cross-check every support count.
"""
import argparse
import re
from math import comb, factorial
from pathlib import Path

H = (0, 0, 0, 0, 75, 75, 2877, 44437, 480895, 3220820)
EXPECTED = {4: 40, 5: 1200, 6: 206528, 7: 47884928,
            8: 9324142464, 9: 1405033324800}


def stirling(n: int, k: int) -> int:
    dp = [1] + [0] * k
    for _ in range(n):
        nxt = [0] * (k + 1)
        for j in range(1, k + 1):
            nxt[j] = dp[j - 1] + j * dp[j]
        dp = nxt
    return dp[k]


def count(d: int) -> tuple[int, int, int]:
    ordered_rooted = sum(H[k] * factorial(k) * stirling(d, k)
                         for k in range(min(d, len(H) - 1) + 1))
    numerator = (1 << d) * ordered_rooted
    assert numerator % factorial(6) == 0
    e = numerator // factorial(6)
    assert (6 * e) % (1 << d) == 0
    rooted = 6 * e // (1 << d)
    return ordered_rooted, rooted, e


def parse_log(path: Path) -> tuple[int, ...]:
    lines = path.read_text(encoding="utf-8").splitlines()
    out = {}
    for line in lines:
        km = re.search(r"\bk=(\d+)\b", line)
        visited = re.search(r"\b(?:total|visited)=(\d+)\b", line)
        valid = re.search(r"\b(?:valid|good)=(\d+)\b", line)
        if km and visited and valid:
            k = int(km.group(1))
            assert int(visited.group(1)) == comb(32, k), (path, line)
            assert k not in out, (path, k)
            out[k] = int(valid.group(1))
    assert sorted(out) == list(range(10)), (path, sorted(out))
    return tuple(out[k] for k in range(10))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("logs", nargs="*", type=Path,
                        help="optional integer and prime checker output logs")
    args = parser.parse_args()
    assert len(args.logs) in (0, 2)
    for path in args.logs:
        assert parse_log(path) == H, path
    assert sum(comb(32, k) for k in range(10)) == 43081973
    for d, expected in EXPECTED.items():
        ordered, rooted, actual = count(d)
        assert actual == expected, (d, actual, expected)
        v2 = (actual & -actual).bit_length() - 1
        print(f"d={d} ordered_rooted={ordered} rooted={rooted} "
              f"E={actual} v2={v2}")


if __name__ == "__main__":
    main()
