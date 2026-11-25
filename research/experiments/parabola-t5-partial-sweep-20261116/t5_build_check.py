import os, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
SRC = Path('/home/hatch/workspace/kyouen-omp/full/research/experiments/parabola-p2207-no-equality-witness-20261107')
sys.path.insert(0, str(SRC))
from search_shape_class import build
ROOT = SRC.parents[2]
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen
p, h = 2207, 1103
size = h - 1  # 1102, class (1,1,3)
t0 = time.time()
gen = str(Path(os.environ["TEMP"]) / "forbidden_edges.exe")
edges = run_gen(gen, p)
t1 = time.time()
print(f"edges={len(edges)} gen={t1-t0:.2f}s", flush=True)
clauses, nv, kept = build(p, edges, 1, 1, 3)
t2 = time.time()
print(f"class(1,1,3) size={size} vars={nv} clauses={len(clauses)} kept={kept} build={t2-t1:.2f}s", flush=True)
