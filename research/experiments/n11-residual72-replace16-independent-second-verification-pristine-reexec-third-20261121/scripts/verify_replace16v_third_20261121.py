#!/usr/bin/env python3
"""
replace16 (K1089) independent-second-verification pristine-reexec THIRD
verification harness.

Target: the independent second verification of the replace16 sweep (geometry
and ledger audit of the 16 replacement roots / residual-72 rows), published at
commit 45a3f3b2b1394fc259ba3269b0a11b37fab20a57 (2026-11-20T00:44:22Z, single
commit: experiment dir 3 files + K1093 item + research log). This harness
re-executes the published verifier, pristine, from published bytes only:

  stage pin     the 3 machine files of the published second verification
                (README, verifier, published audit master) fetched from the pin
                commit raw URL and compared SHA-256 + byte count against the
                published values; the same 3 files fetched from the
                declaration-time main HEAD and byte-compared against the pin
                fetch (current-main stability).
  stage recon   the 5 W inputs (K1085/K1086/K1088/K1089 JSON records +
                runner_v17.ts) fetched from two pinned refs (ref_a =
                declaration-time HEAD, ref_b = declaration note commit),
                each SHA-256 checked against the machine pins, ref_a vs ref_b
                byte-compared, placed into the synthetic verifier tree at the
                canonical repo-relative paths, re-hashed after placement; the
                runner is additionally checked by Git blob SHA-1 pin.
  stage rerun   the published verifier run pristine 4 times per battery in a
                synthetic tree (ROOT = parents[3] of the verifier file):
                r1/r2 same tree/cwd, r3 isolated copytree + isolated env
                (PATH/HOME/TMPDIR only), r4 = r3 + PYTHONHASHSEED=random.
                Each run must be rc==0, stdout exactly
                "PASS 16/16 roots=16 rows=49 probes=32 nodes=6339079", and its
                audit byte-identical to the machine re-exec master
                1741ca01... (5,730 bytes); the 4 outputs mutually identical.
  stage erratum the published audit master (1486d35e..., 5,728 bytes) is NOT
                byte-reproducible from the published verifier; asserted deltas
                are EXACTLY two: (a) gainsHist key order (published sorted
                "2","3","4" vs machine insertion "4","3","2"; values identical
                {"2":2,"3":11,"4":3}), (b) the final interpretation_guard
                sentence-final character (published ASCII "." vs machine
                U+3002 "off the record, same sentence otherwise). Everything
                else (checks 16 gates, summary, inputs, runner) asserted
                semantically identical.
  stage tampers lane-chosen 1 byte XOR 0x20 probes at K1086@5678 and
                K1089@9012 (distinct from every known lane probe offset), in
                fresh trees WITHOUT a pre-existing audit. The published
                verifier aborts on the FIRST SHA pin mismatch (SystemExit in
                readp), so each tamper must produce rc==1, a stderr line
                naming exactly the tampered input plus its tampered SHA-256,
                and NO audit file (pre-absence and post-absence both
                asserted). The main-tree W files are re-hashed unchanged.
  finalize      a byte-deterministic audit JSON (no wall-clock, no absolute
                paths, no volatile) written to <base>/output/.

Usage: python3 verify_replace16v_third_20261121.py <base_dir>

Interpretation guards (unchanged): no search, no root judging, no row closing,
no universe rebuild, no receipt re-issuance. WIN8-D10 candidates are not
certificates. REFUTED-D10 is NOT a LOSS proof. The standard 11x11 empty board,
two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 remain UNKNOWN.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.request

PIN_COMMIT = "45a3f3b2b1394fc259ba3269b0a11b37fab20a57"
REF_A = "4c3dd3af58b9273de8e10892fb3be143e9a66228"   # declaration-time main HEAD
REF_B = "19c4eea1774c972c93ba38e58be9476ae39a809e"   # declaration note commit
RAW = "https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches"
EXP = "research/experiments/n11-residual72-replace16-independent-second-verification-20261120"

PUBLISHED = {
    "readme": {
        "path": EXP + "/README.md",
        "sha256": "e304a654275b555a53a0746056b7b04a84dcc3d6b2fcd91d379a225f8542fc09",
        "bytes": 1691,
    },
    "machine": {
        "path": EXP + "/verify_replace16_second_20261120.py",
        "sha256": "c43ab3ac2cd89a36a6ed2a47149d36e2eaf69da54cfd2912ec9caf3054a007d9",
        "bytes": 9270,
    },
    "audit": {
        "path": EXP + "/output/audit.json",
        "sha256": "1486d35e8740a594ec54f683eb36996967056d0b5fedeafe07db7da663a42949",
        "bytes": 5728,
    },
}

W_PATHS = {
    "k1085": "research/experiments/n11-residual72-unsafe-classification-add2stones-20261120/output/residual72-unsafe-classification-add2stones-20261120.json",
    "k1086": "research/experiments/n11-residual72-addtwo-greedy23-d10-sweep-20261120/output/addtwo-greedy23-d10-sweep-20261120.json",
    "k1088": "research/experiments/n11-residual72-safe8-refuted16-refsolve-20261120/output/safe8-refuted16-refsolve-20261120.json",
    "k1089": "research/experiments/n11-residual72-replace16-d10-sweep-20261120/output/replace16-d10-sweep-20261120.json",
    "runner_v17.ts": "research/experiments/n11-residual72-replace16-d10-sweep-20261120/runner_v17.ts",
}

W_PINS = {
    "k1085": "5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e",
    "k1086": "3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced",
    "k1088": "16b38d04a488617b1b8c002c6a5f3171038f557cd3cca8b8e4dbd4657bc2f724",
    "k1089": "808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc",
    "runner_v17.ts": "192903714b1b06a8ea58aa80e22da23fcf9d9ef175830a65a0da5eb0ca64f3d4",
}

RUNNER_GIT_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"

# machine re-exec master (deterministic output of the published verifier on
# pinned W inputs; 3 preliminary pristine runs byte-stable)
MASTER = {
    "sha256": "1741ca0114c244ed6aa5e61b91d48593acbf4cc18cc5f66673f2dc38c43bb1bb",
    "bytes": 5730,
}

EXPECTED_STDOUT = "PASS 16/16 roots=16 rows=49 probes=32 nodes=6339079"

TAMPERS = [
    {
        "tag": "t1",
        "w": "k1086",
        "off": 5678,
        "stderr": "K1086 SHA-256 mismatch: 28e251b7dd5b571d3cdf65081b3a7b5cc1100479803179988cd005a8e3f9ad10",
    },
    {
        "tag": "t2",
        "w": "k1089",
        "off": 9012,
        "stderr": "K1089 SHA-256 mismatch: afb504844db6f1e255baca9f92487401ac4a613e7f672dc856e90e5c07dddde9",
    },
]

GATES = []


def gate(name, ok, detail):
    GATES.append({"name": name, "pass": bool(ok), "detail": str(detail)})
    return bool(ok)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def git_blob_sha1(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


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


def tree_paths(base):
    return {
        "tree": os.path.join(base, "tree"),
        "machine": os.path.join(base, "tree", EXP, "verify_replace16_second_20261120.py"),
        "audit": os.path.join(base, "tree", EXP, "output", "audit.json"),
    }


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
        # current-main stability: file at declaration-time HEAD identical to pin
        hb = fetch(raw_url(REF_A, meta["path"]))
        gate("pin-" + key + "-head-identical", hb == b, "cmp " + sha256_bytes(hb))
    # published audit master kept for the erratum stage
    with open(os.path.join(d, "audit.bin"), "rb") as f:
        pub = f.read()
    return {"pub_audit": pub}


def stage_recon(base):
    tp = tree_paths(base)
    inp = {}
    for name in sorted(W_PATHS):
        path = W_PATHS[name]
        a = fetch(raw_url(REF_A, path))
        gate("recon-" + name + "-refA-sha256", sha256_bytes(a) == W_PINS[name], sha256_bytes(a))
        bb = fetch(raw_url(REF_B, path))
        gate("recon-" + name + "-refB-sha256", sha256_bytes(bb) == W_PINS[name], sha256_bytes(bb))
        gate("recon-" + name + "-two-ref-identical", a == bb, "cmp")
        dest = os.path.join(base, "tree", path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as f:
            f.write(a)
        with open(dest, "rb") as f:
            back = f.read()
        gate("recon-" + name + "-placed-sha256", sha256_bytes(back) == W_PINS[name], sha256_bytes(back))
        inp[name] = back
    gate("recon-runner-git-blob-sha1", git_blob_sha1(inp["runner_v17.ts"]) == RUNNER_GIT_BLOB,
         git_blob_sha1(inp["runner_v17.ts"]))
    # publish-verifier placement into the synthetic tree
    with open(os.path.join(base, "pin", "machine.bin"), "rb") as f:
        machine = f.read()
    os.makedirs(os.path.dirname(tp["machine"]), exist_ok=True)
    with open(tp["machine"], "wb") as f:
        f.write(machine)
    with open(tp["machine"], "rb") as f:
        back = f.read()
    gate("recon-machine-placed-sha256", sha256_bytes(back) == PUBLISHED["machine"]["sha256"],
         sha256_bytes(back))
    return 0


def run_machine(machine_path, cwd, env):
    r = subprocess.run([sys.executable, os.path.abspath(machine_path)],
                       cwd=cwd, env=env, capture_output=True, text=True, timeout=600)
    return r


def stage_rerun(base):
    tp = tree_paths(base)
    outs = []
    for tag in ("r1", "r2"):
        r = run_machine(tp["machine"], cwd=base, env=None)
        with open(tp["audit"], "rb") as f:
            ob = f.read()
        outs.append((tag, r, ob))
    for tag, extra in (("r3", {}), ("r4", {"PYTHONHASHSEED": "random"})):
        iso = os.path.join(base, "iso", tag)
        if os.path.exists(iso):
            shutil.rmtree(iso)
        os.makedirs(os.path.join(iso, "home"), exist_ok=True)
        os.makedirs(os.path.join(iso, "tmp"), exist_ok=True)
        itree = os.path.join(iso, "tree")
        shutil.copytree(tp["tree"], itree)
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
               "HOME": os.path.join(iso, "home"),
               "TMPDIR": os.path.join(iso, "tmp")}
        env.update(extra)
        r = run_machine(os.path.join(itree, EXP, "verify_replace16_second_20261120.py"),
                        cwd=iso, env=env)
        with open(os.path.join(itree, EXP, "output", "audit.json"), "rb") as f:
            ob = f.read()
        outs.append((tag, r, ob))
    first = None
    for tag, r, ob in outs:
        gate("rerun-" + tag + "-rc0", r.returncode == 0,
             "rc=" + str(r.returncode) + " stderr=" + r.stderr.strip()[:80])
        gate("rerun-" + tag + "-stdout-pass", r.stdout.strip() == EXPECTED_STDOUT,
             r.stdout.strip()[:90])
        gate("rerun-" + tag + "-audit-sha256-master", sha256_bytes(ob) == MASTER["sha256"],
             sha256_bytes(ob))
        gate("rerun-" + tag + "-audit-bytes", len(ob) == MASTER["bytes"], len(ob))
        d = json.loads(ob)
        gate("rerun-" + tag + "-gates16-allpass",
             len(d.get("checks", [])) == 16 and all(c.get("pass") for c in d["checks"]),
             "checks=" + str(len(d.get("checks", []))))
        if first is None:
            first = ob
        else:
            gate("rerun-" + tag + "-byte-identical-first", ob == first, "cmp")
    return outs


def stage_erratum(base, outs, pub_audit):
    m = outs[0][2]
    p = json.loads(pub_audit)
    q = json.loads(m)
    gate("erratum-published-not-byte-reproducible",
         m != pub_audit and len(m) == MASTER["bytes"] and len(pub_audit) == PUBLISHED["audit"]["bytes"],
         "pub=" + str(len(pub_audit)) + "B mac=" + str(len(m)) + "B")
    # (a) gainsHist: values identical, key order differs exactly as recorded
    def gh(doc):
        for c in doc.get("checks", []):
            det = c.get("detail", {})
            if isinstance(det, dict) and "gainsHist" in det:
                return det["gainsHist"]
        return None
    ghp, ghq = gh(p), gh(q)
    gate("erratum-gainshist-values-identical",
         ghp == {"2": 2, "3": 11, "4": 3} and ghq == ghp, json.dumps(ghp))
    gate("erratum-gainshist-order-pub-sorted", list(ghp.keys()) == ["2", "3", "4"],
         str(list(ghp.keys())))
    gate("erratum-gainshist-order-mac-insertion", list(ghq.keys()) == ["4", "3", "2"],
         str(list(ghq.keys())))
    # (b) final interpretation_guard sentence-final character
    gp, gq = p["interpretation_guard"], q["interpretation_guard"]
    gate("erratum-guard-count-and-prefix",
         len(gp) == len(gq) == 4 and gp[:3] == gq[:3], "guards=" + str(len(gq)))
    apub = gp[3].encode("utf-8")
    amac = gq[3].encode("utf-8")
    gate("erratum-guard-pub-final-ascii-period",
         gp[3][-1] == "." and apub.endswith(b".") and b"\xe3\x80\x82" not in apub[-4:],
         repr(gp[3][-8:]))
    gate("erratum-guard-mac-final-u3002",
         gq[3][-1] == "\u3002" and amac.endswith("\u3002".encode("utf-8")),
         repr(gq[3][-8:]))
    gate("erratum-guard-sentence-identical-otherwise", gp[3][:-1] == gq[3][:-1], "cmp")
    # everything else semantically identical
    p2 = json.loads(pub_audit)
    p2["interpretation_guard"][3] = q["interpretation_guard"][3]
    canon = lambda doc: json.dumps(doc, sort_keys=True, ensure_ascii=False)  # noqa: E731
    gate("erratum-no-other-semantic-diffs", canon(p2) == canon(q), "cmp")
    gate("erratum-checks-summary-inputs-runner-identical",
         p["checks"] == q["checks"] and p["summary"] == q["summary"]
         and p["inputs"] == q["inputs"] and p["runner"] == q["runner"],
         "cmp")
    return 0


def stage_tampers(base):
    tp = tree_paths(base)
    tam_dir = os.path.join(base, "tampers")
    os.makedirs(tam_dir, exist_ok=True)
    stderrs = {}
    for t in TAMPERS:
        tag, w, off, want = t["tag"], t["w"], t["off"], t["stderr"]
        probe_tree = os.path.join(tam_dir, tag, "tree")
        if os.path.exists(os.path.join(tam_dir, tag)):
            shutil.rmtree(os.path.join(tam_dir, tag))
        os.makedirs(os.path.join(tam_dir, tag), exist_ok=True)
        shutil.copytree(tp["tree"], probe_tree)
        paud = os.path.join(probe_tree, EXP, "output", "audit.json")
        # fresh tree must NOT carry a pre-existing audit (the probe asserts
        # that the verifier fail-closes without writing one): strip the
        # in-tree audit left by the rerun stage, then assert absence.
        if os.path.isfile(paud):
            os.remove(paud)
        gate("tamper-" + tag + "-fresh-tree-no-audit-pre",
             not os.path.isfile(paud), "exists_then_removed=" + str(True))
        wp = os.path.join(probe_tree, W_PATHS[w])
        with open(wp, "rb") as f:
            original = f.read()
        probe = bytearray(original)
        probe[off] ^= 0x20
        with open(wp, "wb") as f:
            f.write(bytes(probe))
        r = run_machine(os.path.join(probe_tree, EXP, "verify_replace16_second_20261120.py"),
                        cwd=os.path.join(tam_dir, tag), env=None)
        gate("tamper-" + tag + "-rc1", r.returncode == 1, "rc=" + str(r.returncode))
        gate("tamper-" + tag + "-stderr-exact", r.stderr.strip() == want,
             r.stderr.strip()[:100])
        gate("tamper-" + tag + "-no-audit-written-post", not os.path.isfile(paud), "absent")
        main_w = os.path.join(base, "tree", W_PATHS[w])
        with open(main_w, "rb") as f:
            back = f.read()
        gate("tamper-" + tag + "-maintree-w-unchanged", sha256_bytes(back) == W_PINS[w],
             sha256_bytes(back))
        stderrs[tag] = r.stderr.strip()
    gate("tamper-independent-errors",
         stderrs["t1"] != stderrs["t2"] and "K1086 " in stderrs["t1"]
         and "K1089 " in stderrs["t2"] and "K1086" not in stderrs["t2"]
         and "K1089" not in stderrs["t1"], "two distinct stderr identifications")
    return 0


def write_audit():
    pass_count = sum(1 for g in GATES if g["pass"])
    result = {
        "schema": "replace16-second-verification-pristine-reexec-third/1",
        "status": "all-gates-pass" if pass_count == len(GATES) else "gate-failed",
        "gates_total": len(GATES),
        "gates_pass": pass_count,
        "gates_all_pass": pass_count == len(GATES),
        "targets": {
            "second_verification_commit": PIN_COMMIT,
            "declaration_refs": [REF_A, REF_B],
            "published_audit_sha256": PUBLISHED["audit"]["sha256"],
            "machine_reexec_master_sha256": MASTER["sha256"],
            "w_inputs": len(W_PATHS),
        },
        "interpretation_guard": [
            "This third verification re-executes the published replace16 verifier on published bytes; it performs no search, judges no root, closes no row, rebuilds no candidate universe, re-issues no receipt.",
            "WIN8-D10 candidates are not certificates. REFUTED-D10 is NOT a LOSS proof; it certifies no first-player win within depth-10 from that root only.",
            "The erratum recording (published audit not byte-reproducible, exactly two deltas) concerns audit-json provenance only; every verification number (16/16 gates, roots=16, rows=49, probes=32, nodes=6339079) was reproduced identically.",
            "nodes/solved/coverage counts are not verdicts.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
        ],
    }
    return result


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "base"
    os.makedirs(os.path.join(base, "output"), exist_ok=True)
    del GATES[:]
    pin = stage_pin(base)
    stage_recon(base)
    outs = stage_rerun(base)
    stage_erratum(base, outs, pin["pub_audit"])
    stage_tampers(base)
    result = write_audit()
    result["gates"] = GATES
    out = os.path.join(base, "output", "replace16v-third-harness-audit.json")
    with open(out, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("third harness gates", result["gates_total"], "all_pass", result["gates_all_pass"])
    if not result["gates_all_pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
