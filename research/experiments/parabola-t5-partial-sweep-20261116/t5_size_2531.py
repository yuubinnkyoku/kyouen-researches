import os, sys, time
from pathlib import Path
SRC = Path('/home/hatch/workspace/kyouen-omp/full/research/experiments/parabola-p2207-no-equality-witness-20261107')
sys.path.insert(0, str(SRC))
from search_shape_class import build
ROOT = SRC.parents[2]
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen
p = 2531; h = (p-1)//2; size = h-1
t0=time.time()
edges = run_gen(str(Path(os.environ["TEMP"])/"forbidden_edges.exe"), p)
t1=time.time()
clauses, nv, kept = build(p, edges, 1, 1, 3)
t2=time.time()
print(f"p={p} h={h} size={size} edges={len(edges)} gen={t1-t0:.1f}s vars={nv} clauses={len(clauses)} kept={kept} build={t2-t1:.2f}s", flush=True)
