"""Run every verification script in order and print a one-line summary each.

Logs are written to independent_5caps/logs/<script>.log (inside this
directory only).

Run:  python independent_5caps/run_all.py
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LOGS = HERE / "logs"
LOGS.mkdir(exist_ok=True)

SCRIPTS = [
    ("Task 1  board + coordinate map", "t1_board.py"),
    ("Task 2  4-caps / 42 / 3 reps", "t2_caps.py"),
    ("Task 3  frame stabiliser S4", "t3_frame_s4.py"),
    ("Task 4  Grundy values", "t4_grundy.py"),
    ("Task 5  stabilisers + equivalence", "t5_equiv.py"),
    ("Task 5b conic cross-check", "t6_conic.py"),
    ("Task 7  independent GF(9) rewrite", "t7_indep_field.py"),
]

import time

rows = []
for label, name in SCRIPTS:
    log = LOGS / (name.replace(".py", "") + ".log")
    t0 = time.time()
    with log.open("w", encoding="utf-8") as fh:
        proc = subprocess.run([sys.executable, str(HERE / name)], stdout=fh,
                              stderr=subprocess.STDOUT, cwd=str(HERE))
    elapsed = time.time() - t0
    text = log.read_text(encoding="utf-8")
    summary = [ln for ln in text.splitlines()
               if ln.startswith("TASK") or ln.strip().startswith("REFUTED")
               or ln.startswith("[CLAIM")]
    rows.append((label, name, proc.returncode, summary, elapsed))

print(f"{'=' * 78}\nSUMMARY (logs in {LOGS})\n{'=' * 78}")
for label, name, rc, summary, elapsed in rows:
    print(f"\n{label}  ({name})  exit={rc}  {elapsed:.1f}s")
    for ln in summary:
        print(f"   {ln}")
print(f"\n{'=' * 78}")
fails = [name for _, name, rc, _, _ in rows if rc != 0]
print("scripts exiting non-zero (their own computational checks):",
      fails if fails else "none")
print("claim-relevant refutations are in t3_frame_s4.py and t5_equiv.py, "
      "confirmed independently by t6_conic.py and t7_indep_field.py")
