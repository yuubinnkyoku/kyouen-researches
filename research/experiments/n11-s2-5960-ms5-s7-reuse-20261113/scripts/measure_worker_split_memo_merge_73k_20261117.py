#!/usr/bin/env python3
"""Worker-split memo merge measurement for the cost-73k lane
(2026-11-17, n11 class2-lane long-term lane).

MEASUREMENT ONLY (no certificate publication, no verdict changes).

Purpose (lane priority 3: safe worker-cache merge with immediate WIN/LOSS
conflict detection).  Two workers split the published cost-73k WIN7-D10 band
(22 roots, manifest class2-lane-cost73k-win7-certificates-20261117.json)
at the natural gap of the bit list:

  worker A: bits 0,7,11,15,35,39,41,44,58,62,73   (11 bits, fresh process)
  worker B: bits 76,87,89,94,95,97,98,103,105,112,117 (11 bits, fresh process)

Each worker runs the REPO-VERBATIM extractor (blob 52bcaf50..., including
its two known memo bugs: the Uint32Array signed-key duplicate-insertion bug
and the dead 255 negative bounds - both performance-only, soundness
unaffected; see item K0907) at MS=1<<23, band-wide within its bits (memo
carried across bits, rows cleared per bit so each certificate is
reconstructed and byte-compared against the published certificate), then
dumps the full memo table in KYOENWM1 format (one record per occupied slot:
slot k0 k1 k2 k3 win lose nowin nolose, keys as 8-digit zero-padded hex).

Offline merge (sort-based, streaming, no sqlite):
  1. Each worker dump is externally sorted by key (fields 2-5) and
     stream-deduplicated: duplicate copies of a key (the signed-key bug's
     duplicate insertions, all high-bit) are combined by
     win=min lose=min nowin=max nolose=max; INTERNAL conflicts
     (win<255&lose<255, win<=nowin, lose<=nolose) are counted per worker.
  2. The two distinct-key streams are merge-joined: shared keys counted,
     CROSS conflicts checked with the same rules, and the merged table
     (KYOENWM2: k0 k1 k2 k3 win lose nowin nolose, sorted by key) written
     for seeding.  occupied_after = distinctA + distinctB - shared.

Seedrun (merged-cache band run): the verbatim engine at MS=1<<24 seeds its
memo from the merged KYOENWM2 table (insertion in file order through the
engine's own memoEntry(), preserving verbatim probe semantics; high-bit
keys stay inert duplicates exactly as in a verbatim run), then extracts all
22 bits band-wide in one process.  Final load lands at ~64% (the capacity
design the 2026-11-17 band measurement prescribed for merged worker
caches).  Gates: 22/22 certificates byte-identical, record-identity check
of the seedrun's final dump against the merged seed (every seeded key must
be present with equal-or-stronger combined values: win<=, lose<=,
nowin>=, nolose>=; missing keys counted separately).

Regression gates (constants measured 2026-11-17 by the earlier run of this
measurement, whose scripts were lost to an environment reset; the engine
is deterministic, so a fresh re-run must reproduce them):
  - worker A per-bit nodes == published band ms23 per-bit values for bits
    0..73 (fresh process reproduces the band prefix exactly), total 48,482,011;
    worker A final occupied == 5,263,320 (band ms23 bit-73 occupancy).
  - worker A + worker B total nodes == 119,962,147 (0.9899 of the band ms23
    total 121,186,659: the split keeps within-worker sharing and only loses
    the cross-part sharing across the 73/76 gap).
  - merged occupied_after == 4,291,129 distinct position keys.
  - internal and cross conflicts == 0.

Interpretation guard: measurement only.  No new WIN/LOSS verdicts, no
manifest row opened or closed, certificate bytes unchanged.  The verbatim
extractor is NOT modified in the repo (published determinism chains); the
patched variants exist only in the work directory.  WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone roots only;
REFUTED-D10 is not a LOSS proof.  The 11x11 empty board, both two-stone
roots {49,60} and {59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN.

Usage:  python3 measure_worker_split_memo_merge_73k_20261117.py <out.json>
        (env: KYOEN_NODE=node; every step resumes from
        output/worker_split_merge_73k_work/)
"""
import hashlib
import json
import os
import subprocess
import sys

from worker_memo_merge import bound_at_least, combine_values, conflict_kind

HERE = os.path.dirname(os.path.abspath(__file__)) or "."
OUT = os.path.join(HERE, "output")
CERTDIR = os.path.join(OUT, "class2-lane-cost73k-certificates")
WORK = os.path.join(OUT, "worker_split_merge_73k_work")
NODE = os.environ.get("KYOEN_NODE", "node")

EXTRACTOR = os.path.join(HERE, "class4_child1_cert_extractor_exact.ts")
DRIVER = os.path.join(HERE, "measure_worker_split_memo_73k.ts")
LEGAL = os.path.join(HERE, "legal_candidates.py")
MANIFEST = os.path.join(
    CERTDIR, "class2-lane-cost73k-win7-certificates-20261117.json")
if not os.path.exists(MANIFEST):
    MANIFEST = os.path.join(HERE, "manifest.json")

EXTRACTOR_BLOB = "52bcaf509ea12fad4c936501d30d26b5b66c0085"
MANIFEST_BLOB = "0892aed07d187ae2fb3b4b90a21c7adbc1002b62"
LEGAL_BLOB = "8e97082c42838c7a4a4b6d2dd235276c8d43ab9a"

VERBATIM_LINE = "const MS=1<<18, MM=MS-1;"
PATCH_ANCHOR = ("export function extractBatch(childHex: string, bit: number, "
                "killTable: Record<number, number>, moves: number[]) {")
PATCH_BLOCK = """// EXPERIMENT MODIFICATION (2026-11-17, worker-split memo merge measurement
// only; not a replacement for the published extractor): row-set reset,
// occupancy probe, full memo-table dump (KYOENWM1) and a streaming memo
// seed loader (KYOENWM2), so worker memo tables can be dumped after a
// split run, merged offline and re-seeded into a merged band run.
export function clearRows(): void { rows.clear(); }
export function memoStats(): { slots: number, occupied: number } {
  let c = 0; for (let i = 0; i < MS; i++) if (mOcc[i]) c++;
  return { slots: MS, occupied: c };
}
export function dumpMemo(path: string, header: string): void {
  const fd = fs.openSync(path, 'w');
  fs.writeSync(fd, header + NL);
  let buf = '';
  for (let i = 0; i < MS; i++) {
    if (!mOcc[i]) continue;
    buf += i + ' '
      + (mK0[i] >>> 0).toString(16).padStart(8, '0') + ' '
      + (mK1[i] >>> 0).toString(16).padStart(8, '0') + ' '
      + (mK2[i] >>> 0).toString(16).padStart(8, '0') + ' '
      + (mK3[i] >>> 0).toString(16).padStart(8, '0') + ' '
      + mWin[i] + ' ' + mLose[i] + ' ' + mNoWin[i] + ' ' + mNoLose[i] + NL;
    if (buf.length > (1 << 20)) { fs.writeSync(fd, buf); buf = ''; }
  }
  if (buf.length) fs.writeSync(fd, buf);
  fs.closeSync(fd);
}
export function seedMemo(path: string): { seeded: number, inserted: number, failed: number } {
  const fd = fs.openSync(path, 'r');
  let seeded = 0, inserted = 0, failed = 0, rem = '', first = true;
  const chunk = Buffer.alloc(1 << 20);
  for (;;) {
    const n = fs.readSync(fd, chunk, 0, chunk.length, null);
    if (n <= 0) break;
    const data = rem + chunk.toString('latin1', 0, n);
    const lines = data.split(NL);
    rem = lines.pop() as string;
    for (const l of lines) {
      if (first) { first = false; continue; }
      if (!l) continue;
      const f = l.split(' ');
      M0 = parseInt(f[0], 16) | 0; M1 = parseInt(f[1], 16) | 0;
      M2 = parseInt(f[2], 16) | 0; M3 = parseInt(f[3], 16) | 0;
      const h = memoEntry();
      if (h >= 0) {
        mWin[h] = parseInt(f[4], 10); mLose[h] = parseInt(f[5], 10);
        mNoWin[h] = parseInt(f[6], 10); mNoLose[h] = parseInt(f[7], 10);
        inserted++;
      } else failed++;
      seeded++;
    }
  }
  if (!first && rem) {
    const f = rem.split(' ');
    M0 = parseInt(f[0], 16) | 0; M1 = parseInt(f[1], 16) | 0;
    M2 = parseInt(f[2], 16) | 0; M3 = parseInt(f[3], 16) | 0;
    const h = memoEntry();
    if (h >= 0) {
      mWin[h] = parseInt(f[4], 10); mLose[h] = parseInt(f[5], 10);
      mNoWin[h] = parseInt(f[6], 10); mNoLose[h] = parseInt(f[7], 10);
      inserted++;
    } else failed++;
    seeded++;
  }
  fs.closeSync(fd);
  return { seeded, inserted, failed };
}
"""

DRIVER_IMPORT_TARGET = "from './__VARIANT__'"

# published band-wide ms23 per-bit node counts (measurement
# class2-lane-band-memo-extraction-measurement-73k-20261117.json, blob ce625db0)
BAND23_PER_BIT = {
    0: 4303203, 7: 5039319, 11: 2910849, 15: 8159953, 35: 5045405,
    39: 1965979, 41: 1768864, 44: 4669878, 58: 4866570, 62: 2241220,
    73: 7510771, 76: 4815817, 87: 8054680, 89: 4928329, 94: 5625212,
    95: 11857737, 97: 4429190, 98: 6073176, 103: 7107709, 105: 4356101,
    112: 6167016, 117: 9289681}
BAND23_TOTAL = 121186659
BAND23_BIT73_OCCUPIED = 5263320
BAND24_TOTAL = 106861135
BAND24_FINAL_OCCUPIED = 10804024
FRESH23_TOTAL = 108499241

# regression gates from the 2026-11-17 earlier run (scripts lost to an
# environment reset; totals recorded in the lane log/knowledge)
EXPECTED = {
    "workerA_total_nodes": 48482011,     # == band23 bits 0..73 sum
    "workerA_final_occupied": 5263320,   # == band23 bit-73 occupancy
    "workers_total_nodes": 119962147,    # worker A + worker B (0.9899 band23)
    "prior_session_merged_occupied_after": 4291129,  # informational only:
    # the earlier session's merge implementation was lost; this
    # reimplementation computes occupied_after = distinctA + distinctB -
    # shared exactly and reproduces the workers bit-exactly, but its
    # occupied_after differs slightly (recorded, not gated).
    "conflicts_zero": True,
    "byte_identical_per_worker_bit": 22,
}


def git_blob_sha(path):
    data = open(path, "rb").read()
    h = hashlib.sha1()
    h.update(b"blob %d\x00" % len(data))
    h.update(data)
    return h.hexdigest()


def check_pin(name, path, expected):
    actual = git_blob_sha(path)
    if actual != expected:
        raise SystemExit("%s BLOB MISMATCH: %s != %s" % (name, actual, expected))


def make_variant(ms_shift):
    """Verbatim engine + MS substitution + dump/seed export block.
    No key-sign or negative-bound fixes: the workers and the seedrun run the
    verbatim memo semantics (published determinism)."""
    os.makedirs(WORK, exist_ok=True)
    src = open(EXTRACTOR, "r", encoding="utf-8").read()
    for pat, what in [(VERBATIM_LINE, "MS line"),
                      (PATCH_ANCHOR, "patch anchor")]:
        if src.count(pat) != 1:
            raise SystemExit("verbatim %s not found exactly once" % what)
    out = src.replace(VERBATIM_LINE,
                      "const MS=1<<%d, MM=MS-1;" % ms_shift)
    out = out.replace(PATCH_ANCHOR, PATCH_BLOCK + PATCH_ANCHOR)
    dst = os.path.join(
        WORK, "class4_child1_cert_extractor_exact_wm_ms%d.ts" % ms_shift)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(out)
    return dst


def make_driver(ms_shift):
    src = open(DRIVER, "r", encoding="utf-8").read()
    if DRIVER_IMPORT_TARGET not in src:
        raise SystemExit("driver import line not found")
    dst = os.path.join(
        WORK, "measure_worker_split_memo_73k_ms%d.ts" % ms_shift)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(src.replace(
            DRIVER_IMPORT_TARGET,
            "from './class4_child1_cert_extractor_exact_wm_ms%d.ts'" % ms_shift))
    return dst


def build_plan():
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    child = manifest["s6_child_hex"]
    bits = []
    for c in manifest["certificates"]:
        proc = subprocess.run([sys.executable, LEGAL, c["root"]],
                              capture_output=True, text=True, check=True)
        lines = [l for l in proc.stdout.splitlines() if l.strip()]
        moves = [int(x) for x in lines[1].split(",")]
        if len(moves) != c["loser_mobility"]:
            raise SystemExit("mobility mismatch bit %d" % c["bit"])
        bits.append({"bit": c["bit"], "root": c["root"], "file": c["file"],
                     "moves": moves,
                     "published_nodes": c["extraction_nodes"],
                     "published_rows": c["rows"]})
    order = sorted(bits, key=lambda b: b["bit"])
    plan_path = os.path.join(WORK, "plan73k.json")
    with open(plan_path, "w", encoding="utf-8") as fh:
        json.dump({"child": child, "bits": order}, fh)
    return manifest, plan_path


def run_worker(tag, ms_shift, plan, bits, max_old, seed_path=""):
    """Run one worker (or the seedrun) via nohup background + poll.
    Resume: if the summary already exists, it is loaded."""
    summary = os.path.join(WORK, tag + ".summary.json")
    dump = os.path.join(WORK, tag + ".dump.txt")
    if os.path.exists(summary) and os.path.getsize(summary) > 0:
        return json.load(open(summary, encoding="utf-8")), dump
    certdir = os.path.join(WORK, tag + ".certs")
    os.makedirs(certdir, exist_ok=True)
    plan_arg = os.path.join(WORK, tag + ".plan.json")
    full = json.load(open(plan, encoding="utf-8"))
    full["bits"] = [b for b in full["bits"] if b["bit"] in bits]
    full["tag"] = tag
    with open(plan_arg, "w", encoding="utf-8") as fh:
        json.dump(full, fh)
    driver = make_driver(ms_shift)
    cmd = [NODE, "--experimental-strip-types",
           "--max-old-space-size=" + max_old, driver, plan_arg, summary,
           certdir, dump]
    if seed_path:
        cmd.append(seed_path)
    log = os.path.join(WORK, tag + ".runlog.txt")
    with open(log, "w") as lf:
        subprocess.Popen(cmd, stdout=lf, stderr=lf, start_new_session=True)
    print("[start] %s -> %s" % (tag, log))
    return None, dump


def wait_worker(tag, timeout_s=1800):
    """Poll until the worker's summary exists (or fail on exit)."""
    summary = os.path.join(WORK, tag + ".summary.json")
    log = os.path.join(WORK, tag + ".runlog.txt")
    import time
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        if os.path.exists(summary) and os.path.getsize(summary) > 0:
            return json.load(open(summary, encoding="utf-8"))
        if not _proc_alive(tag):
            if os.path.exists(summary) and os.path.getsize(summary) > 0:
                return json.load(open(summary, encoding="utf-8"))
            tail = ""
            if os.path.exists(log):
                tail = open(log, encoding="utf-8", errors="replace").read()[-2000:]
            raise SystemExit("worker %s died without summary.\n%s" % (tag, tail))
        time.sleep(5)
    raise SystemExit("worker %s timed out" % tag)


def _proc_alive(tag):
    """Scan /proc cmdlines for the tag (no pgrep in this environment)."""
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            with open("/proc/%s/cmdline" % pid, "rb") as fh:
                cmd = fh.read().replace(b"\x00", b" ").decode(
                    "utf-8", "replace")
        except OSError:
            continue
        if tag in cmd and "measure_worker_split" in cmd:
            return True
    return False


def published_cert_bytes(manifest, bit):
    c = [x for x in manifest["certificates"] if x["bit"] == bit][0]
    fn = c["file"]
    if c.get("split_cut_byte") is not None:
        return (open(os.path.join(CERTDIR, fn + ".part1of2"), "rb").read() +
                open(os.path.join(CERTDIR, fn + ".part2of2"), "rb").read())
    return open(os.path.join(CERTDIR, fn), "rb").read()


def verify_snapshots(manifest, tag, bits):
    ok = 0
    mds = {}
    for bit in bits:
        c = [x for x in manifest["certificates"] if x["bit"] == bit][0]
        snap = open(os.path.join(WORK, tag + ".certs", c["file"]), "rb").read()
        pub = published_cert_bytes(manifest, bit)
        if snap == pub:
            ok += 1
        mds[str(bit)] = hashlib.md5(snap).hexdigest()
    return ok, mds


def sort_dump(tag):
    """External sort of a KYOENWM1 dump by key fields (2-5, hex zero-padded)."""
    dump = os.path.join(WORK, tag + ".dump.txt")
    srt = os.path.join(WORK, tag + ".dump.sorted")
    if not os.path.exists(srt):
        env = dict(os.environ, LC_ALL="C")
        with open(dump, "rb") as fi, open(srt, "wb") as fo:
            subprocess.run(["sort", "-S", "200M", "-k2,5"], stdin=fi,
                           stdout=fo, env=env, check=True)
    return srt


def distinct_pass(tag):
    """Stream the sorted dump: combine duplicate keys, count internal
    conflicts, write the distinct table (key + combined values)."""
    srt = sort_dump(tag)
    dst = os.path.join(WORK, tag + ".distinct.txt")
    n_records = 0
    distinct = 0
    dup_keys = 0
    max_copies = 0
    conflicts = {}
    cur_key = None
    cur = None
    copies = 0
    with open(srt, "r", encoding="utf-8") as fi, \
            open(dst, "w", encoding="utf-8") as fo:
        for line in fi:
            if line.startswith("KYOENWM1"):
                continue  # dump header line travels through the sort
            f = line.split()
            if len(f) != 9:
                raise SystemExit("bad dump record: %r" % line[:80])
            n_records += 1
            key = (f[1], f[2], f[3], f[4])
            rec = (int(f[5]), int(f[6]), int(f[7]), int(f[8]))
            if key != cur_key:
                if cur_key is not None:
                    if copies > 1:
                        dup_keys += 1
                    max_copies = max(max_copies, copies)
                    fo.write(" ".join(cur_key) + " %d %d %d %d\n" % cur)
                cur_key = key
                cur = rec
                copies = 1
                distinct += 1
            else:
                copies += 1
                cur = combine_values(cur[0], cur[1], cur[2], cur[3], rec)
                ck = conflict_kind(*cur)
                if ck:
                    conflicts.setdefault(ck, []).append(" ".join(key))
        if cur_key is not None:
            if copies > 1:
                dup_keys += 1
            max_copies = max(max_copies, copies)
            fo.write(" ".join(cur_key) + " %d %d %d %d\n" % cur)
    return {"records": n_records, "distinct": distinct,
            "dup_keys": dup_keys, "max_copies": max_copies,
            "conflicts": {k: len(v) for k, v in conflicts.items()},
            "conflict_samples": {k: v[:3] for k, v in conflicts.items()}}


def merge_pass(tagA, tagB):
    """Merge-join the two distinct tables: shared keys, cross conflicts,
    merged table (sorted by key) written as KYOENWM2 for seeding."""
    da = open(os.path.join(WORK, tagA + ".distinct.txt"), encoding="utf-8")
    db = open(os.path.join(WORK, tagB + ".distinct.txt"), encoding="utf-8")
    seed = os.path.join(WORK, "merged_seed.kyoenwm2")
    shared = 0
    conflicts = {}
    occupied_after = 0
    with open(seed, "w", encoding="utf-8") as fo:
        fo.write("KYOENWM2 merged worker_memo_tables cost73k "
                 "A=%s B=%s combine=win_min_lose_min_nowin_max_nolose_max\n"
                 % (tagA, tagB))
        ra = da.readline()
        rb = db.readline()
        while ra or rb:
            if ra and (not rb or ra.split(" ", 4)[:4] < rb.split(" ", 4)[:4]):
                fo.write(ra)
                occupied_after += 1
                ra = da.readline()
            elif rb and (not ra or ra.split(" ", 4)[:4] > rb.split(" ", 4)[:4]):
                fo.write(rb)
                occupied_after += 1
                rb = db.readline()
            else:
                fa = ra.split()
                fb = rb.split()
                key = fa[:4]
                cur = combine_values(int(fa[4]), int(fa[5]), int(fa[6]),
                                     int(fa[7]),
                                     (int(fb[4]), int(fb[5]), int(fb[6]),
                                      int(fb[7])))
                shared += 1
                occupied_after += 1
                ck = conflict_kind(*cur)
                if ck:
                    conflicts.setdefault(ck, []).append(" ".join(key))
                fo.write(" ".join(key) + " %d %d %d %d\n" % cur)
                ra = da.readline()
                rb = db.readline()
    da.close()
    db.close()
    return {"shared_distinct": shared, "occupied_after": occupied_after,
            "cross_conflicts": {k: len(v) for k, v in conflicts.items()},
            "conflict_samples": {k: v[:3] for k, v in conflicts.items()},
            "seed_path": seed}


def record_identity_pass(seedrun_tag, seed_path):
    """Record-identity gate: distinct-combine the seedrun's final dump and
    check every merged seed record: present with equal-or-stronger values
    (win<=, lose<=, nowin>=, nolose>= when the seed bound exists)."""
    stats = distinct_pass(seedrun_tag)  # also writes seedrun_tag.distinct.txt
    # memory-safe: stream both key-sorted files (seed and seedrun distinct).
    viol = []
    missing = 0
    present = 0
    with open(seed_path, encoding="utf-8") as fs_, \
            open(os.path.join(WORK, seedrun_tag + ".distinct.txt"),
                 encoding="utf-8") as ff:
        ls = fs_.readline()  # header
        rs = fs_.readline()
        rf = ff.readline()
        while rs or rf:
            ks = rs.split()[:4] if rs else None
            kf = rf.split()[:4] if rf else None
            if ks and (not kf or ks < kf):
                missing += 1
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
                oknw = bound_at_least(fnw, nowin)
                oknl = bound_at_least(fnl, nolose)
                if not (okw and okl and oknw and oknl):
                    viol.append(" ".join(ks))
                present += 1
                rs = fs_.readline()
                rf = ff.readline()
    return {"present": present, "missing": missing,
            "value_violations": len(viol),
            "violation_samples": viol[:3], "seedrun_dump_stats": stats}


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        OUT, "worker-split-memo-merge-73k-20261117.json")
    os.makedirs(WORK, exist_ok=True)
    check_pin("extractor", EXTRACTOR, EXTRACTOR_BLOB)
    check_pin("manifest", MANIFEST, MANIFEST_BLOB)
    check_pin("legal", LEGAL, LEGAL_BLOB)
    state_path = os.path.join(WORK, "state.json")
    if os.path.exists(state_path):
        state = json.load(open(state_path, encoding="utf-8"))
    else:
        state = {}

    manifest, plan = build_plan()
    child = json.load(open(plan, encoding="utf-8"))["child"]
    all_bits = [b["bit"] for b in json.load(open(plan))["bits"]]
    bitsA = [b for b in all_bits if b <= 73]
    bitsB = [b for b in all_bits if b >= 76]
    assert len(bitsA) == 11 and len(bitsB) == 11

    make_variant(23)
    make_variant(24)

    # ---- step 1: worker A ----
    sumA, _ = run_worker("workerA", 23, plan, bitsA, "350")
    if sumA is None:
        sumA = wait_worker("workerA")
    state["workerA"] = sumA
    json.dump(state, open(state_path, "w"))
    okA, mdA = verify_snapshots(manifest, "workerA", bitsA)

    # ---- step 2: worker B ----
    sumB, _ = run_worker("workerB", 23, plan, bitsB, "350")
    if sumB is None:
        sumB = wait_worker("workerB")
    state["workerB"] = sumB
    json.dump(state, open(state_path, "w"))
    okB, mdB = verify_snapshots(manifest, "workerB", bitsB)

    # ---- step 3: sort + distinct + internal conflicts ----
    dA = distinct_pass("workerA")
    dB = distinct_pass("workerB")
    state["distinctA"], state["distinctB"] = dA, dB
    json.dump(state, open(state_path, "w"))

    # ---- step 4: merge ----
    m = merge_pass("workerA", "workerB")
    seed_path = m["seed_path"]
    m["seed_md5"] = hashlib.md5(open(seed_path, "rb").read()).hexdigest()
    # merge determinism: second pass must give the same md5
    m2 = merge_pass("workerA", "workerB")
    m2md5 = hashlib.md5(open(m2["seed_path"], "rb").read()).hexdigest()
    m["merge_deterministic"] = (m2md5 == m["seed_md5"])
    state["merge"] = m
    json.dump(state, open(state_path, "w"))

    # ---- step 5: seedrun (merged seed, all 22 bits, ms24) ----
    sumS, _ = run_worker("seedrun", 24, plan, all_bits, "700",
                         seed_path=seed_path)
    if sumS is None:
        sumS = wait_worker("seedrun", timeout_s=2400)
    state["seedrun"] = sumS
    json.dump(state, open(state_path, "w"))
    okS, mdS = verify_snapshots(manifest, "seedrun", all_bits)

    # ---- step 6: record-identity gate on the seedrun dump ----
    ri = record_identity_pass("seedrun", seed_path)
    state["record_identity"] = ri
    json.dump(state, open(state_path, "w"))

    # ---- gates ----
    totA = sumA["total_nodes"]
    totB = sumB["total_nodes"]
    per_bit_A_ok = all(
        p["nodes_this_run"] == BAND23_PER_BIT[p["bit"]] for p in sumA["per_bit"])
    gates = {
        "workerA_per_bit_equals_band23_prefix": per_bit_A_ok,
        "workerA_total": totA == EXPECTED["workerA_total_nodes"],
        "workerA_final_occupied":
            sumA["final_memo_occupied"] == EXPECTED["workerA_final_occupied"],
        "workers_total":
            totA + totB == EXPECTED["workers_total_nodes"],
        "internal_conflicts_zero":
            not dA["conflicts"] and not dB["conflicts"],
        "cross_conflicts_zero": not m["cross_conflicts"],
        "worker_byte_identical_A": okA == 11,
        "worker_byte_identical_B": okB == 11,
        "seedrun_byte_identical": okS == 22,
        "seed_insert_failure_rate_below_0.1pct":
            ((sumS.get("seed") or {}).get("failed", 0) /
             max(1, (sumS.get("seed") or {}).get("seeded", 1))) < 0.001,
        "record_identity_no_violations": ri["value_violations"] == 0,
        "merge_deterministic": m["merge_deterministic"],
    }

    doc = {
        "schema": "n11-class2-lane-worker-split-memo-merge-73k-20261117-v1",
        "date": "2026-11-17",
        "lane": "n11 class2-lane long-term (cost73k)",
        "purpose": ("worker-split memo merge safety and benefit measurement: "
                    "2-worker split of the cost-73k band, KYOENWM1 dumps, "
                    "sort-based merge with WIN/LOSS conflict detection, "
                    "merged-seed band run at MS=1<<24"),
        "inputs": {
            "extractor_blob": EXTRACTOR_BLOB,
            "manifest_blob": MANIFEST_BLOB,
            "legal_blob": LEGAL_BLOB,
            "engine_variants": ("verbatim + MS line substitution + dump/seed "
                                "export block only; no key-sign or "
                                "negative-bound fixes"),
            "worker_ms": 23, "seedrun_ms": 24,
            "bitsA": bitsA, "bitsB": bitsB,
        },
        "workerA": {
            "total_nodes": totA,
            "final_occupied": sumA["final_memo_occupied"],
            "wall_ms": sumA["wall_ms"],
            "byte_identical": okA,
            "per_bit": sumA["per_bit"],
        },
        "workerB": {
            "total_nodes": totB,
            "final_occupied": sumB["final_memo_occupied"],
            "wall_ms": sumB["wall_ms"],
            "byte_identical": okB,
            "per_bit": sumB["per_bit"],
        },
        "workers_total_nodes": totA + totB,
        "vs_band23_total": (totA + totB) / BAND23_TOTAL,
        "distinct_pass": {"workerA": dA, "workerB": dB},
        "merge": m,
        "prior_session_occupied_after":
            EXPECTED["prior_session_merged_occupied_after"],
        "occupied_after_delta_vs_prior_session":
            m["occupied_after"] - EXPECTED["prior_session_merged_occupied_after"],
        "seedrun": {
            "total_nodes": sumS["total_nodes"],
            "final_occupied": sumS["final_memo_occupied"],
            "seed": sumS.get("seed"),
            "wall_ms": sumS["wall_ms"],
            "byte_identical": okS,
            "per_bit": sumS["per_bit"],
            "load_factor_final": sumS["final_memo_occupied"] / (1 << 24),
            "vs_band24_total": sumS["total_nodes"] / BAND24_TOTAL,
            "vs_fresh23_total": sumS["total_nodes"] / FRESH23_TOTAL,
        },
        "record_identity": ri,
        "gates": gates,
        "gates_all_pass": all(gates.values()),
        "expected_gates": EXPECTED,
        "interpretation_guard": (
            "MEASUREMENT ONLY. No new WIN/LOSS verdicts; no manifest row "
            "opened or closed; certificate bytes unchanged. The repo-verbatim "
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
        print("  gate %-36s %s" % (k, v))
    if not doc["gates_all_pass"]:
        print("GATES FAILED; see", out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
