#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
K1136/K1137/K1139 WIN8-D10 certificate extraction external re-execution
second verification harness (2026-11-20).

Single-owner declaration:
  research/log/2026-11-20-n11-k1136-k1137-k1139-cert-extract-ext-second-verification-single-owner-note.md
  (commit c9d5b415a8, declaration-first).

Protocol: pin the 61 published files of the three certificate-extraction
experiment dirs by git blob SHA (repo pin commit 28d223a2d, reconstructed by
fetch_master.py), then re-execute from the pinned bytes, per root:
  (1) runner v17 probes (both AND orderings x2 + pilot control each),
  (2) extraction A1 (fresh process per root first-move, pool size 2),
  (3) extraction A2 (full re-execution of A1),
  (4) extraction B (single-process batch over all first moves),
  (5) certificate assembly (header + root line + sort -u of A1 rows)
      compared byte-identical with the published certificate,
  (6) BigInt independent verifier (byte-identical stdout),
  (7) Bareiss verifier root-check and per-subroot stats (byte-identical),
  (8) the published 19-gate audit machine, pristine re-run
      (same cwd x2 + isolated experiment-root x1), byte-identical with the
      published audit master, and once with OUR fresh summaries/probe
      records substituted (gates must still pass),
  (9) three tamper cases at publisher-untested offsets (fail-closed).

ms fields (wall-clock) in summaries and probe records are timing-dependent
and are NOT reproduction targets; all deterministic fields must match.
The harness audit JSON contains no timing data (byte-deterministic).

Usage (each stage fits well under a 300s command cap):
  python3 verify_cert_extract_ext_second_20261120.py --stage pin
  python3 verify_cert_extract_ext_second_20261120.py --stage root --root k1136
  python3 verify_cert_extract_ext_second_20261120.py --stage root --root k1137
  python3 verify_cert_extract_ext_second_20261120.py --stage root --root k1139
  python3 verify_cert_extract_ext_second_20261120.py --stage tampers
  python3 verify_cert_extract_ext_second_20261120.py --stage finalize

Interpretation guard: this harness closes no rows. REFUTED-D10 is not a LOSS
proof. Nodes/solved counts are never read as win/loss. The standard 11x11
emptied board, two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4
remain UNKNOWN. Residual rows and pool 120,416 unchanged.

Machine: python3 stdlib only. CPU-parallelism capped at 2 (2-core sandbox).
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
MASTER_DIR = os.path.abspath(os.path.join(HERE, "master"))
RUN_DIR = os.path.abspath(os.path.join(HERE, "run"))
PARTS_DIR = os.path.join(RUN_DIR, "parts")
NODE = "node"

with open(os.path.join(HERE, "pin-manifest.json"), "r", encoding="utf-8") as f:
    PIN = json.load(f)

ROOTS = [
    {
        "key": "k1136",
        "staging": "n11-residual29-win8-cert-extract-root438000000818-20261120",
        "master": "research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120",
        "root": "00000000000000043800000008180010",
        "child": "00000000000000043800000008180000",
        "bit": 4, "cap": 4000000,
        "n_moves": 50, "mobility": 50,
        "ac1_nodes": 882327, "ac0_nodes": 1054873,
        "cert": "win8-root-00000000000000043800000008180010-20261120.n11",
        "extractor": "scripts/cert_extractor_win8_root00000000000000043800000008180010.ts",
        "assembler": "scripts/assemble_win8_audit_root438000000818.py",
        "term": "14,18",
    },
    {
        "key": "k1137",
        "staging": "n11-residual29-win8-cert-extract-root00000000000200003800200008180000-20261120",
        "master": "research/experiments/n11-residual29-win8-cert-extract-root00000000000200003800200008180000-20261120",
        "root": "00000000000200003800200008180000",
        "child": "00000000000200003800200008100000",
        "bit": 19, "cap": 30000000,
        "n_moves": 42, "mobility": 42,
        "ac1_nodes": 261294, "ac0_nodes": 288448,
        "cert": "win8-root-00000000000200003800200008180000-20261120.n11",
        "extractor": "scripts/cert_extractor_win8_root00000000000200003800200008180000.ts",
        "assembler": "scripts/assemble_win8_audit_root00000000000200003800200008180000.py",
        "term": "14,18",
    },
    {
        "key": "k1139",
        "staging": "n11-residual29-win8-cert-extract-root0810000a-20261120",
        "master": "research/experiments/n11-residual29-win8-cert-extract-root0810000a-20261120",
        "root": "0000000800000000380000000810000a",
        "child": "00000008000000003800000008100008",
        "bit": 1, "cap": 4000000,
        "n_moves": 58, "mobility": 58,
        "ac1_nodes": 1226804, "ac0_nodes": 1416679,
        "cert": "win8-root-0000000800000000380000000810000a-20261120.n11",
        "extractor": "scripts/cert_extractor_win8_root0000000800000000380000000810000a.ts",
        "assembler": "scripts/assemble_win8_audit_root0000000800000000380000000810000a.py",
        "term": "14,18",
    },
]

HEADER_LINE = "n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS"


def new_gate_map():
    return {}


def gate(GATES, name, ok, detail=None):
    GATES[name] = {"pass": bool(ok)}
    if detail is not None:
        GATES[name]["detail"] = detail
    print(("PASS " if ok else "FAIL ") + name +
          ((" :: " + json.dumps(detail, ensure_ascii=False)) if detail else ""))
    return bool(ok)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def git_blob_sha(path):
    data = open(path, "rb").read()
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def sh(cmd, cwd, env=None, timeout=2400, stdout=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    if stdout:
        with open(stdout, "wb") as sink:
            return subprocess.run(cmd, cwd=cwd, env=e, stdout=sink,
                                  stderr=subprocess.PIPE, timeout=timeout)
    return subprocess.run(cmd, cwd=cwd, env=e, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=timeout)


def parse_records(path):
    recs = []
    for line in open(path, "r", encoding="utf-8"):
        line = line.strip()
        if line:
            recs.append(json.loads(line))
    return recs


def scrub_ms(obj):
    """deep-copy obj dropping timing-dependent fields (ms / wall)."""
    if isinstance(obj, dict):
        return {k: scrub_ms(v) for k, v in obj.items() if k not in ("ms", "wall_s")}
    if isinstance(obj, list):
        return [scrub_ms(v) for v in obj]
    return obj


def copy_stage(cfg, dest):
    shutil.copytree(os.path.join(MASTER_DIR, cfg["master"]), dest)


def write_part(name, obj):
    os.makedirs(PARTS_DIR, exist_ok=True)
    with open(os.path.join(PARTS_DIR, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def stage_pin():
    n, fail, fails = 0, 0, []
    for repo_path, meta in PIN["files"].items():
        p = os.path.join(MASTER_DIR, repo_path)
        n += 1
        if not os.path.exists(p):
            fail += 1
            fails.append(repo_path)
            continue
        data = open(p, "rb").read()
        if len(data) != meta["size"] or git_blob_sha(p) != meta["sha"]:
            fail += 1
            fails.append(repo_path)
    G = new_gate_map()
    gate(G, "g_pin_published_61_files", fail == 0 and n == 61,
         {"checked": n, "mismatch_or_missing": fail, "bad": fails})
    write_part("pin.json", {"gates": G})
    return 0 if all(v["pass"] for v in G.values()) else 1


def run_probes(cfg, fresh_dir, stage_dir):
    out = os.path.join(fresh_dir, "probe-fresh.jsonl")
    # publisher order: ac1, ac1, ac0, ac0 (each invocation writes pilot + probe)
    for ac in (1, 1, 0, 0):
        p = sh([NODE, "--experimental-strip-types", "runner_v17.ts",
                "--child", cfg["child"], "--bits", str(cfg["bit"]),
                "--depth", "10", "--cap", str(cfg["cap"]),
                "--andclose", str(ac), "--out", os.path.abspath(out)],
               cwd=stage_dir, timeout=1800)
        if p.returncode != 0:
            return False, {"error": "runner returncode", "rc": p.returncode,
                           "stderr": p.stderr.decode()[:200]}
    pub = parse_records(os.path.join(MASTER_DIR, cfg["master"], "output",
                                     "probe-repro-both-orderings.jsonl"))
    fre = parse_records(out)
    if len(pub) != len(fre) or len(fre) != 8:
        return False, {"len": [len(pub), len(fre)]}
    ok = scrub_ms(pub) == scrub_ms(fre)
    det = {"records": len(fre), "ac1_nodes": fre[1]["nodes"],
           "ac0_nodes": fre[5]["nodes"]}
    return ok, det


def compare_summaries(fresh_path, pub_path, label):
    pub = parse_records(pub_path)
    fre = parse_records(fresh_path)
    if len(pub) != len(fre):
        return False, {"label": label, "len": [len(pub), len(fre)]}
    # per-move map comparison (order-insensitive: the k1139 publisher stored
    # its a1/a2 lines in lexicographic move order, k1136/k1137 in ascending
    # numeric order; per-move values are the reproduction target).
    pm_pub = {r["moves"]: scrub_ms(r) for r in pub}
    pm_fre = {r["moves"]: scrub_ms(r) for r in fre}
    set_ok = set(pm_pub) == set(pm_fre)
    val_ok = set_ok and all(pm_pub[k] == pm_fre[k] for k in pm_pub)
    tp = sum(r.get("sum", 0) for r in pub)
    tf = sum(r.get("sum", 0) for r in fre)
    if not val_ok:
        diffs = [k for k in pm_pub if k in pm_fre and pm_pub[k] != pm_fre[k]]
        return False, {"label": label, "moves": [len(pm_pub), len(pm_fre)],
                       "value_diffs": diffs[:10]}
    return (tp == tf), {
        "label": label, "records": len(fre), "moves": len(pm_fre),
        "per_move_values_identical": True, "line_order_note": {
            "published_a1_a2": "k1139 lexicographic / k1136,k1137 xargs-numeric",
            "fresh": "ascending-numeric",
            "note": "line order is a publisher transport detail, not a "
                    "reproduction target; per-move values match exactly"},
        "pub_total_sum": tp, "fresh_total_sum": tf}


def run_extraction_chunked(cfg, stage_dir, fresh_dir, label):
    """A1/A2: fresh process per root first-move, ThreadPool size 2."""
    moves = [int(x) for x in open(os.path.join(MASTER_DIR, cfg["master"], "output",
                                               "root-legal-moves.txt")).read().strip().split(",")]
    rows_dir = os.path.join(fresh_dir, "rows-" + label)
    os.makedirs(rows_dir, exist_ok=True)
    summary_out = os.path.join(fresh_dir, "ext-summary-" + label + ".jsonl")
    results = {}

    def one(m):
        sm = os.path.join(fresh_dir, "summary-%s-m%d.jsonl" % (label, m))
        rows = os.path.join(rows_dir, "rows-m%d.txt" % m)
        p = sh([NODE, "--experimental-strip-types", cfg["extractor"],
                "--root", cfg["root"], "--moves", str(m), "--subtree-depth", "9",
                "--summary-out", os.path.abspath(sm), "--rows-out", os.path.abspath(rows)],
               cwd=stage_dir, timeout=3600)
        return m, p.returncode

    with ThreadPoolExecutor(max_workers=2) as ex:   # 2-core sandbox
        for m, rc in ex.map(one, moves):
            results[m] = rc
    bad = {m: rc for m, rc in results.items() if rc != 0}
    if bad:
        return False, {"bad_moves": {str(k): v for k, v in bad.items()}}
    with open(summary_out, "wb") as out:
        for m in moves:
            with open(os.path.join(fresh_dir, "summary-%s-m%d.jsonl" % (label, m)), "rb") as sm:
                out.write(sm.read())
    for m in moves:
        os.remove(os.path.join(fresh_dir, "summary-%s-m%d.jsonl" % (label, m)))
    return True, {"moves": len(moves)}


def run_extraction_batch(cfg, stage_dir, fresh_dir, label):
    moves = open(os.path.join(MASTER_DIR, cfg["master"], "output",
                              "root-legal-moves.txt")).read().strip()
    sm = os.path.join(fresh_dir, "ext-summary-" + label + ".jsonl")
    rows = os.path.join(fresh_dir, "rows-batch-" + label + ".txt")
    p = sh([NODE, "--experimental-strip-types", cfg["extractor"],
            "--root", cfg["root"], "--moves", moves, "--subtree-depth", "9",
            "--summary-out", os.path.abspath(sm), "--rows-out", os.path.abspath(rows)],
           cwd=stage_dir, timeout=3600)
    if p.returncode != 0:
        return False, {"returncode": p.returncode, "stderr": p.stderr.decode()[:200]}
    return True, {"ok": True}


def assemble_cert(cfg, fresh_rows_dir, fresh_rows_batch, dest):
    """header + root line + sort -u of the A1 chunk rows (B row set cross-checked)."""
    rows = []
    for fn in sorted(os.listdir(fresh_rows_dir)):
        with open(os.path.join(fresh_rows_dir, fn), "r", encoding="utf-8") as f:
            rows.extend(l for l in f.read().splitlines() if l.strip())
    batch = [l for l in open(fresh_rows_batch, "r", encoding="utf-8").read().splitlines() if l.strip()]
    same_set = sorted(set(rows)) == sorted(set(batch))
    lines = [HEADER_LINE, "root " + cfg["root"]] + sorted(set(rows))
    with open(dest, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return same_set, len(lines) - 2


def run_audit(cfg, stage_dir, out_path, env=None, cwd=None):
    return sh([sys.executable, os.path.join(stage_dir, cfg["assembler"]),
               "--experiment-root", stage_dir, "--out", out_path],
              cwd=cwd or stage_dir, env=env, timeout=2400)


def audit_result(p, out_path, pub_bytes):
    ok_json = gates_pass = byte_id = False
    failing = None
    if os.path.exists(out_path):
        try:
            j = json.load(open(out_path))
            ok_json = True
            gates_pass = bool(j.get("all_gates_pass")) and j.get("gate_count") == 19
            byte_id = open(out_path, "rb").read() == pub_bytes
            failing = [g["gate"] for g in j.get("gates", []) if not g.get("passed")]
        except Exception:
            pass
    return {"returncode": p.returncode, "json_parseable": ok_json,
            "19_gates_pass": gates_pass, "byte_identical": byte_id,
            "failing_gates": failing}


def stage_root(key):
    cfg = next(r for r in ROOTS if r["key"] == key)
    G = new_gate_map()
    fresd = os.path.join(RUN_DIR, "fresh", key)
    os.makedirs(fresd, exist_ok=True)
    stage = os.path.join(RUN_DIR, "stage", key)
    if os.path.exists(stage):
        shutil.rmtree(stage)
    os.makedirs(os.path.dirname(stage), exist_ok=True)
    copy_stage(cfg, stage)

    # ---- probes ----
    ok, det = run_probes(cfg, fresd, stage)
    det = det if isinstance(det, dict) else {"error": str(det)}
    gate(G, key + "_probe_repro", ok, det)

    # ---- extraction A1 ----
    ok, det = run_extraction_chunked(cfg, stage, fresd, "a1")
    if ok:
        ok, det = compare_summaries(
            os.path.join(fresd, "ext-summary-a1.jsonl"),
            os.path.join(MASTER_DIR, cfg["master"], "output", "ext-summary-a1.jsonl"), "a1")
    gate(G, key + "_ext_a1_match", ok, det)

    # ---- extraction A2 ----
    ok, det = run_extraction_chunked(cfg, stage, fresd, "a2")
    if ok:
        ok, det = compare_summaries(
            os.path.join(fresd, "ext-summary-a2.jsonl"),
            os.path.join(MASTER_DIR, cfg["master"], "output", "ext-summary-a2.jsonl"), "a2")
    gate(G, key + "_ext_a2_match", ok, det)

    # ---- A1 == A2 per-move values + per-move rows byte identity ----
    det_eq = {}
    pm1 = {r["moves"]: scrub_ms(r) for r in parse_records(os.path.join(fresd, "ext-summary-a1.jsonl"))}
    pm2 = {r["moves"]: scrub_ms(r) for r in parse_records(os.path.join(fresd, "ext-summary-a2.jsonl"))}
    val_eq = set(pm1) == set(pm2) and all(pm1[k] == pm2[k] for k in pm1)
    rows_eq = True
    rd1, rd2 = os.path.join(fresd, "rows-a1"), os.path.join(fresd, "rows-a2")
    for fn in sorted(os.listdir(rd1)):
        if open(os.path.join(rd1, fn), "rb").read() != open(os.path.join(rd2, fn), "rb").read():
            rows_eq = False
            break
    gate(G, key + "_ext_a1_equals_a2", val_eq and rows_eq,
         {"per_move_values_equal": val_eq, "per_move_rows_byte_identical": rows_eq})

    # ---- extraction B ----
    ok, det = run_extraction_batch(cfg, stage, fresd, "b")
    if ok:
        ok, det = compare_summaries(
            os.path.join(fresd, "ext-summary-b.jsonl"),
            os.path.join(MASTER_DIR, cfg["master"], "output", "ext-summary-b.jsonl"), "b")
    gate(G, key + "_ext_b_match", ok, det)

    # ---- certificate assembly byte-identical to published ----
    cert_fresh = os.path.join(fresd, "cert-fresh.n11")
    same_set, nrows = assemble_cert(cfg, os.path.join(fresd, "rows-a1"),
                                    os.path.join(fresd, "rows-batch-b.txt"), cert_fresh)
    pub_cert = os.path.join(MASTER_DIR, cfg["master"], "certs", cfg["cert"])
    pub_cert_lines = sum(1 for _ in open(pub_cert, "rb"))
    sha_fresh = sha256_file(cert_fresh)
    sha_pub = sha256_file(pub_cert)
    byte_id = open(cert_fresh, "rb").read() == open(pub_cert, "rb").read()
    gate(G, key + "_cert_assembly_byte_identical",
         byte_id and same_set and nrows == pub_cert_lines - 2,
         {"fresh_sha256": sha_fresh, "published_sha256": sha_pub,
          "rows_total": nrows, "published_cert_lines": pub_cert_lines,
          "batch_rowset_equal": same_set})

    # ---- BigInt verifier ----
    big_out = os.path.join(fresd, "bigint-fresh.json")
    p = sh([NODE, "scripts/verify_win8_certificate_bigint_independent.mjs",
            "certs/" + cfg["cert"], str(cfg["mobility"]), cfg["term"]],
           cwd=stage, timeout=2400, stdout=big_out)
    big_byte = p.returncode == 0 and open(big_out, "rb").read() == open(
        os.path.join(MASTER_DIR, cfg["master"], "output", "bigint-verification.json"), "rb").read()
    gate(G, key + "_bigint_reexec_byte_identical", big_byte, {"returncode": p.returncode})

    # ---- Bareiss verifier ----
    brc_out = os.path.join(fresd, "bareiss-rc-fresh.json")
    p = sh([NODE, "--experimental-strip-types", "scripts/verify_win8_cert_bareiss.ts",
            "--cert", "certs/" + cfg["cert"], "--root", cfg["root"], "--root-check"],
           cwd=stage, timeout=2400, stdout=brc_out)
    brc_byte = p.returncode == 0 and open(brc_out, "rb").read() == open(
        os.path.join(MASTER_DIR, cfg["master"], "output", "bareiss-root-check.json"), "rb").read()
    gate(G, key + "_bareiss_rootcheck_byte_identical", brc_byte, {"returncode": p.returncode})

    bst_out = os.path.join(fresd, "bareiss-stats-fresh.txt")
    moves = open(os.path.join(MASTER_DIR, cfg["master"], "output",
                              "root-legal-moves.txt")).read().strip()
    p = sh([NODE, "--experimental-strip-types", "scripts/verify_win8_cert_bareiss.ts",
            "--cert", "certs/" + cfg["cert"], "--root", cfg["root"], "--subroots", moves],
           cwd=stage, timeout=2400, stdout=bst_out)
    bst_byte = p.returncode == 0 and open(bst_out, "rb").read() == open(
        os.path.join(MASTER_DIR, cfg["master"], "output", "bareiss-stats.txt"), "rb").read()
    gate(G, key + "_bareiss_subroots_byte_identical", bst_byte, {"returncode": p.returncode})

    # ---- audit machine pristine re-runs (r1, r2 same cwd; r3 isolated) ----
    pub_audit = os.path.join(MASTER_DIR, cfg["master"], "output",
                             "win8-cert-extract-verification-20261120.json")
    pub_bytes = open(pub_audit, "rb").read()
    for tag, iso in (("r1", False), ("r2", False), ("r3", True)):
        out = os.path.join(fresd, "audit-%s.json" % tag)
        if iso:
            isodir = os.path.join(RUN_DIR, "iso", key + "-" + tag)
            if os.path.exists(isodir):
                shutil.rmtree(isodir)
            os.makedirs(isodir)
            iso_stage = os.path.join(isodir, "stage")
            copy_stage(cfg, iso_stage)
            env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": isodir}
            p = run_audit(cfg, iso_stage, out, env=env, cwd=isodir)
        else:
            p = run_audit(cfg, stage, out)
        det = audit_result(p, out, pub_bytes)
        det["isolated"] = iso
        gate(G, key + "_audit_machine_" + tag,
             p.returncode == 0 and det["19_gates_pass"] and det["byte_identical"], det)

    # ---- audit machine on OUR fresh records (substitution run) ----
    sub_out = os.path.join(fresd, "audit-freshdata.json")
    sub_stage = os.path.join(RUN_DIR, "sub", key)
    if os.path.exists(sub_stage):
        shutil.rmtree(sub_stage)
    copy_stage(cfg, sub_stage)
    for fname, srcname in (("output/probe-repro-both-orderings.jsonl", "probe-fresh.jsonl"),
                           ("output/ext-summary-a1.jsonl", "ext-summary-a1.jsonl"),
                           ("output/ext-summary-a2.jsonl", "ext-summary-a2.jsonl"),
                           ("output/ext-summary-b.jsonl", "ext-summary-b.jsonl")):
        shutil.copyfile(os.path.join(fresd, srcname), os.path.join(sub_stage, fname))
    p = run_audit(cfg, sub_stage, sub_out, cwd=sub_stage)
    det = audit_result(p, sub_out, pub_bytes)
    det["note"] = ("gates evaluated against our freshly regenerated records; "
                   "pub byte-identity also holds because the audit master "
                   "embeds no ms-dependent data")
    gate(G, key + "_audit_machine_on_fresh_records",
         p.returncode == 0 and det["19_gates_pass"], det)

    # heavy intermediates cleanup: keep summaries/probes/audits, drop rows
    for d in ("rows-a1", "rows-a2"):
        p_ = os.path.join(fresd, d)
        if os.path.isdir(p_):
            total = sum(os.path.getsize(os.path.join(p_, fn)) for fn in os.listdir(p_))
            with open(os.path.join(fresd, d + "-bytes.txt"), "w") as g:
                g.write(str(total) + "\n")
            shutil.rmtree(p_)
    for junk in ("cert-fresh.n11", "rows-batch-b.txt"):
        pj = os.path.join(fresd, junk)
        if os.path.exists(pj):
            os.remove(pj)

    write_part(key + ".json", {"gates": G})
    ok_all = all(v["pass"] for v in G.values())
    print(json.dumps({"stage": "root", "root": key, "gates": len(G),
                      "status": "PASS" if ok_all else "FAIL"}))
    return 0 if ok_all else 1


def byte_xor(path, offset, val=0x01):
    data = bytearray(open(path, "rb").read())
    data[offset] ^= val
    open(path, "wb").write(bytes(data))


def audit_failing_names(path):
    try:
        j = json.load(open(path))
        return (None if j.get("all_gates_pass")
                else [g["gate"] for g in j.get("gates", []) if not g.get("passed")])
    except Exception:
        return "unparseable-or-absent"


def run_audit_tampered(cfg, tdir, out):
    return sh([sys.executable, os.path.join(tdir, cfg["assembler"]),
               "--experiment-root", tdir, "--out", out],
              cwd=tdir, timeout=2400)


def stage_tampers():
    cfg = next(r for r in ROOTS if r["key"] == "k1137")
    G = new_gate_map()
    tmp = os.path.join(RUN_DIR, "tamper")
    os.makedirs(tmp, exist_ok=True)

    # t1: certificate body byte tamper (publisher-untested offset) ->
    #     audit machine fail-closed (secondary evidence: bareiss root check scope)
    tdir = os.path.join(tmp, "t1")
    if os.path.exists(tdir):
        shutil.rmtree(tdir)
    copy_stage(cfg, tdir)
    off = 300007
    byte_xor(os.path.join(tdir, "certs", cfg["cert"]), off)
    p = run_audit_tampered(cfg, tdir, os.path.join(tmp, "t1-audit.json"))
    fails = audit_failing_names(os.path.join(tmp, "t1-audit.json"))
    pb = sh([NODE, "--experimental-strip-types", "scripts/verify_win8_cert_bareiss.ts",
             "--cert", "certs/" + cfg["cert"], "--root", cfg["root"], "--root-check"],
            cwd=tdir, timeout=2400, stdout=os.path.join(tmp, "t1-bareiss.out"))
    caught = p.returncode != 0 and fails not in (None,)
    gate(G, "tamper1_cert_body_fail_closed", caught,
         {"offset": off, "xor": "0x01", "audit_returncode": p.returncode,
          "failing_gates": fails, "bareiss_rootcheck_returncode_secondary": pb.returncode,
          "note": ("bareiss --root-check only inspects root-line-derived data and "
                   "returned 0 here; the audit machine's g16 full-tree traversal "
                   "is what catches the tampered strategy row (defense in depth)")})

    # t2: pinned input JSON tamper -> audit pin gate fail-closed
    tdir = os.path.join(tmp, "t2")
    if os.path.exists(tdir):
        shutil.rmtree(tdir)
    copy_stage(cfg, tdir)
    off = 1111
    byte_xor(os.path.join(tdir, "output", ".input-k1086.json"), off)
    p = run_audit_tampered(cfg, tdir, os.path.join(tmp, "t2-audit.json"))
    fails = audit_failing_names(os.path.join(tmp, "t2-audit.json"))
    caught = p.returncode != 0 and fails not in (None,)
    gate(G, "tamper2_input_pin_fail_closed", caught,
         {"file": ".input-k1086.json", "offset": off, "xor": "0x01",
          "audit_returncode": p.returncode, "failing_gates": fails})

    # t3: A1 summary per-move node count tamper (fresh records seeded) ->
    #     g11-style A1==A2 mismatch fail-closed
    tdir = os.path.join(tmp, "t3")
    if os.path.exists(tdir):
        shutil.rmtree(tdir)
    copy_stage(cfg, tdir)
    fres = os.path.join(RUN_DIR, "fresh", "k1137")
    for fname, srcname in (("output/probe-repro-both-orderings.jsonl", "probe-fresh.jsonl"),
                           ("output/ext-summary-a1.jsonl", "ext-summary-a1.jsonl"),
                           ("output/ext-summary-a2.jsonl", "ext-summary-a2.jsonl"),
                           ("output/ext-summary-b.jsonl", "ext-summary-b.jsonl")):
        shutil.copyfile(os.path.join(fres, srcname), os.path.join(tdir, fname))
    sa1 = os.path.join(tdir, "output", "ext-summary-a1.jsonl")
    data = open(sa1, "r", encoding="utf-8").read()
    if '"nodes":2757' not in data:
        gate(G, "tamper3_summary_node_fail_closed", False,
             {"error": "anchor nodes 2757 not found in fresh a1"})
        write_part("tampers.json", {"gates": G})
        return 1
    open(sa1, "w", encoding="utf-8").write(
        data.replace('"nodes":2757', '"nodes":2758', 1))
    p = run_audit_tampered(cfg, tdir, os.path.join(tmp, "t3-audit.json"))
    fails = audit_failing_names(os.path.join(tmp, "t3-audit.json"))
    caught = p.returncode != 0 and fails not in (None,)
    gate(G, "tamper3_summary_node_fail_closed", caught,
         {"change": "ext-summary-a1 move-1 nodes 2757->2758",
          "audit_returncode": p.returncode, "failing_gates": fails})

    write_part("tampers.json", {"gates": G, "tamper_notes": {
        "t1": {"target": "certs/" + cfg["cert"], "offset": 300007, "xor": "0x01"},
        "t2": {"target": "output/.input-k1086.json", "offset": 1111, "xor": "0x01"},
        "t3": {"target": "output/ext-summary-a1.jsonl move-1 nodes 2757->2758"}}})
    ok_all = all(v["pass"] for v in G.values())
    print(json.dumps({"stage": "tampers", "gates": len(G),
                      "status": "PASS" if ok_all else "FAIL"}))
    return 0 if ok_all else 1


def stage_finalize():
    gates = {}
    order = ["pin", "k1136", "k1137", "k1139", "tampers"]
    missing = []
    for name in order:
        p = os.path.join(PARTS_DIR, name + ".json")
        if not os.path.exists(p):
            missing.append(name)
            continue
        j = json.load(open(p))
        for k, v in j["gates"].items():
            gates[k] = v
    audit = {
        "schema": "n11-fold29-win8-cert-extract-ext-second-verification-20261120-v1",
        "experiment": "n11-fold29-win8-cert-extract-ext-second-verification-20261120",
        "status": "PASS" if (not missing and all(v["pass"] for v in gates.values()))
                  else "FAIL",
        "gate_count": len(gates),
        "gates": gates,
        "gates_ordered": [k for k in sorted(gates)],
        "missing_parts": missing,
        "parallelism": {"extraction_workers": 2,
                        "reason": "2-core sandbox; modest CPU use per lane policy"},
        "reproduction_targets": {
            "byte_targets": ("cert 3x (SHA-256), bigint-verification 3x, "
                             "bareiss-root-check 3x, bareiss-stats 3x, audit master 3x "
                             "(r1/r2/r3 + fresh-data substitution run)"),
            "value_targets": ("probe deterministic fields, ext-summary a1/a2/b "
                              "deterministic fields (per-move; ms excluded, publisher "
                              "line order recorded and excluded)"),
            "excluded": "ms / wall-clock fields (timing-dependent)"},
        "interpretation_guard": (
            "rows closed by this harness: 0 (this experiment closes no rows). "
            "REFUTED-D10 is not a LOSS proof. nodes/solved counts are never "
            "win/loss. The standard 11x11 emptied board, two-stone roots "
            "{49,60}/{59,60}, S2 {59,60}, classes 1/2/4 are all UNKNOWN. "
            "Residual rows and pool P^parallel 120,416 unchanged."),
    }
    outp = os.path.join(RUN_DIR, "harness-audit.json")
    with open(outp, "w", encoding="utf-8") as f:
        json.dump(audit, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({"status": audit["status"], "gate_count": len(gates), "out": outp}))
    return 0 if audit["status"] == "PASS" else 1


def main():
    argv = sys.argv[1:]
    if "--stage" not in argv:
        print("usage: --stage pin|root|tampers|finalize [--root k1136|k1137|k1139]")
        return 2
    i = argv.index("--stage")
    stage = argv[i + 1]
    if stage == "pin":
        return stage_pin()
    if stage == "root":
        j = argv.index("--root") if "--root" in argv else -1
        if j < 0:
            return 2
        return stage_root(argv[j + 1])
    if stage == "tampers":
        return stage_tampers()
    if stage == "finalize":
        return stage_finalize()
    return 2


if __name__ == "__main__":
    sys.exit(main())
