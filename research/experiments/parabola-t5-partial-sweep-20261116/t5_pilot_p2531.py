import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path('/home/hatch/workspace/kyouen-omp/full/research/experiments/parabola-p2207-no-equality-witness-20261107')
sys.path.insert(0, str(SRC))
from search_shape_class import build
ROOT = SRC.parents[2]
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen

P, X, C, E = 2531, 1, 1, 3
h = (P - 1) // 2

def vv(pair, kind):
    return 4 * pair - 4 + {"B": 1, "N": 2, "L": 3, "H": 4}[kind]

def decode(model, p, h, x):
    pos = {i for i in model if i > 0}
    chosen = {0} if x else set()
    for i in range(1, h + 1):
        if vv(i, "B") in pos:
            chosen.update({i, p - i})
        elif vv(i, "L") in pos:
            chosen.add(i)
        elif vv(i, "H") in pos:
            chosen.add(p - i)
    return sorted(chosen)

if __name__ == "__main__":
    import time
    from pysat.solvers import Cadical195
    out = Path(sys.argv[1]); out.parent.mkdir(parents=True, exist_ok=True)
    ds = sorted(int(s) for s in sys.argv[2].split(','))
    BUDGET = 100_000
    gen = str(Path(__import__('os').environ['TEMP']) / 'forbidden_edges.exe')
    t0 = time.time()
    edges = run_gen(gen, P)
    edge_sets = [frozenset(q) for q in edges]
    clauses, nv, kept = build(P, edges, X, C, E)
    print(f"p={P} h={h} edges={len(edges)} vars={nv} clauses={len(clauses)} kept={kept} build={time.time()-t0:.1f}s", flush=True)
    doc = {"p": P, "h": h, "class": [X, C, E], "budget": BUDGET, "mode": "fresh-each",
           "vars": nv, "clauses": len(clauses), "kept_edges": kept, "records": []}
    def flush():
        out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8", newline="\n")
    flush()
    for d in ds:
        s = Cadical195(bootstrap_with=clauses)
        s.conf_budget(BUDGET)
        t1 = time.time()
        res = s.solve_limited(assumptions=[vv(d, "B")])
        dt = time.time() - t1
        rec = {"d": d, "k": h - d, "sat": res, "unknown": res is None,
               "seconds": round(dt, 3), "conflicts": s.accum_stats()["conflicts"]}
        if res:
            chosen = decode(s.get_model(), P, h, X)
            cs = frozenset(chosen)
            rec.update({"witness_size": len(chosen),
                        "safe_against_edges": not any(q <= cs for q in edge_sets),
                        "points": chosen})
        doc["records"].append(rec); flush()
        print(f"  d={d} k={rec['k']} sat={res} secs={dt:.3f} conf={rec['conflicts']}", flush=True)
        if res:
            print(f"    witness_size={rec.get('witness_size')} safe={rec.get('safe_against_edges')}", flush=True)
        s.delete()
    print(f"wrote {out} ({len(doc['records'])})", flush=True)
