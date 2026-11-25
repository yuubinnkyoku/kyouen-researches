#!/usr/bin/env python3
"""Third verification of K1151 (replace9 whole-record second verification) via
pristine re-execution of the published verifier, its 10 pinned input snapshots,
and its audit.

Scope (single-owner declaration commit f3097440, 2026-11-20T15:06:08Z):
  1. Verify the published machine and audit byte-match their SHA-256 pins
     (published at commit f7aa541f342d67b33f34fee2df5e31c262cb0691).
  2. Pristine re-execute the machine 4 times, each starting with NO audit file
     present (fresh regeneration from pins only):
       run1: same cwd (ambient, PYTHONHASHSEED unset)
       run2: same cwd again
       run3: isolated tree copy + isolated cwd + isolated HOME
       run4: isolated tree copy + isolated cwd + isolated HOME + PYTHONHASHSEED=random
     Each generated audit must be byte-identical to the published audit.
  3. Tamper test: flip 1 byte of one input snapshot in a copied tree; the
     machine must fail closed (nonzero exit, no output file).
  4. Emit a deterministic audit JSON (sorted keys, no timestamps). Fail-closed.

This harness re-runs the published verifier only. It performs NO DFPN search,
closes NO row, and changes NO other lane's result. Standard 11x11 empty board /
two-stone root {49,60}/{59,60} / S2 {59,60} / classes 1/2/4 remain UNKNOWN.
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

PINNED_COMMIT = "f7aa541f342d67b33f34fee2df5e31c262cb0691"
SOURCE_EXPERIMENT_DIR = "research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120"
MACHINE_SHA256 = "e92fb7556a6f12c6e3cee06477e5387ddb6214cb58875e4ee3385010f9043e8a"
PUBLISHED_AUDIT_SHA256 = "5888afb3e1c07f8555fbafc73fc0b9d1006b0a31c88bbdd55a0d8975c0cabcb4"
MACHINE_RELPATH = "scripts/verify_replace9_whole_record_20261120.py"
AUDIT_RELPATH = "output/replace9-whole-record-second-verification-20261120.json"
INPUTS = [
    "output/.input-k1085.json",
    "output/.input-k1086.json",
    "output/.input-k1089.json",
    "output/.input-k1091.json",
    "output/.input-k1095.json",
    "output/.input-k1097.json",
    "output/.input-cover-decision.json",
    "output/.input-k1147-external-audit.json",
    "output/.input-probe-records-replace9.jsonl",
    "output/.input-replace9.json",
]
TAMPER_INPUT = "output/.input-replace9.json"
GUARD = [
    "本検証は残余23行のどの行も閉じない",
    "WIN8-D10 candidate は証明書ではない",
    "REFUTED-D10 は LOSS 証明ではない",
    "node数・solved数を勝敗として読まない",
    "標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま",
]


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def clone_tree(src_root, dst_root):
    os.makedirs(os.path.join(dst_root, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(dst_root, "output"), exist_ok=True)
    shutil.copy2(os.path.join(src_root, MACHINE_RELPATH), os.path.join(dst_root, MACHINE_RELPATH))
    for rel in INPUTS:
        os.makedirs(os.path.dirname(os.path.join(dst_root, rel)), exist_ok=True)
        shutil.copy2(os.path.join(src_root, rel), os.path.join(dst_root, rel))


def run_machine(root, env, timeout_s=300):
    """Run the published machine once in root (audit file must not pre-exist).

    Returns (returncode, output_exists, output_sha256, output_bytes)."""
    audit_path = os.path.join(root, AUDIT_RELPATH)
    if os.path.exists(audit_path):
        os.remove(audit_path)
    proc = subprocess.run(
        [sys.executable, os.path.abspath(os.path.join(root, MACHINE_RELPATH))],
        cwd=root,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout_s,
    )
    exists = os.path.exists(audit_path)
    if exists:
        out_sha = sha256_of(audit_path)
        with open(audit_path, "rb") as f:
            out_bytes = len(f.read())
    else:
        out_sha = None
        out_bytes = 0
    return proc.returncode, exists, out_sha, out_bytes


def main():
    parser = argparse.ArgumentParser(description="K1151 pristine re-execution third verification harness")
    parser.add_argument("--root", required=True,
                        help="staged experiment root: scripts/ machine + output/.input-* + published-audit.json")
    parser.add_argument("--output", required=True, help="path for this harness's audit JSON")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    machine = os.path.join(root, MACHINE_RELPATH)
    published = os.path.join(root, "published-audit.json")

    failures = []
    audit = {
        "harness": "verify_k1151_reexec_third_20261120",
        "subject": "K1151 replace9 whole-record second verification",
        "pinned_commit": PINNED_COMMIT,
        "source_experiment_dir": SOURCE_EXPERIMENT_DIR,
        "declaration_note": "research/log/2026-11-20-n11-residual72-replace9-whole-record-reexec-third-verification-single-owner-note.md",
        "pins": {
            "machine_sha256": MACHINE_SHA256,
            "published_audit_sha256": PUBLISHED_AUDIT_SHA256,
        },
        "pin_gates": [],
        "input_snapshots": [],
        "runs": [],
        "tamper_test": {},
        "run_gate": None,
        "tamper_gate": None,
        "status": None,
        "interpretation_guard": GUARD,
    }

    # ---- Gate 1: published bytes match pins (fail-closed before any run) ----
    for path, pin, label in (
        (machine, MACHINE_SHA256, "machine_verify_replace9_whole_record_20261120.py"),
        (published, PUBLISHED_AUDIT_SHA256, "published_audit_replace9-whole-record-second-verification-20261120.json"),
    ):
        actual = sha256_of(path)
        ok = actual == pin
        if not ok:
            failures.append("pin mismatch %s: expected %s got %s" % (label, pin, actual))
        audit["pin_gates"].append({"label": label, "expected_sha256": pin, "actual_sha256": actual, "pass": ok})

    # input snapshot existence + sha record (byte-fidelity pinned by commit ref;
    # the machine holds internal fail-closed full-SHA pins for these inputs)
    for rel in INPUTS:
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            failures.append("missing input snapshot %s" % rel)
            continue
        audit["input_snapshots"].append({"path": rel, "sha256": sha256_of(p), "exists": True})
    if len(audit["input_snapshots"]) != len(INPUTS):
        failures.append("input snapshot count mismatch")

    tmp = tempfile.mkdtemp(prefix="k1151-reexec-third-")
    try:
        # ---- Runs 1-2: same cwd, ambient env ----
        for label in ("same-cwd-1", "same-cwd-2"):
            env = {k: v for k, v in os.environ.items() if k != "PYTHONHASHSEED"}
            rc, exists, out_sha, out_bytes = run_machine(root, env)
            byte_identical = exists and out_sha == PUBLISHED_AUDIT_SHA256
            if rc != 0 or not byte_identical:
                failures.append("run %s: rc=%r byte_identical=%r" % (label, rc, byte_identical))
            audit["runs"].append({
                "run": label,
                "environment": "ambient (PYTHONHASHSEED unset), fresh regeneration (audit deleted before run)",
                "returncode": rc,
                "output_sha256": out_sha,
                "output_bytes": out_bytes,
                "byte_identical_to_published_audit": bool(byte_identical),
            })

        # ---- Runs 3-4: isolated tree / cwd / HOME (+ hashseed random) ----
        for label, seed in (("isolated-tree-1", None), ("isolated-plus-hashseed-random", "random")):
            iso_root = os.path.join(tmp, "tree-%s" % label)
            iso_home = os.path.join(tmp, "home-%s" % label)
            os.makedirs(iso_home, exist_ok=True)
            clone_tree(root, iso_root)
            env = {k: v for k, v in os.environ.items() if k not in ("PYTHONHASHSEED", "HOME")}
            env["HOME"] = iso_home
            if seed is not None:
                env["PYTHONHASHSEED"] = seed
            rc, exists, out_sha, out_bytes = run_machine(iso_root, env)
            byte_identical = exists and out_sha == PUBLISHED_AUDIT_SHA256
            if rc != 0 or not byte_identical:
                failures.append("run %s: rc=%r byte_identical=%r" % (label, rc, byte_identical))
            audit["runs"].append({
                "run": label,
                "environment": "isolated tree/cwd/HOME" + (" + PYTHONHASHSEED=random" if seed else " (PYTHONHASHSEED unset)"),
                "returncode": rc,
                "output_sha256": out_sha,
                "output_bytes": out_bytes,
                "byte_identical_to_published_audit": bool(byte_identical),
            })

        audit["run_gate"] = (len(audit["runs"]) == 4
                             and all(r["returncode"] == 0 and r["byte_identical_to_published_audit"] for r in audit["runs"]))
        if not audit["run_gate"]:
            failures.append("run gate failed (4 runs expected, all byte-identical, fresh regeneration)")

        # ---- Gate 3: tamper test in a copied tree ----
        tam_root = os.path.join(tmp, "tamper")
        clone_tree(root, tam_root)
        tam_path = os.path.join(tam_root, TAMPER_INPUT)
        with open(tam_path, "rb") as f:
            data = bytearray(f.read())
        pos = len(data) // 2
        orig = data[pos]
        data[pos] = orig ^ 0x01
        with open(tam_path, "wb") as f:
            f.write(bytes(data))
        env = {k: v for k, v in os.environ.items() if k != "PYTHONHASHSEED"}
        rc, exists, out_sha, out_bytes = run_machine(tam_root, env)
        failed_closed = rc != 0
        no_output = not exists
        audit["tamper_test"] = {
            "mutation": "1 byte flipped at offset %d (XOR 0x01) of %s in a copied tree" % (pos, TAMPER_INPUT),
            "mutated_input_sha256": sha256_of(tam_path),
            "returncode": rc,
            "failed_closed": bool(failed_closed),
            "no_output_written": bool(no_output),
            "pin_caught_mutation": bool(failed_closed and no_output),
        }
        audit["tamper_gate"] = bool(failed_closed and no_output)
        if not audit["tamper_gate"]:
            failures.append("tamper gate failed: mutated input did not fail closed")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    audit["status"] = "k1151-reexec-third-verification-passed" if not failures else "k1151-reexec-third-verification-failed"
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
    print("ALL GATES PASS: pins 2/2 + 10 inputs staged, fresh-regeneration runs 4/4 byte-identical, tamper caught")


if __name__ == "__main__":
    main()
