#!/usr/bin/env python3
"""All 2^20 pure-three-point clutters on six labeled vertices."""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
import time
import argparse
import hashlib

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107'))
from engine import canonical


def core_lookup():
    table = json.loads((ROOT / 'research/experiments/rooted-core-tail-periodicity-20261107/output/audit.json').read_text(encoding='utf-8'))
    values = {(row['n'], tuple(row['forbidden'])): row['prefix'][0] for row in table['records']}
    pairs = [sum(1 << i for i in edge) for edge in combinations(range(5), 2)]
    triples = [sum(1 << i for i in edge) for edge in combinations(range(5), 3)]
    canonical_g = {}
    masks = []
    for p in range(1024):
        selected = [edge for i, edge in enumerate(pairs) if p >> i & 1]
        allowed = sum(1 << j for j, triple in enumerate(triples)
                      if not any(edge & triple == edge for edge in selected))
        masks.append(allowed)
        for t in range(1024):
            effective = t & allowed
            code = p | (effective << 10)
            if code not in canonical_g:
                family = tuple(sorted(selected + [edge for i, edge in enumerate(triples) if effective >> i & 1]))
                canonical_g[code] = values[canonical(5, family)]
    assert len(canonical_g) == 6212
    result = bytearray(1 << 20)
    for code in range(1 << 20):
        p = code & 1023
        result[code] = canonical_g[p | (((code >> 10) & masks[p]) << 10)]
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--values-out',type=Path)
    args=parser.parse_args()
    started = time.monotonic()
    child = core_lookup()
    triples = list(combinations(range(6), 3))
    smaller_pairs = list(combinations(range(5), 2))
    smaller_triples = list(combinations(range(5), 3))
    low, high = [], []
    for vertex in range(6):
        remaining = [v for v in range(6) if v != vertex]
        relabel = {v: i for i, v in enumerate(remaining)}
        bit_images = []
        for triple in triples:
            members = tuple(relabel[v] for v in triple if v != vertex)
            index = smaller_pairs.index(members) if len(members) == 2 else 10 + smaller_triples.index(members)
            bit_images.append(1 << index)
        chunks = []
        for offset in (0, 10):
            array = [0] * 1024
            for mask in range(1, 1024):
                bit = mask & -mask
                array[mask] = array[mask ^ bit] | bit_images[offset + bit.bit_length() - 1]
            chunks.append(array)
        low.append(chunks[0]); high.append(chunks[1])
    mex = [next(g for g in range(7) if not mask >> g & 1) for mask in range(64)]
    counts = Counter()
    by_edges = Counter()
    root_values = bytearray(1 << 20)
    first = {}
    for family in range(1 << 20):
        lower, upper = family & 1023, family >> 10
        options = 0
        children = []
        for vertex in range(6):
            g = child[low[vertex][lower] | high[vertex][upper]]
            children.append(g)
            options |= 1 << g
        value = mex[options]
        root_values[family] = value
        counts[value] += 1
        by_edges[(value,family.bit_count())] += 1
        first.setdefault(value, dict(family_mask=family,
                                    triples=[triples[j] for j in range(20) if family >> j & 1],
                                    child_grundy=children))
    output = dict(scope='all 1048576 labeled 3-uniform hypergraphs on six points',
                  histogram=dict(sorted(counts.items())), maximum=max(counts),
                  by_edge_count={str(g):{str(e):count for (v,e),count in sorted(by_edges.items()) if v==g} for g in sorted(counts)},
                  values_sha256=hashlib.sha256(root_values).hexdigest(),
                  first_witnesses=first)
    if args.values_out is not None:
        args.values_out.write_bytes(root_values)
    target=Path(__file__).with_name('output')/'six_census.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:value for key,value in output.items() if key not in {'by_edge_count','first_witnesses'}},indent=2),flush=True)


if __name__=='__main__':
    main()
