#!/usr/bin/env python3
"""16-worker (N-worker extension) memo split/merge measurement for the
cost-73k lane (2026-11-17, n11 class2-lane long-term lane; K0909 resume
item: worker-count-limit measurement, union growth and seed response at
N=16 of the published 2->4->8 series).

MEASUREMENT ONLY (no certificate publication, no verdict changes).

This extends the published 8-worker measurement (K0909 addendum 4,
measure_worker_split8_memo_merge_73k_20261117.py, commit 175048ff) to a
16-worker split of the same published cost-73k WIN7-D10 band (22 roots,
manifest class2-lane-cost73k-win7-certificates-20261117.json), with the
same repo-verbatim extractor (blob 52bcaf50..., including the two known
performance-only memo bugs; see item K0907).  Split: contiguous DP min-max
partition of the 22 bits by published band-ms23 per-bit node counts
(min-max group weight 11,857,737 = the bit-95 singleton):

  V1: [0]        V2: [7,11]      V3: [15]      V4: [35,39]
  V5: [41,44]    V6: [58,62]     V7: [73]      V8: [76]
  V9: [87]       V10: [89]       V11: [94]     V12: [95]
  V13: [97,98]   V14: [103]      V15: [105,112] V16: [117]

10 singleton-bit workers + 6 two-bit workers.  Each worker carries its
memo band-wide within its own bits (rows cleared per bit; every
certificate reconstructed and byte-compared against the published
certificate), then dumps the full memo table (KYOENWM1).

Offline merge: per-worker external sort + stream dedup (internal
conflicts counted), then a 16-way heapq merge-join (key incidence
histogram up to 16, cross conflicts on combined values, sorted KYOENWM2
merged seed16).  Seedrun: verbatim engine at MS=1<<25 (the published seed
capacity design point; hardened dumpMemo with fsyncSync every 32 MiB on
the ms25 variant only, dump bytes unchanged) seeds its memo from seed16
in file order through the engine's own memoEntry() and extracts all 22
bits band-wide in one process.  A light occupancy-only seeding simulator
(light_sim_seed_73k.mjs, double-anchored in the published design
measurement) predicts the seed insertion failures at MS=1<<24/25/26;
the engine's own seed failure count must equal the MS=1<<25 prediction.

Gates:
  split_exact_partition
  workerV1_per_bit_equals_band23_prefix (+ total + final occupancy at bit0)
  first_bit_fresh_anchors (V2..V16 heads == published fresh per-bit)
  bit95 memo-state-invariant
  internal_conflicts_zero (16 workers)
  cross_conflicts_zero (16-way merge)
  merge_deterministic (byte-identical repeat)
  worker_byte_identical (10x1 + 6x2 = 22)
  seedrun_byte_identical 22/22
  seedrun_seed_failed_equals_sim25
  seed_failure_rate_below_0.1pct (design-rule boundary test: seed16 load
    at MS=1<<25 is expected slightly above the ~0.15 design guideline)
  record_identity_no_violations
  record_identity_missing_equals_seed_failed

Interpretation guard: measurement only.  No new WIN/LOSS verdicts, no
manifest row opened or closed, certificate bytes unchanged.  The
repo-verbatim extractor is NOT modified in the repo (published
determinism chains).  WIN7-D10 proves a first-player win within depth 10
from the individual 7-stone roots only; REFUTED-D10 is not a LOSS proof.
The 11x11 empty board, both two-stone roots {49,60} and {59,60}, S2
{59,60} and classes 1/2/4 all remain UNKNOWN.

Usage: python3 measure_worker_split16_memo_merge_73k_20261117.py <out.json> <workdir>
       (env: KYOEN_NODE=node; every step resumes from <workdir>/)
"""
import hashlib
import json
import os
import subprocess
import sys

import measure_worker_split4_memo_merge_73k_20261117 as base

NODE = base.NODE
BAND23_PER_BIT = base.BAND23_PER_BIT
FRESH23_PER_BIT = base.FRESH23_PER_BIT
BAND23_OCC = base.BAND23_OCC
BAND23_TOTAL = base.BAND23_TOTAL

BITS_V1 = [0]
BITS_V2 = [7, 11]
BITS_V3 = [15]
BITS_V4 = [35, 39]
BITS_V5 = [41, 44]
BITS_V6 = [58, 62]
BITS_V7 = [73]
BITS_V8 = [76]
BITS_V9 = [87]
BITS_V10 = [89]
BITS_V11 = [94]
BITS_V12 = [95]
BITS_V13 = [97, 98]
BITS_V14 = [103]
BITS_V15 = [105, 112]
BITS_V16 = [117]
WORKER_DEFS = [
    ("workerV1", BITS_V1), ("workerV2", BITS_V2), ("workerV3", BITS_V3),
    ("workerV4", BITS_V4), ("workerV5", BITS_V5), ("workerV6", BITS_V6),
    ("workerV7", BITS_V7), ("workerV8", BITS_V8), ("workerV9", BITS_V9),
    ("workerV10", BITS_V10), ("workerV11", BITS_V11),
    ("workerV12", BITS_V12), ("workerV13", BITS_V13),
    ("workerV14", BITS_V14), ("workerV15", BITS_V15),
    ("workerV16", BITS_V16)]
# published comparison constants (K0909 series)
PUB = {
    "band23_total": 121186659,
    "two_way_workers_total": 119962147,
    "two_way_occupied_after": 4291899,
    "two_way_seed_failed_ms24": 1448,
    "nb4_workers_total": 112741501,
    "nb4_occupied_after": 4985986,
    "nb4_seed_md5": "7b098aeb625f722e5bfb13fcc615652a",
    "nb4_seed_failed_ms24": 16137,
    "boundary4_workers_total": 111953183,
    "boundary4_occupied_after": 4975265,
    "boundary4_seed_failed_ms24": 14657,
    "nb4_seedrun25_nodes": 72745351,
    "nb4_seedrun25_seed_failed": 28,
    "nb4_seedrun25_load_factor": 0.419,
    "nb4_seedrun24_nodes": 76903818,
    "way8_workers_total": 110639931,
    "way8_occupied_after": 5243408,
    "way8_seed_md5": "8d07cd7b82a3befc07cc775ea883e2e0",
    "way8_seedrun25_nodes": 70538916,
    "way8_seedrun25_seed_failed": 383,
    "way8_seedrun25_final_occupied": 14053298,
    "hybrid_seedrun25_nodes": 72761010,
}


def merge_pass_nway16(tags, seed_name="merged_seed16.kyoenwm2"):
    """16-way heapq merge-join of the distinct tables (adapted from the
    published merge_pass_nway; identical algebra, '16way' header label)."""
    import heapq
    from worker_memo_merge import combine_values, conflict_kind
    streams = [open(os.path.join(base.WORK, t + ".distinct.txt"),
                    encoding="utf-8") for t in tags]
    seed = os.path.join(base.WORK, seed_name)
    n_workers = len(tags)
    incidence = {k: 0 for k in range(1, n_workers + 1)}
    conflicts = {}
    occupied_after = 0
    shared_total = 0

    def _key_of(line):
        return line.split()[:4]

    def _emit_group(fo, key, vals):
        incidence[len(vals)] += 1
        cur = vals[0]
        for rec in vals[1:]:
            cur = combine_values(cur[0], cur[1], cur[2], cur[3], rec)
        ck = conflict_kind(*cur)
        if ck:
            conflicts.setdefault(ck, []).append(" ".join(key))
        fo.write(" ".join(key) + " %d %d %d %d\n" % cur)

    with open(seed, "w", encoding="utf-8") as fo:
        fo.write("KYOENWM2 merged worker_memo_tables cost73k 16way "
                 "workers=%s combine=win_min_lose_min_nowin_max_nolose_max\n"
                 % ",".join(tags))
        merged = heapq.merge(*streams, key=_key_of)
        group_key = None
        group_vals = []
        for line in merged:
            f = line.split()
            key = f[:4]
            if key != group_key:
                if group_key is not None:
                    _emit_group(fo, group_key, group_vals)
                    occupied_after += 1
                    if len(group_vals) >= 2:
                        shared_total += 1
                group_key = key
                group_vals = []
            group_vals.append((int(f[4]), int(f[5]), int(f[6]), int(f[7])))
        if group_key is not None:
            _emit_group(fo, group_key, group_vals)
            occupied_after += 1
            if len(group_vals) >= 2:
                shared_total += 1
    for s in streams:
        s.close()
    return {"workers": list(tags),
            "incidence_histogram": incidence,
            "shared_total": shared_total,
            "occupied_after": occupied_after,
            "cross_conflicts": {k: len(v) for k, v in conflicts.items()},
            "conflict_samples": {k: v[:5] for k, v in conflicts.items()},
            "seed_path": seed}


def harden_ms25_dump_fsync():
    """I/O-only hardening of the generated MS=1<<25 engine variant's
    dumpMemo (published seed-capacity practice): fs.fsyncSync() the dump
    every 32 MiB and once at the end, bounding dirty page cache during
    the ~0.6-0.7 GB dump write on this 1.09 GiB-cgroup remote-fs
    environment.  Dump bytes are unchanged; only the write schedule
    differs.  Applied ONLY to the ms25 variant, never to ms23/ms24."""
    path = os.path.join(base.WORK,
                        "class4_child1_cert_extractor_exact_wm4_ms25.ts")
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


def run_sim(seed_path, ms_shift):
    sim = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "light_sim_seed_73k.mjs")
    out = os.path.join(base.WORK, "sim_seed16_ms%d.json" % ms_shift)
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return json.load(open(out, encoding="utf-8"))
    cmd = [NODE, sim, seed_path, str(ms_shift), "", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("sim failed ms=%d: %s" % (ms_shift,
                                                   r.stderr[-800:]))
    return json.load(open(out, encoding="utf-8"))


def strip_ms(per_bit):
    out = []
    for p in per_bit:
        q = dict(p)
        q.pop("ms", None)
        out.append(q)
    return out


def drop_caches():
    try:
        with open("/proc/sys/vm/drop_caches", "w") as fh:
            fh.write("1\n")
    except OSError:
        pass


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "wm8.json"
    base.WORK = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "worker_split8_work")
    # local pinned inputs (same blobs as the published orchestrators)
    here = os.path.dirname(os.path.abspath(__file__))
    base.EXTRACTOR = os.path.join(here, "class4_child1_cert_extractor_exact.ts")
    base.DRIVER = os.path.join(here, "measure_worker_split_memo_73k.ts")
    base.LEGAL = os.path.join(here, "legal_candidates.py")
    base.CERTDIR = os.path.join(here, "class2-lane-cost73k-certificates")
    base.MANIFEST = os.path.join(
        base.CERTDIR, "class2-lane-cost73k-win7-certificates-20261117.json")
    os.makedirs(base.WORK, exist_ok=True)
    WORK = base.WORK
    state_path = os.path.join(WORK, "state.json")
    state = json.load(open(state_path, encoding="utf-8")) if \
        os.path.exists(state_path) else {}

    for name, path, exp in [
            ("extractor", base.EXTRACTOR, base.EXTRACTOR_BLOB),
            ("driver", base.DRIVER, "2a95d9527afa3c1a24685b697c822f451aae58a5"),
            ("legal", base.LEGAL, base.LEGAL_BLOB),
            ("manifest", base.MANIFEST, base.MANIFEST_BLOB)]:
        base.check_pin(name, path, exp)

    manifest, plan = base.build_plan()
    all_bits = [b["bit"] for b in json.load(open(plan))[ "bits"]]
    assert all_bits == sorted(sum((b for _, b in WORKER_DEFS), [])), \
        "split must be an exact ordered partition of the band"

    base.make_variant(23)
    base.make_variant(25)
    harden_ms25_dump_fsync()

    # ---- step 1: the eight workers ----
    sums = {}
    oks = {}
    for tag, bits in WORKER_DEFS:
        s, _ = base.run_worker(tag, 23, plan, bits, "350")
        if s is None:
            s = base.wait_worker(tag)
        sums[tag] = s
        state[tag] = {"total_nodes": s["total_nodes"],
                     "final_memo_occupied": s["final_memo_occupied"],
                     "all_bits_ok": s["all_bits_ok"]}
        json.dump(state, open(state_path, "w"))
        ok, _md = base.verify_snapshots(manifest, tag, bits)
        state[tag]["byte_identical"] = ok
        oks[tag] = ok
        json.dump(state, open(state_path, "w"))
        print("[worker] %s nodes %d occ %d bytes_ok %d/%d"
              % (tag, s["total_nodes"], s["final_memo_occupied"], ok,
                 len(bits)), flush=True)

    # ---- step 2: distinct passes (resume from state) ----
    distincts = {}
    for tag, _bits in WORKER_DEFS:
        if "distinct_" + tag in state:
            distincts[tag] = state["distinct_" + tag]
            continue
        distincts[tag] = base.distinct_pass(tag)
        state["distinct_" + tag] = distincts[tag]
        json.dump(state, open(state_path, "w"))
        print("[distinct] %s: %s" % (tag, distincts[tag]["distinct"]),
              flush=True)

    # ---- step 3: 8-way merge (resume from state) ----
    tags = [t for t, _ in WORKER_DEFS]
    seed_path = os.path.join(WORK, "merged_seed16.kyoenwm2")
    if "merge16" in state and os.path.exists(seed_path):
        m = state["merge16"]
        m["seed_path"] = seed_path
        print("[merge16] resumed occupied_after=%s" % m["occupied_after"],
              flush=True)
    else:
        m = merge_pass_nway16(tags)
        m["seed_md5"] = hashlib.md5(open(seed_path, "rb").read()).hexdigest()
        m2 = merge_pass_nway16(tags, seed_name="merged_seed16_repeat.kyoenwm2")
        m2md5 = hashlib.md5(open(m2["seed_path"], "rb").read()).hexdigest()
        os.unlink(m2["seed_path"])
        m["merge_deterministic"] = (m2md5 == m["seed_md5"])
        state["merge16"] = m
        json.dump(state, open(state_path, "w"))
        print("[merge16] occupied_after=%s shared=%s conflicts=%s"
              % (m["occupied_after"], m["shared_total"],
                 m["cross_conflicts"]), flush=True)

    # ---- step 4: sim at MS=1<<24 / 1<<25 / 1<<26 ----
    sims = {}
    for ms in (24, 25, 26):
        sims[ms] = run_sim(seed_path, ms)
        state["sim_ms%d" % ms] = sims[ms]
        json.dump(state, open(state_path, "w"))
        print("[sim] ms=%d failed=%s" % (ms, sims[ms].get("failed")),
              flush=True)

    # ---- step 5: free page cache, then the MS=1<<25 seedrun ----
    for tag, _ in WORKER_DEFS:
        for suffix in (".dump.txt", ".dump.sorted"):
            p = os.path.join(WORK, tag + suffix)
            if os.path.exists(p):
                os.remove(p)
    drop_caches()
    sumS, _ = base.run_worker("seedrun16", 25, plan, all_bits, "200",
                              seed_path=seed_path)
    if sumS is None:
        sumS = base.wait_worker("seedrun16", timeout_s=3600)
    state["seedrun16"] = {"total_nodes": sumS["total_nodes"],
                         "final_memo_occupied": sumS["final_memo_occupied"],
                         "seed": sumS.get("seed")}
    json.dump(state, open(state_path, "w"))
    okS, mdS = base.verify_snapshots(manifest, "seedrun16", all_bits)
    print("[seedrun16] nodes %d occ %d seed %s bytes_ok %d/22"
          % (sumS["total_nodes"], sumS["final_memo_occupied"],
             json.dumps(sumS.get("seed")), okS), flush=True)

    # ---- step 6: record identity on the seedrun dump ----
    ri = base.record_identity_pass("seedrun16", seed_path)
    state["record_identity"] = ri
    json.dump(state, open(state_path, "w"))
    print("[identity] present %d missing %d viol %d"
          % (ri["present"], ri["missing"], ri["value_violations"]),
          flush=True)

    # ---- gates ----
    per_bit_v1 = {p["bit"]: p["nodes_this_run"]
                  for p in sums["workerV1"]["per_bit"]}
    heads = {"workerV2": 7, "workerV3": 15, "workerV4": 35,
             "workerV5": 41, "workerV6": 58, "workerV7": 73,
             "workerV8": 76, "workerV9": 87, "workerV10": 89,
             "workerV11": 94, "workerV12": 95, "workerV13": 97,
             "workerV14": 103, "workerV15": 105, "workerV16": 117}
    anchor_ok = {}
    head_penalty = {}
    for tag, head in heads.items():
        got = [p["nodes_this_run"] for p in sums[tag]["per_bit"]
               if p["bit"] == head][0]
        anchor_ok[tag] = (got == FRESH23_PER_BIT[head])
        head_penalty[tag] = {
            "head_bit": head,
            "fresh_nodes": FRESH23_PER_BIT[head],
            "carried_band23_nodes": BAND23_PER_BIT[head],
            "worker_head_nodes": got,
            "vs_carried": got / BAND23_PER_BIT[head],
        }
    bit95_nodes = [p["nodes_this_run"] for p in sums["workerV12"]["per_bit"]
                   if p["bit"] == 95][0]
    workers_total = sum(sums[t]["total_nodes"] for t, _ in WORKER_DEFS)
    seed = (sumS.get("seed") or {})
    sim25_failed = sims[25].get("failed")
    gates = {
        "split_exact_partition": True,
        "workerV1_per_bit_equals_band23_prefix":
            all(per_bit_v1[b] == BAND23_PER_BIT[b] for b in BITS_V1),
        "workerV1_total":
            sums["workerV1"]["total_nodes"] == sum(BAND23_PER_BIT[b]
                                                   for b in BITS_V1),
        "workerV1_final_occupied":
            sums["workerV1"]["final_memo_occupied"] == BAND23_OCC[0],
        "first_bit_fresh_anchors": all(anchor_ok.values()),
        "bit95_memo_state_invariant": bit95_nodes == 11857737,
        "internal_conflicts_zero":
            all(not distincts[t]["conflicts"] for t, _ in WORKER_DEFS),
        "cross_conflicts_zero": not m["cross_conflicts"],
        "merge_deterministic": m["merge_deterministic"],
        "worker_byte_identical":
            all(oks[t] == len(b) for t, b in WORKER_DEFS),
        "seedrun_byte_identical": okS == 22,
        "seedrun_seed_failed_equals_sim25":
            seed.get("failed", -1) == sim25_failed,
        "seed_failure_rate_below_0.1pct":
            (seed.get("failed", 0) / max(1, seed.get("seeded", 1))) < 0.001,
        "record_identity_no_violations": ri["value_violations"] == 0,
        "record_identity_missing_equals_seed_failed":
            ri["missing"] == seed.get("failed", 0),
    }

    doc = {
        "schema": "n11-class2-lane-worker-split16-memo-merge-73k-20261117-v1",
        "date": "2026-11-17",
        "lane": "n11 class2-lane long-term (cost73k)",
        "purpose": ("16-worker DP min-max split memo merge measurement "
                    "(K0909 N-way extension, worker-count limit): 10 "
                    "singleton + 6 two-bit workers, incidence/conflict "
                    "merge, seed capacity at the MS=1<<25 design point, "
                    "head-bit reverse penalty"),
        "inputs": {
            "extractor_blob": base.EXTRACTOR_BLOB,
            "driver_blob": "2a95d9527afa3c1a24685b697c822f451aae58a5",
            "legal_blob": base.LEGAL_BLOB,
            "manifest_blob": base.MANIFEST_BLOB,
            "worker_memo_merge_blob": "fe2c5411393f789757b6e9a85d1f3925d6d260bc",
            "published_nb4_orchestrator": "measure_worker_split4_memo_merge_73k_20261117.py",
            "worker_ms": 23, "seedrun_ms": 25,
            "split": {t: b for t, b in WORKER_DEFS},
            "split_method": ("contiguous DP min-max by published band ms23 "
                             "per-bit nodes (min-max group weight 11857737)"),
        },
        "workers": {t: {"total_nodes": sums[t]["total_nodes"],
                        "final_occupied": sums[t]["final_memo_occupied"],
                        "byte_identical": oks[t],
                        "per_bit": strip_ms(sums[t]["per_bit"])}
                    for t, _ in WORKER_DEFS},
        "workers_total_nodes": workers_total,
        "workers_total_vs": {
            "band23_total": workers_total / PUB["band23_total"],
            "two_way_workers_total":
                workers_total / PUB["two_way_workers_total"],
            "nb4_workers_total": workers_total / PUB["nb4_workers_total"],
            "boundary4_workers_total":
                workers_total / PUB["boundary4_workers_total"],
            "way8_workers_total": workers_total / PUB["way8_workers_total"],
            "fresh23_total": workers_total / base.FRESH23_TOTAL,
        },
        "head_bit_reverse_penalty": head_penalty,
        "distinct_pass": {t: distincts[t] for t, _ in WORKER_DEFS},
        "merge16": {
            "incidence_histogram": m["incidence_histogram"],
            "shared_total": m["shared_total"],
            "occupied_after": m["occupied_after"],
            "cross_conflicts": m["cross_conflicts"],
            "conflict_samples": m["conflict_samples"],
            "seed_md5": m["seed_md5"],
            "merge_deterministic": m["merge_deterministic"],
            "occupied_after_vs": {
                "two_way": m["occupied_after"] / PUB["two_way_occupied_after"],
                "nb4": m["occupied_after"] / PUB["nb4_occupied_after"],
                "boundary4": m["occupied_after"] / PUB["boundary4_occupied_after"],
                "way8": m["occupied_after"] / PUB["way8_occupied_after"],
            },
        },
        "sim": {str(ms): sims[ms] for ms in (24, 25, 26)},
        "seedrun": {
            "total_nodes": sumS["total_nodes"],
            "final_occupied": sumS["final_memo_occupied"],
            "seed": sumS.get("seed"),
            "byte_identical": okS,
            "per_bit": strip_ms(sumS["per_bit"]),
            "load_factor_final": sumS["final_memo_occupied"] / (1 << 25),
            "total_nodes_vs_nb4_seedrun25":
                sumS["total_nodes"] / PUB["nb4_seedrun25_nodes"],
            "total_nodes_vs_nb4_seedrun24":
                sumS["total_nodes"] / PUB["nb4_seedrun24_nodes"],
            "total_nodes_vs_way8_seedrun25":
                sumS["total_nodes"] / PUB["way8_seedrun25_nodes"],
            "total_nodes_vs_hybrid_seedrun25":
                sumS["total_nodes"] / PUB["hybrid_seedrun25_nodes"],
        },
        "record_identity": ri,
        "published_reference": PUB,
        "gates": gates,
        "gates_all_pass": all(gates.values()),
        "interpretation_guard": (
            "MEASUREMENT ONLY. No new WIN/LOSS verdicts; no manifest row "
            "opened or closed; certificate bytes unchanged. The "
            "repo-verbatim extractor is unmodified in the repo (published "
            "determinism chains). WIN7-D10 proves a first-player win "
            "within depth 10 from the individual 7-stone roots only; "
            "REFUTED-D10 is not a LOSS proof. The 11x11 empty board, both "
            "two-stone roots {49,60} and {59,60}, S2 {59,60} and classes "
            "1/2/4 all remain UNKNOWN."),
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    print("gates_all_pass:", doc["gates_all_pass"], flush=True)
    for k, v in sorted(gates.items()):
        print("  gate %-44s %s" % (k, v), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
