"""Run all independent verification tasks in order.

Usage:  python run_all.py
"""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TASKS = [
    ("task1_board.py", "board construction + parent indexing"),
    ("task2_agl.py", "AGL(2,9) transitivity on triangles"),
    ("task3_cone.py", "cone of F + full Grundy DP + double counting"),
    ("task4_upset.py", "independent Grundy values by full upset DP"),
    ("task5_mex.py", "k<=2 mex chain, global counts k<=5, arithmetic"),
]


def main():
    failed = []
    for script, desc in TASKS:
        print("\n" + "#" * 78)
        print("# running %s : %s" % (script, desc))
        print("#" * 78)
        rc = subprocess.call([sys.executable, str(HERE / script)], cwd=str(HERE))
        if rc != 0:
            failed.append((script, rc))
    print("\n" + "=" * 78)
    if failed:
        print("FAILED:", failed)
        return 1
    print("ALL TASKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
