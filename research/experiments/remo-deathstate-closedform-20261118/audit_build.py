#!/usr/bin/env python3
"""Build the audit artifact output/deathstate_audit.json.

Runs deathstate_verify.py's run_checks() once in-process, then executes
deathstate_verify.py as a cold subprocess twice and requires byte
identical stdout (each cold run itself verifies in-process determinism
by calling run_checks() twice). Writes the verified JSON to
output/deathstate_audit.json and prints its sha256.
"""

import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output", "deathstate_audit.json")


def main():
    sys.path.insert(0, HERE)
    import deathstate_verify as dv

    r = dv.run_checks()
    if not r["all_ok"]:
        print("FATAL: in-process run_checks reported violations",
              file=sys.stderr)
        sys.exit(1)
    canon_r = dv.canon(r).encode("utf-8")

    outs = []
    for _ in range(2):
        p = subprocess.run(
            [sys.executable,
             os.path.join(HERE, "deathstate_verify.py")],
            capture_output=True, check=True)
        outs.append(p.stdout)
    if outs[0] != outs[1]:
        print("FATAL: cold runs differ", file=sys.stderr)
        sys.exit(1)
    if canon_r != outs[0]:
        print("FATAL: in-process and cold outputs differ", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write(canon_r)
    print("wrote %s (%d bytes)" % (OUT, len(canon_r)))
    print("sha256 %s" % hashlib.sha256(canon_r).hexdigest())


if __name__ == "__main__":
    main()
