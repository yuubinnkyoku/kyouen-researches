"""Prevent withdrawn cache ancestry from silently re-entering a current union.

Raw exact replays are evaluated separately; this filter only applies to cache
rows. Rehabilitation requires explicit, hash-bound proof and registry update.
The registry is proof-critical: absence or corruption must fail closed.
"""
import json
from pathlib import Path


def reject_duplicate_json_keys(pairs):
    """Reject ambiguous JSON objects instead of accepting the last duplicate value."""
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f'duplicate JSON key: {key}')
        obj[key] = value
    return obj


def is_canonical_safe_s5_key(pair):
    """Return whether a five-stone key is D4-canonical and quadruple-free."""
    if not isinstance(pair, (tuple, list)) or len(pair) != 2:
        return False
    lo, hi = pair
    if (type(lo) is not int or type(hi) is not int
            or not (0 <= lo < 2**64 and 0 <= hi < 2**57)
            or lo.bit_count() + hi.bit_count() != 5):
        return False

    points = [i for i in range(121)
              if ((lo if i < 64 else hi) >> (i % 64)) & 1]
    if len(points) != 5:
        return False

    masks = []
    for reflection in (False, True):
        for rotation in range(4):
            mask = 0
            for p in points:
                x, y = p % 11, p // 11
                if reflection:
                    x = 10 - x
                for _ in range(rotation):
                    x, y = y, 10 - x
                mask |= 1 << (11 * y + x)
            masks.append((mask & ((1 << 64) - 1), mask >> 64))
    if (lo, hi) != min(masks, key=lambda k: (k[1], k[0])):
        return False

    from itertools import combinations
    for four in combinations(points, 4):
        coords = [(v % 11, v // 11) for v in four]
        x0, y0 = coords[-1]
        a, b, c = [((x*x + y*y) - (x0*x0 + y0*y0),
                    x-x0, y-y0) for x, y in coords[:-1]]
        det = (a[0]*(b[1]*c[2]-b[2]*c[1])
               - a[1]*(b[0]*c[2]-b[2]*c[0])
               + a[2]*(b[0]*c[1]-b[1]*c[0]))
        if det == 0:
            return False
    return True


ROOT = Path(__file__).resolve().parents[4]
REGISTRY = ROOT / 'results/n11-s5-evidence-quarantine.json'


def quarantined_cache_keys():
    try:
        doc = json.loads(REGISTRY.read_text(encoding='utf-8'),\n                       object_pairs_hook=reject_duplicate_json_keys)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f'required S5 evidence quarantine registry missing: {REGISTRY}') from exc
    if doc.get('schema') != 'n11-s5-evidence-quarantine-v1':
        raise ValueError('invalid S5 quarantine registry schema')
    entries = doc.get('entries')
    if not isinstance(entries, list):
        raise ValueError('invalid S5 quarantine entries')
    seen = set()
    quarantine = set()
    for row in entries:
        if not isinstance(row, dict):
            raise ValueError('invalid S5 quarantine row')
        key = row.get('key')
        if (not isinstance(key, list) or len(key) != 2
                or any(type(x) is not int for x in key)
                or not (0 <= key[0] < 2**64 and 0 <= key[1] < 2**57)
                or key[0].bit_count() + key[1].bit_count() != 5):
            raise ValueError(f'invalid S5 quarantine key: {key}')
        pair = tuple(key)
        if not is_canonical_safe_s5_key(pair):
            raise ValueError(f'noncanonical or unsafe S5 quarantine key: {pair}')
        if pair in seen:
            raise ValueError(f'duplicate S5 quarantine key: {pair}')
        seen.add(pair)
        if type(row.get('active')) is not bool:
            raise ValueError(f'invalid S5 quarantine active flag: {pair}')
        if type(row.get('unsupported_verdict')) is not int or row['unsupported_verdict'] not in (1, 2):
            raise ValueError(f'invalid S5 quarantine verdict: {pair}')
        if row['active']:
            quarantine.add(pair)
    return quarantine
