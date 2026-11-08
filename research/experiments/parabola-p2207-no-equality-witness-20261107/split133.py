import sys, time
sys.path.insert(0, "../parabola-equality-extension-2143-2500-20261107")
from probe_driver import run_gen
from search_shape_class import build
from pysat.solvers import Cadical195
p = 2647
edges = run_gen(r"D:\tmp\forbidden_edges.exe", p)
clauses, nv, kept = build(p, edges, 1, 1, 3)
print("class (1,1,3): vars", nv, "clauses", len(clauses), flush=True)
for attempt in range(6):
    s = Cadical195(bootstrap_with=clauses)
    s.conf_budget(300_000 + attempt * 200_000)
    t0 = time.time()
    res = s.solve_limited()
    dt = time.time() - t0
    model = s.get_model() if res else None
    s.delete()
    print(f"attempt {attempt}: budget={300_000 + attempt*200_000} res={res} secs={dt:.1f}", flush=True)
    if res:
        pos = {i for i in model if i > 0}
        chosen = {0}
        for i in range(1, (p-1)//2 + 1):
            B, N, L, H = 4*i-3, 4*i-2, 4*i-1, 4*i
            if B in pos: chosen.update({i, p-i})
            elif L in pos: chosen.add(i)
            elif H in pos: chosen.add(p-i)
        chosen = sorted(chosen)
        safe = not any(set(q) <= set(chosen) for q in edges)
        print("  witness size", len(chosen), "safe", safe, flush=True)
        break
