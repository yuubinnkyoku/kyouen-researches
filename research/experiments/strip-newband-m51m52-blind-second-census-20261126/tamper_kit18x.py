#!/usr/bin/env python3
"""Tamper battery for audit_kit18x.py: 3 fail-closed checks + restore verify."""
import json, os, shutil, subprocess, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
CEN = os.path.join(HERE, "census_kit18x.out")
BAK = CEN + ".bak"
AUD = os.path.join(HERE, "audit_kit18x.py")
PRE = os.path.join(HERE, "audit_recompute.json")
PREBAK = PRE + ".bak"

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def run_audit():
    r = subprocess.run([sys.executable, AUD], capture_output=True, text=True)
    return r.returncode, r.stdout

def restore():
    shutil.copyfile(BAK, CEN)
    shutil.copyfile(PREBAK, PRE)

def main():
    shutil.copyfile(CEN, BAK)
    shutil.copyfile(PRE, PREBAK)
    base_sha = sha(CEN)
    results = []

    # clean control
    rc, out = run_audit()
    results.append(("control", rc == 0 and "AUDIT-PASS" in out))
    print("control rc=%d pass=%s" % (rc, "AUDIT-PASS" in out))

    # T1: frontier m=51 separation value flip (2 -> 3) in frozen census
    d = json.load(open(CEN))
    for r in d["sections"]:
        if r["m_z"] == "51_101":
            r["separations"][0]["value"] = 3
    json.dump(d, open(CEN, "w"), indent=1)
    rc, out = run_audit()
    t1 = rc != 0 and "G4_frontier_exact FAIL" in out and "G8_full_recompute FAIL" in out
    results.append(("T1", t1))
    print("T1 rc=%d G4fail=%s G8fail=%s" % (rc, "G4_frontier_exact FAIL" in out,
                                            "G8_full_recompute FAIL" in out))
    restore()

    # T2: inject a phantom separation into a clean window row
    d = json.load(open(CEN))
    for r in d["sections"]:
        if r["m_z"] == "50_95":
            r["separations"].append({"X": [50, 50], "S": 100, "value": 2,
                                     "collapse": 1, "direction": "UP"})
    json.dump(d, open(CEN, "w"), indent=1)
    rc, out = run_audit()
    t2 = rc != 0 and "G6_windows_clean FAIL" in out and "G8_full_recompute FAIL" in out
    results.append(("T2", t2))
    print("T2 rc=%d G6fail=%s G8fail=%s" % (rc, "G6_windows_clean FAIL" in out,
                                            "G8_full_recompute FAIL" in out))
    restore()

    # T3: tamper the precomputed recompute entries (value flip on an evenlife row)
    d = json.load(open(PRE))
    d["14_58"]["seps"][0]["value"] = 1
    json.dump(d, open(PRE, "w"))
    rc, out = run_audit()
    t3 = rc != 0 and "G8_full_recompute FAIL" in out
    results.append(("T3", t3))
    print("T3 rc=%d G8fail=%s" % (rc, "G8_full_recompute FAIL" in out))
    restore()

    ok_restore = sha(CEN) == base_sha
    rc, out = run_audit()
    print("post-restore clean rc=%d %s byte-identical=%s"
          % (rc, "AUDIT-PASS" in out, ok_restore))
    ok = all(v for _, v in results) and rc == 0 and "AUDIT-PASS" in out and ok_restore
    print("TAMPER-" + ("PASS 3/3 fail-closed" if ok else "FAIL"),
          [(k, v) for k, v in results])
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
