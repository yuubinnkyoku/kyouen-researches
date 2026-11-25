#!/usr/bin/env python3
"""Hybrid seed union measurement for the cost-73k band (2026-11-17, n11
class2-lane long-term lane; K0909 follow-up; executes the
next_measurement stages of the published hybrid seed union design
DESIGN_DERIVED_NOT_MEASURED).

MEASUREMENT ONLY (no certificate publication, no verdict changes).

Context (published, all pins verified at run start):
  - boundary-respecting 4-way measurement (K0909 update, commit 439ad7e3,
    measurement JSON blob b97c9334, orchestrator blob 5ac1e3c0):
    FINAL4 = 4,975,265 keys (md5 35ccec0e...), published 2-way seed =
    4,291,899 keys (md5 e7c2c17e...), shared 4,291,637,
    only_in_final4 = 683,628, only_in_seed2 = 262 (merge non-closure),
    value violations 0.
  - hybrid seed union design (commit 0454908c, design JSON blob 8ec64f21):
    union = FINAL4 records in file order + the 262 only-in-2way records
    appended in deterministic key order under the single FINAL4 header;
    4,975,527 keys, initial load factor 0.1483 at MS=1<<25.
  - seed capacity design (K0909 update, commit 2375b55d, JSON blob pinned
    in K0909 item): node-balanced 4-way seed (4,985,986 keys) at MS=1<<25
    failed 28/4,985,986 (0.00056%), band run 72,745,351 nodes.

This measurement rebuilds the whole published pipeline from pinned blobs
(the six ms23 workers, distinct passes, the 2-way merge with the
published-md5 gate, the cascade merge to FINAL4 with the published-md5
gate), then:

  1. extracts the exact 262 only-in-2way records (seed2 key order),
  2. builds the hybrid seed file (FINAL4 bytes verbatim + 262 appended
     records; byte-prefix gate),
  3. predicts MS=1<<24/25/26 seed insertion failures with the published
     light simulator (light_sim_seed_73k.mjs),
  4. runs the full 22-bit band with the verbatim engine at MS=1<<25
     seeded from the hybrid file (cap 200 + the fsync-hardened ms25
     dumpMemo variant; unnecessary intermediates deleted and page cache
     dropped before the run, per the seed-capacity OOM lessons),
  5. gates: 22/22 certificates byte-identical, engine seed failures ==
     simulator prediction, failure rate < 0.1%, record identity closed
     (missing == failed exactly, value violations 0), bit95 nodes
     invariant 11,857,737.

Interpretation guard: measurement only. No new WIN/LOSS verdicts, no
manifest row opened or closed, certificate bytes unchanged. The verbatim
extractor is NOT modified in the repo (published determinism chains).
WIN7-D10 proves a first-player win within depth 10 from the individual
7-stone roots only; REFUTED-D10 is not a LOSS proof. The 11x11 empty
board, both two-stone roots {49,60} and {59,60}, S2 {59,60} and classes
1/2/4 all remain UNKNOWN.

Usage: python3 measure_hybrid_seed_union_73k_20261117.py <out.json> <workdir>
       (env: KYOEN_NODE=node; every step resumes from <workdir>/)
"""
import hashlib
import json
import os
import subprocess
import sys

os.environ.setdefault(
    "WM4_PROGRESS",
    os.path.join(os.path.dirname(os.path.abspath(__file__)) or ".",
                 "hybrid-progress.md"))

import measure_worker_split4_boundary_memo_merge_73k_20261117 as base

NODE = base.NODE
SIM = os.path.join(base.HERE, "light_sim_seed_73k.mjs")

# published constants (hybrid design + boundary + seed capacity + K0909)
PUBH = {
    "final4_keys": 4975265,
    "final4_md5": "35ccec0eb01e9b1b3719fa7e0c6ff4e9",
    "seed2_keys": 4291899,
    "seed2_md5": "e7c2c17e7a91d8ea17f433f3bb482f29",
    "shared_keys": 4291637,
    "only_in_final4": 683628,
    "only_in_seed2": 262,
    "hybrid_keys": 4975527,
    "initial_load_factor_ms_1_25": 0.1482822597026825,
    "design_upper_bound_ms24": 14919,
    "final4_seedrun24_nodes": 76599320,
    "final4_seedrun24_failed": 14657,
    "final4_seedrun24_final_occupied": 10525071,
    "nb4_seedrun25_nodes": 72745351,
    "nb4_seedrun25_failed": 28,
    "nb4_seedrun25_final_occupied": 14073139,
    "nb4_seedrun24_nodes": 76903818,
    "nb4_seedrun24_failed": 16137,
    "twoway_seedrun24_nodes": 85747496,
    "twoway_seedrun24_failed": 1448,
    "w0_total": 27424708, "w0_occ": 3705871,
    "w2_total": 36575507, "w2_occ": 4869649,
    "bit95_nodes": 11857737,
    "design_json_blob": "8ec64f21b60b378595a749fc941f2232e0db5c21",
    "boundary_json_blob": "b97c9334f04f98f6ba7bb8a4c8b1de9689810d5e",
    "boundary_orchestrator_blob": "5ac1e3c0ec47ec3f9ae63ed709362feb5a1df213",
}

# published per-bit node counts for the two reference seedruns
BOUNDARY_SEEDRUN24_PER_BIT = {
    0: 2765265, 7: 3030474, 11: 1774250, 15: 5571172, 35: 3277134,
    39: 1187014, 41: 836889, 44: 2544270, 58: 2267428, 62: 1331263,
    73: 5077777, 76: 2505884, 87: 4926001, 89: 3057624, 94: 3689968,
    95: 11857737, 97: 2044593, 98: 3541039, 103: 3941504, 105: 2417863,
    112: 3220485, 117: 5733686}
NB4_SEEDRUN25_PER_BIT = {
    0: 2618538, 7: 2801397, 11: 1722684, 15: 5256618, 35: 3038477,
    39: 1165863, 41: 904783, 44: 2507541, 58: 2190542, 62: 1222492,
    73: 4763049, 76: 2678868, 87: 5385605, 89: 2287764, 94: 2782241,
    95: 11857737, 97: 1711491, 98: 3921779, 103: 3574697, 105: 2214120,
    112: 2965299, 117: 5180766}


def progress(line):
    base.progress("[hybrid] " + line)
    print(line, flush=True)


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 22), b""):
            h.update(blk)
    return h.hexdigest()


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 22), b""):
            h.update(blk)
    return h.hexdigest()


def harden_ms25_dump_fsync():
    """I/O-only hardening of the boundary-family MS=1<<25 engine variant's
    dumpMemo (same anchors as the published seed-capacity hardening, here
    applied to the boundary orchestrator's variant file name): fs.fsyncSync()
    the dump every 32 MiB and once at the end. Dump bytes unchanged."""
    path = os.path.join(
        base.WORK, "class4_child1_cert_extractor_exact_wm_ms25.ts")
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


def run_sim(seed_path, ms_shift, tag):
    out = os.path.join(base.WORK, "sim_%s_ms%d.json" % (tag, ms_shift))
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return json.load(open(out, encoding="utf-8"))
    cmd = [NODE, SIM, seed_path, str(ms_shift), "", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("sim failed ms=%d: %s" % (ms_shift, r.stderr[-800:]))
    return json.load(open(out, encoding="utf-8"))


def record_identity_pass_sorted(tag, seed_path):
    """Corrected record-identity gate (bug found on the first full run).

    base.record_identity_pass merge-joins two key-sorted streams, but
    the hybrid seed file is NOT key-sorted as a whole: it is the sorted
    FINAL4 table with the 262 extracted records appended at the end.
    Feeding it to the sorted merge miscounts (first run measured
    missing 282 = 20 real + all 262 appended tail keys, present
    4975245).  This variant externally sorts a headerless copy of the
    seed records, asserts the distinct table is key-sorted, then runs
    the same equal-or-stronger value merge as the base pass.  Returns
    the base fields plus the full missing-key list as evidence.
    """
    stats = base.distinct_pass(tag)
    env = dict(os.environ, LC_ALL="C")
    dst = os.path.join(base.WORK, tag + ".distinct.txt")
    with open(dst, "rb") as fh:
        subprocess.run(["sort", "-c"], stdin=fh, env=env, check=True)
    rec_sorted = os.path.join(base.WORK, tag + ".seedrec.sorted")
    with open(seed_path, "rb") as fi, open(rec_sorted, "wb") as fo:
        subprocess.run(["tail", "-n", "+2"], stdin=fi, stdout=fo,
                        check=True)
    with open(rec_sorted, "rb") as fi, \
            open(rec_sorted + ".s", "wb") as fo:
        subprocess.run(["sort", "-S", "200M"], stdin=fi, stdout=fo,
                       env=env, check=True)
    os.replace(rec_sorted + ".s", rec_sorted)
    viol = []
    missing_keys = []
    present = 0
    with open(rec_sorted, encoding="utf-8") as fs_, \
            open(dst, encoding="utf-8") as ff:
        rs = fs_.readline()
        rf = ff.readline()
        while rs or rf:
            ks = rs.split()[:4] if rs else None
            kf = rf.split()[:4] if rf else None
            if ks and (not kf or ks < kf):
                missing_keys.append(" ".join(ks))
                rs = fs_.readline()
            elif kf and (not ks or kf < ks):
                rf = ff.readline()
            else:
                fsd = rs.split()
                ffd = rf.split()
                win, lose = int(fsd[4]), int(fsd[5])
                nowin, nolose = int(fsd[6]), int(fsd[7])
                fw, fl = int(ffd[4]), int(ffd[5])
                fnw, fnl = int(ffd[6]), int(ffd[7])
                okw = win == 255 or fw <= win
                okl = lose == 255 or fl <= lose
                oknw = base.bound_at_least(fnw, nowin)
                oknl = base.bound_at_least(fnl, nolose)
                if not (okw and okl and oknw and oknl):
                    viol.append(" ".join(ks))
                present += 1
                rs = fs_.readline()
                rf = ff.readline()
    return {"present": present, "missing": len(missing_keys),
            "value_violations": len(viol),
            "violation_samples": viol[:3], "missing_keys": missing_keys,
            "identity_method": "external_sort_merge",
            "seed_file_sorted": False, "seedrun_dump_stats": stats}


def extract_seed2_only(seed2_path, seed4_path, out_path):
    """Stream both key-sorted tables (one header line each); write every
    seed2 record whose key is absent from FINAL4, verbatim, in seed2 key
    order. Returns stats + the written record keys."""
    n = 0
    keys = []
    with open(seed2_path, encoding="utf-8") as f2, \
            open(seed4_path, encoding="utf-8") as f4:
        f2.readline()  # header
        f4.readline()  # header
        r2 = f2.readline()
        r4 = f4.readline()
        with open(out_path, "w", encoding="utf-8") as fo:
            while r2:
                k2 = r2.split()[:4]
                if r4:
                    k4 = r4.split()[:4]
                    if k4 < k2:
                        r4 = f4.readline()
                        continue
                    if k4 == k2:
                        r2 = f2.readline()
                        continue
                fo.write(r2)
                keys.append(" ".join(k2))
                n += 1
                r2 = f2.readline()
    return {"count": n, "keys": keys}


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "hybrid.json"
    base.WORK = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        base.HERE, "hybrid_seed_work")
    os.makedirs(base.WORK, exist_ok=True)
    state_path = os.path.join(base.WORK, "state.json")
    state = json.load(open(state_path, encoding="utf-8")) if \
        os.path.exists(state_path) else {}

    for name, path, exp in [
            ("extractor", base.EXTRACTOR, base.EXTRACTOR_BLOB),
            ("driver", base.DRIVER, base.DRIVER_BLOB),
            ("legal", base.LEGAL, base.LEGAL_BLOB),
            ("manifest", base.MANIFEST, base.MANIFEST_BLOB)]:
        base.check_pin(name, path, exp)

    plan = os.path.join(base.WORK, "plan73k.json")
    if not os.path.exists(plan):
        manifest, plan = base.build_plan()

    extra_path = os.path.join(base.WORK, "seed2_only_262.kyoenwm2x")
    hybrid_path = os.path.join(base.WORK, "hybrid_seed_73k.kyoenwm2")

    if state.get("phaseA_complete") and os.path.exists(hybrid_path):
        # resume: phase A (workers/merges) results already in state
        sums = state["sums"]
        dist = state["dist"]
        m2 = state["merge2"]
        m01 = state["m01"]
        m23 = state["m23"]
        mf = state["merge_final"]
        pairwise = state["pairwise"]
        cmp42 = state["final4_vs_seed2"]
        ex = state["extract"]
        hb = state["hybrid_build"]
        wa_nodes, wa_occ = state["series"]["workerA"]
        wb_nodes, wb_occ = state["series"]["workerB"]
        w0_nodes, w0_occ = state["series"]["w0"]
        w1_nodes, w1_occ = state["series"]["w1"]
        w2_nodes, w2_occ = state["series"]["w2"]
        w3_nodes, w3_occ = state["series"]["w3"]
    else:
        base.make_variant(23)
        base.make_variant(24)

        # ---- step 1: the six ms23 workers ----
        specs = [("workerA", base.BITS_WA, "350"),
                 ("workerB", base.BITS_WB, "350"),
                 ("w0", base.BITS_W0, "350"), ("w1", base.BITS_W1, "350"),
                 ("w2", base.BITS_W2, "350"), ("w3", base.BITS_W3, "350")]
        sums = {}
        for tag, bits, old in specs:
            s, _ = base.run_worker(tag, 23, plan, bits, old)
            if s is None:
                s = base.wait_worker(tag)
            sums[tag] = s
            ok, _mds = base.verify_snapshots(tag, bits)
            state[tag] = {"total_nodes": s["total_nodes"],
                          "final_memo_occupied": s["final_memo_occupied"],
                          "all_bits_ok": s["all_bits_ok"],
                          "byte_identical": ok}
            json.dump(state, open(state_path, "w"))
            progress("worker %s: nodes %d occ %d bytes_ok %d/%d"
                     % (tag, s["total_nodes"], s["final_memo_occupied"],
                        ok, len(bits)))

        def series(tag):
            pb = sorted(sums[tag]["per_bit"], key=lambda p: p["bit"])
            return ([p["nodes_this_run"] for p in pb],
                    [p["memo_occupied_after"] for p in pb])

        wa_nodes, wa_occ = series("workerA")
        wb_nodes, wb_occ = series("workerB")
        w0_nodes, w0_occ = series("w0")
        w1_nodes, w1_occ = series("w1")
        w2_nodes, w2_occ = series("w2")
        w3_nodes, w3_occ = series("w3")

        # ---- step 2: distinct passes ----
        dist = {}
        for tag, _, _ in specs:
            dist[tag] = base.distinct_pass(tag)
            state["distinct_" + tag] = dist[tag]
            json.dump(state, open(state_path, "w"))
            progress("distinct %s: records %d distinct %d dup %d"
                     % (tag, dist[tag]["records"], dist[tag]["distinct"],
                        dist[tag]["dup_keys"]))

        dpath = lambda t: os.path.join(base.WORK, t + ".distinct.txt")

        # ---- step 3: 2-way reproduction merge (published md5 gate) ----
        seed2_path = os.path.join(base.WORK, "merged_seed_2way.kyoenwm2")
        m2 = base.merge_join(dpath("workerA"), dpath("workerB"),
                             seed2_path, base.SEED2_HEADER)
        m2["seed_md5"] = md5_of(seed2_path)
        base.merge_join(dpath("workerA"), dpath("workerB"),
                        seed2_path + ".tmp", base.SEED2_HEADER)
        m2["merge_deterministic"] = (
            md5_of(seed2_path + ".tmp") == m2["seed_md5"])
        os.remove(seed2_path + ".tmp")
        state["merge2"] = m2
        json.dump(state, open(state_path, "w"))
        progress("merge2: shared %d occ_after %d md5 %s det %s"
                 % (m2["shared_distinct"], m2["occupied_after"],
                    m2["seed_md5"], m2["merge_deterministic"]))

        # ---- step 4: six pairwise merges among w0..w3 ----
        pairwise = {}
        for i in range(4):
            for j in range(i + 1, 4):
                ti, tj = "w%d" % i, "w%d" % j
                out = os.path.join(base.WORK,
                                   "pair_%s_%s.kyoenwm2m" % (ti, tj))
                st = base.merge_join(dpath(ti), dpath(tj), out, None)
                pairwise["%s_%s" % (ti, tj)] = st
                os.remove(out)
        state["pairwise"] = pairwise
        json.dump(state, open(state_path, "w"))
        progress("pairwise: " + json.dumps(
            {k: [v["shared_distinct"], v["occupied_after"],
                 v["cross_conflicts"]] for k, v in pairwise.items()}))

        # ---- step 5: cascade merge to FINAL4 ----
        m01_path = os.path.join(base.WORK, "m01.kyoenwm2m")
        m23_path = os.path.join(base.WORK, "m23.kyoenwm2m")
        m01 = base.merge_join(dpath("w0"), dpath("w1"), m01_path, None)
        m23 = base.merge_join(dpath("w2"), dpath("w3"), m23_path, None)
        seed4_path = os.path.join(base.WORK, "merged_seed_4way.kyoenwm2")
        mf = base.merge_join(m01_path, m23_path, seed4_path,
                             base.SEED4_HEADER)
        mf["seed_md5"] = md5_of(seed4_path)
        base.merge_join(m01_path, m23_path, seed4_path + ".tmp",
                        base.SEED4_HEADER)
        mf["merge_deterministic"] = (
            md5_of(seed4_path + ".tmp") == mf["seed_md5"])
        os.remove(seed4_path + ".tmp")
        state["m01"] = m01
        state["m23"] = m23
        state["merge_final"] = mf
        json.dump(state, open(state_path, "w"))
        progress("cascade: m01 %d m23 %d final occ %d shared %d md5 %s"
                 % (m01["occupied_after"], m23["occupied_after"],
                    mf["occupied_after"], mf["shared_distinct"],
                    mf["seed_md5"]))

        # ---- step 6: FINAL4 vs seed2 (non-closure constants) ----
        cmp42 = base.compare_final4_vs_seed2(seed4_path, seed2_path)
        state["final4_vs_seed2"] = cmp42
        json.dump(state, open(state_path, "w"))
        progress("final4_vs_seed2: shared %d only4 %d only2 %d viol %d"
                 % (cmp42["shared"], cmp42["only_in_final4"],
                    cmp42["only_in_seed2"], cmp42["value_violations"]))

        # ---- step 7: extract the 262 only-in-2way records ----
        ex = extract_seed2_only(seed2_path, seed4_path, extra_path)
        # determinism: second extraction byte-identical
        extract_seed2_only(seed2_path, seed4_path, extra_path + ".tmp")
        ex["deterministic"] = (open(extra_path, "rb").read() ==
                               open(extra_path + ".tmp", "rb").read())
        os.remove(extra_path + ".tmp")
        ex["md5"] = md5_of(extra_path)
        ex["sha256"] = sha256_of(extra_path)
        state["extract"] = {k: ex[k] for k in
                            ("count", "deterministic", "md5", "sha256")}
        state["extract"]["first_keys"] = ex["keys"][:5]
        state["extract"]["last_keys"] = ex["keys"][-3:]
        json.dump(state, open(state_path, "w"))
        progress("extract only-in-2way: count %d det %s md5 %s"
                 % (ex["count"], ex["deterministic"], ex["md5"]))

        # ---- step 8: build the hybrid seed (byte-prefix gate) ----
        size4 = os.path.getsize(seed4_path)
        sizex = os.path.getsize(extra_path)
        with open(hybrid_path, "wb") as fo:
            with open(seed4_path, "rb") as fi:
                remaining = size4
                while remaining:
                    blk = fi.read(min(1 << 22, remaining))
                    fo.write(blk)
                    remaining -= len(blk)
            with open(extra_path, "rb") as fi:
                while True:
                    blk = fi.read(1 << 22)
                    if not blk:
                        break
                    fo.write(blk)
        hb = {
            "final4_bytes": size4, "extra_bytes": sizex,
            "hybrid_bytes": os.path.getsize(hybrid_path),
            "size_sum_gate": os.path.getsize(hybrid_path) == size4 + sizex,
            "byte_prefix_gate": (open(hybrid_path, "rb").read(size4) ==
                                 open(seed4_path, "rb").read()),
            "hybrid_md5": md5_of(hybrid_path),
            "hybrid_sha256": sha256_of(hybrid_path),
        }
        with open(hybrid_path, encoding="utf-8") as fh:
            fh.readline()  # header
            hb["hybrid_records"] = sum(1 for _ in fh)
        state["hybrid_build"] = hb
        json.dump(state, open(state_path, "w"))
        progress("hybrid built: %d records %d bytes md5 %s prefix_ok %s"
                 % (hb["hybrid_records"], hb["hybrid_bytes"],
                    hb["hybrid_md5"], hb["byte_prefix_gate"]))

        state["sums"] = sums
        state["dist"] = dist
        state["series"] = {
            "workerA": [wa_nodes, wa_occ], "workerB": [wb_nodes, wb_occ],
            "w0": [w0_nodes, w0_occ], "w1": [w1_nodes, w1_occ],
            "w2": [w2_nodes, w2_occ], "w3": [w3_nodes, w3_occ]}
        state["phaseA_complete"] = True
        json.dump(state, open(state_path, "w"))

    # ---- step 9: cleanup + drop caches before the ms25 seedrun ----
    # (idempotent; removes merge intermediates that are no longer needed
    # so the MS=1<<25 seedrun starts with a cold page cache, per the
    # seed-capacity OOM lessons)
    removed = 0
    for t in ("workerA", "workerB", "w0", "w1", "w2", "w3"):
        for suf in (".dump.txt", ".dump.sorted", ".distinct.txt"):
            q = os.path.join(base.WORK, t + suf)
            if os.path.exists(q):
                removed += os.path.getsize(q)
                os.remove(q)
    for p in ("m01.kyoenwm2m", "m23.kyoenwm2m",
              "merged_seed_2way.kyoenwm2", "merged_seed_4way.kyoenwm2"):
        q = os.path.join(base.WORK, p)
        if os.path.exists(q):
            removed += os.path.getsize(q)
            os.remove(q)
    if removed:
        progress("cleanup: removed %.2f GiB of merge intermediates"
                 % (removed / (1 << 30)))
    drop = None
    try:
        subprocess.run(["sync"], check=True)
        with open("/proc/sys/vm/drop_caches", "w") as fh:
            fh.write("3\n")
        drop = "ok"
    except Exception as e:  # noqa: BLE001
        drop = "failed: %s" % e
    if not state.get("cleanup_removed_bytes"):
        state["cleanup_removed_bytes"] = removed
    state["drop_caches"] = drop
    json.dump(state, open(state_path, "w"))
    progress("drop_caches: %s" % drop)

    # ---- step 10: sim predictions (hybrid seed) ----
    sim = {}
    for ms in (25, 24, 26):
        sim["ms%d" % ms] = run_sim(hybrid_path, ms, "hybrid")
    progress("sim: ms25 failed %d / ms24 failed %d / ms26 failed %d"
             % (sim["ms25"]["failed"], sim["ms24"]["failed"],
                sim["ms26"]["failed"]))

    # ---- step 11: hybrid seedrun, verbatim engine MS=1<<25, cap 200 ----
    base.make_variant(25)
    harden_ms25_dump_fsync()
    tag = "hybridseed25"
    sumS, _ = base.run_worker(tag, 25, plan, base.ALL_BITS, "200",
                              seed_path=hybrid_path)
    if sumS is None:
        sumS = base.wait_worker(tag, timeout_s=3600)
    state["seedrun25"] = {"total_nodes": sumS["total_nodes"],
                          "final_memo_occupied": sumS["final_memo_occupied"],
                          "seed": sumS.get("seed")}
    json.dump(state, open(state_path, "w"))
    okS, mdS = base.verify_snapshots(tag, base.ALL_BITS)
    progress("seedrun25: nodes %d occ %d seed %s bytes_ok %d/22"
             % (sumS["total_nodes"], sumS["final_memo_occupied"],
                json.dumps(sumS.get("seed")), okS))

    # ---- step 12: record identity on the seedrun dump ----
    # corrected variant: the base sorted-merge miscounts on the hybrid
    # seed file (FINAL4 sorted + 262 appended records, not key-sorted)
    ri = record_identity_pass_sorted(tag, hybrid_path)
    state["record_identity"] = ri
    json.dump(state, open(state_path, "w"))
    progress("record_identity: present %d missing %d viol %d"
             % (ri["present"], ri["missing"], ri["value_violations"]))

    # ---- gates ----
    seedstats = sumS.get("seed") or {}
    hybrid_per_bit = {p["bit"]: p["nodes_this_run"]
                      for p in sumS["per_bit"]}
    gates = {
        # published 2-way reproduction (pipeline correctness anchor)
        "repro_workerA_total":
            sums["workerA"]["total_nodes"] == base.PUB["workerA_total"],
        "repro_workerA_occ":
            sums["workerA"]["final_memo_occupied"] == base.PUB["workerA_occ"],
        "repro_workerA_per_bit_nodes":
            wa_nodes == base.PUB["workerA_nodes"],
        "repro_workerA_per_bit_occ":
            wa_occ == base.PUB["workerA_occ_series"],
        "repro_workerB_total":
            sums["workerB"]["total_nodes"] == base.PUB["workerB_total"],
        "repro_workerB_occ":
            sums["workerB"]["final_memo_occupied"] == base.PUB["workerB_occ"],
        "repro_workerB_per_bit_nodes":
            wb_nodes == base.PUB["workerB_nodes"],
        "repro_workerB_per_bit_occ":
            wb_occ == base.PUB["workerB_occ_series"],
        "repro_merged2_seed_md5":
            m2["seed_md5"] == PUBH["seed2_md5"],
        "repro_merged2_occupied_after":
            m2["occupied_after"] == PUBH["seed2_keys"],
        "repro_merged2_shared":
            m2["shared_distinct"] == base.PUB["merged2_shared"],
        "merge2_deterministic": m2["merge_deterministic"],
        # boundary 4-way worker prefix anchors
        "w0_per_bit_nodes": w0_nodes == base.PUB["workerA_nodes"][:6],
        "w0_per_bit_occ": w0_occ == base.PUB["workerA_occ_series"][:6],
        "w0_total": sums["w0"]["total_nodes"] == PUBH["w0_total"],
        "w0_final_occ": sums["w0"]["final_memo_occupied"] == PUBH["w0_occ"],
        "w2_per_bit_nodes": w2_nodes == base.PUB["workerB_nodes"][:6],
        "w2_per_bit_occ": w2_occ == base.PUB["workerB_occ_series"][:6],
        "w2_total": sums["w2"]["total_nodes"] == PUBH["w2_total"],
        "w2_final_occ": sums["w2"]["final_memo_occupied"] == PUBH["w2_occ"],
        # conflict detection (merge safety)
        "internal_conflicts_zero":
            all(not d["conflicts"] for d in dist.values()),
        "pairwise_cross_conflicts_zero":
            all(not st["cross_conflicts"] for st in pairwise.values()),
        "cascade_cross_conflicts_zero":
            (not m01["cross_conflicts"] and not m23["cross_conflicts"]
             and not mf["cross_conflicts"]),
        "merge4_deterministic": mf["merge_deterministic"],
        # FINAL4 reproduction (published boundary measurement)
        "repro_final4_occupied_after":
            mf["occupied_after"] == PUBH["final4_keys"],
        "repro_final4_seed_md5": mf["seed_md5"] == PUBH["final4_md5"],
        # published non-closure constants
        "final4_vs_seed2_shared":
            cmp42["shared"] == PUBH["shared_keys"],
        "final4_vs_seed2_only_in_final4":
            cmp42["only_in_final4"] == PUBH["only_in_final4"],
        "final4_vs_seed2_only_in_seed2_262":
            cmp42["only_in_seed2"] == PUBH["only_in_seed2"],
        "final4_vs_seed2_value_violations_zero":
            cmp42["value_violations"] == 0,
        # byte-identity of all worker snapshots
        "worker_byte_identical_A":
            state["workerA"]["byte_identical"] == 11,
        "worker_byte_identical_B":
            state["workerB"]["byte_identical"] == 11,
        "worker_byte_identical_w0":
            state["w0"]["byte_identical"] == 6,
        "worker_byte_identical_w1":
            state["w1"]["byte_identical"] == 5,
        "worker_byte_identical_w2":
            state["w2"]["byte_identical"] == 6,
        "worker_byte_identical_w3":
            state["w3"]["byte_identical"] == 5,
        # hybrid construction gates (the design's step 1-2)
        "hybrid_extract_count_262": ex["count"] == 262,
        "hybrid_extract_deterministic": ex["deterministic"],
        "hybrid_size_sum_gate": hb["size_sum_gate"],
        "hybrid_byte_prefix_gate": hb["byte_prefix_gate"],
        "hybrid_record_count_4975527":
            hb["hybrid_records"] == PUBH["hybrid_keys"],
        # simulator gates (the design's step 3 prediction)
        "sim25_failure_below_0.1pct":
            sim["ms25"]["failed"] / max(1, sim["ms25"]["seeded"]) < 0.001,
        "sim24_within_design_upper_bound":
            sim["ms24"]["failed"] <= PUBH["design_upper_bound_ms24"],
        # engine seedrun gates (the design's step 3-4)
        "seedrun25_byte_identical_22": okS == 22,
        "seedrun25_seed_failed_equals_sim25":
            seedstats.get("failed") == sim["ms25"]["failed"],
        "seedrun25_seed_failure_below_0.1pct":
            seedstats.get("failed", 10 ** 9) /
            max(1, seedstats.get("seeded", 1)) < 0.001,
        "record_identity_no_violations": ri["value_violations"] == 0,
        "record_identity_missing_equals_seed_failed":
            ri["missing"] == seedstats.get("failed", -1),
        "record_identity_present_equals_inserted":
            ri["present"] == seedstats.get("inserted", -1),
        # memo-state-invariant root (independent confirmation #4)
        "bit95_nodes_invariant_11857737":
            hybrid_per_bit.get(95) == PUBH["bit95_nodes"],
    }

    ratios_vs_boundary24 = {
        str(b): hybrid_per_bit[b] / BOUNDARY_SEEDRUN24_PER_BIT[b]
        for b in hybrid_per_bit}
    ratios_vs_nb4_25 = {
        str(b): hybrid_per_bit[b] / NB4_SEEDRUN25_PER_BIT[b]
        for b in hybrid_per_bit}

    doc = {
        "schema": "n11-class2-lane-hybrid-seed-union-measurement-73k-20261117-v2",
        "date": "2026-11-17",
        "lane": "n11 class2-lane long-term (cost73k)",
        "purpose": ("Hybrid seed union measurement (K0909 follow-up; executes "
                    "the published DESIGN_DERIVED_NOT_MEASURED "
                    "next_measurement): rebuild the published boundary 4-way "
                    "pipeline from pinned blobs, extract the 262 "
                    "only-in-2way records, build the hybrid union seed, "
                    "simulate MS=1<<24/25/26 insertion failures, and run "
                    "the full 22-bit band with the verbatim engine at "
                    "MS=1<<25 seeded from the hybrid file."),
        "inputs": {
            "extractor_blob": base.EXTRACTOR_BLOB,
            "driver_blob": base.DRIVER_BLOB,
            "manifest_blob": base.MANIFEST_BLOB,
            "legal_blob": base.LEGAL_BLOB,
            "design_json_blob": PUBH["design_json_blob"],
            "boundary_json_blob": PUBH["boundary_json_blob"],
            "boundary_orchestrator_blob": PUBH["boundary_orchestrator_blob"],
            "engine_variants": ("verbatim + MS line substitution + dump/seed "
                                "export block only; ms25 variant additionally "
                                "fsync-hardened dumpMemo (bytes unchanged); "
                                "no key-sign or negative-bound fixes"),
            "worker_ms": 23, "seedrun_ms": 25,
        },
        "repro_2way": {
            "workerA_total_nodes": sums["workerA"]["total_nodes"],
            "workerB_total_nodes": sums["workerB"]["total_nodes"],
            "merge_shared": m2["shared_distinct"],
            "merge_occupied_after": m2["occupied_after"],
            "seed_md5": m2["seed_md5"],
            "merge_deterministic": m2["merge_deterministic"],
        },
        "workers_4way": {
            "w0_total_nodes": sums["w0"]["total_nodes"],
            "w1_total_nodes": sums["w1"]["total_nodes"],
            "w2_total_nodes": sums["w2"]["total_nodes"],
            "w3_total_nodes": sums["w3"]["total_nodes"],
            "workers4_total_nodes": (
                sums["w0"]["total_nodes"] + sums["w1"]["total_nodes"]
                + sums["w2"]["total_nodes"] + sums["w3"]["total_nodes"]),
        },
        "distinct_pass": {t: {k: dist[t][k] for k in
                              ("records", "distinct", "dup_keys",
                               "max_copies", "conflicts")}
                          for t in dist},
        "cascade_merge": {
            "m01_occupied_after": m01["occupied_after"],
            "m23_occupied_after": m23["occupied_after"],
            "final_occupied_after": mf["occupied_after"],
            "final_shared": mf["shared_distinct"],
            "final_seed_md5": mf["seed_md5"],
            "cross_conflicts": mf["cross_conflicts"],
        },
        "final4_vs_seed2": {
            "shared": cmp42["shared"],
            "only_in_final4": cmp42["only_in_final4"],
            "only_in_seed2": cmp42["only_in_seed2"],
            "value_violations": cmp42["value_violations"],
        },
        "hybrid_extract": {
            "count": ex["count"],
            "deterministic": ex["deterministic"],
            "md5": ex["md5"], "sha256": ex["sha256"],
            "first_keys": state["extract"]["first_keys"],
            "last_keys": state["extract"]["last_keys"],
        },
        "hybrid_seed": {
            "key_count": hb["hybrid_records"],
            "final4_bytes": hb["final4_bytes"],
            "extra_bytes": hb["extra_bytes"],
            "hybrid_bytes": hb["hybrid_bytes"],
            "byte_prefix_gate": hb["byte_prefix_gate"],
            "size_sum_gate": hb["size_sum_gate"],
            "md5": hb["hybrid_md5"], "sha256": hb["hybrid_sha256"],
            "initial_load_factor_ms_1_25":
                hb["hybrid_records"] / (1 << 25),
            "header_note": ("the single header line is the FINAL4 header "
                            "verbatim (A=m01 B=m23); the appended 262 "
                            "records come after the FINAL4 records, so the "
                            "hybrid file is byte-prefix-identical to the "
                            "published-boundary FINAL4 seed file"),
        },
        "sim": {
            "ms25": {"failed": sim["ms25"]["failed"],
                     "seeded": sim["ms25"]["seeded"],
                     "inserted": sim["ms25"]["inserted"],
                     "load_factor": sim["ms25"]["load_factor"],
                     "max_cluster": sim["ms25"]["base_clusters"]["max_cluster"],
                     "own_cluster_ge64":
                         sim["ms25"]["failure_attribution"]["own_cluster_ge64"],
                     "spill_over_lt64":
                         sim["ms25"]["failure_attribution"]["spill_over_lt64"]},
            "ms24": {"failed": sim["ms24"]["failed"],
                     "seeded": sim["ms24"]["seeded"],
                     "design_upper_bound": PUBH["design_upper_bound_ms24"]},
            "ms26": {"failed": sim["ms26"]["failed"],
                     "seeded": sim["ms26"]["seeded"]},
        },
        "seedrun25_hybrid": {
            "total_nodes": sumS["total_nodes"],
            "final_occupied": sumS["final_memo_occupied"],
            "load_factor_final": sumS["final_memo_occupied"] / (1 << 25),
            "seed": seedstats,
            "byte_identical": okS,
            "per_bit_nodes": {str(b): hybrid_per_bit[b]
                              for b in sorted(hybrid_per_bit)},
            "vs_final4_seedrun24_nodes":
                sumS["total_nodes"] / PUBH["final4_seedrun24_nodes"],
            "vs_nb4_seedrun25_nodes":
                sumS["total_nodes"] / PUBH["nb4_seedrun25_nodes"],
            "vs_nb4_seedrun24_nodes":
                sumS["total_nodes"] / PUBH["nb4_seedrun24_nodes"],
            "vs_twoway_seedrun24_nodes":
                sumS["total_nodes"] / PUBH["twoway_seedrun24_nodes"],
            "per_bit_ratio_vs_final4_seedrun24": ratios_vs_boundary24,
            "per_bit_ratio_vs_nb4_seedrun25": ratios_vs_nb4_25,
            "published_reference": {
                "final4_seedrun24_nodes": PUBH["final4_seedrun24_nodes"],
                "nb4_seedrun25_nodes": PUBH["nb4_seedrun25_nodes"],
                "nb4_seedrun24_nodes": PUBH["nb4_seedrun24_nodes"],
                "twoway_seedrun24_nodes": PUBH["twoway_seedrun24_nodes"],
            },
        },
        "record_identity": {
            "present": ri["present"], "missing": ri["missing"],
            "value_violations": ri["value_violations"],
            "identity_method": ri["identity_method"],
            "missing_keys": ri["missing_keys"],
            "seedrun_dump_stats": {k: ri["seedrun_dump_stats"][k] for k in
                                   ("records", "distinct", "dup_keys",
                                    "max_copies", "conflicts")},
        },
        "cleanup_facts": {
            "removed_bytes": state.get("cleanup_removed_bytes", 0),
            "drop_caches": state.get("drop_caches"),
        },
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
        print("  gate %-46s %s" % (k, v), flush=True)
    progress("GATES all_pass=%s | seedrun25 hybrid nodes=%d seed=%s "
             "sim25=%d" % (doc["gates_all_pass"], sumS["total_nodes"],
                           json.dumps(seedstats), sim["ms25"]["failed"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
