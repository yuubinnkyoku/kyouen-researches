"""Run every independent verification script and store the logs.

Usage (from anywhere):
    python run_all.py

Each script is run in a fresh interpreter; its stdout+stderr is written to
logs/<name>.txt and echoed to the console summary.
"""

from __future__ import annotations

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "logs")

SCRIPTS = [
    ("task1_board.py", "TASK 1  board is PG(2,8), ordering = sorted canonical vectors"),
    ("task2_conic.py", "TASK 2  5-cap and the unique conic through it"),
    ("task3_pgl.py", "TASK 3  PGL(2,8), conic parameterisation, k-subset orbits"),
    ("task4_grundy.py", "TASK 4  Grundy values of the conic k-caps (k=3..8)"),
    ("task5_parity.py", "TASK 5  parity-theorem consequence"),
    ("supplement_census.py", "SUPP  S1 global cap census / hyperoval count"),
]


def main():
    os.makedirs(LOGS, exist_ok=True)
    results = []
    for script, title in SCRIPTS:
        path = os.path.join(HERE, script)
        proc = subprocess.run(
            [sys.executable, path],
            cwd=HERE,
            capture_output=True,
            text=True,
        )
        out = proc.stdout + (("\n[stderr]\n" + proc.stderr) if proc.stderr.strip() else "")
        logname = os.path.join(LOGS, script.replace(".py", ".txt"))
        with open(logname, "w", encoding="utf-8") as fh:
            fh.write(out)
        results.append((script, proc.returncode, logname, title))
        print(f"{title:62s} exit={proc.returncode}  log={os.path.relpath(logname, HERE)}")

    print("\n" + "=" * 78)
    all_ok = True
    for script, rc, logname, title in results:
        last = ""
        with open(logname, encoding="utf-8") as fh:
            for line in fh:
                if line.startswith(("TASK ", "SUPPLEMENT ")):
                    last = line.strip()
        status = "PASS" if rc == 0 else "FAIL"
        all_ok = all_ok and rc == 0
        print(f"  {script:24s} {status}   [{last}]")
    print("=" * 78)
    print("OVERALL:", "ALL PASS" if all_ok else "FAILURES PRESENT")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
