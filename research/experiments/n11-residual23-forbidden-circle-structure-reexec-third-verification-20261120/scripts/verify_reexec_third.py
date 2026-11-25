#!/usr/bin/env python3
"""Pristine re-exec third verification for the forbidden-circle D4-orbit structure publication.

Target: commit 3ccde3e385137b1a51cd2821a078ede38a2b3dfb (2026-11-20T16:41:05Z),
experiment research/experiments/n11-residual23-zero-triple-forbidden-circle-structure-20261121/

Gates (all fail-closed, exit 1 on any mismatch, audit only written on success):
  G1 pin: the four staged published bytes match the pinned SHA-256 values.
  G2 fresh-run: four pristine re-executions (runA/runB same cwd, runC isolated
     tree/cwd/HOME with copied inputs, runD same isolation plus PYTHONHASHSEED=random)
     each produce output byte-identical to the published audit canonical.
  G3 tamper: a 1-byte XOR on each input at offsets not tested by the publisher
     (fixture offset 200, K1156-audit offset 150) is caught fail-closed
     (returncode 1, no output file created).
  G4 harness determinism: the audit JSON is sorted-keys, timestamp-free, and
     byte-stable across repeated invocations (checked externally by the audit
     record of this harness being reproduced byte-identically in three runs).

The verifier and both inputs staged here are byte-copies of the published
files; no local state is trusted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PUBLISHED_COMMIT = "3ccde3e385137b1a51cd2821a078ede38a2b3dfb"
PUBLISHED_EXPERIMENT = "research/experiments/n11-residual23-zero-triple-forbidden-circle-structure-20261121"

PIN_VERIFIER_SHA256 = "45e5d7d61781e96e1e0afff8f457f06ff69a00a2b5e6777dc03d710e2a122951"
PIN_PUBLISHED_AUDIT_SHA256 = "0e16f29b259eac1864ce826324f5a51dfe4d5bd5946a0ea5ef7998daaf39c638"
PIN_FIXTURE_SHA256 = "51e7a465e18646097073e4f8231f89cbff327d05f9bfeac102e57c754b4ff822"
PIN_K1156_AUDIT_SHA256 = "c4e55dbe8d937dce93430f5804296dcd5cf42a9d42de14f8e90bbebe262eb61f"
PUBLISHED_AUDIT_BYTES = 9730

TAMPER_FIXTURE_OFFSET = 200   # publisher README tested offset 100 on this file
TAMPER_K1156_AUDIT_OFFSET = 150

INTERPRETATION_GUARD = [
    "This third verification only confirms reproducibility of a finite structural post-analysis; no row is closed.",
    "The safe-candidate exclusion relies on pinned REFUTED-D10 facts, not on geometry; REFUTED-D10 is not a LOSS proof.",
    "The candidate-cover accounting is bookkeeping for a covering plan, not a game-theoretic certificate.",
    "Node counts and solved counts are never read as game outcomes.",
    "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 all remain UNKNOWN.",
]


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL-CLOSED: {msg}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_verifier(python: str, script: Path, input_path: Path, audit_path: Path,
                out_path: Path, cwd: Path, env: dict) -> tuple[int, bytes, str]:
    proc = subprocess.run(
        [python, str(script), "--input", str(input_path), "--audit", str(audit_path), "--output", str(out_path)],
        cwd=str(cwd), env=env, capture_output=True, text=True)
    out_bytes = out_path.read_bytes() if out_path.exists() else b""
    return proc.returncode, out_bytes, (proc.stdout + proc.stderr).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="staging root containing stage/ (default: this directory)")
    ap.add_argument("--output", default=None, help="audit JSON output path (default: <root>/output/third-verification-audit.json)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    stage = root / "stage"
    verifier = stage / "derive_forbidden_circles.py"
    fixture = stage / "residual23-provider-input.json"
    k1156_audit = stage / "k1156-direct-fourth-audit.json"
    published_audit = stage / "forbidden-circle-structure.json"
    for p in (verifier, fixture, k1156_audit, published_audit):
        if not p.is_file():
            fail(f"staged published byte missing: {p.name}")

    # G1 pin gate
    pin_results = {}
    for name, path, pin in [
        ("derivative verifier", verifier, PIN_VERIFIER_SHA256),
        ("published audit canonical", published_audit, PIN_PUBLISHED_AUDIT_SHA256),
        ("K1156 provider fixture", fixture, PIN_FIXTURE_SHA256),
        ("K1156 direct-fourth audit", k1156_audit, PIN_K1156_AUDIT_SHA256),
    ]:
        actual = sha256_bytes(path.read_bytes())
        ok = actual == pin
        pin_results[name] = {"sha256": actual, "expected": pin, "ok": ok,
                             "bytes": path.stat().st_size}
        if not ok:
            fail(f"pin mismatch for {name}: {actual} != {pin}")
    if pin_results["published audit canonical"]["bytes"] != PUBLISHED_AUDIT_BYTES:
        fail("published audit size mismatch")
    pin_gate = len(pin_results) == 4 and all(v["ok"] for v in pin_results.values())
    python = sys.executable or "python3"

    # G2 fresh-run gate (four pristine re-executions, tmp workdir under /tmp-equivalent OS default)
    work = root / "fresh-works"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    fresh_runs = {}
    fresh_specs = [
        ("runA", False, False, None),
        ("runB", False, False, None),
        ("runC", True, True, None),
        ("runD", True, True, "random"),
    ]
    for name, isolated, isolated_home, hashseed in fresh_specs:
        run_dir = work / name
        if isolated:
            run_dir.mkdir()
            (run_dir / "scripts").mkdir()
            (run_dir / "input").mkdir()
            shutil.copy2(verifier, run_dir / "scripts" / "derive_forbidden_circles.py")
            shutil.copy2(fixture, run_dir / "input" / "residual23-provider-input.json")
            shutil.copy2(k1156_audit, run_dir / "input" / "k1156-direct-fourth-audit.json")
            script = run_dir / "scripts" / "derive_forbidden_circles.py"
            inp = run_dir / "input" / "residual23-provider-input.json"
            aud = run_dir / "input" / "k1156-direct-fourth-audit.json"
        else:
            script = verifier
            inp = fixture
            aud = k1156_audit
        env = dict(os.environ)
        if isolated_home:
            env["HOME"] = str(run_dir)
        if hashseed:
            env["PYTHONHASHSEED"] = hashseed
        elif isolated_home:
            env.pop("PYTHONHASHSEED", None)
        out = run_dir / "out.json"
        rc, out_bytes, _ = run_verifier(python, script, inp, aud, out,
                                         cwd=run_dir if isolated else root, env=env)
        identical = out_bytes == published_audit.read_bytes()
        fresh_runs[name] = {
            "returncode": rc,
            "output_sha256": sha256_bytes(out_bytes),
            "output_bytes": len(out_bytes),
            "byte_identical_to_published_audit": identical,
            "isolated_tree_cwd_home": isolated and isolated_home,
            "pythonhashseed": hashseed,
        }
        if rc != 0 or not identical:
            fail(f"fresh run {name} did not reproduce the published audit byte-identically (rc={rc})")
    fresh_gate = all(v["returncode"] == 0 and v["byte_identical_to_published_audit"] for v in fresh_runs.values())

    # G3 tamper gate (1-byte XOR at offsets the publisher did not test)
    tamper_results = []
    for name, src, offset in [
        ("fixture offset %d XOR 0x01" % TAMPER_FIXTURE_OFFSET, fixture, TAMPER_FIXTURE_OFFSET),
        ("k1156-audit offset %d XOR 0x01" % TAMPER_K1156_AUDIT_OFFSET, k1156_audit, TAMPER_K1156_AUDIT_OFFSET),
    ]:
        tam_dir = work / ("tamper-" + name.replace(" ", "-"))
        tam_dir.mkdir()
        data = bytearray(src.read_bytes())
        data[offset] ^= 0x01
        tampered = tam_dir / src.name
        tampered.write_bytes(bytes(data))
        other = k1156_audit if src is fixture else fixture
        out = tam_dir / "out.json"
        env = dict(os.environ)
        env.pop("PYTHONHASHSEED", None)
        rc, out_bytes, stderr_txt = run_verifier(python, verifier, tampered, other, out, cwd=tam_dir, env=env)
        caught = rc == 1 and not out.exists() and len(out_bytes) == 0
        tamper_results.append({
            "tamper": name,
            "tampered_input_sha256": sha256_bytes(bytes(data)),
            "returncode": rc,
            "output_created": out.exists(),
            "fail_closed_captured": caught,
            "verifier_message": stderr_txt.splitlines()[-1] if stderr_txt else "",
        })
        if not caught:
            fail(f"tamper {name} was not caught fail-closed (rc={rc}, output_created={out.exists()})")
    tamper_gate = all(v["fail_closed_captured"] for v in tamper_results)

    # audit canonical
    harness_bytes = Path(__file__).read_bytes()
    result = {
        "schema": "n11-residual23-forbidden-circle-structure-reexec-third-verification-20261120-v1",
        "status": "third-verification-passed",
        "published_commit": PUBLISHED_COMMIT,
        "published_experiment_dir": PUBLISHED_EXPERIMENT,
        "pins": pin_results,
        "gates": {
            "g1_pin_4_of_4": pin_gate,
            "g2_fresh_runs_4_of_4_byte_identical": fresh_gate,
            "g3_tamper_2_of_2_fail_closed": tamper_gate,
        },
        "fresh_runs": fresh_runs,
        "tamper": tamper_results,
        "harness_sha256": sha256_bytes(harness_bytes),
        "interpretation_guard": INTERPRETATION_GUARD,
    }
    out_json = json.dumps(result, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n"
    out_path = Path(args.output).resolve() if args.output else root / "output" / "third-verification-audit.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out_json, encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "gates": result["gates"],
        "fresh_runs": {k: {"sha256": v["output_sha256"], "bytes": v["output_bytes"]} for k, v in fresh_runs.items()},
        "audit_path": str(out_path),
    }, ensure_ascii=True, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
