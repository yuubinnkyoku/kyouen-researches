"""Run the complete independent verification from scratch.

Usage (from this directory):
    python run_all.py

Python standard library only; the C census is compiled with the system gcc.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def run(args, capture=False):
    print("\n$ " + " ".join(args), flush=True)
    if capture:
        out = subprocess.check_output(args, cwd=HERE, text=True)
        print(out, end="", flush=True)
        return out
    subprocess.run(args, cwd=HERE, check=True)
    return None


def main():
    run([PY, "common.py"])
    run([PY, "group.py"])
    run([PY, "task1_board.py"])
    run([PY, "reps.py"])
    run([PY, "task2_group.py"])
    run([PY, "bfs.py"])
    run([PY, "task3_orbits.py"])
    run([PY, "task3b_pgammal_bfs.py"])
    # C census (compiled here, in this directory)
    run(["gcc", "-O2", "-o", "cap_census.exe", "cap_census.c"])
    out = run([os.path.join(HERE, "cap_census.exe"),
               os.path.join(HERE, "..", "output", "board_pg2q8.txt")],
              capture=True)
    with open(os.path.join(HERE, "census_output.txt"), "w",
              encoding="utf-8") as f:
        f.write(out)
    run([PY, "task45_analysis.py"])
    print("\nALL SCRIPTS COMPLETED")


if __name__ == "__main__":
    main()
