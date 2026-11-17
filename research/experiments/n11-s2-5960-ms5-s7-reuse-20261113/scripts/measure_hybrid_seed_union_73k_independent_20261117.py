#!/usr/bin/env python3
"""Hybrid seed union MEASUREMENT for the cost-73k lane (2026-11-17, n11
class2-lane long-term lane; K0909 follow-up; converts the published
DESIGN_DERIVED_NOT_MEASURED hybrid seed union design into a measured
seedrun).

MEASUREMENT ONLY (no certificate publication, no verdict changes).

Design source (published, commit 0454908c / f8b72c55): the
boundary-preserving 4-worker merged seed FINAL4 (4,975,265 keys, md5
35ccec0e...) is NOT a superset of the published 2-way merged seed
(4,291,899 keys, md5 e7c2c17e...): exactly 262 keys are only in the 2-way
seed (only_in_final4=683,628, shared=4,291,637, value violations 0).  The
published design derives the union arithmetic (4,975,527 keys, initial
load 14.83% at MS=1<<25) but reconstructs NO actual records and runs NO
engine.  This measurement performs the design's "next measurement"
verbatim:

  1. Rebuild both merged seeds from the pinned inputs with the published
     boundary-respecting 4-worker pipeline (workers A/B + w0..w3 at
     MS=1<<23, KYOENWM1 full-table dumps, offline sort-based merge, all
     reproduction gates against the published boundary measurement JSON,
     blob b97c9334...).
  2. Reconstruct the exact 262 only-in-2way key/value records from the
     two rebuilt seed tables (stream key-join, deterministic key order;
     tail pinned by sha256).
  3. Append them after FINAL4 WITHOUT reordering existing FINAL4
     records and with ONE KYOENWM2 header; the first len(FINAL4) bytes
     of the hybrid seed are byte-identical to FINAL4 (base insertions
     preserved).  Build twice, require byte-identical md5.
  4. Validate the light occupancy simulator against BOTH published
     MS=1<<24 engine anchors using the REBUILT seeds (2-way: 1,448
     failures; boundary FINAL4: 14,657 failures), predict the hybrid
     failure counts at MS=1<<24 (<= 14,919, the design upper bound) and
     MS=1<<25.
  5. Reproduce the published boundary MS=1<<24 FINAL4 seedrun (76,599,320
     nodes, 14,657 seed failures, 22/22 byte-identical certificates,
     record identity closed) as an engine anchor in this environment.
  6. Run the FULL 22-root band with the hybrid seed at MS=1<<25
     (fsync-hardened dump variant, cap 200 as published for the
     design-point run) and close all gates:
       - 22/22 certificates byte-identical to the published band
         certificates;
       - engine seed failures == simulator prediction (exact);
       - seed failure rate < 0.1%;
       - record identity of the seedrun final dump vs the hybrid seed:
         value violations 0, missing == seed failures exactly;
       - per-bit node comparison against the published node-balanced
         4-way MS=1<<25 seedrun (72,745,351) and the published boundary
         FINAL4 MS=1<<24 seedrun (76,599,320).

Resume semantics: every phase writes <workdir>/hstate.json and skips on
re-entry.  After the heavy-intermediate cleanup (which precedes the two
engine seedruns) a restart resumes from hstate.json WITHOUT needing the
worker dumps, distinct tables or merge intermediates.

Interpretation guard: measurement only.  No new WIN/LOSS verdicts, no
manifest row opened or closed, certificate bytes unchanged.  The verbatim
extractor is NOT modified in the repo (published determinism chains); the
patched variants exist only in the work directory.  WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone roots only;
REFUTED-D10 is not a LOSS proof.  The 11x11 empty board, both two-stone
roots {49,60} and {59,60}, S2 {59,60} and classes 1/2/4 all remain
UNKNOWN.

Usage: python3 measure_hybrid_seed_union_73k_20261117.py <out.json> <workdir> [published_dir]
       (env: KYOEN_NODE=node; WM4_PROGRESS=<progress file>;
        HYBRID_STATE_COPY=<durable state copy>)
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) or "."
sys.path.insert(0, HERE)

_progress_default = os.path.join(
    "/home/user/knowledge/kyouen-research/_scratch", "hybrid-progress.md")
os.environ.setdefault("WM4_PROGRESS", _progress_default)
try:
    os.makedirs(os.path.dirname(_progress_default), exist_ok=True)
except OSError:
    pass

import measure_worker_split4_boundary_memo_merge_73k_20261117 as b4  # noqa: E402

NODE = b4.NODE
WORK = "."
SIM = os.path.join(HERE, "light_sim_seed_73k.mjs")

# git blob pins of the published reference JSONs (fetched from main,
# byte-identical; the pinned bytes are the measurement's ground truth)
PUB_BLOBS = {
    "boundary": "b97c9334f04f98f6ba7bb8a4c8b1de9689810d5e",
    "seed_design": "bf588d6a8dc4788e85912b57ac4401b9ac751e29",
    "hybrid_design": "8ec64f21b60b378595a749fc941f2232e0db5c21",
}

# published hybrid design arithmetic (design JSON, machine-checked there;
# re-checked here against the rebuilt tables)
DESIGN = {
    "boundary_final4_keys": 4975265,
    "published_2way_seed_keys": 4291899,
    "shared_keys": 4291637,
    "only_in_boundary_final4": 683628,
    "only_in_published_2way_seed": 262,
    "union_key_count": 4975527,
    "initial_load_factor_ms_1_25": 0.1482822597026825,
    "hybrid_ms_1_24_failure_upper_bound_if_appended": 14919,
    "boundary_final4_seed_md5": "35ccec0eb01e9b1b3719fa7e0c6ff4e9",
    "published_2way_seed_md5": "e7c2c17e7a91d8ea17f433f3bb482f29",
}

# published boundary MS=1<<24 FINAL4 seedrun anchors
PUB_SEEDRUN24 = {
    "total_nodes": 76599320,
    "final_occupied": 10525071,
    "seed": {"seeded": 4975265, "inserted": 4960608, "failed": 14657},
}

# published node-balanced 4-way MS=1<<25 design-point seedrun anchors
PUB_SEEDRUN25 = {
    "total_nodes": 72745351,
    "final_occupied": 14073139,
    "seed": {"seeded": 4985986, "inserted": 4985958, "failed": 28},
}

ALL_BITS = b4.ALL_BITS
WORKER_TAGS = ["workerA", "workerB", "w0", "w1", "w2", "w3"]


def progress(line):
    b4.progress(line)


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


def check_pin(name, path, expected):
    actual = b4.git_blob_sha(path)
    if actual != expected:
        raise SystemExit("%s BLOB MISMATCH: %s != %s" % (name, actual,
                                                         expected))


def hsave(state, state_path):
    json.dump(state, open(state_path, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1, sort_keys=True)
    try:
        dur = os.environ.get("HYBRID_STATE_COPY")
        if dur:
            with open(dur, "w", encoding="utf-8") as fh:
                json.dump(state, fh, ensure_ascii=False, indent=1,
                          sort_keys=True)
    except OSError:
        pass


def run_sim(seed_path, ms_shift, tag):
    out = os.path.join(WORK, "sim_%s_ms%d.json" % (tag, ms_shift))
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return json.load(open(out, encoding="utf-8"))
    cmd = [NODE, SIM, seed_path, str(ms_shift), "", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("sim failed %s ms=%d: %s"
                         % (tag, ms_shift, r.stderr[-800:]))
    return json.load(open(out, encoding="utf-8"))


def extract_only_in_seed2(seed2_path, seed4_path, tail_path):
    """Stream key-join of the two rebuilt seed tables (both key-sorted,
    one header line each): write the seed2-only records to tail_path in
    their file order (deterministic key order); return the full
    partition statistics (mirrors the published cmp42)."""
    only2 = 0
    only4 = 0
    shared = 0
    viol = 0
    with open(seed2_path, encoding="utf-8") as f2, \
            open(seed4_path, encoding="utf-8") as f4, \
            open(tail_path, "w", encoding="utf-8") as fo:
        f2.readline()  # header
        f4.readline()  # header
        r2 = f2.readline()
        r4 = f4.readline()
        while r2 or r4:
            k2 = r2.split()[:4] if r2 else None
            k4 = r4.split()[:4] if r4 else None
            if k2 and (not k4 or k2 < k4):
                fo.write(r2)
                only2 += 1
                r2 = f2.readline()
            elif k4 and (not k2 or k4 < k2):
                only4 += 1
                r4 = f4.readline()
            else:
                f2d = r2.split()
                f4d = r4.split()
                w2, l2 = int(f2d[4]), int(f2d[5])
                nw2, nl2 = int(f2d[6]), int(f2d[7])
                w4, l4 = int(f4d[4]), int(f4d[5])
                nw4, nl4 = int(f4d[6]), int(f4d[7])
                okw = w2 == 255 or w4 <= w2
                okl = l2 == 255 or l4 <= l2
                oknw = b4.bound_at_least(nw4, nw2)
                oknl = b4.bound_at_least(nl4, nl2)
                if not (okw and okl and oknw and oknl):
                    viol += 1
                shared += 1
                r2 = f2.readline()
                r4 = f4.readline()
    return {"shared": shared, "only_in_final4": only4,
            "only_in_seed2": only2, "value_violations": viol}


def count_lines(path):
    n = 0
    with open(path, "rb") as fh:
        for _ in iter(lambda: fh.readline(), b""):
            n += 1
    return n


def build_hybrid(seed4_path, tail_path, hybrid_path):
    """hybrid = exact FINAL4 bytes + appended tail records.  Returns
    construction stats (byte prefix identity is asserted)."""
    n4 = os.path.getsize(seed4_path)
    with open(seed4_path, "rb") as f4, \
            open(tail_path, "rb") as ft, \
            open(hybrid_path, "wb") as fo:
        while True:
            blk = f4.read(1 << 22)
            if not blk:
                break
            fo.write(blk)
        n_prefix = fo.tell()
        while True:
            blk = ft.read(1 << 22)
            if not blk:
                break
            fo.write(blk)
    assert n_prefix == n4
    return {"key_count": count_lines(hybrid_path) - 1,  # minus header
            "md5": md5_of(hybrid_path),
            "sha256": sha256_of(hybrid_path),
            "prefix_bytes_identical": n_prefix == n4,
            "bytes": os.path.getsize(hybrid_path)}


def harden_ms25_dump_fsync():
    """I/O-only hardening of the generated MS=1<<25 engine variant's
    dumpMemo (published for the design-point run in the seed capacity
    design): fs.fsyncSync() the dump every 32 MiB and once at the end,
    bounding dirty page cache during the ~0.6-0.7 GB dump write on this
    ~1.09 GiB-cgroup remote-fs environment.  Dump bytes are unchanged;
    only the write schedule differs.  Applied ONLY to the ms25 variant."""
    path = os.path.join(WORK, "class4_child1_cert_extractor_exact_wm_ms25.ts")
    src = open(path, encoding="utf-8").read()
    old_flush = ("    if (buf.length > (1 << 20)) { fs.writeSync(fd, buf); "
                 "buf = ''; }\n")
    new_flush = ("    if (buf.length > (1 << 20)) { fs.writeSync(fd, buf); "
                 "buf = '';\n"
                 "      if (++_nfl >= 32) { fs.fsyncSync(fd); _nfl = 0; } }\n")
    old_decl = "  let buf = '';\n  for (let i = 0; i < MS; i++) {"
    new_decl = ("  let buf = '';\n  let _nfl = 0;\n"
                "  for (let i = 0; i < MS; i++) {")
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


def cleanup_before_ms24(work):
    """Delete the heavy intermediates that are no longer needed once the
    merges, the hybrid construction and the sims are done (frees page
    cache ahead of the memory-tight engine seedruns)."""
    removed = 0
    for name in os.listdir(work):
        if name.endswith((".dump.txt", ".dump.sorted", ".distinct.txt")) \
                or name in ("m01.kyoenwm2m", "m23.kyoenwm2m") \
                or name.startswith("pair_"):
            p = os.path.join(work, name)
            removed += os.path.getsize(p)
            os.remove(p)
    return removed


def cleanup_seedrun(tag, work):
    removed = 0
    for suffix in (".dump.txt", ".dump.sorted", ".distinct.txt"):
        p = os.path.join(work, tag + suffix)
        if os.path.exists(p):
            removed += os.path.getsize(p)
            os.remove(p)
    return removed


def drop_caches():
    subprocess.run(["sync"], check=False)
    try:
        with open("/proc/sys/vm/drop_caches", "w") as fh:
            fh.write("3\n")
        return True
    except OSError:
        return False


def per_bit_nodes_of_list(per_bit):
    pb = sorted(per_bit, key=lambda p: p["bit"])
    return [p["nodes_this_run"] for p in pb]


def strip_ms(per_bit):
    out = []
    for p in per_bit:
        q = dict(p)
        q.pop("ms", None)
        out.append(q)
    return out


def _ri_value_ok(seed_vals, dump_vals):
    win, lose, nowin, nolose = seed_vals
    fw, fl, fnw, fnl = dump_vals
    okw = win == 255 or fw <= win
    okl = lose == 255 or fl <= lose
    oknw = b4.bound_at_least(fnw, nowin)
    oknl = b4.bound_at_least(fnl, nolose)
    return okw and okl and oknw and oknl


def record_identity_hybrid(tag, hybrid_path, tail_path,
                            tail_records=262):
    """Hybrid-aware record identity for the seedrunH dump.

    The hybrid seed file is FINAL4 (sorted) with the 262-record tail
    appended WITHOUT reordering (design rule), so the file is not
    globally sorted.  The published sorted merge join
    (b4.record_identity_pass) assumes a sorted seed file; on this file
    it counted missing=282 (= 20 engine insert failures + all 262 tail
    records), a join-order artifact rather than missing memo records.
    This pass merge-joins the FINAL4 prefix and hash-joins the tail,
    so 'missing' again counts only records genuinely absent from the
    final dump.  Value comparison semantics are identical to
    b4.record_identity_pass (equal-or-stronger, sentinel 255)."""
    stats = b4.distinct_pass(tag)
    dpath = os.path.join(WORK, tag + ".distinct.txt")
    n_final4 = DESIGN["boundary_final4_keys"]
    prefix = {"present": 0, "missing": 0, "value_violations": 0}
    tail_recs = {}
    samples = []
    with open(hybrid_path, encoding="utf-8") as fs_, \
            open(dpath, encoding="utf-8") as ff:
        fs_.readline()  # header
        rs = fs_.readline()
        rf = ff.readline()
        n = 0
        while rs:
            if n >= n_final4:
                f = rs.split()
                tail_recs[" ".join(f[:4])] = [int(x) for x in f[4:8]]
                rs = fs_.readline()
                continue
            ks = rs.split()[:4]
            kf = rf.split()[:4] if rf else None
            if not kf or ks < kf:
                prefix["missing"] += 1
                rs = fs_.readline()
                n += 1
            elif kf < ks:
                rf = ff.readline()
            else:
                ok = _ri_value_ok([int(x) for x in rs.split()[4:8]],
                                  [int(x) for x in rf.split()[4:8]])
                if ok:
                    prefix["present"] += 1
                else:
                    prefix["value_violations"] += 1
                    if len(samples) < 3:
                        samples.append(" ".join(ks))
                rs = fs_.readline()
                n += 1
                rf = ff.readline()
    if n != n_final4 or len(tail_recs) != tail_records:
        raise SystemExit("hybrid seed shape mismatch: prefix %d tail %d"
                         % (n, len(tail_recs)))
    tstats = {"present": 0, "missing": 0, "value_violations": 0}
    with open(dpath, encoding="utf-8") as ff:
        for line in ff:
            f = line.split()
            k = " ".join(f[:4])
            if k in tail_recs:
                if _ri_value_ok(tail_recs[k],
                                [int(x) for x in f[4:8]]):
                    tstats["present"] += 1
                else:
                    tstats["value_violations"] += 1
                    if len(samples) < 3:
                        samples.append(k)
                del tail_recs[k]
    tstats["missing"] = len(tail_recs)
    return {"present": prefix["present"] + tstats["present"],
            "missing": prefix["missing"] + tstats["missing"],
            "value_violations": prefix["value_violations"]
                                + tstats["value_violations"],
            "violation_samples": samples[:3],
            "method": ("prefix merge join + tail hash join (hybrid seed "
                       "file is FINAL4-sorted with an unordered "
                       "262-record tail appended; a single sorted "
                       "merge join mis-reads the tail)"),
            "final4_prefix": prefix,
            "tail_262": tstats,
            "seedrun_dump_stats": stats}


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "hybrid.json"
    work = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        HERE, "hybrid_work")
    pubdir = sys.argv[3] if len(sys.argv) > 3 else os.path.join(
        HERE, "published")
    global WORK
    WORK = work
    b4.WORK = work
    RUNTAG = "[hyb]"
    os.makedirs(WORK, exist_ok=True)
    state_path = os.path.join(WORK, "hstate.json")
    state = {}
    if os.path.exists(state_path):
        state = json.load(open(state_path, encoding="utf-8"))

    # ---------- pins ----------
    for name, path, exp in [
            ("extractor", b4.EXTRACTOR, b4.EXTRACTOR_BLOB),
            ("driver", b4.DRIVER, b4.DRIVER_BLOB),
            ("legal", b4.LEGAL, b4.LEGAL_BLOB),
            ("manifest", b4.MANIFEST, b4.MANIFEST_BLOB)]:
        check_pin(name, path, exp)
    for name, fn, key in [
            ("boundary_json",
             "worker-split4-boundary-memo-merge-73k-20261117.json", "boundary"),
            ("seed_design_json",
             "seed-capacity-design-73k-20261117.json", "seed_design"),
            ("hybrid_design_json",
             "hybrid-seed-union-design-73k-20261117.json", "hybrid_design")]:
        check_pin(name, os.path.join(pubdir, fn), PUB_BLOBS[key])
    pub_boundary = json.load(open(os.path.join(
        pubdir, "worker-split4-boundary-memo-merge-73k-20261117.json"),
        encoding="utf-8"))
    pub_seed_design = json.load(open(os.path.join(
        pubdir, "seed-capacity-design-73k-20261117.json"),
        encoding="utf-8"))
    pub_design = json.load(open(os.path.join(
        pubdir, "hybrid-seed-union-design-73k-20261117.json"),
        encoding="utf-8"))

    gates = {}
    if "gates_early" in state:
        gates.update(state["gates_early"])

    b4.build_plan()
    plan = os.path.join(WORK, "plan73k.json")
    b4.make_variant(23)
    b4.make_variant(24)

    seed2_path = os.path.join(WORK, "merged_seed_2way.kyoenwm2")
    seed4_path = os.path.join(WORK, "merged_seed_4way.kyoenwm2")
    hybrid_path = os.path.join(WORK, "hybrid_seed.kyoenwm2")
    tail_path = os.path.join(WORK, "hybrid_tail.txt")

    # ---------- phase 1: six workers (2-way repro + boundary 4-way) ------
    specs = [("workerA", b4.BITS_WA), ("workerB", b4.BITS_WB),
             ("w0", b4.BITS_W0), ("w1", b4.BITS_W1),
             ("w2", b4.BITS_W2), ("w3", b4.BITS_W3)]
    sums = {}
    for tag, bits in specs:
        s, _ = b4.run_worker(tag, 23, plan, bits, "350")
        if s is None:
            s = b4.wait_worker(tag)
        sums[tag] = s
        state[tag] = {"total_nodes": s["total_nodes"],
                      "final_memo_occupied": s["final_memo_occupied"],
                      "all_bits_ok": s["all_bits_ok"]}
        ok, mds = b4.verify_snapshots(tag, bits)
        state[tag]["byte_identical"] = ok
        hsave(state, state_path)
        progress(RUNTAG + " worker %s: nodes %d occ %d bytes_ok %d/%d"
                 % (tag, s["total_nodes"], s["final_memo_occupied"], ok,
                    len(bits)))
        print("[worker] %s nodes %d occ %d bytes_ok %d/%d"
              % (tag, s["total_nodes"], s["final_memo_occupied"], ok,
                 len(bits)), flush=True)

    def series(tag):
        pb = sorted(sums[tag]["per_bit"], key=lambda p: p["bit"])
        return [p["nodes_this_run"] for p in pb], \
               [p["memo_occupied_after"] for p in pb]

    wa_nodes, wa_occ = series("workerA")
    wb_nodes, wb_occ = series("workerB")
    w0_nodes, w0_occ = series("w0")
    w2_nodes, w2_occ = series("w2")

    gates["repro_workerA_total"] = \
        sums["workerA"]["total_nodes"] == b4.PUB["workerA_total"]
    gates["repro_workerA_occ"] = \
        sums["workerA"]["final_memo_occupied"] == b4.PUB["workerA_occ"]
    gates["repro_workerA_per_bit_nodes"] = wa_nodes == b4.PUB["workerA_nodes"]
    gates["repro_workerA_per_bit_occ"] = wa_occ == b4.PUB["workerA_occ_series"]
    gates["repro_workerB_total"] = \
        sums["workerB"]["total_nodes"] == b4.PUB["workerB_total"]
    gates["repro_workerB_occ"] = \
        sums["workerB"]["final_memo_occupied"] == b4.PUB["workerB_occ"]
    gates["repro_workerB_per_bit_nodes"] = wb_nodes == b4.PUB["workerB_nodes"]
    gates["repro_workerB_per_bit_occ"] = wb_occ == b4.PUB["workerB_occ_series"]
    gates["repro_byte_identical_A"] = state["workerA"]["byte_identical"] == 11
    gates["repro_byte_identical_B"] = state["workerB"]["byte_identical"] == 11
    gates["w0_per_bit_nodes"] = w0_nodes == b4.PUB["workerA_nodes"][:6]
    gates["w0_per_bit_occ"] = w0_occ == b4.PUB["workerA_occ_series"][:6]
    gates["w0_total"] = sums["w0"]["total_nodes"] == 27424708
    gates["w0_final_occ"] = sums["w0"]["final_memo_occupied"] == 3705871
    gates["w2_per_bit_nodes"] = w2_nodes == b4.PUB["workerB_nodes"][:6]
    gates["w2_per_bit_occ"] = w2_occ == b4.PUB["workerB_occ_series"][:6]
    gates["w2_total"] = sums["w2"]["total_nodes"] == 36575507
    gates["w2_final_occ"] = sums["w2"]["final_memo_occupied"] == 4869649
    gates["workers_byte_identical_w0"] = state["w0"]["byte_identical"] == 6
    gates["workers_byte_identical_w1"] = state["w1"]["byte_identical"] == 5
    gates["workers_byte_identical_w2"] = state["w2"]["byte_identical"] == 6
    gates["workers_byte_identical_w3"] = state["w3"]["byte_identical"] == 5
    if not all(v for k, v in gates.items() if k.startswith(
            ("repro_worker", "repro_byte", "w0_", "w2_",
             "workers_byte"))):
        hsave(state, state_path)
        raise SystemExit("worker reproduction gates failed: %s"
                         % json.dumps(gates))

    if "hybrid" not in state:
        # ---------- phase 2: distinct passes (needs the dumps) ----------
        dist = {}
        for tag, _ in specs:
            dist[tag] = b4.distinct_pass(tag)
            state["distinct_" + tag] = dist[tag]
            hsave(state, state_path)
            print("[distinct] %s: %s" % (tag, dist[tag]["distinct"]),
                  flush=True)
        gates["internal_conflicts_zero"] = all(
            not d["conflicts"] for d in dist.values())
        gates["repro_distincts_match_published"] = (
            dist["workerA"]["distinct"] == 2619833
            and dist["workerB"]["distinct"] == 2554155
            and all(dist["w%d" % i]["distinct"]
                    == pub_boundary["distinct_pass"]["w%d" % i]["distinct"]
                    for i in range(4)))

        dpath = lambda t: os.path.join(WORK, t + ".distinct.txt")

        # ---------- phase 3: 2-way merge (published md5 gate) ----------
        m2 = b4.merge_join(dpath("workerA"), dpath("workerB"), seed2_path,
                           b4.SEED2_HEADER)
        m2["seed_md5"] = md5_of(seed2_path)
        b4.merge_join(dpath("workerA"), dpath("workerB"),
                      seed2_path + ".tmp", b4.SEED2_HEADER)
        m2["merge_deterministic"] = (md5_of(seed2_path + ".tmp")
                                     == m2["seed_md5"])
        os.remove(seed2_path + ".tmp")
        state["merge2"] = m2
        hsave(state, state_path)
        gates["repro_merged2_seed_md5"] = \
            m2["seed_md5"] == b4.PUB["merged2_seed_md5"]
        gates["repro_merged2_occupied_after"] = \
            m2["occupied_after"] == b4.PUB["merged2_occupied_after"]
        gates["repro_merged2_shared"] = \
            m2["shared_distinct"] == b4.PUB["merged2_shared"]
        gates["merge2_deterministic"] = m2["merge_deterministic"]
        gates["merge2_cross_conflicts_zero"] = not m2["cross_conflicts"]

        # ---------- phase 4: pairwise + cascade to FINAL4 ----------
        pairwise = {}
        for i in range(4):
            for j in range(i + 1, 4):
                ti, tj = "w%d" % i, "w%d" % j
                out = os.path.join(WORK, "pair_%s_%s.kyoenwm2m" % (ti, tj))
                st = b4.merge_join(dpath(ti), dpath(tj), out, None)
                pairwise["%s_%s" % (ti, tj)] = st
                os.remove(out)
        state["pairwise"] = pairwise
        hsave(state, state_path)
        gates["pairwise_cross_conflicts_zero"] = all(
            not st["cross_conflicts"] for st in pairwise.values())
        gates["pairwise_match_published"] = all(
            pairwise[k]["shared_distinct"]
            == pub_boundary["pairwise_merges"][k]["shared_distinct"]
            and pairwise[k]["occupied_after"]
            == pub_boundary["pairwise_merges"][k]["occupied_after"]
            for k in pairwise)

        m01_path = os.path.join(WORK, "m01.kyoenwm2m")
        m23_path = os.path.join(WORK, "m23.kyoenwm2m")
        m01 = b4.merge_join(dpath("w0"), dpath("w1"), m01_path, None)
        m23 = b4.merge_join(dpath("w2"), dpath("w3"), m23_path, None)
        mf = b4.merge_join(m01_path, m23_path, seed4_path, b4.SEED4_HEADER)
        mf["seed_md5"] = md5_of(seed4_path)
        b4.merge_join(m01_path, m23_path, seed4_path + ".tmp",
                      b4.SEED4_HEADER)
        mf["merge_deterministic"] = (md5_of(seed4_path + ".tmp")
                                     == mf["seed_md5"])
        os.remove(seed4_path + ".tmp")
        state["merge_cascade"] = {"m01": m01, "m23": m23, "final": mf}
        hsave(state, state_path)
        gates["cascade_cross_conflicts_zero"] = (
            not m01["cross_conflicts"] and not m23["cross_conflicts"]
            and not mf["cross_conflicts"])
        gates["merge4_deterministic"] = mf["merge_deterministic"]
        gates["final4_seed_md5_matches_published"] = \
            mf["seed_md5"] == DESIGN["boundary_final4_seed_md5"]
        gates["final4_keys_match_published"] = \
            mf["occupied_after"] == DESIGN["boundary_final4_keys"]

        # ---------- phase 5: cmp42 + hybrid construction ----------
        cmp42 = b4.compare_final4_vs_seed2(seed4_path, seed2_path)
        state["final4_vs_seed2"] = cmp42
        hsave(state, state_path)
        gates["cmp42_matches_design"] = (
            cmp42["only_in_seed2"] == DESIGN["only_in_published_2way_seed"]
            and cmp42["only_in_final4"] == DESIGN["only_in_boundary_final4"]
            and cmp42["shared"] == DESIGN["shared_keys"]
            and cmp42["value_violations"] == 0)

        part = extract_only_in_seed2(seed2_path, seed4_path, tail_path)
        gates["hybrid_partition_matches_design"] = (
            part["only_in_seed2"] == DESIGN["only_in_published_2way_seed"]
            and part["only_in_final4"] == DESIGN["only_in_boundary_final4"]
            and part["shared"] == DESIGN["shared_keys"]
            and part["value_violations"] == 0)
        tail_sha = sha256_of(tail_path)
        tail_lines = count_lines(tail_path)
        gates["hybrid_tail_lines_262"] = tail_lines == 262

        hb = build_hybrid(seed4_path, tail_path, hybrid_path)
        hb2_md5 = build_hybrid(seed4_path, tail_path,
                               hybrid_path + ".tmp")["md5"]
        os.remove(hybrid_path + ".tmp")
        gates["hybrid_deterministic"] = hb2_md5 == hb["md5"]
        gates["hybrid_prefix_bytes_identical"] = hb["prefix_bytes_identical"]
        gates["hybrid_key_count_4975527"] = \
            hb["key_count"] == DESIGN["union_key_count"]
        gates["hybrid_key_count_arithmetic"] = \
            hb["key_count"] == DESIGN["boundary_final4_keys"] + tail_lines
        gates["hybrid_initial_load_matches_design"] = abs(
            hb["key_count"] / (1 << 25)
            - DESIGN["initial_load_factor_ms_1_25"]) < 1e-12
        state["hybrid"] = {**hb, "tail_sha256": tail_sha,
                           "tail_lines": tail_lines, "partition": part}
        state["gates_early"] = dict(gates)
        hsave(state, state_path)
        progress(RUNTAG + " hybrid built: keys %d md5 %s tail %d"
                 % (hb["key_count"], hb["md5"], tail_lines))
        if not all(gates.values()):
            hsave(state, state_path)
            raise SystemExit("hybrid construction gates failed: %s"
                             % json.dumps(gates))
    else:
        gates = dict(state["gates_early"])
        hb = state["hybrid"]
        tail_lines = hb["tail_lines"]
        progress(RUNTAG + " resume: hybrid already built (keys %d md5 %s)"
                 % (hb["key_count"], hb["md5"]))

    # ---------- phase 6: sims (validation anchors + predictions) --------
    if not (os.path.exists(seed2_path) and os.path.exists(seed4_path)
            and os.path.exists(hybrid_path)):
        raise SystemExit("seed files missing; hybrid phase not resumable")
    sim2_24 = run_sim(seed2_path, 24, "seed2")
    sim4_24 = run_sim(seed4_path, 24, "final4")
    simH_24 = run_sim(hybrid_path, 24, "hybrid")
    simH_25 = run_sim(hybrid_path, 25, "hybrid")
    gates["sim24_seed2_failed_equals_published_engine"] = \
        sim2_24["failed"] == b4.PUB["seedrun2_seed"]["failed"]
    gates["sim24_final4_failed_equals_published_engine"] = \
        sim4_24["failed"] == PUB_SEEDRUN24["seed"]["failed"]
    gates["sim24_hybrid_within_design_bound"] = \
        simH_24["failed"] <= DESIGN[
            "hybrid_ms_1_24_failure_upper_bound_if_appended"]
    gates["sim25_hybrid_failure_below_0.1pct"] = \
        simH_25["failed"] / max(1, simH_25["seeded"]) < 0.001
    info_sim = {"seed2_ms24": sim2_24, "final4_ms24": sim4_24,
                "hybrid_ms24": simH_24, "hybrid_ms25": simH_25}
    state["sim_gates"] = {k: gates[k] for k in gates
                          if k.startswith("sim")}
    state["sim_results"] = {k: {kk: info_sim[k][kk] for kk in
                                ("seeded", "inserted", "failed",
                                 "load_factor")}
                            for k in info_sim}
    hsave(state, state_path)
    progress(RUNTAG + " sims: seed2_24 %d final4_24 %d hybrid_24 %d "
             "hybrid_25 %d" % (sim2_24["failed"], sim4_24["failed"],
                               simH_24["failed"], simH_25["failed"]))

    # ---------- phase 7: cleanup + drop caches, then MS=1<<24 repro ----
    if "seedrun24" not in state:
        removed = cleanup_before_ms24(WORK)
        dropped = drop_caches()
        progress(RUNTAG + " cleanup %.2f GB drop_caches=%s before ms24 "
                 "seedrun" % (removed / 1e9, dropped))
        sum24, _ = b4.run_worker("seedrun", 24, plan, ALL_BITS,
                                 "700", seed_path=seed4_path)
        if sum24 is None:
            sum24 = b4.wait_worker("seedrun", timeout_s=3000)
        ok24, md24 = b4.verify_snapshots("seedrun", ALL_BITS)
        ri24 = b4.record_identity_pass("seedrun", seed4_path)
        state["seedrun24"] = {
            "total_nodes": sum24["total_nodes"],
            "final_memo_occupied": sum24["final_memo_occupied"],
            "seed": sum24.get("seed"), "byte_identical": ok24,
            "per_bit": strip_ms(sum24["per_bit"]),
            "record_identity": {k: ri24[k] for k in
                                ("present", "missing", "value_violations")},
            "dump_stats": {k: ri24["seedrun_dump_stats"][k] for k in
                           ("records", "distinct", "dup_keys", "max_copies",
                            "conflicts")}}
        hsave(state, state_path)
        cleanup_seedrun("seedrun", WORK)
        drop_caches()
    s24 = state["seedrun24"]
    gates["repro_seedrun24_nodes_match_published"] = \
        s24["total_nodes"] == PUB_SEEDRUN24["total_nodes"]
    gates["repro_seedrun24_final_occupied_match_published"] = \
        s24["final_memo_occupied"] == PUB_SEEDRUN24["final_occupied"]
    gates["repro_seedrun24_seed_failed_match_published"] = \
        s24["seed"]["failed"] == PUB_SEEDRUN24["seed"]["failed"]
    gates["repro_seedrun24_byte_identical_22"] = s24["byte_identical"] == 22
    gates["repro_seedrun24_record_identity_closed"] = (
        s24["record_identity"]["value_violations"] == 0
        and s24["record_identity"]["missing"]
        == PUB_SEEDRUN24["seed"]["failed"])
    gates["repro_seedrun24_per_bit_match_published"] = \
        per_bit_nodes_of_list(s24["per_bit"]) \
        == per_bit_nodes_of_list(pub_boundary["seedrun"]["per_bit"])
    progress(RUNTAG + " seedrun24 repro: nodes %d failed %d bytes_ok %d"
             % (s24["total_nodes"], s24["seed"]["failed"],
                s24["byte_identical"]))

    # ---------- phase 8: MS=1<<25 hybrid seedrun -------------------------
    if "seedrunH" not in state:
        b4.make_variant(25)
        harden_ms25_dump_fsync()
        sumH, _ = b4.run_worker("seedrunH", 25, plan, ALL_BITS,
                                "200", seed_path=hybrid_path)
        if sumH is None:
            sumH = b4.wait_worker("seedrunH", timeout_s=3600)
        okH, mdH = b4.verify_snapshots("seedrunH", ALL_BITS)
        riH = record_identity_hybrid("seedrunH", hybrid_path, tail_path)
        state["seedrunH"] = {
            "total_nodes": sumH["total_nodes"],
            "final_memo_occupied": sumH["final_memo_occupied"],
            "seed": sumH.get("seed"), "byte_identical": okH,
            "per_bit": strip_ms(sumH["per_bit"]),
            "wall_ms": sumH["wall_ms"],
            "record_identity": riH}
        hsave(state, state_path)
        cleanup_seedrun("seedrunH", WORK)
        drop_caches()
    sH = state["seedrunH"]
    gates["hybrid_seedrun_byte_identical_22"] = sH["byte_identical"] == 22
    seedH = sH["seed"] or {}
    gates["hybrid_seedrun_seed_failed_equals_sim25"] = \
        seedH.get("failed") == simH_25["failed"]
    gates["hybrid_seedrun_seed_arithmetic_closed"] = \
        seedH.get("seeded") == seedH.get("inserted", 0) \
        + seedH.get("failed", -1)
    gates["hybrid_seedrun_seed_failure_below_0.1pct"] = \
        seedH.get("failed", 1) / max(1, seedH.get("seeded", 1)) < 0.001
    gates["hybrid_seedrun_record_identity_no_violations"] = \
        sH["record_identity"]["value_violations"] == 0
    gates["hybrid_seedrun_record_identity_missing_equals_seed_failed"] = \
        sH["record_identity"]["missing"] == seedH.get("failed", -1)
    progress(RUNTAG + " seedrunH ms25: nodes %d occ %d seed %s bytes_ok %d"
             % (sH["total_nodes"], sH["final_memo_occupied"],
                json.dumps(seedH), sH["byte_identical"]))

    # ---------- phase 9: comparisons (recorded, not gated) --------------
    bits_sorted = [p["bit"] for p in sorted(sH["per_bit"],
                                            key=lambda x: x["bit"])]
    hyb_nodes = per_bit_nodes_of_list(sH["per_bit"])
    pub25_nodes = per_bit_nodes_of_list(pub_seed_design["seedrun25"]["per_bit"])
    bnd24_nodes = per_bit_nodes_of_list(pub_boundary["seedrun"]["per_bit"])
    diffs = [{"bit": b, "hybrid_ms25": h, "nodebal_ms25": p,
              "boundary_ms24": q, "ratio_vs_nodebal25": h / p}
             for b, h, p, q in zip(bits_sorted, hyb_nodes, pub25_nodes,
                                   bnd24_nodes)]
    comparisons = {
        "hybrid_ms25_total": sH["total_nodes"],
        "vs_node_balanced_ms25": sH["total_nodes"]
        / PUB_SEEDRUN25["total_nodes"],
        "vs_boundary_ms24": sH["total_nodes"] / PUB_SEEDRUN24["total_nodes"],
        "per_bit": diffs,
        "bit95": {"hybrid_ms25": hyb_nodes[bits_sorted.index(95)],
                  "published_invariant": 11857737},
        "final_load_factor": sH["final_memo_occupied"] / (1 << 25),
        "wall_ms": sH["wall_ms"],
    }

    # ---------- output ----------------------------------------------------
    m2 = state.get("merge2", {})
    mf = (state.get("merge_cascade", {}).get("final", {}))
    doc = {
        "schema": ("n11-class2-lane-hybrid-seed-union-measurement-73k-"
                   "20261117-v1"),
        "date": "2026-11-17",
        "lane": "n11 class2-lane long-term (cost73k)",
        "purpose": ("K0909 follow-up: hybrid seed union measurement. "
                    "Converts the published DESIGN_DERIVED_NOT_MEASURED "
                    "hybrid seed union design (boundary FINAL4 + the 262 "
                    "only-in-2way records, 4,975,527 keys) into a full "
                    "MS=1<<25 band seedrun with certificate, simulator "
                    "and record-identity gates."),
        "design_source": {
            "design_json_git_blob": PUB_BLOBS["hybrid_design"],
            "design_status_published": pub_design["status"],
            "boundary_measurement_git_blob": PUB_BLOBS["boundary"],
            "boundary_orchestrator_git_blob":
                pub_design["source_pins"][
                    "boundary_4way_orchestrator_git_blob"],
            "seed_capacity_design_git_blob": PUB_BLOBS["seed_design"],
            "design_next_measurement_executed": [
                "262 records reconstructed from the rebuilt 2-way and "
                "boundary-4way seed tables (tail sha256 pinned)",
                "appended after FINAL4 without reordering, one header",
                "hybrid seed run at MS=1<<25; inserted/failed/conflict/"
                "record-identity recorded",
                "22 roots re-run; 22/22 certificate byte identity gate; "
                "per-bit nodes compared against boundary-4way-only "
                "(MS=1<<24) and node-balanced-4way (MS=1<<25) published "
                "seedruns"],
        },
        "inputs": {
            "extractor_blob": b4.EXTRACTOR_BLOB,
            "driver_blob": b4.DRIVER_BLOB,
            "manifest_blob": b4.MANIFEST_BLOB,
            "legal_blob": b4.LEGAL_BLOB,
            "engine_variants": ("verbatim + MS line substitution + "
                                "dump/seed export block only (ms23/ms24 as "
                                "published); ms25 additionally fsync-"
                                "hardened dumpMemo I/O scheduling (bytes "
                                "unchanged, as published for the design-"
                                "point run)"),
            "worker_ms": 23, "boundary_seedrun_ms": 24,
            "hybrid_seedrun_ms": 25,
            "bits_workerA": b4.BITS_WA, "bits_workerB": b4.BITS_WB,
            "bits_w0": b4.BITS_W0, "bits_w1": b4.BITS_W1,
            "bits_w2": b4.BITS_W2, "bits_w3": b4.BITS_W3,
        },
        "repro_workers": {
            t: {"total_nodes": state[t]["total_nodes"],
                "final_occupied": state[t]["final_memo_occupied"],
                "byte_identical": state[t]["byte_identical"]}
            for t in WORKER_TAGS},
        "repro_merges": {
            "merge2": {k: m2.get(k) for k in
                       ("shared_distinct", "occupied_after",
                        "cross_conflicts", "seed_md5",
                        "merge_deterministic")},
            "pairwise": state.get("pairwise", {}),
            "cascade": state.get("merge_cascade", {}),
        },
        "distinct_pass": {t: {k: state.get("distinct_" + t, {}).get(k)
                              for k in ("records", "distinct", "dup_keys",
                                        "max_copies", "conflicts")}
                          for t in WORKER_TAGS},
        "hybrid_construction": {
            "partition_vs_published_2way": state.get("final4_vs_seed2", {}),
            "partition_recomputed": hb.get("partition", {}),
            "tail_records": tail_lines,
            "tail_sha256": hb.get("tail_sha256"),
            "final4_seed_md5": mf.get("seed_md5"),
            "seed2_seed_md5": m2.get("seed_md5"),
            "hybrid_seed_md5": hb.get("md5"),
            "hybrid_seed_sha256": hb.get("sha256"),
            "hybrid_key_count": hb.get("key_count"),
            "hybrid_bytes": hb.get("bytes"),
            "prefix_bytes_identical": hb.get("prefix_bytes_identical"),
            "initial_load_factor_ms_1_25": hb.get("key_count", 0) / (1 << 25),
            "design_initial_load_factor_ms_1_25":
                DESIGN["initial_load_factor_ms_1_25"],
        },
        "sim": info_sim,
        "repro_seedrun24_boundary": s24,
        "hybrid_seedrun25": sH,
        "published_reference": {
            "seedrun24_boundary": PUB_SEEDRUN24,
            "seedrun25_node_balanced": PUB_SEEDRUN25,
        },
        "comparisons": comparisons,
        "design_json_null_fields_filled": {
            "capacity_bounds.hybrid_ms_1_25_failure_count":
                seedH.get("failed"),
            "capacity_bounds.hybrid_ms_1_25_band_nodes": sH["total_nodes"],
            "note": ("measured in this run; the published design JSON is "
                     "left untouched (DESIGN_DERIVED_NOT_MEASURED stays "
                     "historical)"),
        },
        "gates": gates,
        "gates_all_pass": all(gates.values()),
        "interpretation_guard": (
            "MEASUREMENT ONLY. No new WIN/LOSS verdicts; no manifest row "
            "opened or closed; certificate bytes unchanged (22/22 "
            "byte-identical gates re-derive the published certificates). "
            "The repo-verbatim extractor is unmodified in the repo "
            "(published determinism chains). The published boundary "
            "measurement's two FAILED gates (FINAL4 non-closure with 262 "
            "only-in-2way keys; MS=1<<24 seed failure rate 0.295%) are "
            "expected reproductions, not failures here. WIN7-D10 proves a "
            "first-player win within depth 10 from the individual "
            "7-stone roots only; REFUTED-D10 is not a LOSS proof. The "
            "11x11 empty board, both two-stone roots {49,60} and {59,60}, "
            "S2 {59,60} and classes 1/2/4 all remain UNKNOWN."),
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    print("gates_all_pass:", doc["gates_all_pass"], flush=True)
    for k, v in sorted(gates.items()):
        print("  gate %-58s %s" % (k, v), flush=True)
    progress(RUNTAG + " GATES all_pass=%s | hybrid keys %d md5 %s | "
             "ms25 nodes %d (nodebal25 %d, boundary ms24 %d) | seed %s"
             % (doc["gates_all_pass"], hb.get("key_count"), hb.get("md5"),
                sH["total_nodes"], PUB_SEEDRUN25["total_nodes"],
                PUB_SEEDRUN24["total_nodes"], json.dumps(seedH)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
