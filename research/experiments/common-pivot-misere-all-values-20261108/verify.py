#!/usr/bin/env python3
"""Mutual cograph recursion with arbitrary binary-restriction nimber."""
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]


def mex(values):
    answer = 0
    while answer in values:
        answer += 1
    return answer


@lru_cache(None)
def graph(m, a):
    if m == 0:
        return (0, ()) if a else (6, (3, 6, 24, 48))
    blocks = [graph(j, 1-a) for j in range(m)]
    sizes = [n+1 for n, edges in blocks]
    edges = []; offset = 0
    for (n, inner), size in zip(blocks, sizes):
        edges.extend(edge << offset for edge in inner)
        edges.extend((1 << u) | (1 << v) for u in range(offset) for v in range(offset, offset+size))
        offset += size
    assert len(edges) == len(set(edges))
    return offset, tuple(sorted(edges))


def audit_graph(n, edges):
    closed = [1 << v for v in range(n)]
    for edge in edges:
        low = edge & -edge; u = low.bit_length()-1; v = (edge ^ low).bit_length()-1
        closed[u] |= 1 << v; closed[v] |= 1 << u
    visited = set()

    @lru_cache(None)
    def game(active, free):
        visited.add(active)
        children = [game(active & ~closed[v], free) for v in range(n) if active >> v & 1]
        if free:
            children.append(game(active, free-1))
        g = mex({row[0] for row in children})
        h = mex({row[1] for row in children}) if children else 1
        t = mex({row[2] for row in children if row[1] < 2}) if h < 2 else None
        return g, h, t

    full = (1 << n)-1
    roots = [game(full, free) for free in range(3)]
    for active in list(visited):
        zero, one, two = [game(active, free) for free in range(3)]
        assert zero == two
        if zero[1] < 2:
            assert one[1] == 1-zero[1] and one[2] == zero[2] ^ 1
        else:
            assert one[1] >= 2
    option_t = sorted({game(full & ~closed[v], 0)[2] for v in range(n)
                       if game(full & ~closed[v], 0)[1] < 2})
    option_g = sorted({game(full & ~closed[v], 0)[0] for v in range(n)})
    return dict(roots=roots, restricted_option_values=option_t, normal_option_values=option_g,
                active_residuals=len(visited), evaluated_states=game.cache_info().currsize)


def paired(n, edges, a):
    # Ensure outside parity 1-a, activating the exact pivot transform.
    poison = 1 if (n+1) % 2 == 1-a else 2
    forbidden = tuple([1 | 1 << (n+1+j) for j in range(poison)] + [1 | edge << 1 for edge in edges])
    return n+1+poison, forbidden, poison


def main():
    directory = Path(__file__).resolve().parent
    graph_records = []; paired_records = []; raw_cases = []
    for m in range(7):
        for a in (0, 1):
            n, edges = graph(m, a)
            row = audit_graph(n, edges)
            assert row['roots'][0][1:] == (a, m)
            assert row['restricted_option_values'] == list(range(m))
            if m >= 2:
                assert n == 5*(1 << (m-1))-1
                assert row['roots'][0][0] == m+2
                assert row['normal_option_values'] == list(range(m+2))
            if m >= 3:
                assert len(edges) == 5*(1 << (m-2))*(5*(1 << (m-1))-m-5)
            row.update(m=m, auxiliary=a, n=n, edge_count=len(edges))
            graph_records.append(row)
            legal, forbidden, poison = paired(n, edges, a)
            g_after = row['roots'][0][0]
            normal = (2 if g_after == 0 else 0) if (legal-1)%2 == 0 else (3 if g_after == 1 else 1)
            paired_records.append(dict(m=m, auxiliary=m+2, normal=normal, legal_points=legal,
                                       poison_points=poison, triple_edges=len(edges), link_auxiliary=a))
            if m <= 2:
                raw_cases.extend([(n, edges, row['roots'][0][0], a),
                                  (n+1, edges, row['roots'][1][0], row['roots'][1][1]),
                                  (legal, forbidden, normal, m+2)])
            print(dict(m=m, a=a, n=n, states=row['evaluated_states'], paired_aux=m+2), flush=True)
    compiler = shutil.which('g++')
    if not compiler:
        raise SystemExit('g++ is required')
    with tempfile.TemporaryDirectory(prefix='kyouen-misere-all-values-') as scratch:
        temp = Path(scratch).resolve(); assert temp.parent == Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt'; exe=temp/'verify.exe'; values=temp/'values.bin'; metadata=temp/'raw.json'
        data.write_text(str(len(raw_cases))+'\n'+'\n'.join(' '.join(map(str,[n,len(edges),*edges])) for n,edges,g,h in raw_cases)+'\n', encoding='ascii')
        cpp=ROOT/'research/experiments/common-pivot-misere-bound-20261108/independent.cpp'
        subprocess.run([compiler,'-std=c++17','-O3',str(cpp),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(data),str(values),str(metadata)],check=True)
        assert values.read_bytes() == bytes(value for n,edges,g,h in raw_cases for value in (g,h))
        native=json.loads(metadata.read_text())
    output=dict(audit='PASS',graph_audits=graph_records,paired_audits=paired_records,
                cpp_cases=len(raw_cases),cpp_safe_states=native['safe_states'],
                infinite_claim='For every m>=0 and a in {0,1}, h(G_m^a)=a and t(G_m^a)=m; paired pivot h=m+2.',
                limitation='Infinite statement is proved by mutual induction; this finite audit alone is not the proof.')
    target=directory/'output/audit.json';target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k not in ('graph_audits','paired_audits')},indent=2),flush=True)


if __name__ == '__main__':
    main()
