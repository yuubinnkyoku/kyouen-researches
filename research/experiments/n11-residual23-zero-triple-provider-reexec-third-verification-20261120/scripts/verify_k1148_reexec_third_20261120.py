#!/usr/bin/env python3
"""Third verification of K1148 (residual23 zero-triple-provider third geometry)
via pristine re-execution of the published machine, fixture, and audit.

Scope (single-owner declaration commit 75fde9d8, 2026-11-20T14:53:03Z):
  1. Verify the three published files byte-match their SHA-256 pins
     (published at commit 6564fded75038c887c095873c5d3e5633c4fcd35).
  2. Pristine re-execute the machine 4 times:
       run1: same cwd (ambient environment)
       run2: same cwd again (ambient environment)
       run3: isolated tree copy, isolated cwd + isolated HOME
       run4: isolated tree copy, isolated cwd + isolated HOME + PYTHONHASHSEED=random
     Each output must be byte-identical to the published audit.
  3. Tamper test: flip 1 byte of the fixture; the machine must fail closed.
  4. Emit a deterministic audit JSON (sorted keys, no timestamps, no randomness,
     no environment-dependent output). Exit nonzero on any failed gate.

This harness performs NO new geometric computation and closes NO residual row.
Standard 11x11 empty board / two-stone root {49,60}/{59,60} / S2 {59,60} /
classes 1/2/4 all remain UNKNOWN.
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

PINNED_COMMIT = "6564fded75038c887c095873c5d3e5633c4fcd35"
SOURCE_EXPERIMENT_DIR = "research/experiments/n11-residual23-zero-triple-provider-third-geometry-20261120"
MACHINE_SHA256 = "cb8c95c8799e6c12bbc7fdb2cc9b6236f664724f29827e56d2e75de62a084892"
FIXTURE_SHA256 = "51e7a465e18646097073e4f8231f89cbff327d05f9bfeac102e57c754b4ff822"
PUBLISHED_AUDIT_SHA256 = "526eada2c94457f06a7cf27a86011586e394c342687e539a6b545b42577b9573"
DECLARATION_NOTE = "research/log/2026-11-20-n11-residual23-zero-triple-provider-reexec-third-verification-single-owner-note.md"

GUARD = [
    "この検証は残余23行のどの行も閉じない",
    "zero rows の列挙は残余行の勝敗決着ではない",
    "nodes/solved 等の計数を勝敗として読まない",
    "本検証は幾何の新規計算を含まない（出版機械のpristine再実行のみ）",
    "標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま",
]


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check_pin(path, expected, label, failures):
    actual = sha256_of(path)
    ok = actual == expected
    if not ok:
        failures.append("pin mismatch %s: expected %s got %s" % (label, expected, actual))
    return {
        "label": label,
        "expected_sha256": expected,
        "actual_sha256": actual,
        "pass": ok,
    }


def run_machine(machine_path, fixture_path, output_path, cwd, env, timeout_s=900):
    """Run the published machine once. Returns (returncode, output_exists, output_sha256, output_bytes)."""
    proc = subprocess.run(
        [sys.executable, os.path.abspath(machine_path),
         "--input", os.path.abspath(fixture_path),
         "--output", os.path.abspath(output_path)],
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout_s,
    )
    out_exists = os.path.exists(output_path)
    if out_exists:
        out_sha = sha256_of(output_path)
        with open(output_path, "rb") as f:
            out_bytes = len(f.read())
    else:
        out_sha = None
        out_bytes = 0
    duration = None  # never recorded in the audit (non-deterministic)
    return {
        "returncode": proc.returncode,
        "output_exists": out_exists,
        "output_sha256": out_sha,
        "output_bytes": out_bytes,
    }, duration


def clone_tree(src_dir, dst_dir):
    """Copy machine.py + input/ into an isolated tree (pristine bytes)."""
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy2(os.path.join(src_dir, "machine.py"), os.path.join(dst_dir, "machine.py"))
    os.makedirs(os.path.join(dst_dir, "input"), exist_ok=True)
    shutil.copy2(os.path.join(src_dir, "input", "residual23-provider-input.json"),
                 os.path.join(dst_dir, "input", "residual23-provider-input.json"))


def main():
    parser = argparse.ArgumentParser(description="K1148 pristine re-execution third verification harness")
    parser.add_argument("--root", required=True,
                        help="directory containing machine.py, input/residual23-provider-input.json, published-audit.json (byte-pinned)")
    parser.add_argument("--output", required=True, help="path for this harness's audit JSON")
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    machine = os.path.join(root, "machine.py")
    fixture = os.path.join(root, "input", "residual23-provider-input.json")
    published = os.path.join(root, "published-audit.json")

    failures = []
    audit = {
        "harness": "verify_k1148_reexec_third_20261120",
        "subject": "K1148 residual23 zero-triple-provider third geometry",
        "pinned_commit": PINNED_COMMIT,
        "source_experiment_dir": SOURCE_EXPERIMENT_DIR,
        "declaration_note": DECLARATION_NOTE,
        "pins": {},
        "pin_gates": [],
        "runs": [],
        "tamper_test": {},
        "run_gate": None,
        "tamper_gate": None,
        "status": None,
        "interpretation_guard": GUARD,
    }

    # ---- Gate 1: published bytes match pins (fail-closed before any run) ----
    for path, pin, label in (
        (machine, MACHINE_SHA256, "machine_audit_zero_triple_providers.py"),
        (fixture, FIXTURE_SHA256, "fixture_residual23-provider-input.json"),
        (published, PUBLISHED_AUDIT_SHA256, "published_audit_third-geometry-audit.json"),
    ):
        g = check_pin(path, pin, label, failures)
        audit["pin_gates"].append(g)

    with open(published, "rb") as f:
        published_bytes = f.read()
    published_obj = json.loads(published_bytes.decode("utf-8"))

    # ---- Gate 2: four pristine re-executions ----
    tmp = tempfile.mkdtemp(prefix="k1148-reexec-third-")
    try:
        # run1/run2: same cwd, ambient env (PYTHONHASHSEED stripped to default semantics)
        for label in ("same-cwd-1", "same-cwd-2"):
            out_path = os.path.join(tmp, "out-%s.json" % label)
            env = {k: v for k, v in os.environ.items() if k != "PYTHONHASHSEED"}
            res, _ = run_machine(machine, fixture, out_path, cwd=root, env=env, timeout_s=args.timeout)
            byte_identical = res["output_exists"] and res["output_sha256"] == PUBLISHED_AUDIT_SHA256
            if res["returncode"] != 0 or not byte_identical:
                failures.append("run %s: returncode=%r byte_identical=%r" % (label, res["returncode"], byte_identical))
            audit["runs"].append({
                "run": label,
                "environment": "ambient (PYTHONHASHSEED unset)",
                "returncode": res["returncode"],
                "output_sha256": res["output_sha256"],
                "output_bytes": res["output_bytes"],
                "byte_identical_to_published_audit": bool(byte_identical),
            })

        # run3/run4: isolated tree + isolated cwd + isolated HOME; run4 adds PYTHONHASHSEED=random
        for label, seed in (("isolated-tree-1", None), ("isolated-plus-hashseed-random", "random")):
            iso_root = os.path.join(tmp, "tree-%s" % label)
            iso_home = os.path.join(tmp, "home-%s" % label)
            os.makedirs(iso_home, exist_ok=True)
            clone_tree(root, iso_root)
            iso_machine = os.path.join(iso_root, "machine.py")
            iso_fixture = os.path.join(iso_root, "input", "residual23-provider-input.json")
            if sha256_of(iso_machine) != MACHINE_SHA256 or sha256_of(iso_fixture) != FIXTURE_SHA256:
                failures.append("isolated tree %s: byte copy mismatch" % label)
            out_path = os.path.join(iso_root, "out-%s.json" % label)
            env = {k: v for k, v in os.environ.items() if k not in ("PYTHONHASHSEED", "HOME")}
            env["HOME"] = iso_home
            if seed is not None:
                env["PYTHONHASHSEED"] = seed
            res, _ = run_machine(iso_machine, iso_fixture, out_path, cwd=iso_root, env=env, timeout_s=args.timeout)
            byte_identical = res["output_exists"] and res["output_sha256"] == PUBLISHED_AUDIT_SHA256
            if res["returncode"] != 0 or not byte_identical:
                failures.append("run %s: returncode=%r byte_identical=%r" % (label, res["returncode"], byte_identical))
            audit["runs"].append({
                "run": label,
                "environment": "isolated tree/cwd/HOME" + (" + PYTHONHASHSEED=random" if seed else " (PYTHONHASHSEED unset)"),
                "returncode": res["returncode"],
                "output_sha256": res["output_sha256"],
                "output_bytes": res["output_bytes"],
                "byte_identical_to_published_audit": bool(byte_identical),
            })
            # parsed-object equality belt-and-braces
            if res["output_exists"]:
                with open(out_path, "rb") as f:
                    run_obj = json.loads(f.read().decode("utf-8"))
                if run_obj != published_obj:
                    failures.append("run %s: parsed output != published audit object" % label)

        audit["run_gate"] = (len(audit["runs"]) == 4
                             and all(r["returncode"] == 0 and r["byte_identical_to_published_audit"] for r in audit["runs"]))
        if not audit["run_gate"]:
            failures.append("run gate failed (4 runs expected, all byte-identical)")

        # ---- Gate 3: tamper test (1-byte fixture mutation must fail closed) ----
        tam_dir = os.path.join(tmp, "tamper")
        os.makedirs(tam_dir, exist_ok=True)
        tam_fixture = os.path.join(tam_dir, "residual23-provider-input.json")
        with open(fixture, "rb") as f:
            data = bytearray(f.read())
        pos = len(data) // 2
        orig = data[pos]
        data[pos] = orig ^ 0x01  # single byte flip
        with open(tam_fixture, "wb") as f:
            f.write(bytes(data))
        tam_out = os.path.join(tam_dir, "tampered-output.json")
        env = {k: v for k, v in os.environ.items() if k != "PYTHONHASHSEED"}
        res, _ = run_machine(machine, tam_fixture, tam_out, cwd=root, env=env, timeout_s=args.timeout)
        mut_detected = (sha256_of(tam_fixture) != FIXTURE_SHA256) and data[pos] != orig
        failed_closed = res["returncode"] != 0
        no_output_written = not os.path.exists(tam_out)
        audit["tamper_test"] = {
            "mutation": "1 byte flipped at offset %d (XOR 0x01) of fixture" % pos,
            "mutated_fixture_sha256": sha256_of(tam_fixture),
            "returncode": res["returncode"],
            "failed_closed": bool(failed_closed),
            "no_output_written": bool(no_output_written),
            "pin_caught_mutation": bool(mut_detected and failed_closed and no_output_written),
        }
        audit["tamper_gate"] = bool(failed_closed and no_output_written)
        if not audit["tamper_gate"]:
            failures.append("tamper gate failed: mutated fixture did not fail closed")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    audit["pins"] = {
        "machine_sha256": MACHINE_SHA256,
        "fixture_sha256": FIXTURE_SHA256,
        "published_audit_sha256": PUBLISHED_AUDIT_SHA256,
    }
    audit["status"] = "k1148-reexec-third-verification-passed" if not failures else "k1148-reexec-third-verification-failed"
    if failures:
        audit["failures"] = failures

    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)
    with open(args.output, "wb") as f:
        f.write((json.dumps(audit, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))

    if failures:
        for msg in failures:
            print("FAIL: %s" % msg, file=sys.stderr)
        sys.exit(1)
    print("ALL GATES PASS: pins 3/3, pristine runs 4/4 byte-identical, tamper caught")


if __name__ == "__main__":
    main()
