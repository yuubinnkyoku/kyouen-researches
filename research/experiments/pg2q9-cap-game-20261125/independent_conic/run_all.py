"""Run the whole independent verification suite; write logs and a summary."""
import json
import os
import subprocess
import sys
import time

STEPS = [
    # (script, json, title)
    ("selfcheck_linear.py", "results_selfcheck.json", "Self-check: field / determinant / projectivity machinery"),
    ("task1_board.py", "results_task1.json", "Task 1: board is PG(2,9), coordinate map"),
    ("task2_conic.py", "results_task2.json", "Task 2: C is a conic, uniqueness, one conic orbit"),
    ("task3_orbits.py", "results_task3.json", "Task 3: PGL(2,9) orbits on k-subsets"),
    ("task4_grundy.py", "results_task4.json", "Task 4: Grundy values by upset DP"),
    ("task5_counts.py", "results_task5.json", "Task 5: incidence / distinct cap counts"),
    ("check_parent_reps.py", "results_parent_reps.json", "Extra (informational): parent representative labels"),
]


def main():
    os.makedirs("logs", exist_ok=True)
    summary = []
    total = 0.0
    for script, jsonfile, title in STEPS:
        t0 = time.time()
        proc = subprocess.run([sys.executable, script], capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
        dt = time.time() - t0
        total += dt
        log = os.path.join("logs", script.replace(".py", ".log"))
        with open(log, "w", encoding="utf-8") as fh:
            fh.write(proc.stdout)
            if proc.stderr:
                fh.write("\n--- stderr ---\n")
                fh.write(proc.stderr)
        verdict = None
        if os.path.exists(jsonfile):
            with open(jsonfile, encoding="utf-8") as fh:
                data = json.load(fh)
            verdict = data.get("pass", data.get("all_match"))
        ok = proc.returncode == 0 and (verdict is not False)
        summary.append({"script": script, "log": log, "json": jsonfile,
                        "title": title, "seconds": round(dt, 1),
                        "exit": proc.returncode,
                        "json_verdict": verdict,
                        "pass": ok})
        print("%-24s %7.1fs  exit=%d  pass=%s  (%s)"
              % (script, dt, proc.returncode, ok, verdict))
        if proc.returncode != 0:
            print(proc.stderr[-3000:])
    tasks = [s for s in summary if not s["script"].startswith("check_")]
    with open("results_summary.json", "w", encoding="utf-8") as fh:
        json.dump({"steps": summary, "total_seconds": round(total, 1),
                   "tasks_all_pass": all(s["pass"] for s in tasks),
                   "all_pass": all(s["pass"] for s in summary)}, fh, indent=1)
    print("\ntotal %.1fs, tasks all pass: %s"
          % (total, all(s["pass"] for s in tasks)))


main()
