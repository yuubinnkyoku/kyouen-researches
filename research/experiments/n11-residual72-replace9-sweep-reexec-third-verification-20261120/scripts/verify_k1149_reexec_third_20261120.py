#!/usr/bin/env python3
"""Third verification of K1149 (replace9 18-probe full re-execution second
verification) via pristine re-execution of the published verification machine,
its pinned runner and inputs, with fresh re-execution of BOTH passes.

Scope (single-owner declaration commit c3c4dd28b48ccf4f5782ddb9f1a81e46d24e4787,
2026-11-20T16:01:30Z):
  1. Pin gate: published machine verify_replace9_reexec_20261120.py, runner v17
     fixed copy (git blob pin), 2 published sweep artifacts (records JSONL +
     volume), 6 upstream ledger inputs, the published sweep machine, and the
     published audit all byte-match their SHA pins.
  2. Fresh pass A: 18 probes re-executed in this tree (4 workers, budget 240s,
     Node runner v17 pinned by git blob). Fresh pass B: 18 probes re-executed
     in an isolated tree/cwd/HOME with copied inputs.
  3. Pristine reassemble: the published sweep machine re-assembled in an
     isolated tree on the published probe records; its output must be
     byte-identical to the published sweep volume.
  4. Assemble: the published verification machine assembles both fresh pass
     records + the pristine volume; its audit must be byte-identical to the
     published audit (24/24 gates). One assemble re-execution with
     PYTHONHASHSEED=random must also be byte-identical.
  5. Tamper test: 1 byte of the K1097 input flipped in a copied tree; the run
     mode must fail closed (nonzero exit, no probe records written).
  6. Emit a deterministic audit JSON (sorted keys, no timestamps, no wall
     timings). Fail-closed.

This harness re-executes the published depth-10 probe facts only. loss=true
(uncapped) is a probe fact, not a certificate; loss=false (uncapped) is a
REFUTED-D10 probe fact, not a LOSS proof; node counts are not win/loss
readings; NO residual row is closed. 11x11 empty board / two-stone roots
{49,60}/{59,60} / S2 {59,60} / classes 1/2/4 remain UNKNOWN.
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

PINNED_FETCH_COMMIT = "87f569328b4f2cc416c0b9b54f0eed0999c1192a"
SOURCE_EXPERIMENT_DIR = "research/experiments/n11-residual72-replace9-sweep-reexec-second-verification-20261120"
SOURCE_SWEEP_DIR = "research/experiments/n11-residual72-replace9-d10-sweep-20261120"
MACHINE_SHA256 = "77cdd9e3450aed9d2c900475f15d9e09367985b909027c50e485995737252db4"
PUBLISHED_AUDIT_SHA256 = "27fc420c58ac0c979e09c3a35b0b0b886fe1b521efea9de8f9f98e51e6264072"
RUNNER_BLOB_PIN = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
SWEEP_MACHINE_SHA256 = "d163b2a120ac46abee40d0b9a32269bce14a73901a85a80e5925b7d2512bcd41"
SWEEP_VOLUME_SHA256 = "e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e"
SWEEP_RECORDS_SHA256 = "bdacf0e7056093145bef917ad384220b70c06be68bdd892b56dd23b3a7d4cb06"
INPUT_PINS = {
    "k1085": "5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e",
    "k1086": "3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced",
    "k1089": "808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc",
    "k1091": "edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25",
    "k1095": "335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707",
    "k1097": "2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40",
}
PIN_NODES_TOTAL = 3_574_172
PIN_PROBES = 18
PIN_TAMPER_OFFSET = 500
TAMPER_INPUT = "k1097.json"
GUARD = [
    "本検証は残余23行のどの行も閉じない",
    "loss=true（uncapped）はdepth-10内必敗のprobe事実の再現であり証明書抽出の資格を与えない",
    "loss=false（uncapped）はREFUTED-D10 probe事実の再現でありLOSS証明ではない",
    "node数・solved数を勝敗として読まない",
    "標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま",
]


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1(path):
    with open(path, "rb") as f:
        raw = f.read()
    digest = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw)
    return digest.hexdigest()


def input_args(root):
    return [
        "--k1085", os.path.join(root, "input/k1085.json"),
        "--k1086", os.path.join(root, "input/k1086.json"),
        "--k1089", os.path.join(root, "input/k1089.json"),
        "--k1091", os.path.join(root, "input/k1091.json"),
        "--k1095", os.path.join(root, "input/k1095.json"),
        "--k1097", os.path.join(root, "input/k1097.json"),
        "--records", os.path.join(root, "input/records.jsonl"),
        "--volume", os.path.join(root, "input/volume.json"),
    ]


def copy_machine_tree(src, dst):
    """Copy machine + runner + inputs + sweep tree (fresh output dirs)."""
    for rel in ("scripts/verify_replace9_reexec_20261120.py",
                "runner_v17.ts", "published-audit.json",
                "sweep/scripts/replace9_d10_sweep_20261120.py",
                "sweep/runner_v17.ts", "sweep/output/probe-records-replace9.jsonl"):
        dst_path = os.path.join(dst, rel)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(os.path.join(src, rel), dst_path)
    for name in ("k1085.json", "k1086.json", "k1089.json", "k1091.json",
                 "k1095.json", "k1097.json", "records.jsonl", "volume.json"):
        os.makedirs(os.path.join(dst, "input"), exist_ok=True)
        shutil.copy2(os.path.join(src, "input", name), os.path.join(dst, "input", name))


def run_pass(root, pass_name, env, tmp, workers=4, budget="240"):
    """Fresh re-execution pass in root. Returns (rc, records_path, stats)."""
    out_dir = os.path.join(root, "output")
    os.makedirs(out_dir, exist_ok=True)
    rec_path = os.path.join(out_dir, "probe-records-reexec-pass%s.jsonl" % pass_name)
    if os.path.exists(rec_path):
        os.remove(rec_path)
    cmd = [sys.executable, os.path.join(root, "scripts/verify_replace9_reexec_20261120.py"),
           "run", budget, "--pass", pass_name, "--workers", str(workers)] + input_args(root)
    proc = subprocess.run(cmd, cwd=root, env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=400)
    stats = {"returncode": proc.returncode,
             "records_written": os.path.exists(rec_path)}
    if stats["records_written"]:
        with open(rec_path, encoding="utf-8") as f:
            recs = [json.loads(line) for line in f if line.strip()]
        nodes = 0
        loss_true = 0
        loss_false = 0
        for r in recs:
            res = r.get("result") or {}
            nodes += int(res.get("nodes", 0))
            if res.get("loss") is True:
                loss_true += 1
            elif res.get("loss") is False:
                loss_false += 1
        stats["records"] = len(recs)
        stats["nodes_sum"] = nodes
        stats["loss_true_probes"] = loss_true
        stats["loss_false_probes"] = loss_false
    return proc.returncode, rec_path, stats


def assemble_audit(root, pass_a_dir, pass_b_dir, pristine_vol, out_path, env):
    cmd = [sys.executable, os.path.join(root, "scripts/verify_replace9_reexec_20261120.py"),
           "assemble",
           "--pass-a", pass_a_dir, "--pass-b", pass_b_dir,
           "--pristine", pristine_vol, "--out", out_path] + input_args(root)
    proc = subprocess.run(cmd, cwd=root, env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def main():
    parser = argparse.ArgumentParser(description="K1149 pristine re-execution third verification harness")
    parser.add_argument("--root", required=True,
                        help="staged experiment root: scripts/ machine + runner + input/ + published-audit.json + sweep/")
    parser.add_argument("--output", required=True, help="path for this harness's audit JSON")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    ambient = {k: v for k, v in os.environ.items() if k != "PYTHONHASHSEED"}

    failures = []
    audit = {
        "harness": "verify_k1149_reexec_third_20261120",
        "subject": "K1149 replace9 sweep re-execution second verification",
        "pinned_fetch_commit": PINNED_FETCH_COMMIT,
        "source_experiment_dir": SOURCE_EXPERIMENT_DIR,
        "source_sweep_dir": SOURCE_SWEEP_DIR,
        "declaration_note": "research/log/2026-11-20-n11-residual72-replace9-sweep-reexec-third-verification-single-owner-note.md",
        "publication": {
            "machine_sha256": MACHINE_SHA256,
            "runner_git_blob": RUNNER_BLOB_PIN,
            "sweep_machine_sha256": SWEEP_MACHINE_SHA256,
            "sweep_volume_sha256": SWEEP_VOLUME_SHA256,
            "sweep_records_sha256": SWEEP_RECORDS_SHA256,
            "published_audit_sha256": PUBLISHED_AUDIT_SHA256,
            "input_pins": dict(INPUT_PINS),
            "targets": {"probes": PIN_PROBES, "nodes_total": PIN_NODES_TOTAL},
        },
        "pin_gates": [],
        "pass_A": {},
        "pass_B": {},
        "pristine_reassemble": {},
        "assemble": {},
        "assemble_hashseed_random": {},
        "tamper_test": {},
        "gates": {},
        "status": None,
        "interpretation_guard": GUARD,
    }

    # ---- Gate 1: pins ----
    pin_items = [
        ("machine_verify_replace9_reexec_20261120.py", os.path.join(root, "scripts/verify_replace9_reexec_20261120.py"), MACHINE_SHA256, "sha256"),
        ("runner_v17.ts", os.path.join(root, "runner_v17.ts"), RUNNER_BLOB_PIN, "git_blob_sha1"),
        ("sweep_machine_replace9_d10_sweep_20261120.py", os.path.join(root, "sweep/scripts/replace9_d10_sweep_20261120.py"), SWEEP_MACHINE_SHA256, "sha256"),
        ("sweep_runner_v17.ts", os.path.join(root, "sweep/runner_v17.ts"), RUNNER_BLOB_PIN, "git_blob_sha1"),
        ("published_audit_replace9-sweep-reexec-second-verification-20261120.json", os.path.join(root, "published-audit.json"), PUBLISHED_AUDIT_SHA256, "sha256"),
        ("sweep_volume_published", os.path.join(root, "input/volume.json"), SWEEP_VOLUME_SHA256, "sha256"),
        ("sweep_records_published", os.path.join(root, "input/records.jsonl"), SWEEP_RECORDS_SHA256, "sha256"),
    ]
    for key, pin in INPUT_PINS.items():
        pin_items.append(("input_%s.json" % key, os.path.join(root, "input/%s.json" % key), pin, "sha256"))
    for label, path, pin, kind in pin_items:
        actual = git_blob_sha1(path) if kind == "git_blob_sha1" else sha256_of(path)
        ok = actual == pin
        if not ok:
            failures.append("pin mismatch %s: expected %s got %s" % (label, pin, actual))
        audit["pin_gates"].append({"label": label, "pin_kind": kind, "expected": pin, "actual": actual, "pass": ok})

    tmp = tempfile.mkdtemp(prefix="k1149-reexec-third-")
    try:
        # ---- Pass A: fresh re-execution in this tree ----
        rc, rec_a, stats_a = run_pass(root, "A", ambient, tmp)
        pass_a_ok = (rc == 0 and stats_a.get("records") == PIN_PROBES
                     and stats_a.get("nodes_sum") == PIN_NODES_TOTAL)
        if not pass_a_ok:
            failures.append("pass A: rc=%r stats=%r" % (rc, stats_a))
        audit["pass_A"] = {"environment": "this tree (ambient, PYTHONHASHSEED unset), 4 workers, fresh regeneration",
                           **stats_a,
                           "matches_published": bool(pass_a_ok)}

        # ---- Pass B: fresh re-execution in isolated tree/cwd/HOME ----
        iso_root = os.path.join(tmp, "passB-tree")
        iso_home = os.path.join(tmp, "passB-home")
        os.makedirs(iso_home, exist_ok=True)
        copy_machine_tree(root, iso_root)
        env_b = {k: v for k, v in os.environ.items() if k not in ("PYTHONHASHSEED", "HOME")}
        env_b["HOME"] = iso_home
        rc_b, rec_b, stats_b = run_pass(iso_root, "B", env_b, tmp)
        pass_b_ok = (rc_b == 0 and stats_b.get("records") == PIN_PROBES
                     and stats_b.get("nodes_sum") == PIN_NODES_TOTAL)
        if not pass_b_ok:
            failures.append("pass B: rc=%r stats=%r" % (rc_b, stats_b))
        audit["pass_B"] = {"environment": "isolated tree/cwd/HOME (PYTHONHASHSEED unset), copied inputs, 4 workers, fresh regeneration",
                           **stats_b,
                           "matches_published": bool(pass_b_ok)}

        # ---- Pristine reassemble: published sweep machine on published records ----
        pr_root = os.path.join(tmp, "pristine-tree")
        copy_machine_tree(root, pr_root)
        cmd = [sys.executable, os.path.join(pr_root, "sweep/scripts/replace9_d10_sweep_20261120.py"),
               "assemble"] + input_args(pr_root)[:12]  # --k1085..--k1097 only
        env_p = {k: v for k, v in os.environ.items() if k != "PYTHONHASHSEED"}
        proc = subprocess.run(cmd, cwd=pr_root, env=env_p,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
        pr_out = os.path.join(pr_root, "sweep/output/replace9-d10-sweep-20261120.json")
        pr_ok = proc.returncode == 0 and os.path.exists(pr_out)
        pr_sha = sha256_of(pr_out) if pr_ok else None
        pr_ident = pr_ok and pr_sha == SWEEP_VOLUME_SHA256
        if not pr_ident:
            failures.append("pristine reassemble: rc=%r sha=%r" % (proc.returncode, pr_sha))
        audit["pristine_reassemble"] = {
            "environment": "isolated tree, published sweep machine, published probe records",
            "returncode": proc.returncode,
            "output_sha256": pr_sha,
            "byte_identical_to_published_volume": bool(pr_ident),
        }

        # ---- Assemble: fresh audit from both fresh passes + pristine volume ----
        fresh_audit = os.path.join(tmp, "third-verification-audit.json")
        rc_asm, out_log = assemble_audit(root, os.path.join(root, "output"),
                                         os.path.join(iso_root, "output"), pr_out,
                                         fresh_audit, ambient)
        asm_exists = os.path.exists(fresh_audit)
        asm_sha = sha256_of(fresh_audit) if asm_exists else None
        asm_ident = rc_asm == 0 and asm_exists and asm_sha == PUBLISHED_AUDIT_SHA256
        if not asm_ident:
            failures.append("assemble: rc=%r sha=%r tail=%r" % (rc_asm, asm_sha, out_log[-200:]))
        audit["assemble"] = {
            "environment": "this tree, fresh passA + fresh passB (isolated) + pristine volume inputs",
            "returncode": rc_asm,
            "output_sha256": asm_sha,
            "byte_identical_to_published_audit": bool(asm_ident),
        }

        # ---- Assemble re-run with PYTHONHASHSEED=random (determinism of machine output) ----
        fresh_audit2 = os.path.join(tmp, "third-verification-audit-hashseed.json")
        env_r = {k: v for k, v in os.environ.items() if k != "PYTHONHASHSEED"}
        env_r["PYTHONHASHSEED"] = "random"
        rc2, out_log2 = assemble_audit(root, os.path.join(root, "output"),
                                       os.path.join(iso_root, "output"), pr_out,
                                       fresh_audit2, env_r)
        asm2_exists = os.path.exists(fresh_audit2)
        asm2_sha = sha256_of(fresh_audit2) if asm2_exists else None
        asm2_ident = rc2 == 0 and asm2_exists and asm2_sha == PUBLISHED_AUDIT_SHA256
        if not asm2_ident:
            failures.append("assemble hashseed-random: rc=%r sha=%r" % (rc2, asm2_sha))
        audit["assemble_hashseed_random"] = {
            "environment": "same inputs, PYTHONHASHSEED=random",
            "returncode": rc2,
            "output_sha256": asm2_sha,
            "byte_identical_to_published_audit": bool(asm2_ident),
        }

        # ---- Tamper gate: 1 byte of K1097 flipped in a copied tree, run mode ----
        tam_root = os.path.join(tmp, "tamper-tree")
        copy_machine_tree(root, tam_root)
        tam_input = os.path.join(tam_root, "input", TAMPER_INPUT)
        with open(tam_input, "rb") as f:
            data = bytearray(f.read())
        pos = PIN_TAMPER_OFFSET
        data[pos] = data[pos] ^ 0x01
        with open(tam_input, "wb") as f:
            f.write(bytes(data))
        env_t = {k: v for k, v in os.environ.items() if k != "PYTHONHASHSEED"}
        rc_t, rec_t, stats_t = run_pass(tam_root, "A", env_t, tmp)
        failed_closed = rc_t != 0
        no_records = not stats_t["records_written"]
        audit["tamper_test"] = {
            "mutation": "1 byte flipped at offset %d (XOR 0x01) of input/%s in a copied tree (run mode)" % (pos, TAMPER_INPUT),
            "mutated_input_sha256": sha256_of(tam_input),
            "returncode": rc_t,
            "failed_closed": bool(failed_closed),
            "no_probe_records_written": bool(no_records),
            "pin_caught_mutation": bool(failed_closed and no_records),
        }
        if not (failed_closed and no_records):
            failures.append("tamper gate failed")

        audit["gates"] = {
            "pin_gate": len(audit["pin_gates"]) == len(pin_items) and all(g["pass"] for g in audit["pin_gates"]),
            "pass_A_gate": bool(pass_a_ok),
            "pass_B_gate": bool(pass_b_ok),
            "pristine_reassemble_gate": bool(pr_ident),
            "assemble_gate": bool(asm_ident),
            "assemble_hashseed_random_gate": bool(asm2_ident),
            "tamper_gate": bool(failed_closed and no_records),
        }
        if not all(audit["gates"].values()):
            failures.append("one or more gates failed: %r" % audit["gates"])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    audit["status"] = "k1149-reexec-third-verification-passed" if not failures else "k1149-reexec-third-verification-failed"
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
    print("ALL GATES PASS: pins %d/%d, passA/passB fresh 18-probe re-runs nodes_sum %d, pristine reassemble byte-identical, assemble byte-identical, hashseed-random byte-identical, tamper caught"
          % (len(pin_items), len(pin_items), PIN_NODES_TOTAL))


if __name__ == "__main__":
    main()
