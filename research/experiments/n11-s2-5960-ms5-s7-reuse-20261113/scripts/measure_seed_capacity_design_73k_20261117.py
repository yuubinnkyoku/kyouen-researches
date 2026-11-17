#!/usr/bin/env python3
"""Seed capacity design measurement for N-way merged worker-memo seeds
(cost-73k lane, 2026-11-17, n11 class2-lane long-term lane; K0909 follow-up).

MEASUREMENT ONLY (no certificate publication, no verdict changes).

Context (K0909, published): the 4-worker merged memo seed of the cost-73k
band (4,985,986 distinct keys, seed md5 7b098aeb625f722e5bfb13fcc615652a)
seeded into the verbatim engine at MS=1<<24 lost 16,137 records (0.324%) to
64-slot probe-window saturation, breaking the pre-run gate
"seed insertion failure < 0.1%", while the record-identity gate stayed
closed (missing == failed exactly, value violations 0).  The 2-way merged
seed (4,291,899 keys, md5 e7c2c17e7a91d8ea17f433f3bb482f29) at the same
MS=1<<24 lost only 1,448 (0.034%) and passed.  This measurement supplies
the missing design rule:

  1. Rebuild both merged seeds with the published pipeline (4-way from
     the running repro of measure_worker_split4..., 2-way rebuilt here
     from the published K0909 split) and pin both md5s against the
     published values.
  2. Validate a light occupancy-only seeding simulator (light_sim_seed_
     73k.mjs: verbatim mHash + 64-slot linear probe, no key arrays) at
     MS=1<<24 against BOTH published engine failure counts (16,137 and
     1,448).  With distinct-key seeds the engine's key-match branch
     never fires during seeding, so the occupancy-only table is exact.
  3. Sweep MS = 1<<25, 1<<26 with the simulator (MS=1<<26 already gives
     zero failures; full engine runs at MS>=1<<26 exceed this
     environment's ~1.0 GiB cgroup; the simulator is validated in step 2
     and cross-checked again at the design point in step 5).
  4. Localise the MS=1<<24 failure knee in seed size S with prefix
     simulations of the 4-way seed (real keys, insertion order of the
     merged file).
  5. Run the FULL band seedrun at the design point MS=1<<25 with the
     verbatim engine (21 B/slot -> ~704 MB table) and close all gates:
     22/22 certificates byte-identical, seed failure < 0.1%,
     record-identity violations 0 with missing == failed, and the
     engine's own seedMemo failure count == simulator prediction.

Gates (all must pass):
  repro_4way_seed_md5_matches_published
  repro_workers_match_published
  repro_distincts_match_published
  repro_seedrun4_seed_failed_matches_published_16137 (engine, MS=24)
  repro_seedrun4_nodes_match_published
  sim24_4way_failed_equals_engine (light sim == 16137)
  sim24_2way_seed_md5_matches_published (e7c2c17e...)
  sim24_2way_failed_equals_engine (light sim == 1448)
  sim25_design_point_failure_below_0.1pct
  two_way_workers_match_published
  two_way_distincts_match_published
  seedrun25_byte_identical_22
  seedrun25_seed_failed_equals_sim25
  seedrun25_seed_failure_below_0.1pct
  seedrun25_record_identity_no_violations
  seedrun25_record_identity_missing_equals_seed_failed

Interpretation guard: measurement only.  No new WIN/LOSS verdicts, no
manifest row opened or closed, certificate bytes unchanged.  The verbatim
extractor is NOT modified in the repo (published determinism chains).
WIN7-D10 proves a first-player win within depth 10 from the individual
7-stone roots only; REFUTED-D10 is not a LOSS proof.  The 11x11 empty
board, both two-stone roots {49,60} and {59,60}, S2 {59,60} and classes
1/2/4 all remain UNKNOWN.

Usage: python3 measure_seed_capacity_design_73k_20261117.py <out.json>
       (env: KYOEN_NODE=node; every step resumes from the shared work
       directory output/worker_split4_merge_73k_work/)
"""
import hashlib
import json
import os
import subprocess
import sys

import measure_worker_split4_memo_merge_73k_20261117 as base

HERE = base.HERE
OUT = base.OUT
WORK = base.WORK
NODE = base.NODE
CERTDIR = base.CERTDIR
SIM = os.path.join(HERE, "light_sim_seed_73k.mjs")

PUB = {
    "w_totals": {"workerW1": 29193572, "workerW2": 30417638,
                 "workerW3": 31104578, "workerW4": 22025713},
    "w_occ": {"workerW1": 3816312, "workerW2": 4026734,
              "workerW3": 4605832, "workerW4": 3358092},
    "w_distinct": {"workerW1": 1979858, "workerW2": 1793658,
                   "workerW3": 1544867, "workerW4": 1565935},
    "seed4_md5": "7b098aeb625f722e5bfb13fcc615652a",
    "seed4_keys": 4985986,
    "seedrun4_nodes": 76903818,
    "seedrun4_failed": 16137,
    "seedrun4_inserted": 4969849,
    "seedA_md5": "e7c2c17e7a91d8ea17f433f3bb482f29",
    "seedA_keys": 4291899,
    "seedrunA_failed": 1448,
    "seedrunA_nodes": 85747496,
    "workerA_total": 48482011,
    "workerB_total": 71480136,
    "distinctA": 2619833,
    "distinctB": 2554155,
}
BITS_A = [0, 7, 11, 15, 35, 39, 41, 44, 58, 62, 73]
BITS_B = [76, 87, 89, 94, 95, 97, 98, 103, 105, 112, 117]
ALL_BITS = BITS_A + BITS_B
PREFIXES_MS24 = [1000000, 2000000, 3000000, 3500000, 4000000,
                 4291899, 4500000, 4750000, 4985986]


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 22), b""):
            h.update(blk)
    return h.hexdigest()


def harden_ms25_dump_fsync():
    """I/O-only hardening of the generated MS=1<<25 engine variant's
    dumpMemo (see the phase-6 NOTE): fs.fsyncSync() the dump every 32 MiB
    and once at the end, bounding dirty page cache during the ~0.6-0.7 GB
    dump write on this 1.09 GiB-cgroup remote-fs environment.  Dump bytes
    are unchanged (same records, order and formatting); only the write
    schedule differs.  Applied ONLY to the ms25 variant, never to the
    published ms23/ms24 variants."""
    path = os.path.join(WORK, "class4_child1_cert_extractor_exact_wm4_ms25.ts")
    src = open(path, encoding="utf-8").read()
    old_flush = ("    if (buf.length > (1 << 20)) { fs.writeSync(fd, buf); "
                 "buf = ''; }\n")
    new_flush = ("    if (buf.length > (1 << 20)) { fs.writeSync(fd, buf); "
                 "buf = '';\n"
                 "      if (++_nfl >= 32) { fs.fsyncSync(fd); _nfl = 0; } }\n")
    old_decl = "  let buf = '';\n  for (let i = 0; i < MS; i++) {"
    new_decl = "  let buf = '';\n  let _nfl = 0;\n  for (let i = 0; i < MS; i++) {"
    old_tail = ("  if (buf.length) fs.writeSync(fd, buf);\n"
                "  fs.closeSync(fd);\n}")
    new_tail = ("  if (buf.length) fs.writeSync(fd, buf);\n"
                "  fs.fsyncSync(fd);\n  fs.closeSync(fd);\n}")
    for a in (old_flush, old_decl, old_tail):
        if src.count(a) != 1:
            raise SystemExit("ms25 dump hardening anchor not unique: %r"
                             % a[:40])
    src = src.replace(old_decl, new_decl).replace(old_flush, new_flush) \
             .replace(old_tail, new_tail)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(src)


def run_sim(seed_path, ms_shift, prefix=None):
    out = os.path.join(WORK, "sim_%s_ms%d%s.json"
                       % (os.path.basename(seed_path).split(".")[0], ms_shift,
                          ("_p%d" % prefix) if prefix else ""))
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return json.load(open(out, encoding="utf-8"))
    # sim argv: [2]=seedPath [3]=msShift [4]=prefixLimit ('' = unlimited)
    #           [5]=outJson
    cmd = [NODE, SIM, seed_path, str(ms_shift),
           str(prefix) if prefix else "", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("sim failed ms=%d: %s" % (ms_shift, r.stderr[-800:]))
    return json.load(open(out, encoding="utf-8"))


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        OUT, "seed-capacity-design-73k-20261117.json")
    os.makedirs(WORK, exist_ok=True)
    gates = {}
    info = {}

    manifest, plan = base.build_plan()
    seed4 = os.path.join(WORK, "merged_seed4.kyoenwm2")
    seedA = os.path.join(WORK, "merged_seedA.kyoenwm2")

    # ---------- phase 1: 4-way repro state (workers + seed + seedrun4) ------
    state_path = os.path.join(WORK, "state.json")
    state = json.load(open(state_path, encoding="utf-8")) \
        if os.path.exists(state_path) else {}
    workers = {}
    for tag in ["workerW1", "workerW2", "workerW3", "workerW4"]:
        if tag not in state:
            raise SystemExit("4-way repro incomplete: %s missing; run the "
                             "published orchestrator first" % tag)
        workers[tag] = state[tag]
    gates["repro_workers_match_published"] = (
        all(workers[t]["total_nodes"] == PUB["w_totals"][t] for t in workers)
        and all(workers[t]["final_memo_occupied"] == PUB["w_occ"][t]
                for t in workers))
    if "distinct_workerW1" not in state:
        raise SystemExit("4-way repro incomplete: distinct passes missing")
    distincts = {t: state["distinct_" + t] for t in workers}
    gates["repro_distincts_match_published"] = (
        all(distincts[t]["distinct"] == PUB["w_distinct"][t] for t in distincts)
        and all(not distincts[t]["conflicts"] for t in distincts))
    if not os.path.exists(seed4):
        raise SystemExit("4-way seed missing; let the published orchestrator "
                         "finish the merge first")
    seed4_md5 = md5_of(seed4)
    gates["repro_4way_seed_md5_matches_published"] = seed4_md5 == PUB["seed4_md5"]
    seedrun4 = state.get("seedrun4") or {}
    gates["repro_seedrun4_seed_failed_matches_published_16137"] = (
        seedrun4.get("seed", {}).get("failed") == PUB["seedrun4_failed"])
    gates["repro_seedrun4_nodes_match_published"] = (
        seedrun4.get("total_nodes") == PUB["seedrun4_nodes"])

    # ---------- phase 2: light-sim validation at MS=1<<24 -------------------
    sim24 = run_sim(seed4, 24)
    gates["sim24_4way_failed_equals_engine"] = (
        sim24["failed"] == PUB["seedrun4_failed"]
        and sim24["seeded"] == PUB["seed4_keys"])
    info["sim24_4way"] = sim24

    # ---------- phase 3: MS sweep with the simulator (4-way seed) -----------
    sweep = {}
    for ms in (25, 26):
        sweep["ms%d" % ms] = run_sim(seed4, ms)
    gates["sim25_design_point_failure_below_0.1pct"] = (
        sweep["ms25"]["failed"] / max(1, sweep["ms25"]["seeded"]) < 0.001)
    info["sweep_4way"] = sweep

    # ---------- phase 4: prefix knee localisation at MS=1<<24 --------------
    prefixes = [run_sim(seed4, 24, p) for p in PREFIXES_MS24]
    info["prefix_ms24"] = prefixes

    # ---------- phase 5: 2-way rebuild (published K0909 split) --------------
    sumsA = {}
    for tag, bits in (("workerA", BITS_A), ("workerB", BITS_B)):
        s, _ = base.run_worker(tag, 23, plan, bits, "350")
        if s is None:
            s = base.wait_worker(tag, timeout_s=3600)
        sumsA[tag] = s
        state[tag] = s
        json.dump(state, open(state_path, "w"))
        ok, _md = base.verify_snapshots(manifest, tag, bits)
        if ok != len(bits):
            raise SystemExit("worker %s certificates not byte-identical" % tag)
        print("[done] %s nodes=%d" % (tag, s["total_nodes"]))
        print("[flush]", flush=True)
    gates["two_way_workers_match_published"] = (
        sumsA["workerA"]["total_nodes"] == PUB["workerA_total"]
        and sumsA["workerB"]["total_nodes"] == PUB["workerB_total"])
    distA = {}
    for tag in ("workerA", "workerB"):
        if "distinct_" + tag not in state:
            d = base.distinct_pass(tag)
            state["distinct_" + tag] = d
            json.dump(state, open(state_path, "w"))
        distA[tag] = state["distinct_" + tag]
        print("[distinct] %s -> %s" % (tag, distA[tag]["distinct"]), flush=True)
    gates["two_way_distincts_match_published"] = (
        distA["workerA"]["distinct"] == PUB["distinctA"]
        and distA["workerB"]["distinct"] == PUB["distinctB"]
        and not distA["workerA"]["conflicts"]
        and not distA["workerB"]["conflicts"])
    if not os.path.exists(seedA):
        mA = base.merge_pass_nway(["workerA", "workerB"],
                                   seed_name="merged_seedA.kyoenwm2")
        state["mergeA"] = mA
        json.dump(state, open(state_path, "w"))
    else:
        mA = state.get("mergeA") or {}
    mA["seed_md5"] = md5_of(seedA)
    # Record-level byte identity against the published 2-way seed
    # (K0909, md5 e7c2c17e...): this orchestrator reuses the 4-way
    # merge_pass_nway, whose header line hardcodes "cost73k 4way
    # workers=workerA,workerB".  The published 2-way merge wrote
    # "cost73k A=workerA B=workerB".  Replacing the first line of the
    # rebuilt file with the published 2-way header must reproduce the
    # published md5 exactly; any record difference would not.
    pub_2way_header = (b"KYOENWM2 merged worker_memo_tables cost73k "
                       b"A=workerA B=workerB "
                       b"combine=win_min_lose_min_nowin_max_nolose_max\n")
    _data = open(seedA, "rb").read()
    _nl = _data.index(b"\n")
    mA["seed_md5_published_header"] = hashlib.md5(
        pub_2way_header + _data[_nl + 1:]).hexdigest()
    mA["published_2way_header_note"] = (
        "record-level byte identity gate; the rebuilt file's own header "
        "line differs (4-way merge_pass_nway header), the published-header "
        "substitution reproduces the published md5 exactly")
    gates["sim24_2way_seed_md5_matches_published"] = (
        mA["seed_md5_published_header"] == PUB["seedA_md5"])
    sim24A = run_sim(seedA, 24)
    gates["sim24_2way_failed_equals_engine"] = (
        sim24A["failed"] == PUB["seedrunA_failed"]
        and sim24A["seeded"] == PUB["seedA_keys"])
    info["sim24_2way"] = sim24A
    sweepA = {("ms%d" % ms): run_sim(seedA, ms) for ms in (25, 26)}
    info["sweep_2way"] = sweepA

    # ---------- phase 6: design-point full seedrun MS=1<<25 -----------------
    # NOTE (experiment facts, 2026-11-17, cgroup ~1.09 GiB):
    #  - attempt 1 (--max-old-space-size=500) was oom-killed DURING dumpMemo
    #    (dump truncated at slot index 8,628,069 / 33,554,431, ~26%).
    #  - attempt 2 (cap 200) was oom-killed again during dumpMemo, at index
    #    17,136,175 (~61% of slots, ~426 MB written; VmRSS steady 806 MB).
    #    The full 22-bit search itself COMPLETED at cap 200.
    #  - an isolated reproduction (672 MB of MS=1<<25 typed arrays + the
    #    verbatim dumpMemo string-chunk loop, cap 200) writing 678 MB
    #    SURVIVES, so the dump-time kill is not explained by arrays +
    #    dump loop alone (residual suspects: post-search heap state and
    #    dirty-page-cache headroom on this remote-backed fs).
    #  - attempt 3 (cap 150, fsync-hardened variant, fresh cgroup with
    #    ~5.6 GB of prior dumps in page cache) was oom-killed MID-SEARCH
    #    before bit 15 (memory.peak hit the cgroup limit exactly;
    #    seeding and bits 0/7/11 byte-identical to earlier attempts).
    #    ~5.1 GB of no-longer-needed dump/sort/distinct intermediates
    #    were then deleted and the page cache dropped before the redo.
    # Hardening for the redo: cap 200 (empirically completed the full
    # band search in attempt 2) plus the variant-local dumpMemo I/O
    # patch below.  The dump's BYTES are unchanged (same records,
    # order, formatting); only write scheduling differs.  Measured
    # cost: a 32 MiB chunk+fsync on this fs is ~36 ms.
    base.make_variant(25)  # engine variant for the design point
    harden_ms25_dump_fsync()
    sum25, _ = base.run_worker("seedrun25", 25, plan, ALL_BITS, "200",
                               seed_path=seed4)
    if sum25 is None:
        sum25 = base.wait_worker("seedrun25", timeout_s=3600)
    state["seedrun25"] = sum25
    json.dump(state, open(state_path, "w"))
    ok25, md25 = base.verify_snapshots(manifest, "seedrun25", ALL_BITS)
    seedstats25 = sum25.get("seed") or {}
    gates["seedrun25_byte_identical_22"] = ok25 == 22
    gates["seedrun25_seed_failed_equals_sim25"] = (
        seedstats25.get("failed") == sweep["ms25"]["failed"])
    gates["seedrun25_seed_failure_below_0.1pct"] = (
        seedstats25.get("failed", 0) / max(1, seedstats25.get("seeded", 1))
        < 0.001)
    ri25 = base.record_identity_pass("seedrun25", seed4)
    state["record_identity25"] = ri25
    json.dump(state, open(state_path, "w"))
    gates["seedrun25_record_identity_no_violations"] = (
        ri25["value_violations"] == 0)
    gates["seedrun25_record_identity_missing_equals_seed_failed"] = (
        ri25["missing"] == seedstats25.get("failed", -1))
    info["seedrun25"] = {
        "total_nodes": sum25["total_nodes"],
        "final_occupied": sum25["final_memo_occupied"],
        "load_factor_final": sum25["final_memo_occupied"] / (1 << 25),
        "seed": seedstats25,
        "wall_ms": sum25["wall_ms"],
        "byte_identical": ok25,
        "per_bit": sum25["per_bit"],
        "vs_seedrun24_nodes": sum25["total_nodes"] / PUB["seedrun4_nodes"],
    }
    info["record_identity25"] = ri25

    # ---------- output ------------------------------------------------------
    doc = {
        "schema": "n11-class2-lane-seed-capacity-design-73k-20261117-v1",
        "date": "2026-11-17",
        "lane": "n11 class2-lane long-term (cost73k)",
        "purpose": ("K0909 follow-up: seed capacity design for N-way merged "
                    "worker-memo seeds. Light-sim validation against both "
                    "published engine failure counts, MS sweep, prefix knee "
                    "localisation, design-point full band seedrun at MS=1<<25."),
        "inputs": {
            "extractor_blob": base.EXTRACTOR_BLOB,
            "manifest_blob": base.MANIFEST_BLOB,
            "legal_blob": base.LEGAL_BLOB,
            "published_4way_seed_md5": PUB["seed4_md5"],
            "published_2way_seed_md5": PUB["seedA_md5"],
            "light_sim": ("verbatim mHash line + 64-slot linear probe; "
                          "occupancy-only table (distinct-key seeds make "
                          "the engine's key-match branch unreachable "
                          "during seeding)"),
        },
        "repro": {
            "workers": {t: {"total_nodes": workers[t]["total_nodes"],
                            "final_occupied": workers[t]["final_memo_occupied"]}
                        for t in workers},
            "distincts": {t: {k: distincts[t][k] for k in
                               ("records", "distinct", "dup_keys", "max_copies",
                                "conflicts")} for t in distincts},
            "seed4_md5": seed4_md5,
            "seedrun4_nodes": seedrun4.get("total_nodes"),
            "seedrun4_seed": seedrun4.get("seed"),
        },
        "sim": {
            "validation": {
                "ms24_4way": {"failed": sim24["failed"],
                              "engine_failed": PUB["seedrun4_failed"]},
                "ms24_2way": {"failed": sim24A["failed"],
                              "engine_failed": PUB["seedrunA_failed"]},
            },
            "sweep_4way": {k: {"failed": v["failed"], "seeded": v["seeded"],
                               "inserted": v["inserted"],
                               "occupied_after": v["occupied_after"],
                               "load_factor": v["load_factor"],
                               "max_cluster": v["base_clusters"]["max_cluster"],
                               "bases_ge_64": v["base_clusters"]["bases_ge_64"],
                               "bases_ge_32": v["base_clusters"]["bases_ge_32"],
                               "bases_ge_16": v["base_clusters"]["bases_ge_16"],
                               "own_cluster_ge64": v["failure_attribution"]["own_cluster_ge64"],
                               "spill_over_lt64": v["failure_attribution"]["spill_over_lt64"]}
                          for k, v in sweep.items()},
            "sweep_2way": {k: {"failed": v["failed"], "seeded": v["seeded"],
                               "max_cluster": v["base_clusters"]["max_cluster"],
                               "own_cluster_ge64": v["failure_attribution"]["own_cluster_ge64"],
                               "spill_over_lt64": v["failure_attribution"]["spill_over_lt64"]}
                           for k, v in sweepA.items()},
            "prefix_ms24_4way": [
                {"prefix": p["prefix_limit"], "seeded": p["seeded"],
                 "failed": p["failed"], "max_cluster": p["base_clusters"]["max_cluster"],
                 "own_cluster_ge64": p["failure_attribution"]["own_cluster_ge64"],
                 "spill_over_lt64": p["failure_attribution"]["spill_over_lt64"]}
                for p in prefixes],
            "mechanism_4way_ms24": {
                "base_clusters": sim24["base_clusters"],
                "failure_attribution": sim24["failure_attribution"],
            },
        },
        "seedrun25": info["seedrun25"],
        "record_identity25": {
            "present": ri25["present"], "missing": ri25["missing"],
            "value_violations": ri25["value_violations"],
            "seedrun_dump_stats": {k: ri25["seedrun_dump_stats"][k] for k in
                                   ("records", "distinct", "dup_keys",
                                    "max_copies", "conflicts")},
        },
        "two_way_rebuild": {
            "workers": {t: sumsA[t]["total_nodes"] for t in sumsA},
            "distincts": {t: distA[t]["distinct"] for t in distA},
            "merge": {k: mA.get(k) for k in
                      ("occupied_after", "shared_total", "seed_md5",
                       "seed_md5_published_header")},
        },
        "gates": gates,
        "gates_all_pass": all(gates.values()),
        "interpretation_guard": (
            "MEASUREMENT ONLY. No new WIN/LOSS verdicts; no manifest row "
            "opened or closed; certificate bytes unchanged. The verbatim "
            "extractor is unmodified in the repo (published determinism "
            "chains). WIN7-D10 proves a first-player win within depth 10 "
            "from the individual 7-stone roots only; REFUTED-D10 is not a "
            "LOSS proof. The 11x11 empty board, both two-stone roots "
            "{49,60} and {59,60}, S2 {59,60} and classes 1/2/4 all remain "
            "UNKNOWN."),
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    print("gates_all_pass:", doc["gates_all_pass"])
    for k, v in gates.items():
        print("  gate %-52s %s" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
