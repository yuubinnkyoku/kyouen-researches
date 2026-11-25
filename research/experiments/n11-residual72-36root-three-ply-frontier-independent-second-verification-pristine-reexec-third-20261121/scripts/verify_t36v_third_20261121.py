#!/usr/bin/env python3
"""
36root-three-ply frontier (K1084) independent second-verification
pristine-reexec THIRD verification harness.

Target: the independent second verification of the residual72 36-root
three-ply D4 frontier census (K1075 candidate supply master, 36 fresh-safe
7-stone roots, three-move geometry census), published at commit
67766eac2f30c856543a1319cdfc5d1458382c73 (2026-11-19T23:25:16Z, single
commit: experiment dir 3 files + K1084 item + research log + README bullet).
This harness re-executes the published verifier, pristine, from published
bytes only:

  stage pin     the 3 machine files of the published second verification
                (README, verifier, published audit master) fetched from the
                pin commit raw URL and compared SHA-256 + byte count against
                the published values; the same 3 files fetched from the
                declaration-time main HEAD and byte-compared against the pin
                fetch (current-main stability).
  stage recon   the 2 W inputs (K1075 candidate-supply master and the prior
                three-ply census master) fetched from two pinned refs
                (ref_a = declaration-time HEAD, ref_b = declaration note
                commit), each SHA-256 checked against the machine pins,
                ref_a vs ref_b byte-compared, placed into the synthetic
                verifier tree at the canonical repo-relative paths, and
                re-hashed after placement.
  stage rerun   the published verifier run pristine 4 times per battery in a
                synthetic tree (ROOT = parents[4] of the verifier file):
                r1/r2 same tree/cwd, r3 isolated copytree + isolated env
                (PATH/HOME/TMPDIR only), r4 = r3 + PYTHONHASHSEED=random.
                Each run must be rc==0, report stdout JSON with
                status=second-verified / check_count=19 / all_pass=true, and
                write an audit byte-identical to the published audit master
                a6272056... (55,614 bytes); the 4 outputs must be mutually
                identical. (~16 s per run.)
  stage tampers lane-chosen 1 byte XOR 0x20 probes at the candidate-supply
                master @51,234 and the census master @8,765 (distinct from
                every known lane probe offset), in fresh trees WITHOUT a
                pre-existing audit. The published verifier raises RuntimeError
                on the FIRST SHA mismatch (traceback type), so each tamper
                must produce rc==1, an empty stdout, a stderr whose final
                line names exactly the tampered input, and NO audit file
                (pre-absence and post-absence both asserted). The main-tree
                W files are re-hashed unchanged.
  finalize      a byte-deterministic audit JSON (no wall-clock, no absolute
                paths, no volatile) written to <base>/output/.

Usage: python3 verify_t36v_third_20261121.py <base_dir>

Interpretation guards (unchanged): no search, no root judging, no row
closing, no universe rebuild, no receipt re-issuance, no 36-root depth-10
sweep launch (owned by a separate lane). The census measures geometric state
overlap only, not DFPN node cost or TT hit rate. REFUTED-D10 is NOT a LOSS
proof. The standard 11x11 empty board, two-stone roots {49,60}/{59,60},
S2 {59,60}, classes 1/2/4 remain UNKNOWN.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.request

PIN_COMMIT = "67766eac2f30c856543a1319cdfc5d1458382c73"
REF_A = "3ba28e88fd1d5c0fffaa9ae042fe3dfa68318ca0"   # declaration-time main HEAD
REF_B = "ffba79856ecbc4e915d01a4b74c4b1bfeee62f31"   # declaration note commit
RAW = "https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches"
EXP = "research/experiments/n11-residual72-36root-three-ply-frontier-independent-second-verification-20261120"

PUBLISHED = {
    "readme": {
        "path": EXP + "/README.md",
        "sha256": "bbc9b255e63e46941b372b145f2440b0d6a774c7c455f23d573af374db9ee34c",
        "bytes": 2782,
    },
    "machine": {
        "path": EXP + "/scripts/verify_frontier.py",
        "sha256": "d8876e5b61d7df02cca4958407ad310b3ceba4de8746f04657598df471834481",
        "bytes": 14671,
    },
    "audit": {
        "path": EXP + "/output/independent-second-verification-20261120.json",
        "sha256": "a6272056df6aa1dc348a00e1961a95223b4642a230a7da95a04b857bd9118b83",
        "bytes": 55614,
    },
}

W_PATHS = {
    "cand": "research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json",
    "census": "research/experiments/n11-residual72-36root-three-ply-frontier-20261120/output/36-root-three-ply-frontier-20261120.json",
}

W_PINS = {
    "cand": "49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa",
    "census": "94fdb0c6e3503f1e9d19aaaf345f4478157c5a44374f10642c52325f346c2023",
}

TAMPERS = [
    {
        "tag": "t1",
        "w": "cand",
        "off": 51234,
        "final": "RuntimeError: K1075 source SHA-256 mismatch",
        "other": "RuntimeError: published frontier SHA-256 mismatch",
    },
    {
        "tag": "t2",
        "w": "census",
        "off": 8765,
        "final": "RuntimeError: published frontier SHA-256 mismatch",
        "other": "RuntimeError: K1075 source SHA-256 mismatch",
    },
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


def tree_paths(base):
    return {
        "tree": os.path.join(base, "tree"),
        "machine": os.path.join(base, "tree", EXP, "scripts", "verify_frontier.py"),
        "audit": os.path.join(base, "tree", EXP, "output", "independent-second-verification-20261120.json"),
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
        hb = fetch(raw_url(REF_A, meta["path"]))
        gate("pin-" + key + "-head-identical", hb == b, "cmp " + sha256_bytes(hb))
    return 0


def stage_recon(base):
    tp = tree_paths(base)
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
                       cwd=cwd, env=env, capture_output=True, text=True, timeout=900)
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
        r = run_machine(os.path.join(itree, EXP, "scripts", "verify_frontier.py"),
                        cwd=iso, env=env)
        with open(os.path.join(itree, EXP, "output", "independent-second-verification-20261120.json"), "rb") as f:
            ob = f.read()
        outs.append((tag, r, ob))
    first = None
    for tag, r, ob in outs:
        gate("rerun-" + tag + "-rc0", r.returncode == 0,
             "rc=" + str(r.returncode) + " stderr=" + r.stderr.strip()[-120:])
        ok_stdout = False
        try:
            so = json.loads(r.stdout)
            ok_stdout = (so.get("status") == "second-verified"
                         and so.get("check_count") == 19 and so.get("all_pass") is True)
        except Exception:  # noqa: BLE001
            so = {}
        gate("rerun-" + tag + "-stdout-second-verified", ok_stdout,
             r.stdout.strip()[:90])
        gate("rerun-" + tag + "-audit-sha256-published",
             sha256_bytes(ob) == PUBLISHED["audit"]["sha256"], sha256_bytes(ob))
        gate("rerun-" + tag + "-audit-bytes", len(ob) == PUBLISHED["audit"]["bytes"], len(ob))
        d = json.loads(ob)
        gate("rerun-" + tag + "-gates19-allpass",
             d.get("check_count") == 19 and d.get("all_pass") is True
             and d.get("status") == "second-verified" and len(d.get("checks", [])) == 19,
             "checks=" + str(len(d.get("checks", []))))
        if first is None:
            first = ob
        else:
            gate("rerun-" + tag + "-byte-identical-first", ob == first, "cmp")
    return 0


def stage_tampers(base):
    tp = tree_paths(base)
    tam_dir = os.path.join(base, "tampers")
    os.makedirs(tam_dir, exist_ok=True)
    finals = {}
    for t in TAMPERS:
        tag, w, off, want, othermsg = t["tag"], t["w"], t["off"], t["final"], t["other"]
        if os.path.exists(os.path.join(tam_dir, tag)):
            shutil.rmtree(os.path.join(tam_dir, tag))
        os.makedirs(os.path.join(tam_dir, tag), exist_ok=True)
        probe_tree = os.path.join(tam_dir, tag, "tree")
        shutil.copytree(tp["tree"], probe_tree)
        paud = os.path.join(probe_tree, EXP, "output", "independent-second-verification-20261120.json")
        # fresh tree must NOT carry a pre-existing audit: strip the in-tree
        # audit left by the rerun stage, then assert absence.
        if os.path.isfile(paud):
            os.remove(paud)
        gate("tamper-" + tag + "-fresh-tree-no-audit-pre", not os.path.isfile(paud), "removed")
        wp = os.path.join(probe_tree, W_PATHS[w])
        with open(wp, "rb") as f:
            original = f.read()
        probe = bytearray(original)
        probe[off] ^= 0x20
        with open(wp, "wb") as f:
            f.write(bytes(probe))
        r = run_machine(os.path.join(probe_tree, EXP, "scripts", "verify_frontier.py"),
                        cwd=os.path.join(tam_dir, tag), env=None)
        gate("tamper-" + tag + "-rc1", r.returncode == 1, "rc=" + str(r.returncode))
        gate("tamper-" + tag + "-stdout-empty", r.stdout.strip() == "", "len=" + str(len(r.stdout.strip())))
        lastline = r.stderr.strip().splitlines()[-1].strip() if r.stderr.strip() else ""
        gate("tamper-" + tag + "-stderr-final-line", lastline == want, lastline[:100])
        gate("tamper-" + tag + "-stderr-exclusive", othermsg not in r.stderr, "exclusive")
        gate("tamper-" + tag + "-no-audit-written-post", not os.path.isfile(paud), "absent")
        main_w = os.path.join(base, "tree", W_PATHS[w])
        with open(main_w, "rb") as f:
            back = f.read()
        gate("tamper-" + tag + "-maintree-w-unchanged", sha256_bytes(back) == W_PINS[w],
             sha256_bytes(back))
        finals[tag] = lastline
    gate("tamper-independent-errors",
         finals["t1"] != finals["t2"] and "K1075 source" in finals["t1"]
         and "published frontier" in finals["t2"], "two distinct RuntimeError identifications")
    return 0


def write_audit():
    pass_count = sum(1 for g in GATES if g["pass"])
    result = {
        "schema": "t36-frontier-second-verification-pristine-reexec-third/1",
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
            "This third verification re-executes the published 36-root three-ply frontier second-verifier on published bytes; it performs no search, judges no root, closes no row, rebuilds no candidate universe, launches no depth-10 sweep (separate lane).",
            "The census measures geometric state overlap only, not DFPN node cost or transposition-table hit rate, and justifies no sharing implementation or worker split by itself.",
            "REFUTED-D10 is NOT a LOSS proof; the 36 roots are candidate roots, not WIN certificates.",
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
    out = os.path.join(base, "output", "frontier-third-harness-audit.json")
    with open(out, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("third harness gates", result["gates_total"], "all_pass", result["gates_all_pass"])
    if not result["gates_all_pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
