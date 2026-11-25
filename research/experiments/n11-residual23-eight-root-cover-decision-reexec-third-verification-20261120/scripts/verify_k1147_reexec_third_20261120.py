#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
K1147 (residual23 eight-root cover decision, external second verification)
pristine re-execution THIRD verification (2026-11-20).

Single-owner note:
  research/log/2026-11-20-n11-residual23-eight-root-cover-third-verification-single-owner-note.md
  (commit 887e594de7, published ahead of this experiment)

What this harness proves, from GitHub published bytes ONLY (no local memory of
the original run): a third party who re-fetches the seven published files

  * the decision machine eight_root_cover_decision_20261120.py
    (SHA-256 da51063c..., published in n11-residual23-eight-root-cover-decision-20261120/scripts/)
  * the decision record residual23-eight-root-cover-decision-20261120.json
    (SHA-256 c5aaf83e..., published .../output/), staged here as published-decision.json
  * K1097 refsolve record (SHA-256 2896deb0..., n11-residual72-safe8-refuted50-refsolve-20261120/output/)
  * K1102 second-verification record (SHA-256 d0b5d845..., n11-residual72-refuted50-refsolve-second-verification-20261120/output/)
  * lower-bound strengthening audit (SHA-256 1310ef74..., n11-residual23-cover-lower-bound-strengthening-20261120/output/)
  * the external verification machine verify_external_cover8_decision_20261120.py
    (SHA-256 7bee45ec..., n11-residual23-eight-root-cover-decision-external-second-verification-20261120/scripts/)
  * the published external verification audit (SHA-256 17dbd6ab..., .../output/)

can (1) regenerate the four decision-machine re-execution outputs of the K1147
run byte-identically (each equal to the published decision record c5aaf83e...),
(2) re-run the published external verification machine on those fresh outputs
and reproduce the published audit 17dbd6ab... byte-identically (71/71 checks),
(3) observe the fail-closed pins catch a 1-byte tamper of a published record.

REPRODUCIBILITY CAVEAT first observed by this third verification run (recorded
here as an experiment fact): the published external verification machine
records os.path.basename() of each record input inside the pin-* check
details of its audit JSON.  A byte-identical reproduction of the published
audit therefore requires the four record inputs to carry the same basenames as
the K1147 original stage (published-decision.json / k1097-refsolve.json /
k1102-second-verification.json / lower-bound-audit.json).  All SHA-256 pins are
content-level and independent of the names; only those recorded detail strings
depend on them.  The input snapshots in this experiment dir use exactly those
names, so any re-run of this harness from this dir reproduces the audit.

Interpretation: this is a record-level determinism / reproducibility check of
published bookkeeping (candidate-root plan cover numbers). NO row is closed.
Cover numbers are plan bookkeeping, not certificates. REFUTED-D10 is not a LOSS
proof; nodes/solved counts are not game values. The standard 11x11 empty board,
two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 remain UNKNOWN.

Runtime note: the decision machine takes ~40s per run; four fresh re-executions
plus three verifier runs plus tamper gates take a few minutes. Timing is NOT
recorded in the audit (non-deterministic by nature).

Usage:
  python3 verify_k1147_reexec_third_20261120.py --indir INPUTS --workdir WORK --out AUDIT.json
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys

DECISION_MACHINE_SHA256 = "da51063c6db43cb9d0fe7c69dbbbe17268c250abec3080390384a14316168277"
DECISION_RECORD_SHA256 = "c5aaf83e23b6a716e981aaff745996668c60edba164fb3f5288b60ff9b8ac4d1"
K1097_SHA256 = "2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40"
K1102_SHA256 = "d0b5d845c234cf51c55555295f1fe3042f262cccaa0e2923c9c4205d6b6e168b"
LB_AUDIT_SHA256 = "1310ef74f40a98095d6128f28cba1c5e87e45a45694a3ec6940b541ec0dd3b00"
EXT_MACHINE_SHA256 = "7bee45ec2b8a83cc931ada1d3ef88da9ab79ee3f4175efa95ab770707352b353"
EXT_AUDIT_SHA256 = "17dbd6ab3a9a9b5aef1cf1cf517a5a0fd216dff755f0ed86fcf029e1612cabcb"

INPUT_ROLES = [
    ("eight-root-cover-decision-machine.py", "decision machine", DECISION_MACHINE_SHA256),
    ("published-decision.json", "decision record (published master)", DECISION_RECORD_SHA256),
    ("k1097-refsolve.json", "K1097 refsolve record", K1097_SHA256),
    ("k1102-second-verification.json", "K1102 second-verification record", K1102_SHA256),
    ("lower-bound-audit.json", "lower-bound strengthening audit", LB_AUDIT_SHA256),
    ("verify_external_cover8_decision_20261120.py", "external verification machine", EXT_MACHINE_SHA256),
    ("external-verification-audit.json", "published external verification audit", EXT_AUDIT_SHA256),
]

TAMPER_OFFSET_DECISION = 7701  # inside the 16,324-byte decision record
TAMPER_OFFSET_K1097 = 77       # inside the 43,540-byte K1097 record


def fail(msg):
    print("GATE FAILED :: " + msg)
    sys.exit(2)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 16)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def xor_one_byte(src, dst, offset):
    with open(src, "rb") as f:
        data = bytearray(f.read())
    if not 0 <= offset < len(data):
        fail("tamper offset out of range")
    data[offset] ^= 0x01
    with open(dst, "wb") as f:
        f.write(bytes(data))


def run_decision(machine, k1097, k1102, audit, out_path, cwd=None, env_extra=None):
    """Run the published decision machine; return (returncode, out_sha_or_None, log)."""
    cmd = [sys.executable, os.path.abspath(machine),
           "--k1097", os.path.abspath(k1097),
           "--k1102", os.path.abspath(k1102),
           "--audit", os.path.abspath(audit),
           "--out", os.path.abspath(out_path)]
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    sha = sha256_file(out_path) if os.path.isfile(out_path) else None
    return r.returncode, sha, r.stdout + r.stderr


def run_ext_verifier(ext_machine, machine, decision, reexecs, k1097, k1102, audit,
                     out_path, cwd=None, env_extra=None):
    """Run the published external verification machine; return (rc, out_sha_or_None, log)."""
    cmd = [sys.executable, os.path.abspath(ext_machine),
           "--machine", os.path.abspath(machine),
           "--decision", os.path.abspath(decision),
           "--reexec", ",".join(os.path.abspath(p) for p in reexecs),
           "--k1097", os.path.abspath(k1097),
           "--k1102", os.path.abspath(k1102),
           "--audit", os.path.abspath(audit),
           "--out", os.path.abspath(out_path)]
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    sha = sha256_file(out_path) if os.path.isfile(out_path) else None
    return r.returncode, sha, r.stdout + r.stderr


def main():
    argv = list(sys.argv[1:])

    def opt(name):
        return argv[argv.index(name) + 1] if name in argv else None

    indir = opt("--indir")
    workdir = opt("--workdir")
    out_path = opt("--out")
    if not (indir and workdir and out_path):
        fail("usage: --indir INPUTS --workdir WORK --out AUDIT.json")
    indir = os.path.abspath(indir)
    workdir = os.path.abspath(workdir)

    # ---- 1. fail-closed pins of the seven published inputs ------------------
    pins = []
    paths = {}
    for name, role, want in INPUT_ROLES:
        p = os.path.join(indir, name)
        if not os.path.isfile(p):
            fail(f"input missing: {name}")
        got = sha256_file(p)
        if got != want:
            fail(f"pin mismatch {name}: {got} != {want}")
        paths[name] = p
        pins.append({"name": name, "role": role, "sha256": got, "pin_ok": True})

    dm = paths["eight-root-cover-decision-machine.py"]
    drec = paths["published-decision.json"]
    k97 = paths["k1097-refsolve.json"]
    k102 = paths["k1102-second-verification.json"]
    lba = paths["lower-bound-audit.json"]
    evm = paths["verify_external_cover8_decision_20261120.py"]
    eva = paths["external-verification-audit.json"]

    # published decision record bytes, for byte comparison of fresh outputs
    with open(drec, "rb") as f:
        drec_bytes = f.read()
    with open(eva, "rb") as f:
        eva_bytes = f.read()

    # ---- 2. four pristine re-executions of the decision machine -------------
    os.makedirs(workdir, exist_ok=True)
    rundir = os.path.join(workdir, "reexec")
    iso_root = os.path.join(workdir, "iso")
    for d in (rundir, iso_root):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)

    # pass B / B' isolated tree: fresh copies of machine + three input records
    # under different relative paths, isolated cwd, isolated HOME.
    def make_iso(tag):
        tree = os.path.join(iso_root, tag)
        os.makedirs(tree, exist_ok=True)
        os.makedirs(os.path.join(tree, "home"), exist_ok=True)
        copies = {
            "machine": os.path.join(tree, "machine-copy.py"),
            "k1097": os.path.join(tree, "k1097-copy.json"),
            "k1102": os.path.join(tree, "k1102-copy.json"),
            "audit": os.path.join(tree, "lb-audit-copy.json"),
        }
        shutil.copyfile(dm, copies["machine"])
        shutil.copyfile(k97, copies["k1097"])
        shutil.copyfile(k102, copies["k1102"])
        shutil.copyfile(lba, copies["audit"])
        for c in copies.values():
            if not os.path.isfile(c):
                fail("iso copy failed")
        return tree, copies

    reexec_specs = [
        ("passA1", None, None),
        ("passA2", None, None),
        ("passB", "B", None),
        ("passB_hashseed_random", "Br", "random"),
    ]
    reexec_info = {}
    reexec_outs = []
    for tag, iso_tag, hashseed in reexec_specs:
        out = os.path.join(rundir, f"decision-{tag}.json")
        if iso_tag is None:
            rc, sha, log = run_decision(dm, k97, k102, lba, out)
            cwd_desc = "same cwd, inputs from indir paths"
            iso_desc = False
        else:
            tree, copies = make_iso(iso_tag)
            env_extra = {"HOME": os.path.join(tree, "home")}
            if hashseed:
                env_extra["PYTHONHASHSEED"] = hashseed
            rc, sha, log = run_decision(copies["machine"], copies["k1097"],
                                        copies["k1102"], copies["audit"], out,
                                        cwd=tree, env_extra=env_extra)
            cwd_desc = ("isolated tree/cwd/HOME, input copies at different paths"
                        + (", PYTHONHASHSEED=random" if hashseed else ""))
            iso_desc = True
        if rc != 0:
            fail(f"decision re-exec {tag}: nonzero returncode {rc}")
        if sha != DECISION_RECORD_SHA256:
            fail(f"decision re-exec {tag}: sha {sha} != published {DECISION_RECORD_SHA256}")
        with open(out, "rb") as f:
            b = f.read()
        if b != drec_bytes:
            fail(f"decision re-exec {tag}: not byte-identical to published record")
        reexec_outs.append(out)
        reexec_info[tag] = {
            "returncode": rc,
            "sha256": sha,
            "byte_identical_to_published_record": True,
            "isolated": iso_desc,
            "cwd_note": cwd_desc,
        }

    if len({sha256_file(p) for p in reexec_outs}) != 1:
        fail("re-exec outputs not all identical")
    if sha256_file(reexec_outs[0]) != DECISION_RECORD_SHA256:
        fail("re-exec outputs differ from published record")

    # ---- 3. three runs of the external verification machine -----------------
    vdir = os.path.join(workdir, "extverify")
    if os.path.exists(vdir):
        shutil.rmtree(vdir)
    os.makedirs(vdir)
    ver_info = {}
    ver_outs = []
    for tag, iso in (("V1", False), ("V2", False), ("V3", True)):
        out = os.path.join(vdir, f"external-verification-audit-{tag}.json")
        if iso:
            # Isolated tree / cwd / HOME with all files re-copied, but each copy
            # keeps its published-stage basename: the verifier records input
            # basenames in its pin-* details, so byte-identity of the audit
            # requires stable names (isolation is by directory, not by name).
            tree = os.path.join(iso_root, "V3")
            os.makedirs(tree, exist_ok=True)
            os.makedirs(os.path.join(tree, "home"), exist_ok=True)
            srcs = {"machine": dm, "decision": drec, "k1097": k97,
                    "k1102": k102, "audit": lba, "evm": evm}
            c = {nm: os.path.join(tree, os.path.basename(p)) for nm, p in srcs.items()}
            for nm, p in srcs.items():
                shutil.copyfile(p, c[nm])
            rd = os.path.join(tree, "reexec")
            os.makedirs(rd, exist_ok=True)
            cres = []
            for i, rp in enumerate(reexec_outs):
                cp = os.path.join(rd, f"reexec-copy-{i}.json")
                shutil.copyfile(rp, cp)
                cres.append(cp)
            rc, sha, log = run_ext_verifier(c["evm"], c["machine"], c["decision"],
                                            cres, c["k1097"], c["k1102"], c["audit"],
                                            out, cwd=tree,
                                            env_extra={"HOME": os.path.join(tree, "home")})
            note = "isolated tree/cwd/HOME, copies keep published-stage basenames (isolation by directory)"
        else:
            rc, sha, log = run_ext_verifier(evm, dm, drec, reexec_outs,
                                            k97, k102, lba, out)
            note = "same cwd, indir paths"
        if rc != 0:
            fail(f"external verifier {tag}: nonzero returncode {rc}")
        if sha != EXT_AUDIT_SHA256:
            fail(f"external verifier {tag}: sha {sha} != published {EXT_AUDIT_SHA256}")
        with open(out, "rb") as f:
            b = f.read()
        if b != eva_bytes:
            fail(f"external verifier {tag}: not byte-identical to published audit")
        with open(out, "r", encoding="utf-8") as f:
            got_json = json.load(f)
        ver_info[tag] = {
            "returncode": rc,
            "sha256": sha,
            "byte_identical_to_published_audit": True,
            "checks_total": got_json.get("checks_total"),
            "checks_all_ok": got_json.get("checks_all_ok"),
            "cwd_note": note,
        }
        ver_outs.append(out)

    if not (ver_info["V1"]["checks_total"] == 71 and ver_info["V1"]["checks_all_ok"] is True):
        fail("published audit shape mismatch (checks_total / checks_all_ok)")

    # ---- 4. tamper gates: fail-closed pins must catch 1-byte corruption -----
    tdir = os.path.join(workdir, "tamper")
    if os.path.exists(tdir):
        shutil.rmtree(tdir)
    os.makedirs(tdir)

    # (a) tampered copy of the published decision record fed to the verifier
    t_dec = os.path.join(tdir, "decision-record-tampered.json")
    xor_one_byte(drec, t_dec, TAMPER_OFFSET_DECISION)
    t_sha = sha256_file(t_dec)
    if t_sha == DECISION_RECORD_SHA256:
        fail("tamper did not change decision record")
    tv_out = os.path.join(tdir, "tampered-verifier-audit.json")
    rc_t, _, log_t = run_ext_verifier(evm, dm, t_dec, reexec_outs, k97, k102, lba, tv_out)
    caught_a = (rc_t != 0) and (not os.path.isfile(tv_out))
    if not caught_a:
        fail(f"tamper (a) not caught: rc={rc_t} out_exists={os.path.isfile(tv_out)}")

    # (b) tampered copy of the K1097 record fed to the decision machine's pin
    t_k97 = os.path.join(tdir, "k1097-tampered.json")
    xor_one_byte(k97, t_k97, TAMPER_OFFSET_K1097)
    if sha256_file(t_k97) == K1097_SHA256:
        fail("tamper did not change k1097 record")
    td_out = os.path.join(tdir, "tampered-decision-output.json")
    rc_d, _, log_d = run_decision(dm, t_k97, k102, lba, td_out)
    caught_b = (rc_d != 0) and (not os.path.isfile(td_out))
    if not caught_b:
        fail(f"tamper (b) not caught: rc={rc_d} out_exists={os.path.isfile(td_out)}")

    tamper = {
        "decision_record_1byte_xor": {
            "offset": TAMPER_OFFSET_DECISION,
            "sha256_after_tamper": t_sha,
            "caught": True,
            "returncode": rc_t,
            "output_written": False,
        },
        "k1097_record_1byte_xor": {
            "offset": TAMPER_OFFSET_K1097,
            "sha256_after_tamper": sha256_file(t_k97),
            "caught": True,
            "returncode": rc_d,
            "output_written": False,
        },
    }

    # ---- 5. deterministic audit ---------------------------------------------
    result = {
        "schema": "n11-residual23-eight-root-cover-reexec-third-verification-20261120/v1",
        "verification_kind": ("third verification: regenerate K1147's four decision-machine "
                              "re-executions and its 71-check external verification audit "
                              "from GitHub published bytes only"),
        "single_owner_note": ("research/log/2026-11-20-n11-residual23-eight-root-cover-"
                              "third-verification-single-owner-note.md (commit 887e594de7)"),
        "pinned_inputs": pins,
        "published_decision_record_sha256": DECISION_RECORD_SHA256,
        "published_external_audit_sha256": EXT_AUDIT_SHA256,
        "reexecution": {
            "passes": reexec_info,
            "all_four_byte_identical_to_published": True,
        },
        "external_verifier": {
            "runs": ver_info,
            "all_byte_identical_to_published_audit": True,
            "checks_total": 71,
            "checks_all_ok": True,
        },
        "tamper_gates": tamper,
        "rows_closed": 0,
        "trust_boundary": ("record-level determinism and pin-chain reproducibility only; "
                           "the touching universe / safe8 predicates were re-executed by the "
                           "published decision machine, not re-derived by yet another implementation here"),
        "interpretation_guard": [
            "No row is closed by this verification or by the cover decision it re-checks.",
            "The cover numbers are candidate-root plan bookkeeping, not certificates.",
            "REFUTED-D10 is not a LOSS proof; nodes and solved counts are not game values.",
            "The audit lower bound 8 remains valid on any universe; 9 is specific to pool P-triple-prime.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 remain UNKNOWN.",
        ],
        "status": "all gates pass",
    }
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    txt = json.dumps(result, ensure_ascii=True, indent=1, sort_keys=True) + "\n"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print("WROTE", out_path)
    print("sha256", hashlib.sha256(txt.encode("utf-8")).hexdigest())


main()
