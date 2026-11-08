import sys, time
sys.path.insert(0, "../parabola-equality-extension-2143-2500-20261107")
from probe_driver import run_gen
from search_shape_class import build
from pysat.solvers import Glucose4, Minisat22
p, size = 2647, 1322
h = (p - 1) // 2
edges = run_gen(r"D:\tmp\forbidden_edges.exe", p)
clauses, nv, kept = build(p, edges, 1, 1, 3)
print("class (1,1,3): vars", nv, "clauses", len(clauses), "kept", kept, flush=True)
for cls in (Glucose4, Minisat22):
    s = cls(bootstrap_with=clauses)
    s.conf_budget(5_000_000)
    t0 = time.time()
    res = s.solve_limited()
    print(cls.__name__, "res", res, "secs", round(time.time()-t0, 1), flush=True)
    s.delete()
