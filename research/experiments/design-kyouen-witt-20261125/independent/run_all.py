"""Run all independent verifications in order.

    python independent/run_all.py

Writes JSON results into independent/out/ and prints the tables.
"""
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = ["verify_designs.py", "verify_k3_graded.py", "verify_grundy.py",
           "verify_k4.py"]

if __name__ == "__main__":
    env = dict(os.environ)
    env["PYTHONPATH"] = HERE + os.pathsep + env.get("PYTHONPATH", "")
    rc = 0
    for s in SCRIPTS:
        print("\n" + "#" * 80, flush=True)
        print("#", s, flush=True)
        print("#" * 80, flush=True)
        p = subprocess.run([sys.executable, os.path.join(HERE, s)], cwd=HERE, env=env)
        rc = rc or p.returncode
    sys.exit(rc)
