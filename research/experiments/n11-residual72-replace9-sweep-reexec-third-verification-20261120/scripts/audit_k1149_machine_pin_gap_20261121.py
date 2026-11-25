#!/usr/bin/env python3
"""Audit the K1149 second-verifier's K1146 sweep-machine source pin.

The K1149 verifier records SWEEP_MACHINE_SHA256 in its output metadata, but
this audit checks whether that constant is well-formed and actually enforced
by a gate. It then confirms that K1159 independently pins the exact K1146
machine bytes and that the published K1149 audit records the same metadata.
Only Python's standard library is required.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path

K1149_VERIFIER_SHA256 = "77cdd9e3450aed9d2c900475f15d9e09367985b909027c50e485995737252db4"
K1149_AUDIT_SHA256 = "27fc420c58ac0c979e09c3a35b0b0b886fe1b521efea9de8f9f98e51e6264072"
K1146_SWEEP_MACHINE_SHA256 = "d163b2a120ac46abee40d0b9a32269bce14a73901a85a80e5925b7d2512bcd41"
K1149_MALFORMED_MACHINE_PIN = "d163b2a120ac46abee40d0b9a32269bce14a73901a85a80e595b7d2512bcd41"
K1159_HARNESS_SHA256 = "ec55f78a2a109a60d295569aa856a9c01764859c64655ed6aae405d678234979"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def assigned_string(tree, name):
    found = []
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(t, ast.Name) and t.id == name for t in targets):
                found.append((node.lineno, ast.literal_eval(node.value)))
    if len(found) != 1:
        raise SystemExit(f"expected one top-level {name} assignment, got {len(found)}")
    return found[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--output", default=None)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    second_path = root / "scripts/verify_replace9_reexec_20261120.py"
    third_path = root / "scripts/verify_k1149_reexec_third_20261120.py"
    sweep_path = root / "sweep/scripts/replace9_d10_sweep_20261120.py"
    audit_path = root / "published-audit.json"

    second_raw = second_path.read_bytes()
    third_raw = third_path.read_bytes()
    second_text = second_raw.decode("utf-8")
    third_text = third_raw.decode("utf-8")
    second_tree = ast.parse(second_text)
    third_tree = ast.parse(third_text)
    pin_line, second_pin = assigned_string(second_tree, "SWEEP_MACHINE_SHA256")
    third_pin_line, third_pin = assigned_string(third_tree, "SWEEP_MACHINE_SHA256")

    load_lines = []
    gate_lines = []
    for node in ast.walk(second_tree):
        if isinstance(node, ast.Name) and node.id == "SWEEP_MACHINE_SHA256" and isinstance(node.ctx, ast.Load):
            load_lines.append(node.lineno)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "gate":
            if any(isinstance(x, ast.Name) and x.id == "SWEEP_MACHINE_SHA256"
                   for arg in node.args for x in ast.walk(arg)):
                gate_lines.append(node.lineno)

    published_audit = json.loads(audit_path.read_text(encoding="utf-8"))
    audit_pin = published_audit.get("inputs", {}).get("k1146_sweep_machine_sha256")
    gate_names = [g.get("name") for g in published_audit.get("gates", [])]
    pristine_source = "\n".join(second_text.splitlines()[230:252])
    actual_second_sha = hashlib.sha256(second_raw).hexdigest()
    actual_third_sha = hashlib.sha256(third_raw).hexdigest()
    actual_sweep_sha = sha256(sweep_path)
    records_check_present = "if got != SWEEP_RECORDS_SHA256:" in second_text
    third_external_pin_present = (
        third_pin == K1146_SWEEP_MACHINE_SHA256
        and "sweep_machine_replace9_d10_sweep_20261120.py" in third_text
    )
    gap_detected = (
        second_pin == K1149_MALFORMED_MACHINE_PIN
        and len(second_pin) == 63
        and audit_pin == second_pin
        and not gate_lines
        and actual_sweep_sha == K1146_SWEEP_MACHINE_SHA256
    )
    gates = {
        "k1149_second_verifier_sha256": actual_second_sha == K1149_VERIFIER_SHA256,
        "k1149_published_audit_sha256": sha256(audit_path) == K1149_AUDIT_SHA256,
        "k1149_machine_pin_is_63_char_metadata_only": gap_detected,
        "k1149_machine_pin_has_no_gate_reference": len(gate_lines) == 0,
        "k1149_records_pin_is_actively_checked": records_check_present,
        "k1146_machine_actual_sha256": actual_sweep_sha == K1146_SWEEP_MACHINE_SHA256,
        "k1159_harness_sha256": actual_third_sha == K1159_HARNESS_SHA256,
        "k1159_external_machine_pin_is_correct_and_present": third_external_pin_present,
    }
    doc = {
        "schema": "n11-k1149-machine-source-pin-gap-review-20261121-v1",
        "subject": "K1149 replace9 sweep re-execution second-verifier source pin review",
        "source_commits": {
            "k1149_verifier_publication": "7ab77aa1bb5e80c2355261edc8e3f1ab08acd9d5",
            "k1146_sweep_machine_publication": "e9ea153bc469aa551689a5d275773553852f3342",
            "k1159_third_verification_part1": "76ef33b2cf84a6fc5b837784ea1a80c987820962",
        },
        "k1149_second_verifier": {
            "sha256": actual_second_sha,
            "machine_pin_constant": second_pin,
            "machine_pin_length": len(second_pin),
            "machine_pin_assignment_line": pin_line,
            "machine_pin_load_reference_lines": sorted(load_lines),
            "machine_pin_gate_reference_lines": sorted(gate_lines),
            "published_audit_machine_pin": audit_pin,
            "published_audit_has_machine_source_gate": any(
                n and "machine" in n and "pin" in n for n in gate_names
            ),
            "pristine_gate_source_excerpt": pristine_source,
            "records_pin_direct_check_present": records_check_present,
        },
        "k1146_sweep_machine": {
            "sha256": actual_sweep_sha,
            "expected_sha256": K1146_SWEEP_MACHINE_SHA256,
            "bytes": sweep_path.stat().st_size,
        },
        "k1159_third_verifier": {
            "sha256": actual_third_sha,
            "machine_pin_constant": third_pin,
            "machine_pin_assignment_line": third_pin_line,
            "external_pin_gate_label_present": third_external_pin_present,
        },
        "gates": gates,
        "interpretation": (
            "K1149's 24/24 audit gates do not validate the K1146 sweep-machine source hash: "
            "the 63-character value is metadata-only. K1159 independently pins the actual "
            "64-character source hash and reassembles the published machine, closing this "
            "provenance gap at the third-verification layer. This does not invalidate the "
            "freshly re-executed probe facts and does not close any residual row."
        ),
        "status": "source-pin-gap-confirmed-and-covered-by-k1159" if all(gates.values()) else "failed",
    }
    out = Path(args.output) if args.output else root / "output/k1149-machine-pin-gap-audit-20261121.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    digest = sha256(out)
    print(f"gates: {sum(gates.values())}/{len(gates)} pass")
    print(f"machine pin length: {len(second_pin)} (K1149) vs {len(third_pin)} (K1159)")
    print(f"output sha256: {digest}")
    if not all(gates.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
