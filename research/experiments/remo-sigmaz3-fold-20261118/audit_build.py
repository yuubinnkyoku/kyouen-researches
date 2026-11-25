#!/usr/bin/env python3
"""K0944 audit builder.

Runs run_checks() once in-process, then executes sigmaz3_verify.py
(which runs run_checks() twice internally and asserts determinism)
as a cold subprocess TWICE and byte-compares the two stdout payloads.
Writes output/sigmaz3_audit.json (byte-stable: no timings/timestamps).
"""
import sys, os, json, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

def _sha_b(b):
    return hashlib.sha256(b).hexdigest()

def main():
    from sigmaz3_verify import run_checks
    inproc = run_checks()

    outs = []
    for _ in range(2):
        p = subprocess.run([sys.executable, os.path.join(HERE, "sigmaz3_verify.py")],
                           capture_output=True, text=True, cwd=HERE)
        assert p.returncode == 0, p.stderr[-2000:]
        outs.append(p.stdout.strip())
    cold_deterministic = outs[0] == outs[1]
    cold = json.loads(outs[0])
    cold_sha = _sha_b(outs[0].encode())

    payload = json.dumps(cold, sort_keys=True, separators=(",", ":"))
    assert json.dumps(inproc, sort_keys=True, separators=(",", ":")) == payload

    audit = {
        "item": "K0943-sigmaz3-fold-onechar (numbering re-checked at publish)",
        "in_process_all_ok": bool(inproc["all_ok"]),
        "cold_runs": 2,
        "cold_deterministic": bool(cold_deterministic),
        "cold_payload_sha256": cold_sha,
        "checks": cold,
        "files": {
            "sievegen_core.py": _sha_b(open(os.path.join(HERE, "sievegen_core.py"), "rb").read()),
            "composite_core.py": _sha_b(open(os.path.join(HERE, "composite_core.py"), "rb").read()),
            "sigmaz3_core.py": _sha_b(open(os.path.join(HERE, "sigmaz3_core.py"), "rb").read()),
            "sigmaz3_verify.py": _sha_b(open(os.path.join(HERE, "sigmaz3_verify.py"), "rb").read()),
        },
        "all_ok": bool(inproc["all_ok"]) and cold_deterministic and cold["all_ok"],
    }
    outdir = os.path.join(HERE, "output")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "sigmaz3_audit.json")
    with open(out, "w") as f:
        f.write(json.dumps(audit, sort_keys=True, separators=(",", ":")))
    print("all_ok =", audit["all_ok"])
    print("audit sha256 =", _sha_b(open(out, "rb").read()))
    print("cold payload sha256 =", cold_sha)
    if not audit["all_ok"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
