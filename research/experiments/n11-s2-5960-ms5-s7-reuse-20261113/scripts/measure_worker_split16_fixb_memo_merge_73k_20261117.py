#!/usr/bin/env python3
"""fixB 16-way worker split memo merge measurement for the cost-73k lane
(2026-11-17, n11 class2-lane long-term lane).

MEASUREMENT ONLY (no certificate publication, no verdict changes).

Extends the published fixB measurements (2-way d3060c8e/2ead47be, 8-way
claim 7dca832c published at 49bf709e) to the 16-worker configuration of
the published verbatim 16-way measurement (claim c3d9c918): the 22 band
bits are partitioned contiguously by DP min-max on the fixB band ms23
per-bit node counts (min-max value 2,900,183 = bit 117 alone, which is
the structural lower bound; 10 single-bit workers + 6 two-bit workers),
V1 = the fixB band ms23 prefix anchor. All arms reuse the blob-pinned
pipeline of the fixB 2-way orchestrator (imported as a module, WORK
swapped to a fresh directory):
  arm0 band23   : fixB band ms23 single process (all 22 bits), distinct
                  table for the band-vs-merged comparison.
  arm1 v1..v16  : 16 fresh fixB workers (MS=1<<23, band-carried memo),
                  per-bit nodes, KYOENWM1 dumps, certificate byte gates,
                  head-bit anchors vs the fixB fresh battery values.
  arm2 census   : distinct pass per worker dump (expect records ==
                  distinct, dup_keys 0, max copies 1 on the fixed engine).
  arm3 merge    : 16-way merge-join with LIVE nowin/nolose bounds,
                  incidence histogram, cross conflict detection, merged
                  KYOENWM2 seed, determinism (second pass md5).
  arm4 sim      : light_sim_seed_73k.mjs MS sweep (1<<24 / 1<<25 / 1<<26)
                  on the 16-way merged seed.
  arm5 seedrun  : design-point MS=1<<25 full-band seedrun with the 16-way
                  seed: seed failures vs sim prediction, record-identity
                  gate, certificates 22/22 byte-identical.
  arm6 cmp      : fixB band23 distinct table vs the 16-way merged table
                  (merge non-closure under the fixed engine at N=16).

Interpretation guard: measurement only.  No new WIN/LOSS verdicts, no
manifest row opened or closed, certificate bytes unchanged.  The
repo-verbatim extractor is NOT modified in the repo (published determinism
chains); the fixB variants exist only in the work directory.  Adoption of
fixB as a production extractor is a separate lane decision.  WIN7-D10
proves a first-player win within depth 10 from the individual 7-stone
roots only; REFUTED-D10 is not a LOSS proof.  The 11x11 empty board, both
two-stone roots {49,60} and {59,60}, S2 {59,60} and classes 1/2/4 all
remain UNKNOWN.

Usage:  python3 measure_worker_split16_fixb_memo_merge_73k_20261117.py <out.json>
        (env: KYOEN_NODE=node; every step resumes from the state file)
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) or "."

# ---- load the published fixB 2-way orchestrator as a module ----
_src = os.path.join(HERE, "measure_worker_split_fixb_memo_merge_73k_20261117.py")
_spec = importlib.util.spec_from_file_location("fixb2way_mod", _src)
m = importlib.util.module_from_spec(_spec)
sys.modules["fixb2way_mod"] = m
_spec.loader.exec_module(m)

# fresh work directory (never writes into the 2-way session workdir)
WORK = os.path.join(m.OUT, "fixb_worker_split16_merge_73k_work")
m.WORK = WORK

NODE = m.NODE
SIM = m.SIM

# ---- published references (ratio reporting only) ----
FIXB_BAND23_TOTAL = 28620380          # published fixB band ms23 (2-way JSON)
FIXB_2WAY_WORKERS_TOTAL = 27837399    # published fixB 2-way workers
FIXB_2WAY_MERGED = 5479157            # published fixB 2-way merged keys
FIXB_2WAY_SEEDRUN25 = 6005236         # published fixB 2-way design-point run
FIXB_BAND24_TOTAL = 21697814          # published unseeded fixB band ms24
VERBATIM_8WAY_WORKERS_TOTAL = 110639931
VERBATIM_8WAY_MERGED = 5243408
VERBATIM_8WAY_SEEDRUN25 = 70538916
FIXB_8WAY_WORKERS_TOTAL = 27878487     # published fixB 8-way (49bf709e)
FIXB_8WAY_MERGED = 5773620
FIXB_8WAY_SEEDRUN25 = 5235505
VERBATIM_16WAY_WORKERS_TOTAL = 108802603   # published verbatim 16-way
VERBATIM_16WAY_MERGED = 5404082
VERBATIM_16WAY_SEEDRUN25 = 68006820

# fixB band ms23 per-bit nodes / per-bit memo occupancy (published 2-way
# measurement JSON: band23_fixb.per_bit) -- the DP min-max split inputs
BAND23_PB = {
    0: 1277392, 7: 1599816, 11: 802348, 15: 1860741, 35: 1366866,
    39: 448212, 41: 492423, 44: 1018910, 58: 970441, 62: 578116,
    73: 1247733, 76: 1025857, 87: 2486463, 89: 1185850, 94: 1425010,
    95: 1804296, 97: 1051712, 98: 1141194, 103: 1671971, 105: 916668,
    112: 1348178, 117: 2900183}
BAND23_OCC = {
    0: 372070, 7: 870291, 11: 1097055, 15: 1637447, 35: 2017802,
    39: 2139775, 41: 2266125, 44: 2560151, 58: 2796270, 62: 2887381,
    73: 3159518, 76: 3345235, 87: 3602778, 89: 3728353, 94: 3878095,
    95: 4029340, 97: 4267466, 98: 4412375, 103: 4593519, 105: 4732984,
    112: 4868771, 117: 5028453}

# DP min-max contiguous 16-partition of the 22 band bits on BAND23_PB
# (min-max value 2,900,183 = bit 117 alone, the structural lower bound;
# 10 single-bit workers + 6 two-bit workers); V1 = the band23 prefix anchor.
GROUPS = [
    ("v1", [0]),
    ("v2", [7]),
    ("v3", [11]),
    ("v4", [15]),
    ("v5", [35, 39]),
    ("v6", [41, 44]),
    ("v7", [58, 62]),
    ("v8", [73, 76]),
    ("v9", [87]),
    ("v10", [89]),
    ("v11", [94]),
    ("v12", [95]),
    ("v13", [97, 98]),
    ("v14", [103]),
    ("v15", [105, 112]),
    ("v16", [117]),
]
DP_MINMAX_VALUE = 2900183


def nway_merge(tags, seed_name="merged_seed16_fixb.kyoenwm2"):
    """N-way merge-join over the per-worker distinct tables (all sorted
    by the 4-tuple key, LC_ALL=C): per-key incidence histogram, LIVE
    bound cross-conflict detection, combined-record KYOENWM2 seed."""
    n = len(tags)
    files = [open(os.path.join(WORK, t + ".distinct.txt"),
                  encoding="utf-8") for t in tags]
    lines = [f.readline() for f in files]
    keys = [l.split(" ", 4)[:4] if l else None for l in lines]
    incidence = {i: 0 for i in range(1, n + 1)}
    conflicts = {}
    occupied_after = 0
    seed_path = os.path.join(WORK, seed_name)
    with open(seed_path, "w", encoding="utf-8") as fo:
        fo.write("KYOENWM2 merged fixb_worker_memo_tables cost73k 16way "
                 "V=%s combine=win_min_lose_min_nowin_max_nolose_max\n"
                 % ",".join(tags))
        while True:
            cur_key = None
            for k in keys:
                if k is not None and (cur_key is None or k < cur_key):
                    cur_key = k
            if cur_key is None:
                break
            vals = None
            cnt = 0
            for i in range(n):
                if keys[i] is not None and keys[i] == cur_key:
                    f = lines[i].split()
                    rec = (int(f[4]), int(f[5]), int(f[6]), int(f[7]))
                    if vals is None:
                        vals = rec
                    else:
                        vals = m_combine(vals[0], vals[1], vals[2],
                                         vals[3], rec)
                    cnt += 1
                    lines[i] = files[i].readline()
                    keys[i] = (lines[i].split(" ", 4)[:4]
                               if lines[i] else None)
            incidence[cnt] += 1
            occupied_after += 1
            ck = m_conflict(*vals)
            if ck:
                conflicts.setdefault(ck, []).append(" ".join(cur_key))
            fo.write(" ".join(cur_key) + " %d %d %d %d\n" % vals)
    for f in files:
        f.close()
    shared = sum(v for k, v in incidence.items() if k >= 2)
    return {"workers": list(tags), "shared_distinct": shared,
            "occupied_after": occupied_after,
            "incidence": {str(k): v for k, v in incidence.items()},
            "cross_conflicts": {k: len(v) for k, v in conflicts.items()},
            "conflict_samples": {k: v[:3] for k, v in conflicts.items()},
            "seed_path": seed_path}


def main():
    from worker_memo_merge import combine_values, conflict_kind
    global m_combine, m_conflict
    m_combine, m_conflict = combine_values, conflict_kind

    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        m.OUT, "fixb-worker-split16-memo-merge-73k-20261117.json")
    os.makedirs(WORK, exist_ok=True)
    m.check_pin("extractor", m.EXTRACTOR, m.EXTRACTOR_BLOB)
    m.check_pin("manifest", m.MANIFEST, m.MANIFEST_BLOB)
    m.check_pin("legal", m.LEGAL, m.LEGAL_BLOB)
    state_path = os.path.join(WORK, "state.json")
    state = {}
    if os.path.exists(state_path):
        state = json.load(open(state_path, encoding="utf-8"))

    manifest, plan = m.build_plan()
    m.MANIFEST_CACHE = manifest
    all_bits = [b["bit"] for b in json.load(open(plan))["bits"]]
    assert sorted(b for _, g in GROUPS for b in g) == sorted(all_bits), \
        "GROUPS must partition the 22 band bits"

    m.make_fixb_variant(23)
    m.make_fixb_variant(25)

    def arm(tag, ms_shift, bits, max_old, seed_path=""):
        if tag in state and isinstance(state[tag], dict) and \
                state[tag].get("total_nodes"):
            return state[tag]
        s, _ = m.run_worker(tag, ms_shift, plan, bits, max_old,
                            seed_path=seed_path)
        if s is None:
            s = m.wait_worker(tag)
        ok, _mds = m.verify_snapshots(tag, bits)
        doc = {"total_nodes": s["total_nodes"],
               "final_occupied": s["final_memo_occupied"],
               "seed": s.get("seed"),
               "wall_ms": s["wall_ms"],
               "byte_identical": ok,
               "per_bit": s["per_bit"]}
        state[tag] = doc
        json.dump(state, open(state_path, "w"))
        print("[done] %s nodes=%d occ=%d byte=%d/%d"
              % (tag, s["total_nodes"], s["final_memo_occupied"], ok,
                 len(bits)), flush=True)
        return doc

    # ---- arm0: fixB band ms23 single process (band-vs-merged input) ----
    band23 = arm("band23", 23, all_bits, "400")

    # ---- arm1: 16 fixB workers ----
    workers = {}
    for tag, bits in GROUPS:
        workers[tag] = arm(tag, 23, bits, "350")

    # ---- arm2: per-worker dump census ----
    distinct = {}
    for tag, _bits in GROUPS:
        if ("distinct_" + tag) not in state:
            state["distinct_" + tag] = m.distinct_pass(tag)
            json.dump(state, open(state_path, "w"))
        distinct[tag] = state["distinct_" + tag]
        print("[census] %s records=%d distinct=%d dup=%d"
              % (tag, distinct[tag]["records"], distinct[tag]["distinct"],
                 distinct[tag]["dup_keys"]), flush=True)

    # ---- arm3: 16-way live-bound merge (determinism double run) ----
    if "merge" not in state:
        mg = nway_merge([t for t, _ in GROUPS])
        mg["seed_md5"] = hashlib.md5(
            open(mg["seed_path"], "rb").read()).hexdigest()
        mg2 = nway_merge([t for t, _ in GROUPS],
                         "merged_seed16_fixb_repeat.kyoenwm2")
        mg["seed_md5_repeat"] = hashlib.md5(
            open(mg2["seed_path"], "rb").read()).hexdigest()
        mg["merge_deterministic"] = (mg["seed_md5"] ==
                                     mg["seed_md5_repeat"])
        os.remove(mg2["seed_path"])
        state["merge"] = mg
        json.dump(state, open(state_path, "w"))
    mg = state["merge"]
    print("[merge] occupied_after=%d shared=%d deterministic=%s"
          % (mg["occupied_after"], mg["shared_distinct"],
             mg["merge_deterministic"]), flush=True)
    seed_path = mg["seed_path"]

    # ---- arm4: sim MS sweep on the 16-way merged seed ----
    for shift in (24, 25, 26):
        key = "sim_ms%d" % shift
        if key not in state:
            sim_out = os.path.join(WORK, key + ".json")
            subprocess.run([NODE, SIM, seed_path, str(shift), "", sim_out],
                           capture_output=True, text=True, check=True)
            state[key] = json.loads(open(sim_out, encoding="utf-8").read())
            json.dump(state, open(state_path, "w"))
        print("[sim] ms%d failed=%d rate=%.6f load=%.4f"
              % (shift, state[key]["failed"], state[key]["failure_rate"],
                 state[key]["load_factor"]), flush=True)
    sim24, sim25, sim26 = state["sim_ms24"], state["sim_ms25"], state["sim_ms26"]

    # ---- arm5: design-point MS=1<<25 seedrun with the 16-way seed ----
    seedrun25 = arm("seedrun25", 25, all_bits, "220", seed_path=seed_path)
    if "record_identity25" not in state:
        state["record_identity25"] = m.record_identity_pass("seedrun25",
                                                            seed_path)
        json.dump(state, open(state_path, "w"))
    ri25 = state["record_identity25"]
    print("[ri25] present=%d missing=%d violations=%d"
          % (ri25["present"], ri25["missing"],
             ri25["value_violations"]), flush=True)

    # ---- arm6: band23 table vs 16-way merged table ----
    if "distinct_band23" not in state:
        state["distinct_band23"] = m.distinct_pass("band23")
        json.dump(state, open(state_path, "w"))
    if "band_vs_merged" not in state:
        state["band_vs_merged"] = m.band_vs_merged_pass("band23",
                                                        seed_path)
        json.dump(state, open(state_path, "w"))
    bvm = state["band_vs_merged"]
    print("[bvm] shared=%d only_in_band=%d only_in_merged=%d"
          % (bvm["shared"], bvm["only_in_band"], bvm["only_in_merged"]),
          flush=True)

    # ---- gates ----
    v1 = workers["v1"]
    v1_pb = {p["bit"]: p["nodes_this_run"] for p in v1["per_bit"]}
    heads = []
    for tag, bits in GROUPS[1:]:
        pb = {p["bit"]: p["nodes_this_run"] for p in workers[tag]["per_bit"]}
        hb = bits[0]
        heads.append({"tag": tag, "head_bit": hb,
                      "nodes": pb[hb],
                      "battery": m.FIXB_BATTERY_PER_BIT_NODES[hb],
                      "ok": pb[hb] == m.FIXB_BATTERY_PER_BIT_NODES[hb]})
    workers_total = sum(w["total_nodes"] for w in workers.values())
    seeded = (seedrun25["seed"] or {}).get("seeded", 0)
    failed = (seedrun25["seed"] or {}).get("failed", 0)
    gates = {
        "all_workers_byte_identical":
            sum(w["byte_identical"] for w in workers.values()) == 22,
        "v1_per_bit_equals_band23_prefix":
            all(v1_pb[b] == BAND23_PB[b] for b in GROUPS[0][1]),
        "v1_final_occupied_equals_band23":
            v1["final_occupied"] == BAND23_OCC[GROUPS[0][1][-1]],
        "head_bits_equal_fixb_battery": all(h["ok"] for h in heads),
        "no_duplicate_keys_all_workers":
            all(distinct[t]["dup_keys"] == 0 and
                 distinct[t]["max_copies"] == 1
                 for t, _ in GROUPS),
        "internal_conflicts_zero":
            all(not distinct[t]["conflicts"] for t, _ in GROUPS),
        "cross_conflicts_zero": not mg["cross_conflicts"],
        "merge_deterministic": mg["merge_deterministic"],
        "seed25_failed_equals_sim25_prediction": failed == sim25["failed"],
        "record_identity25_no_violations":
            ri25["value_violations"] == 0,
        "record_identity25_missing_equals_seed25_failed":
            ri25["missing"] == failed,
        "seedrun25_byte_identical": seedrun25["byte_identical"] == 22,
        "seed25_failure_rate_below_0.1pct":
            (failed / max(1, seeded)) < 0.001,
        "band_vs_merged16_shared_no_conflicts":
            not bvm["shared_value_conflicts"],
        "workers_total_sanity":
            workers_total <= band23["total_nodes"] * 1.05,
    }

    doc = {
        "schema": "n11-class2-lane-fixb-worker-split16-memo-merge-73k-20261117-v1",
        "date": "2026-11-17",
        "lane": "n11 class2-lane long-term (cost73k)",
        "purpose": ("fixB 16-way worker split memo merge measurement "
                    "(DP min-max 16 split on the fixB band ms23 per-bit "
                    "node counts, min-max 2,900,183 = bit 117 alone; "
                    "verbatim 16-way configuration on the "
                    "fixB engine; live-bound 16-way merge; sim sweep; "
                    "MS=1<<25 design-point seedrun)"),
        "inputs": {
            "extractor_blob": m.EXTRACTOR_BLOB,
            "manifest_blob": m.MANIFEST_BLOB,
            "legal_blob": m.LEGAL_BLOB,
            "engine_variant": m.ENGINE_VARIANT_TEXT
            if hasattr(m, "ENGINE_VARIANT_TEXT") else
            ("verbatim + MS substitution + Int32Array memo keys + "
             "sentinel-aware nowin/nolose updates (fixB, K0907) + "
             "dump/seed export block; line-level changes asserted"),
            "worker_ms": 23,
            "seedrun_ms": 25,
            "groups": {t: b for t, b in GROUPS},
            "dp_minmax_value": DP_MINMAX_VALUE,
        },
        "workers": {t: workers[t] for t, _ in GROUPS},
        "workers_total_nodes": workers_total,
        "ratios": {
            "vs_fixb_band23_28620380": workers_total / FIXB_BAND23_TOTAL,
            "vs_fixb_2way_workers_27837399":
                workers_total / FIXB_2WAY_WORKERS_TOTAL,
            "vs_verbatim_8way_workers_110639931":
                workers_total / VERBATIM_8WAY_WORKERS_TOTAL,
            "vs_fixb_8way_workers_27878487":
                workers_total / FIXB_8WAY_WORKERS_TOTAL,
            "vs_verbatim_16way_workers_108802603":
                workers_total / VERBATIM_16WAY_WORKERS_TOTAL,
            "merged_vs_fixb_2way_merged_5479157":
                mg["occupied_after"] / FIXB_2WAY_MERGED,
            "merged_vs_verbatim_8way_merged_5243408":
                mg["occupied_after"] / VERBATIM_8WAY_MERGED,
            "merged_vs_fixb_8way_merged_5773620":
                mg["occupied_after"] / FIXB_8WAY_MERGED,
            "merged_vs_verbatim_16way_merged_5404082":
                mg["occupied_after"] / VERBATIM_16WAY_MERGED,
            "seedrun25_vs_fixb_2way_seedrun25_6005236":
                seedrun25["total_nodes"] / FIXB_2WAY_SEEDRUN25,
            "seedrun25_vs_verbatim_8way_seedrun25_70538916":
                seedrun25["total_nodes"] / VERBATIM_8WAY_SEEDRUN25,
            "seedrun25_vs_fixb_8way_seedrun25_5235505":
                seedrun25["total_nodes"] / FIXB_8WAY_SEEDRUN25,
            "seedrun25_vs_verbatim_16way_seedrun25_68006820":
                seedrun25["total_nodes"] / VERBATIM_16WAY_SEEDRUN25,
            "seedrun25_vs_fixb_band24_21697814":
                seedrun25["total_nodes"] / FIXB_BAND24_TOTAL,
        },
        "distinct_pass": {t: distinct[t] for t, _ in GROUPS},
        "merge": mg,
        "sim_ms24": sim24,
        "sim_ms25": sim25,
        "sim_ms26": sim26,
        "seedrun25_fixb": seedrun25,
        "record_identity25": ri25,
        "band_vs_merged": bvm,
        "head_bit_anchors": {h["tag"]: {"head_bit": h["head_bit"],
                                        "nodes": h["nodes"],
                                        "battery": h["battery"],
                                        "ok": h["ok"]} for h in heads},
        "gates": gates,
        "gates_all_pass": all(gates.values()),
        "interpretation_guard": (
            "MEASUREMENT ONLY. No new WIN/LOSS verdicts; no manifest row "
            "opened or closed; certificate bytes unchanged (byte-identity "
            "is a gate, not a republication). The repo-verbatim extractor "
            "is unmodified in the repo (published determinism chains); "
            "fixB adoption is a separate lane decision. Node counts of "
            "published certificates remain the verbatim-engine values. "
            "WIN7-D10 proves a first-player win within depth 10 from the "
            "individual 7-stone roots only; REFUTED-D10 is not a LOSS "
            "proof. The 11x11 empty board, both two-stone roots {49,60} "
            "and {59,60}, S2 {59,60} and classes 1/2/4 all remain "
            "UNKNOWN."),
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    print("gates_all_pass:", doc["gates_all_pass"], flush=True)
    for k, v in gates.items():
        print("  gate %-44s %s" % (k, v), flush=True)
    return 0


m_combine = None
m_conflict = None

if __name__ == "__main__":
    sys.exit(main())
