"""Run every task in order and write a single log.

    python run_all.py           # ~2 minutes
"""
import contextlib
import io
import json
import sys
import time

import core
import task2_counts
import task3_orbits
import task4_grundy
import task5_observations
import bonus_census
import genset_check


def section(buf, title, fn):
    buf.write("\n" + "=" * 78 + "\n" + title + "\n" + "=" * 78 + "\n")
    t = time.time()
    with contextlib.redirect_stdout(buf):
        fn()
    buf.write("[section time %.1fs]\n" % (time.time() - t))


def main():
    buf = io.StringIO()
    t0 = time.time()
    buf.write("independent_small / run_all.py  (python %s)\n" % sys.version.split()[0])
    buf.write(time.strftime("run started %Y-%m-%dT%H:%M:%S\n"))
    buf.write("board: ../output/board_pg2q9.txt\n")

    buf.write("\n" + "=" * 78 + "\nTASK 1  board is PG(2,9)\n" + "=" * 78 + "\n")
    res1 = core.check_board()
    buf.write(json.dumps(res1, indent=1) + "\n")

    section(buf, "TASK 2  3-caps and 4-caps (independent enumeration)",
            task2_counts.main)
    section(buf, "TASK 3  PGL(3,9), |G|, orbits, stabilizers",
            task3_orbits.main)
    section(buf, "TASK 4  Grundy values and upsets", task4_grundy.main)
    section(buf, "TASK 5  observations", task5_observations.main)
    section(buf, "BONUS  census layer / reference consistency",
            bonus_census.main)
    section(buf, "BONUS  which generator sets generate PGL(3,9)",
            genset_check.main)

    buf.write("\ntotal time %.1fs\n" % (time.time() - t0))
    text = buf.getvalue()
    with open("run_all.log", "w", encoding="utf-8") as fh:
        fh.write(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
