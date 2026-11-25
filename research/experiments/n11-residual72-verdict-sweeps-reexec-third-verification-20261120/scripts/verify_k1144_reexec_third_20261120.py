#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Third verification (post-publication pristine re-execution) of K1144:
the residual72 4-sweep (K1086 greedy23 / K1089 replace16 / K1091 replace15 /
K1095 replace12) depth-10 132-probe full re-execution second verification.

A post-publication third party re-fetched the published bytes, re-executed
the published machine's two-pass full re-implementation (132 probes per
pass, pinned runner v17 git blob), and confirmed that

  (a) every fetched input matches its SHA-256 / git-blob pin,
  (b) four fresh machine re-executions (runA same-cwd, runB isolated
      tree/cwd/HOME, runC same-cwd PYTHONHASHSEED=random, runD same-cwd
      PYTHONHASHSEED=0) each reproduce all 132 probes with zero errors and
      deterministic fields byte-equal to the published second-verification
      records, with the published nodes total 37,454,794 in every pass,
  (c) the machine's canonical assemble audit regenerated from the fresh
      runs is byte-identical to the published audit
      6297c646c32a0b1e0643f9f727fe712d1135dad15c0f5b0418ba8b3350596637
      for all three passA-variant x passB pairings,
  (d) 1-byte input tampering (record JSON offset 500 XOR 0x01; probe
      JSONL offset 300 XOR 0x01) is caught fail-closed by the machine's
      SHA-256 pins before any probing, and no output records are written.

Design note (structural difference from the K1147/K1158 third
verification): the second-verification machine records wall-clock seconds
(`wall_s`) inside its per-probe JSONL run outputs, so the run JSONLs of the
original publication are NOT byte-reproducible by construction; the
byte-reproducible canonical artifact of that machine is its assemble-mode
audit JSON. This harness therefore pins the published run JSONLs as
provenance and reproduces *semantic equality of deterministic fields plus
canonical-audit byte equality*. No timestamps, wall times, absolute paths,
randomness, or environment-dependent values enter this harness's own
audit JSON, which is emitted with sorted keys.

Fail-closed: any pin mismatch, field mismatch, gate failure, or missing
input aborts with a nonzero exit before the audit JSON is written.
stdlib only. Deterministic. No network access.

Usage:
  python3 verify_k1144_reexec_third_20261120.py [--exp-root DIR]
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# pinned SHA-256 of the published second verification (commit c84e2b0e...)
# ---------------------------------------------------------------------------
PIN_MACHINE = ("verify_sweeps_reexec_20261120.py",
               "7f0729840a3cd6c8f3010cc16de4c5e9d8f19e8f81fa0b1687e64b9a0e8f0228")
RUNNER_BLOB_PIN = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
PIN_PUB_PASS_A = ("published-probe-records-reexec-passA.jsonl",
                  "1ade916b06f887c622449613f068f99bd2bf93404527a397ee2438c0f22f6f12")
PIN_PUB_PASS_B = ("published-probe-records-reexec-passB.jsonl",
                  "e351f6cc64eca23f1b68d1811a65779e20d1ab727f0ac48e9c4a7b3624845897")
PIN_PUB_AUDIT = ("published-verdict-sweeps-reexec-second-verification-20261120.json",
                 "6297c646c32a0b1e0643f9f727fe712d1135dad15c0f5b0418ba8b3350596637")
PIN_SWEEP_ORDER = ["n11-residual72-addtwo-greedy23-d10-sweep-20261120",
                   "n11-residual72-replace16-d10-sweep-20261120",
                   "n11-residual72-replace15-d10-sweep-20261120",
                   "n11-residual72-replace12-d10-sweep-20261120"]

PIN_RUNNER_TS = ("runner_v17.ts",
                 "192903714b1b06a8ea58aa80e22da23fcf9d9ef175830a65a0da5eb0ca64f3d4")
PIN_SWEEPS = {
    "n11-residual72-addtwo-greedy23-d10-sweep-20261120": (
        "addtwo-greedy23-d10-sweep-20261120.json",
        "3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced",
        "probe-records-add2greedy23.jsonl",
        "773fef4262a9c69766402d3c0f846f5569ce095107efedaa02a76690ab35b8f3"),
    "n11-residual72-replace16-d10-sweep-20261120": (
        "replace16-d10-sweep-20261120.json",
        "808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc",
        "probe-records-replace16.jsonl",
        "75fda6ade767e731ba4e42049230bcea6498eee6e9b2348a9d909a1832f329f6"),
    "n11-residual72-replace15-d10-sweep-20261120": (
        "replace15-d10-sweep-20261120.json",
        "edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25",
        "probe-records-replace15.jsonl",
        "47165331b68f10684db9217a18fd3a2aab6748ecf1191f0216905981737a773a"),
    "n11-residual72-replace12-d10-sweep-20261120": (
        "replace12-d10-sweep-20261120.json",
        "335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707",
        "probe-records-replace12.jsonl",
        "89e2c30d93fc26b5f760c3f9f00c6190595e6adc2fd6320fd2ac69a2603f9c56"),
}

NODES_TOTAL = 37_454_794
PROBES = 132
PILOT_D6_NODES = 3402


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git_blob_sha1(p):
    data = Path(p).read_bytes()
    h = hashlib.sha1()
    h.update(b"blob %d\0" % len(data))
    h.update(data)
    return h.hexdigest()


def load_jsonl_records(p):
    recs = []
    for line in Path(p).read_text(encoding="utf-8").splitlines():
        if line.strip():
            recs.append(json.loads(line))
    return recs


def det_fields(rec):
    """Deterministic projection of a run record (excludes wall_s)."""
    r = {k: rec.get(k) for k in ("label", "root", "ordering", "depth", "bit",
                                 "child", "cap", "timeout_s")}
    res = rec.get("result") or {}
    r["result"] = {k: res.get(k) for k in ("nodes", "loss", "capped",
                                           "terminalStoneRange")}
    ctl = rec.get("control") or {}
    r["control_nodes"] = ctl.get("nodes")
    r["has_error"] = bool(rec.get("error"))
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp-root", default=str(EXP))
    args = ap.parse_args()
    exp = Path(args.exp_root)
    inp = exp / "input"
    runs = exp / "fresh-runs"
    out_path = exp / "output" / "third-verification-audit-20261120.json"

    pins = []
    gates = []
    fails = []

    def pin(name, path, want, kind="sha256"):
        got = sha256_file(path) if kind == "sha256" else git_blob_sha1(path)
        ok = got == want
        pins.append({"name": name, "kind": kind, "sha": got, "match": ok})
        if not ok:
            fails.append(f"pin-mismatch {name}")
        return ok

    # ---- gate 1: published input pins -----------------------------------
    pin("second-verification-machine", inp / PIN_MACHINE[0], PIN_MACHINE[1])
    pin("pinned-runner_v17.ts", inp / PIN_RUNNER_TS[0], PIN_RUNNER_TS[1])
    blob_ok = git_blob_sha1(inp / PIN_RUNNER_TS[0]) == RUNNER_BLOB_PIN
    pin("runner-git-blob", inp / PIN_RUNNER_TS[0], RUNNER_BLOB_PIN, kind="blob")
    pin("published-passA-jsonl", inp / PIN_PUB_PASS_A[0], PIN_PUB_PASS_A[1])
    pin("published-passB-jsonl", inp / PIN_PUB_PASS_B[0], PIN_PUB_PASS_B[1])
    pin("published-assembly-audit", inp / PIN_PUB_AUDIT[0], PIN_PUB_AUDIT[1])
    for d in PIN_SWEEP_ORDER:
        jf, jp, lf, lp = PIN_SWEEPS[d]
        pin(f"{d}/record-json", inp / "sweeps" / d / "output" / jf, jp)
        pin(f"{d}/probe-jsonl", inp / "sweeps" / d / "output" / lf, lp)
    n_pins = len(pins)
    gates.append({"name": "input-pin-gate",
                  "pass": not fails,
                  "detail": {"pins_checked": n_pins,
                             "content_sha256_pins": n_pins - 1,
                             "git_blob_pins": 1}})
    if fails:
        print(json.dumps({"error": fails}, indent=2))
        return 1

    # ---- gate 2: semantic equality of the 4 fresh runs ------------------
    pub_a = load_jsonl_records(inp / PIN_PUB_PASS_A[0])
    pub_b = load_jsonl_records(inp / PIN_PUB_PASS_B[0])

    def index_by_key(recs):
        return {(r["label"], r["root"], r["ordering"]): r for r in recs}

    idx_a, idx_b = index_by_key(pub_a), index_by_key(pub_b)
    if len(pub_a) != PROBES or len(pub_b) != PROBES:
        print("published pass records != 132")
        return 1

    run_defs = [
        ("runA-same-cwd", "probe-records-reexec-passA.jsonl", idx_a),
        ("runB-isolated-cwd-home", "probe-records-reexec-passB.jsonl", idx_b),
        ("runC-same-cwd-hashseed-random", "probe-records-reexec-passA.jsonl", idx_a),
        ("runD-same-cwd-hashseed-0", "probe-records-reexec-passA.jsonl", idx_a),
    ]
    fresh_summary = {}
    run_ok = True
    for name, fname, ref in run_defs:
        path = runs / name / fname
        if not path.exists():
            fails.append(f"missing fresh run {name}")
            run_ok = False
            continue
        recs = load_jsonl_records(path)
        bad = []
        nodes_total = 0
        controls_ok = 0
        for r in recs:
            det = det_fields(r)
            if det["has_error"]:
                bad.append({"why": "error-field", "key": det["label"]})
                continue
            nodes_total += det["result"]["nodes"] or 0
            if det["control_nodes"] == PILOT_D6_NODES:
                controls_ok += 1
            if r.get("wall_s") is None:
                bad.append({"why": "wall-missing", "key": det["label"]})
        # semantic compare against published
        idx = index_by_key(recs)
        mism = 0
        for key, pref in ref.items():
            mine = idx.get(key)
            if mine is None or det_fields(mine) != det_fields(pref):
                mism += 1
        ok = (len(recs) == PROBES and not bad and mism == 0
              and nodes_total == NODES_TOTAL and controls_ok == PROBES)
        fresh_summary[name] = {
            "records": len(recs),
            "errors": sum(1 for b in bad),
            "mismatches_vs_published": mism,
            "nodes_total": nodes_total,
            "pilot_d6_controls": controls_ok,
            "wall_seconds_present": all(r.get("wall_s") is not None
                                       for r in recs),
        }
        run_ok &= ok
    gates.append({"name": "fresh-run-semantic-gate",
                  "pass": run_ok,
                  "detail": {"runs": 4, "probes_per_run": PROBES,
                             "nodes_total": NODES_TOTAL,
                             "runs": fresh_summary}})
    if not run_ok:
        fails.append("fresh-run-semantic-gate")
        print(json.dumps({"error": fails}, indent=2))
        return 1

    # ---- gate 3: assemble canonical byte reproduction -------------------
    tmp = Path(tempfile.mkdtemp(prefix="k1144-third-"))
    try:
        machine_dir = tmp / "exp"
        (machine_dir / "scripts").mkdir(parents=True, exist_ok=True)
        shutil.copy2(inp / PIN_MACHINE[0], machine_dir / "scripts" / PIN_MACHINE[0])
        shutil.copy2(inp / PIN_RUNNER_TS[0], machine_dir / PIN_RUNNER_TS[0])
        (machine_dir / "output").mkdir(exist_ok=True)
        sweeps_root = inp / "sweeps"
        pairs = [("runA-same-cwd", "runB-isolated-cwd-home"),
                 ("runC-same-cwd-hashseed-random", "runB-isolated-cwd-home"),
                 ("runD-same-cwd-hashseed-0", "runB-isolated-cwd-home")]
        pair_info = []
        assembles_ok = True
        machine = machine_dir / "scripts" / PIN_MACHINE[0]
        if sha256_file(machine) != PIN_MACHINE[1]:
            fails.append("machine-copy-pin")
            print(json.dumps({"error": fails}, indent=2))
            return 1
        for a, b in pairs:
            out = tmp / f"assemble-{a}-x-{b}.json"
            cmd = [sys.executable, str(machine_dir / "scripts" / PIN_MACHINE[0]),
                   "assemble",
                   "--pass-a", str(runs / a),
                   "--pass-b", str(runs / b),
                   "--inputs", str(sweeps_root),
                   "--out", str(out)]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=280)
            got = sha256_file(out) if out.exists() else None
            pub_bytes = (inp / PIN_PUB_AUDIT[0]).read_bytes()
            byte_same = out.exists() and out.read_bytes() == pub_bytes
            ok = r.returncode == 0 and got == PIN_PUB_AUDIT[1] and byte_same
            pair_info.append({"pair": [a, b], "returncode": r.returncode,
                              "audit_sha256": got,
                              "byte_identical_to_published": bool(byte_same)})
            assembles_ok &= ok
        gates.append({"name": "assemble-canonical-byte-gate",
                      "pass": assembles_ok,
                      "detail": {"pairs": pair_info,
                                 "canonical_sha256": PIN_PUB_AUDIT[1]}})
        if not assembles_ok:
            fails.append("assemble-canonical-byte-gate")
            print(json.dumps({"error": fails}, indent=2))
            return 1

        # ---- gate 4: tamper fail-closed --------------------------------
        tamper_info = []
        tampers = [
            ("k1086-record-json-offset500",
             "n11-residual72-addtwo-greedy23-d10-sweep-20261120/output/addtwo-greedy23-d10-sweep-20261120.json",
             500, "83520f33df362ebf65e4fa69c05252cf733457c835b9a112c4f7257bbf63425a"),
            ("k1095-probe-jsonl-offset300",
             "n11-residual72-replace12-d10-sweep-20261120/output/probe-records-replace12.jsonl",
             300, "b6cf0f8601c7d635fcc4ec5545743072842598ab335e43268098013834b068d1"),
        ]
        tampers_ok = True
        for tname, rel, off, want_sha in tampers:
            troot = tmp / ("tampered-" + tname)
            shutil.copytree(sweeps_root, troot)
            target = troot / rel
            data = bytearray(target.read_bytes())
            data[off] ^= 0x01
            target.write_bytes(bytes(data))
            got_sha = hashlib.sha256(bytes(data)).hexdigest()
            trec = tmp / ("tamper-records-" + tname)
            trec.mkdir(exist_ok=True)
            cmd = [sys.executable, str(machine_dir / "scripts" / PIN_MACHINE[0]),
                   "run", "5", "--pass", "T", "--inputs", str(troot),
                   "--root", str(trec)]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            wrote = (trec / "probe-records-reexec-passT.jsonl").exists()
            ok = (r.returncode != 0 and "sha256 pin FAIL" in (r.stdout + r.stderr)
                  and not wrote and got_sha == want_sha)
            tamper_info.append({"name": tname, "offset": off, "xor": "0x01",
                               "tampered_sha256": got_sha,
                               "returncode": r.returncode,
                               "fail_closed_message":
                                   "sha256 pin FAIL" in (r.stdout + r.stderr),
                               "records_written": bool(wrote)})
            tampers_ok &= ok
        gates.append({"name": "tamper-fail-closed-gate",
                      "pass": tampers_ok,
                      "detail": {"variants": tamper_info, "count": 2}})
        if not tampers_ok:
            fails.append("tamper-fail-closed-gate")
            print(json.dumps({"error": fails}, indent=2))
            return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ---- canonical audit -------------------------------------------------
    audit = {
        "schema": "n11-residual72-verdict-sweeps-reexec-third-verification-20261120-v1",
        "status": "k1144-reexec-third-verification-passed",
        "target": {
            "item": "K1144",
            "second_verification_publication": "commit c84e2b0e",
            "machine": PIN_MACHINE[1],
            "runner_blob": RUNNER_BLOB_PIN,
            "published_assembly_audit_sha256": PIN_PUB_AUDIT[1],
        },
        "pins": pins,
        "gates": gates,
        "fresh_runs": fresh_summary,
        "interpretation_guard": {
            "rows_closed": 0,
            "refuted_d10_is_not_a_loss_proof": True,
            "win8_d10_candidates_are_not_certificates": True,
            "nodes_and_solved_counts_are_not_win_loss": True,
            "standard_11x11_empty_board_unknown": True,
            "two_stone_roots_unknown": "{49,60}/{59,60} and S2 {59,60} and classes 1/2/4 remain UNKNOWN",
        },
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    print("all gates pass; audit written:", out_path)
    print("audit sha256:", sha256_file(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
