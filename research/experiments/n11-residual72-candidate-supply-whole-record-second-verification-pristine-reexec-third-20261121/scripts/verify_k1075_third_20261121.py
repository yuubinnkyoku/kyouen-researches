#!/usr/bin/env python3
"""
candidate-supply whole-record (K1075) independent second-verification
pristine-reexec THIRD verification harness.

Target: the independent whole-record second verification of the K1075
residual-72 full cache-join candidate-supply master (87 gates: raw probe
corpus rebuild, K1059 dead-sweep rebuild, resolve6 value identity, fold-chain
numerics, row-demand re-aggregation, matching-36, cross-lane consistency),
published at commit 3e0d2df9af0361fa73e000724ea5a0c458517250
(2026-11-19T21:55:31Z, single commit: experiment dir 3 files + research log;
its own 2026-11-20 single-owner declaration note was published beforehand by
the publishing lane). This harness re-executes the published verifier,
pristine, from published bytes only:

  stage pin     the 3 machine files of the published second verification
                (README, verifier, published audit master) plus its research
                log fetched from the pin-commit raw URL and compared
                SHA-256 + byte count against the published values; the same
                files fetched from the declaration-time main HEAD and
                byte-compared against the pin fetch.
  stage recon   the 15 W inputs (k1075 master, resolve5/6, fold9/10, sv17,
                sweep39 live/dead, resolve7, r7second, roots.json, raw
                4-worker probe records) fetched from two pinned refs
                (ref_a = declaration-time HEAD, ref_b = declaration note
                commit), each SHA-256 checked against the machine-internal
                pins, ref_a vs ref_b byte-compared, placed into the synthetic
                verifier input dir at the canonical regular names, and
                re-hashed after placement.
  stage rerun   the published verifier run pristine 4 times per battery
                (r1/r2 same tree/cwd, r3 isolated copytree + isolated env
                PATH/HOME/TMPDIR, r4 = r3 + PYTHONHASHSEED=random). Each run
                must be rc==0, print "gates 87 all_pass True faithful True",
                and write an audit byte-identical to the published audit
                master 753f9a07... (16,462 bytes); the 4 outputs must be
                mutually identical. (~0.07 s per run.)
  stage tampers lane-chosen 1 byte XOR 0x20 probes at sweep39dead.json
                @33,333 (15th = final read) and k1075.json @44,456 (3rd
                read), distinct from every known lane probe offset, in fresh
                trees with a probe-local out path asserted absent before
                and after. The published verifier raises SystemExit("pin
                mismatch for <name>") on the FIRST SHA mismatch and writes
                no audit (no-write fail-closed, no traceback). Each tamper
                must produce rc==1, an empty stdout, a stderr whose final
                line names exactly the tampered input, and NO audit file.
                The main-tree W files are re-hashed unchanged.
  finalize      a byte-deterministic audit JSON (no wall-clock, no absolute
                paths, no volatile) written to <base>/output/.

Usage: python3 verify_k1075_third_20261121.py <base_dir>

Interpretation guards (unchanged): no search, no root judging, no row
closing, no universe rebuild, no receipt re-issuance, no re-verification of
the geometry lane (44 gates, separate publication). The census measures
record identity only. REFUTED-D10 is NOT a LOSS proof; witness roots and the
candidate supply are a conditional depth-10 sweep plan, not certificates.
The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60},
classes 1/2/4 remain UNKNOWN.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.request

PIN_COMMIT = "3e0d2df9af0361fa73e000724ea5a0c458517250"
REF_A = "5487dad0442b9744a4206ceef7a026a2946c97d5"   # declaration-time main HEAD
REF_B = "9e7ac2a1fe6233ca1913acb4b495f8c5f64b7496"   # declaration note commit
RAW = "https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches"
EXP = "research/experiments/n11-residual72-candidate-supply-whole-record-second-verification-20261120"
RLOG = "research/log/2026-11-20-n11-candidate-supply-whole-record-second-verification.md"

PUBLISHED = {
    "readme": {
        "path": EXP + "/README.md",
        "sha256": "69db6635a0eb178047573f71c8067776cbd8964ae1b4da9736adcb7aa76c277b",
        "bytes": 9065,
    },
    "machine": {
        "path": EXP + "/scripts/k1075_second_verification.py",
        "sha256": "f808279d82927ed7ab8abdeedb6a266c75537490edf2e2fe7b2fa231b0cc0847",
        "bytes": 35127,
    },
    "audit": {
        "path": EXP + "/output/candidate-supply-whole-record-second-verification-20261120.json",
        "sha256": "753f9a07599525ae17eb66cb1a72f59164d995190d50b182bf26a6e7f07f9de9",
        "bytes": 16462,
    },
    "researchlog": {
        "path": RLOG,
        "sha256": "9724e961ffdd2df702b9f100fdb21cbc36b9bb2e574d073563a55abc50ffe9f0",
        "bytes": 3331,
    },
}

LIVE = "research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120"

W_PATHS = {
    "k1075.json": "research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json",
    "resolve5.json": "research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/fold/output/post-twelfth-receipt-cover-resolve5-20261119.json",
    "resolve6.json": "research/experiments/n11-residual78-cache-join-resolve6-20261120/output/post-saturation-full-cache-join-resolve6-20261120.json",
    "fold9.json": "research/experiments/n11-residual78-windfall4-receipt-fold-20261120/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json",
    "fold10.json": "research/experiments/n11-seventeenth-win7-receipt-fold-20261120/fold/output/seventeenth-win7-receipt-fold-20261120.json",
    "sv17.json": "research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/output/seventeenth-cert-triple-verification-20261120.json",
    "sweep39.json": LIVE + "/output/witness-39live-root-depth10-sweep-20261120.json",
    "sweep39dead.json": "research/experiments/n11-residual78-39witness-depth10-sweep-20261119/output/witness-39-root-depth10-sweep-20261119.json",
    "resolve7.json": "research/experiments/n11-residual72-postfold-witness-recheck-20261120/output/residual72-postfold-witness-recheck-20261120.json",
    "r7second.json": "research/experiments/n11-residual72-resolve7-second-verification-20261120/output/resolve7-second-verification-20261120.json",
    "roots.json": LIVE + "/roots.json",
    "probes-w0.jsonl": LIVE + "/output/probe-records-w0.jsonl",
    "probes-w1.jsonl": LIVE + "/output/probe-records-w1.jsonl",
    "probes-w2.jsonl": LIVE + "/output/probe-records-w2.jsonl",
    "probes-w3.jsonl": LIVE + "/output/probe-records-w3.jsonl",
}

W_PINS = {
    "resolve5.json": "5a2f4815c1d5fbbf40a76f839425a6e3750673bb37a60b64aca8ff03e5aeef9e",
    "resolve6.json": "e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a",
    "fold9.json": "24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2",
    "fold10.json": "bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a",
    "sv17.json": "c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc",
    "sweep39.json": "22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc",
    "sweep39dead.json": "f8608d0a04a132012f0aa692099cebe851cdf261a3ea916dc4c15d6841fc5246",
    "resolve7.json": "207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f",
    "probes-w0.jsonl": "6b045eaefdd59e2c0fbd0f9b4a1e876b89c3f8b03cfade8f0ab1f8192cd0a984",
    "probes-w1.jsonl": "4aaa4d0a691f6da40e68dbaa41a353aaf3ea518a6863aec04886c17197e00967",
    "probes-w2.jsonl": "2d4ff7dd40b2fc66745068f6772724f38ccd04dd2a65507af925fb85252b3032",
    "probes-w3.jsonl": "e04e20bdadd1cba94cd0a285ff9fb72bb9e9d0a2d5a687f1d76ceccc7d0ccb0c",
    "roots.json": "9f0161a8a61d311534fd3a4035b1c367426691c72ad5eb44efd01a5fae37e0cc",
    "r7second.json": "4286100804d82376418066da89167c50017244f2c6f02b81ad76a07b45bd91d6",
    "k1075.json": "49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa",
}

# the published verifier reads pins in sorted(PINS) order:
# fold10, fold9, k1075, probes-w0..3, r7second, resolve5, resolve6, resolve7,
# roots, sv17, sweep39, sweep39dead  (15 reads)
TAMPERS = [
    {
        "tag": "t1",
        "w": "sweep39dead.json",
        "off": 33333,
        "read_index": 15,
        "final": "pin mismatch for sweep39dead.json",
        "other": "pin mismatch for k1075.json",
    },
    {
        "tag": "t2",
        "w": "k1075.json",
        "off": 44456,
        "read_index": 3,
        "final": "pin mismatch for k1075.json",
        "other": "pin mismatch for sweep39dead.json",
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


def input_dir(base):
    return os.path.join(base, "verifier_input")


def machine_path(base):
    return os.path.join(base, "machine", "k1075_second_verification.py")


def stage_pin(base):
    d = os.path.join(base, "pin")
    os.makedirs(d, exist_ok=True)
    for key in ("readme", "machine", "audit", "researchlog"):
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
    idir = input_dir(base)
    os.makedirs(idir, exist_ok=True)
    for name in sorted(W_PATHS):
        path = W_PATHS[name]
        a = fetch(raw_url(REF_A, path))
        gate("recon-" + name + "-refA-sha256", sha256_bytes(a) == W_PINS[name], sha256_bytes(a))
        bb = fetch(raw_url(REF_B, path))
        gate("recon-" + name + "-refB-sha256", sha256_bytes(bb) == W_PINS[name], sha256_bytes(bb))
        gate("recon-" + name + "-two-ref-identical", a == bb, "cmp")
        dest = os.path.join(idir, name)
        with open(dest, "wb") as f:
            f.write(a)
        with open(dest, "rb") as f:
            back = f.read()
        gate("recon-" + name + "-placed-sha256", sha256_bytes(back) == W_PINS[name], sha256_bytes(back))
    with open(os.path.join(base, "pin", "machine.bin"), "rb") as f:
        machine = f.read()
    os.makedirs(os.path.dirname(machine_path(base)), exist_ok=True)
    with open(machine_path(base), "wb") as f:
        f.write(machine)
    with open(machine_path(base), "rb") as f:
        back = f.read()
    gate("recon-machine-placed-sha256", sha256_bytes(back) == PUBLISHED["machine"]["sha256"],
         sha256_bytes(back))
    return 0


def run_machine(machine, argv_in, argv_out, cwd, env):
    r = subprocess.run([sys.executable, os.path.abspath(machine),
                        os.path.abspath(argv_in), os.path.abspath(argv_out)],
                       cwd=cwd, env=env, capture_output=True, text=True, timeout=900)
    return r


def stage_rerun(base):
    idir = input_dir(base)
    mp = machine_path(base)
    outs = []
    for tag in ("r1", "r2"):
        outj = os.path.join(base, "rerun", tag + ".json")
        os.makedirs(os.path.dirname(outj), exist_ok=True)
        r = run_machine(mp, idir, outj, cwd=base, env=None)
        with open(outj, "rb") as f:
            ob = f.read()
        outs.append((tag, r, ob))
    for tag, extra in (("r3", {}), ("r4", {"PYTHONHASHSEED": "random"})):
        iso = os.path.join(base, "iso", tag)
        if os.path.exists(iso):
            shutil.rmtree(iso)
        os.makedirs(os.path.join(iso, "home"), exist_ok=True)
        os.makedirs(os.path.join(iso, "tmp"), exist_ok=True)
        iinput = os.path.join(iso, "verifier_input")
        imachine = os.path.join(iso, "machine", "k1075_second_verification.py")
        shutil.copytree(idir, iinput)
        os.makedirs(os.path.dirname(imachine), exist_ok=True)
        shutil.copyfile(mp, imachine)
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
               "HOME": os.path.join(iso, "home"),
               "TMPDIR": os.path.join(iso, "tmp")}
        env.update(extra)
        outj = os.path.join(iso, "rerun", tag + ".json")
        r = run_machine(imachine, iinput, outj, cwd=iso, env=env)
        with open(outj, "rb") as f:
            ob = f.read()
        outs.append((tag, r, ob))
    want_stdout = "gates 87 all_pass True faithful True"
    first = None
    for tag, r, ob in outs:
        gate("rerun-" + tag + "-rc0", r.returncode == 0,
             "rc=" + str(r.returncode) + " stderr=" + r.stderr.strip()[-120:])
        gate("rerun-" + tag + "-stdout-pass87", r.stdout.strip() == want_stdout,
             r.stdout.strip()[:90])
        gate("rerun-" + tag + "-audit-sha256-published",
             sha256_bytes(ob) == PUBLISHED["audit"]["sha256"], sha256_bytes(ob))
        gate("rerun-" + tag + "-audit-bytes", len(ob) == PUBLISHED["audit"]["bytes"], len(ob))
        d = json.loads(ob)
        gate("rerun-" + tag + "-gates87-allpass",
             d.get("gates_total") == 87 and d.get("gates_all_pass") is True
             and len(d.get("gates", [])) == 87
             and all(g.get("pass") for g in d.get("gates", [])),
             "gates=" + str(len(d.get("gates", []))))
        if first is None:
            first = ob
        else:
            gate("rerun-" + tag + "-byte-identical-first", ob == first, "cmp")
    return 0


def stage_tampers(base):
    idir = input_dir(base)
    mp = machine_path(base)
    tam_dir = os.path.join(base, "tampers")
    os.makedirs(tam_dir, exist_ok=True)
    finals = {}
    for t in TAMPERS:
        tag, w, off = t["tag"], t["w"], t["off"]
        want, othermsg = t["final"], t["other"]
        tdir = os.path.join(tam_dir, tag)
        if os.path.exists(tdir):
            shutil.rmtree(tdir)
        os.makedirs(tdir, exist_ok=True)
        # fresh probe input WITHOUT any pre-existing audit (probe-local out
        # path asserted absent before and after; the verifier never writes on
        # a pin mismatch anyway).
        pinput = os.path.join(tdir, "verifier_input")
        shutil.copytree(idir, pinput)
        wp = os.path.join(pinput, w)
        with open(wp, "rb") as f:
            original = f.read()
        probe = bytearray(original)
        probe[off] ^= 0x20
        with open(wp, "wb") as f:
            f.write(bytes(probe))
        pout = os.path.join(tdir, "probe_out.json")
        gate("tamper-" + tag + "-no-audit-pre", not os.path.isfile(pout), "absent")
        r = run_machine(mp, pinput, pout, cwd=tdir, env=None)
        gate("tamper-" + tag + "-rc1", r.returncode == 1, "rc=" + str(r.returncode))
        gate("tamper-" + tag + "-stdout-empty", r.stdout.strip() == "",
             "len=" + str(len(r.stdout.strip())))
        lastline = r.stderr.strip().splitlines()[-1].strip() if r.stderr.strip() else ""
        gate("tamper-" + tag + "-stderr-final-line", lastline == want, lastline[:100])
        gate("tamper-" + tag + "-stderr-exclusive", othermsg not in r.stderr, "exclusive")
        gate("tamper-" + tag + "-no-audit-written-post", not os.path.isfile(pout), "absent")
        gate("tamper-" + tag + "-maintree-w-unchanged",
             sha256_bytes(open(os.path.join(idir, w), "rb").read()) == W_PINS[w], "rehash")
        finals[tag] = lastline
    gate("tamper-independent-errors",
         finals["t1"] != finals["t2"] and "sweep39dead.json" in finals["t1"]
         and "k1075.json" in finals["t2"]
         and TAMPERS[0]["read_index"] > TAMPERS[1]["read_index"],
         "two distinct SystemExit identifications, read-order independent")
    return 0


def write_audit():
    pass_count = sum(1 for g in GATES if g["pass"])
    result = {
        "schema": "candidate-supply-whole-record-second-verification-pristine-reexec-third/1",
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
            "This third verification re-executes the published candidate-supply whole-record second-verifier on published bytes; it performs no search, judges no root, closes no row, rebuilds no candidate universe, and does not re-run the geometry lane.",
            "The record-identity routes measure published-record agreement only, not DFPN node cost or transposition-table hit rate, and justify no sharing implementation or worker split by themselves.",
            "REFUTED-D10 is NOT a LOSS proof; witness roots and the candidate supply are a conditional depth-10 sweep plan, not certificates.",
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
    out = os.path.join(base, "output", "k1075-third-harness-audit.json")
    with open(out, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("third harness gates", result["gates_total"], "all_pass", result["gates_all_pass"])
    if not result["gates_all_pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
