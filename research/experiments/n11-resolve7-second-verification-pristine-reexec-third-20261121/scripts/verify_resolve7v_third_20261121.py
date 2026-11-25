#!/usr/bin/env python3
"""
resolve7 (K1072) second-verification pristine-reexec THIRD verification harness.

Target: the independent second verification of resolve7 (post-fold witness recheck),
published at commit e836dd127a90e520d8e2801e62b59eb4966f0ed8 (2026-11-19T21:33:29Z,
single commit, 4 files: README + verifier script + audit master + research log).
This harness re-executes the published verifier, pristine, from published bytes only:

  stage pin     the 3 machine files of the published second verification
                (README, verifier, audit master) fetched from the pin commit raw
                URL and compared SHA-256 + byte count against the published values.
  stage recon   the 12 W inputs (published records) fetched from two pinned refs
                (ref_a = declaration-time HEAD, ref_b = declaration commit),
                each SHA-256 checked against the machine pins, ref_a vs ref_b
                byte-compared, placed into the verifier input dir (canonical
                names), and re-hashed after placement.
  stage rerun   the published verifier run pristine 4 times per battery:
                r1/r2 same cwd, r3 isolated copytree + env -i isolated
                HOME/TMPDIR, r4 = r3 + PYTHONHASHSEED=random. Each run must be
                rc==0 and byte-identical to the published audit master; the 4
                outputs must be mutually identical.
  stage tampers lane-chosen 1 byte XOR 0x01 probes at sweep39.json@2345 and
                resolve6.json@23456 (distinct from every known lane probe
                offset). The published verifier aborts on the FIRST pin
                mismatch (SystemExit), so each tamper must produce rc!=0, a
                stderr line naming exactly the tampered input
                ("pin mismatch for <name>"), and NO audit file. The two stderr
                messages must name different inputs (independent pin gates).
                W is restored and re-hashed after both probes.
  finalize      a byte-deterministic audit JSON (no wall-clock, no absolute
                paths, no volatile) written to <base>/output/.

Usage: python3 verify_resolve7v_third_20261121.py <base_dir>

Interpretation guards (unchanged): no search, no root judging, no row closing,
no universe rebuild. REFUTED-D10 is NOT a LOSS proof. The standard 11x11 empty
board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 remain UNKNOWN.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.request

PIN_COMMIT = "e836dd127a90e520d8e2801e62b59eb4966f0ed8"
REF_A = "12eefdeae3198852cd0a8ca14f42457547b92773"   # declaration-time main HEAD
REF_B = "86c6d546e20b4b1809425dbdf8270700186d955a"   # declaration note commit
RAW = "https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches"
EXP = "research/experiments/n11-residual72-resolve7-second-verification-20261120"

PUBLISHED = {
    "readme": {
        "path": EXP + "/README.md",
        "sha256": "2a9405aacb98b1a8558e1ec1a4642776479bd9a46ac7c8c2a7b73eb5938a3ead",
        "bytes": 5772,
    },
    "machine": {
        "path": EXP + "/scripts/resolve7_second_verification.py",
        "sha256": "695e56d7371e4ee974eab8aa67fab5477c7afd9c78eaabbc5c012c8501cb9773",
        "bytes": 29959,
    },
    "audit": {
        "path": EXP + "/output/resolve7-second-verification-20261120.json",
        "sha256": "4286100804d82376418066da89167c50017244f2c6f02b81ad76a07b45bd91d6",
        "bytes": 21842,
    },
}

W_PATHS = {
    "fold10.json": "research/experiments/n11-seventeenth-win7-receipt-fold-20261120/fold/output/seventeenth-win7-receipt-fold-20261120.json",
    "fold10second.json": "research/experiments/n11-seventeenth-receipt-fold-second-verification-20261120/output/fold10-second-verification-20261120.json",
    "fold9.json": "research/experiments/n11-residual78-windfall4-receipt-fold-20261120/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json",
    "probes-w0.jsonl": "research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/output/probe-records-w0.jsonl",
    "probes-w1.jsonl": "research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/output/probe-records-w1.jsonl",
    "probes-w2.jsonl": "research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/output/probe-records-w2.jsonl",
    "probes-w3.jsonl": "research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/output/probe-records-w3.jsonl",
    "resolve6.json": "research/experiments/n11-residual78-cache-join-resolve6-20261120/output/post-saturation-full-cache-join-resolve6-20261120.json",
    "resolve7.json": "research/experiments/n11-residual72-postfold-witness-recheck-20261120/output/residual72-postfold-witness-recheck-20261120.json",
    "roots.json": "research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/roots.json",
    "sweep39.json": "research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/output/witness-39live-root-depth10-sweep-20261120.json",
    "sv17.json": "research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/output/seventeenth-cert-triple-verification-20261120.json",
}

W_PINS = {
    "fold10.json": "bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a",
    "fold10second.json": "a62d6d50ffe3196ad2de1ff7b1df67ff8208b2a13510cce3f13aee0e9a085054",
    "fold9.json": "24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2",
    "probes-w0.jsonl": "6b045eaefdd59e2c0fbd0f9b4a1e876b89c3f8b03cfade8f0ab1f8192cd0a984",
    "probes-w1.jsonl": "4aaa4d0a691f6da40e68dbaa41a353aaf3ea518a6863aec04886c17197e00967",
    "probes-w2.jsonl": "2d4ff7dd40b2fc66745068f6772724f38ccd04dd2a65507af925fb85252b3032",
    "probes-w3.jsonl": "e04e20bdadd1cba94cd0a285ff9fb72bb9e9d0a2d5a687f1d76ceccc7d0ccb0c",
    "resolve6.json": "e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a",
    "resolve7.json": "207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f",
    "roots.json": "9f0161a8a61d311534fd3a4035b1c367426691c72ad5eb44efd01a5fae37e0cc",
    "sweep39.json": "22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc",
    "sv17.json": "c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc",
}

TAMPERS = [
    ("sweep39.json", 2345),
    ("resolve6.json", 23456),
]

GATES = []


def gate(name, ok, detail):
    GATES.append({"name": name, "pass": bool(ok), "detail": str(detail)})
    return bool(ok)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def fetch(url, tries=4):
    last = None
    for _ in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
    raise SystemExit("fetch failed for " + url + ": " + repr(last))


def raw_url(ref, path):
    return RAW + "/" + ref + "/" + path


def stage_pin(base):
    d = os.path.join(base, "pin")
    os.makedirs(d, exist_ok=True)
    for key in ("readme", "machine", "audit"):
        meta = PUBLISHED[key]
        b = fetch(raw_url(PIN_COMMIT, meta["path"]))
        gate("pin-" + key + "-sha256", sha256_bytes(b) == meta["sha256"], sha256_bytes(b))
        gate("pin-" + key + "-bytes", len(b) == meta["bytes"], len(b))
        with open(os.path.join(d, key + ".bin"), "wb") as f:
            f.write(b)
    return 0


def stage_recon(base):
    inp = os.path.join(base, "input")
    os.makedirs(inp, exist_ok=True)
    for name in sorted(W_PATHS):
        path = W_PATHS[name]
        a = fetch(raw_url(REF_A, path))
        gate("recon-" + name + "-refA-sha256", sha256_bytes(a) == W_PINS[name], sha256_bytes(a))
        bb = fetch(raw_url(REF_B, path))
        gate("recon-" + name + "-refB-sha256", sha256_bytes(bb) == W_PINS[name], sha256_bytes(bb))
        gate("recon-" + name + "-two-ref-identical", a == bb, "cmp")
        with open(os.path.join(inp, name), "wb") as f:
            f.write(a)
        with open(os.path.join(inp, name), "rb") as f:
            back = f.read()
        gate("recon-" + name + "-placed-sha256", sha256_bytes(back) == W_PINS[name],
             sha256_bytes(back))
    return 0


def run_machine(machine_path, input_dir, out_path, cwd, env):
    r = subprocess.run(
        [sys.executable, os.path.abspath(machine_path), os.path.abspath(input_dir),
         os.path.abspath(out_path)],
        cwd=cwd, env=env, capture_output=True, text=True, timeout=600)
    return r


def stage_rerun(base):
    machine = os.path.join(base, "pin", "machine.bin")
    master = os.path.join(base, "pin", "audit.bin")
    with open(master, "rb") as f:
        master_bytes = f.read()
    input_dir = os.path.join(base, "input")
    outs = []
    runs_dir = os.path.join(base, "runs")
    os.makedirs(runs_dir, exist_ok=True)
    for tag in ("r1", "r2"):
        out = os.path.join(runs_dir, tag, "audit.json")
        os.makedirs(os.path.join(runs_dir, tag), exist_ok=True)
        r = run_machine(machine, input_dir, out, cwd=base, env=None)
        outs.append((tag, r, out))
    for tag, extra in (("r3", {}), ("r4", {"PYTHONHASHSEED": "random"})):
        iso = os.path.join(base, "iso", tag)
        if os.path.exists(iso):
            shutil.rmtree(iso)
        os.makedirs(os.path.join(iso, "home"), exist_ok=True)
        os.makedirs(os.path.join(iso, "tmp"), exist_ok=True)
        cwd = os.path.join(iso, "run")
        shutil.copytree(input_dir, cwd)
        shutil.copy(machine, os.path.join(cwd, "machine.py"))
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
               "HOME": os.path.join(iso, "home"),
               "TMPDIR": os.path.join(iso, "tmp")}
        env.update(extra)
        out = os.path.join(cwd, "audit.json")
        r = run_machine(os.path.join(cwd, "machine.py"), cwd, out, cwd=cwd, env=env)
        outs.append((tag, r, out))
    for tag, r, out in outs:
        gate("rerun-" + tag + "-rc0", r.returncode == 0,
             "rc=" + str(r.returncode) + " stderr=" + r.stderr.strip()[:80])
        gate("rerun-" + tag + "-audit-exists", os.path.isfile(out), "file")
        with open(out, "rb") as f:
            ob = f.read()
        d = json.loads(ob)
        gate("rerun-" + tag + "-gates76-allpass",
             d.get("gates_total") == 76 and d.get("gates_all_pass") is True
             and d.get("resolve7_record_faithful") is True,
             "gates_total=" + str(d.get("gates_total")))
        gate("rerun-" + tag + "-sha256-published",
             sha256_bytes(ob) == PUBLISHED["audit"]["sha256"], sha256_bytes(ob))
        gate("rerun-" + tag + "-byte-identical-master", ob == master_bytes, "cmp")
        gate("rerun-" + tag + "-bytes", len(ob) == PUBLISHED["audit"]["bytes"], len(ob))
    b0 = None
    same = True
    for tag, r, out in outs:
        with open(out, "rb") as f:
            ob = f.read()
        if b0 is None:
            b0 = ob
        elif ob != b0:
            same = False
    gate("rerun-4outputs-mutually-identical", same, "cmp")
    return 0




def stage_tampers(base):
    machine = os.path.join(base, "pin", "machine.bin")
    input_dir = os.path.join(base, "input")
    tam_dir = os.path.join(base, "tampers")
    os.makedirs(tam_dir, exist_ok=True)
    stderrs = {}
    for i, (name, off) in enumerate(TAMPERS):
        tag = "t%d" % (i + 1)
        p = os.path.join(input_dir, name)
        with open(p, "rb") as f:
            original = f.read()
        probe = bytearray(original)
        probe[off] ^= 1
        with open(p, "wb") as f:
            f.write(bytes(probe))
        out = os.path.join(tam_dir, tag, "audit.json")
        r = run_machine(machine, input_dir, out, cwd=base, env=None)
        gate("tamper-" + tag + "-rc-not0", r.returncode != 0, "rc=" + str(r.returncode))
        want = "pin mismatch for " + name
        gate("tamper-" + tag + "-stderr-names-input",
            want in r.stderr, "stderr=" + r.stderr.strip()[:80])
        other = [n for n, _ in TAMPERS if n != name]
        gate("tamper-" + tag + "-stderr-name-exclusive",
             all(("pin mismatch for " + n) not in r.stderr for n in other),
             "exclusive")
        gate("tamper-" + tag + "-no-audit-written", not os.path.isfile(out), "absent")
        stderrs[tag] = r.stderr.strip()
        with open(p, "wb") as f:
            f.write(original)
        with open(p, "rb") as f:
            back = f.read()
        gate("tamper-" + tag + "-w-restored-sha", sha256_bytes(back) == W_PINS[name],
             sha256_bytes(back))
    gate("tamper-independent-gates",
         stderrs["t1"] != stderrs["t2"] and "pin mismatch for sweep39.json" in stderrs["t1"]
         and "pin mismatch for resolve6.json" in stderrs["t2"],
         "two distinct stderr identifications")
    return 0


def write_audit():
    pass_count = sum(1 for g in GATES if g["pass"])
    result = {
        "schema": "resolve7-second-verification-pristine-reexec-third/1",
        "status": "all-gates-pass" if pass_count == len(GATES) else "gate-failed",
        "gates_total": len(GATES),
        "gates_pass": pass_count,
        "gates_all_pass": pass_count == len(GATES),
        "targets": {
            "second_verification_commit": PIN_COMMIT,
            "declaration_refs": [REF_A, REF_B],
            "published_audit_sha256": PUBLISHED["audit"]["sha256"],
            "w_inputs": len(W_PATHS),
        },
        "interpretation_guard": [
            "This third verification re-executes the published resolver verifier on published bytes; it performs no search, judges no root, closes no row, rebuilds no candidate universe.",
            "REFUTED-D10 is NOT a LOSS proof; it certifies no first-player win within depth-10 from that root only.",
            "Folds and coverage are row bookkeeping and say nothing about the game-theoretic value of any row.",
            "nodes/solved/coverage counts are not verdicts.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
        ],
    }
    return result


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "base"
    os.makedirs(os.path.join(base, "output"), exist_ok=True)
    del GATES[:]
    stage_pin(base)
    stage_recon(base)
    stage_rerun(base)
    stage_tampers(base)
    result = write_audit()
    result["gates"] = GATES
    out = os.path.join(base, "output", "resolve7v-third-harness-audit.json")
    with open(out, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("third harness gates", result["gates_total"], "all_pass", result["gates_all_pass"])
    if not result["gates_all_pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
