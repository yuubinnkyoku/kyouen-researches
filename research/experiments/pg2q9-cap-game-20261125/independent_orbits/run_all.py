"""run_all.py -- reproduce the whole independent verification, in order.

    python run_all.py

Total runtime is dominated by the BFS orbit of the 8-cap (~3.5 min); everything
else takes well under a minute.  Each step writes its own results/*.json.
"""

from __future__ import annotations

import subprocess
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
STEPS = [
    ["task1_caps.py"],
    ["task2_model_iso.py"],
    ["task3_orbits.py", "6", "7", "8", "10"],
    ["task4_second_caps.py"],
    ["task5_stabilizers.py"],
    ["extra_checks.py"],
]

for step in STEPS:
    print("=" * 78)
    print("RUN: python " + " ".join(step), flush=True)
    print("=" * 78, flush=True)
    r = subprocess.run([sys.executable] + step, cwd=HERE)
    if r.returncode != 0:
        print(f"STEP FAILED (exit {r.returncode}): {' '.join(step)}")
        sys.exit(r.returncode)
print("\nAll steps completed.")
