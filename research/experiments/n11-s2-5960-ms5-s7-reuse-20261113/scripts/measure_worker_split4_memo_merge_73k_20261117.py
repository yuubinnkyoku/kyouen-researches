#!/usr/bin/env python3
"""4-worker (N-worker extension) memo split/merge measurement for the
cost-73k lane (2026-11-17, n11 class2-lane long-term lane).

MEASUREMENT ONLY (no certificate publication, no verdict changes).

This extends the published 2-worker measurement (K0909,
measure_worker_split_memo_merge_73k_20261117.py, commit f9e3acf8) to a
4-worker split of the same published cost-73k WIN7-D10 band (22 roots,
manifest class2-lane-cost73k-win7-certificates-20261117.json), with the
same repo-verbatim extractor (blob 52bcaf50..., including the two known
performance-only memo bugs; see item K0907):

  worker W1: bits 0,7,11,15,35,39,41      (7 bits, fresh process; band-prefix)
  worker W2: bits 44,58,62,73,76,87       (6 bits, fresh process)
  worker W3: bits 89,94,95,97,98          (5 bits, fresh process)
  worker W4: bits 103,105,112,117         (4 bits, fresh process)

Split chosen for approximate node-count balance across workers at MS=1<<23
(published band/fresh per-bit values).  Each worker carries its memo
band-wide within its own bits (rows cleared per bit; every certificate is
reconstructed and byte-compared against the published certificate), then
dumps the full memo table in KYOENWM1 format.

Offline N-way merge (sort-based, streaming, no sqlite):
  1. Each worker dump is externally sorted by key and stream-deduplicated
     (duplicate keys from the signed-key bug, all high-bit, combined by
     win=min lose=min nowin=max nolose=max); INTERNAL conflicts counted
     per worker (same rules as the published 2-worker measurement).
  2. The four distinct-key streams are N-way merge-joined with a heap:
     key incidence histogram (how many keys appear in exactly 1/2/3/4
     workers - new data for the shared-cache design), CROSS conflicts
     checked on the combined values, merged KYOENWM2 table written sorted
     by key for seeding.  occupied_after = size of the key union.

Seedrun: verbatim engine at MS=1<<24 seeds its memo from the merged
4-worker table (insertion in file order through the engine's own
memoEntry(), preserving verbatim probe semantics), then extracts all 22
bits band-wide in one process.  Gates: 22/22 certificates byte-identical,
record-identity check of the seedrun final dump against the merged seed,
seed insertion-failure rate < 0.1%.

Regression anchors (published constants this run must reproduce):
  - worker W1 is exactly the band-ms23 prefix through bit 41, so every
    W1 per-bit node count must equal the published band ms23 per-bit
    value (total 29,193,572) and W1's final memo occupancy must equal the
    band ms23 bit-41 occupancy 3,816,312.
  - The first bit of each fresh worker runs with an empty memo, so it
    must equal the published fresh-ms23 per-bit value exactly:
    W2 bit 44 = 4,617,329; W3 bit 89 = 3,869,180; W4 bit 103 = 5,828,967.
  - Natural internal and cross conflicts == 0 (same result as 2-worker).
  - bit 95 is memo-state-invariant: 11,857,737 nodes in every worker.

Comparison (informational, recorded not gated): 2-worker published values
(total 119,962,147 nodes, distinct 2,619,833+2,554,155, shared 882,089,
occupied_after 4,291,899, seedrun 85,747,496 nodes, load 63.27%, seed md5
e7c2c17e...).  The 4-worker merged union is NOT expected to be byte-equal
to the 2-worker merged table (per-worker insertion-failure sets differ);
the union size and seedrun response are the measured quantities.

Interpretation guard: measurement only.  No new WIN/LOSS verdicts, no
manifest row opened or closed, certificate bytes unchanged.  The verbatim
extractor is NOT modified in the repo (published determinism chains).
WIN7-D10 proves a first-player win within depth 10 from the individual
7-stone roots only; REFUTED-D10 is not a LOSS proof.  The 11x11 empty
board, both two-stone roots {49,60} and {59,60}, S2 {59,60} and classes
1/2/4 all remain UNKNOWN.

Usage:  python3 measure_worker_split4_memo_merge_73k_20261117.py <out.json>
        (env: KYOEN_NODE=node; every step resumes from
        output/worker_split4_merge_73k_work/)
"""
import hashlib
import heapq
import json
import os
import subprocess
import sys

from worker_memo_merge import bound_at_least, combine_values, conflict_kind

HERE = os.path.dirname(os.path.abspath(__file__)) or "."
OUT = os.path.join(HERE, "output")
CERTDIR = os.path.join(OUT, "class2-lane-cost73k-certificates")
WORK = os.path.join(OUT, "worker_split4_merge_73k_work")
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
# published band ms23 per-bit memo occupancy (same JSON)
BAND23_OCC = {
    0: 710449, 7: 1469800, 11: 1882289, 15: 2897951, 35: 3473099,
    39: 3705871, 41: 3816312, 44: 4351136, 58: 4733550, 62: 4840253,
    73: 5263320, 76: 5455717, 87: 5740141, 89: 5897703, 94: 6052245,
    95: 6461036, 97: 6605363, 98: 6715861, 103: 6850436, 105: 6957410,
    112: 7051664, 117: 7144086}
# published fresh-per-bit ms23 node counts (same JSON, attribution section)
FRESH23_PER_BIT = {
    0: 4303203, 7: 4970943, 11: 2910026, 15: 8108353, 35: 4871692,
    39: 2037105, 41: 1868639, 44: 4617329, 58: 4567866, 62: 1771346,
    73: 7370204, 76: 4098489, 87: 6581793, 89: 3869180, 94: 4204274,
    95: 11857737, 97: 3815019, 98: 5336993, 103: 5828967, 105: 3641568,
    112: 4767520, 117: 7100995}
BAND23_TOTAL = 121186659
BAND23_BIT41_OCCUPIED = BAND23_OCC[41]
BAND24_TOTAL = 106861135
FRESH23_TOTAL = 108499241

BITS_W1 = [0, 7, 11, 15, 35, 39, 41]
BITS_W2 = [44, 58, 62, 73, 76, 87]
BITS_W3 = [89, 94, 95, 97, 98]
BITS_W4 = [103, 105, 112, 117]
W1_TOTAL = sum(BAND23_PER_BIT[b] for b in BITS_W1)

# published 2-worker measurement (K0909) comparison constants
TWO_WAY = {
    "workers_total_nodes": 119962147,
    "workerA_total_nodes": 48482011,
    "workerB_total_nodes": 71480136,
    "distinctA": 2619833,
    "distinctB": 2554155,
    "shared_distinct": 882089,
    "occupied_after": 4291899,
    "merged_seed_md5": "e7c2c17e7a91d8ea17f433f3bb482f29",
    "seedrun_total_nodes": 85747496,
    "seedrun_load_factor": 0.6327,
    "seedrun_seed_inserted": 4290451,
    "seedrun_seed_failed": 1448,
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
        WORK, "class4_child1_cert_extractor_exact_wm4_ms%d.ts" % ms_shift)
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
            "from './class4_child1_cert_extractor_exact_wm4_ms%d.ts'" % ms_shift))
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


def _key_of(line):
    return line.split()[:4]


def _emit_group(fo, key, vals, incidence, conflicts):
    incidence[len(vals)] += 1
    cur = vals[0]
    for rec in vals[1:]:
        cur = combine_values(cur[0], cur[1], cur[2], cur[3], rec)
    ck = conflict_kind(*cur)
    if ck:
        conflicts.setdefault(ck, []).append(" ".join(key))
    fo.write(" ".join(key) + " %d %d %d %d\n" % cur)


def merge_pass_nway(tags, seed_name="merged_seed4.kyoenwm2"):
    """N-way merge-join of the distinct tables: key incidence histogram,
    cross conflicts on combined values, merged sorted KYOENWM2 table."""
    streams = [open(os.path.join(WORK, t + ".distinct.txt"),
                    encoding="utf-8") for t in tags]
    seed = os.path.join(WORK, seed_name)
    n_workers = len(tags)
    incidence = {k: 0 for k in range(1, n_workers + 1)}
    conflicts = {}
    occupied_after = 0
    shared_total = 0  # keys present in >= 2 workers
    with open(seed, "w", encoding="utf-8") as fo:
        fo.write("KYOENWM2 merged worker_memo_tables cost73k 4way "
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
                    _emit_group(fo, group_key, group_vals, incidence,
                                conflicts)
                    occupied_after += 1
                    if len(group_vals) >= 2:
                        shared_total += 1
                group_key = key
                group_vals = []
            group_vals.append((int(f[4]), int(f[5]), int(f[6]), int(f[7])))
        if group_key is not None:
            _emit_group(fo, group_key, group_vals, incidence, conflicts)
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


def record_identity_pass(seedrun_tag, seed_path):
    """Record-identity gate: distinct-combine the seedrun's final dump and
    check every merged seed record: present with equal-or-stronger values
    (win<=, lose<=, nowin>=, nolose>= when the seed bound exists)."""
    stats = distinct_pass(seedrun_tag)
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
        OUT, "worker-split4-memo-merge-73k-20261117.json")
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
    all_bits = [b["bit"] for b in json.load(open(plan))["bits"]]
    assert all_bits == sorted(BITS_W1 + BITS_W2 + BITS_W3 + BITS_W4), \
        "split must be an exact ordered partition of the band"

    make_variant(23)
    make_variant(24)

    worker_defs = [("workerW1", BITS_W1), ("workerW2", BITS_W2),
                   ("workerW3", BITS_W3), ("workerW4", BITS_W4)]
    sums = {}
    oks = {}
    for tag, bits in worker_defs:
        s, _ = run_worker(tag, 23, plan, bits, "350")
        if s is None:
            s = wait_worker(tag)
        state[tag] = s
        json.dump(state, open(state_path, "w"))
        ok, _md = verify_snapshots(manifest, tag, bits)
        sums[tag] = s
        oks[tag] = ok
        print("[done] %s nodes=%d occ=%d byte_identical=%d/%d"
              % (tag, s["total_nodes"], s["final_memo_occupied"], ok,
                 len(bits)))

    # ---- sort + distinct + internal conflicts per worker ----
    distincts = {}
    for tag, _bits in worker_defs:
        distincts[tag] = distinct_pass(tag)
        state["distinct_" + tag] = distincts[tag]
        json.dump(state, open(state_path, "w"))
        print("[distinct] %s -> %s" % (tag, distincts[tag]["distinct"]))

    # ---- 4-way merge ----
    m = merge_pass_nway([t for t, _ in worker_defs])
    seed_path = m["seed_path"]
    m["seed_md5"] = hashlib.md5(open(seed_path, "rb").read()).hexdigest()
    m2 = merge_pass_nway([t for t, _ in worker_defs],
                         seed_name="merged_seed4_repeat.kyoenwm2")
    m2md5 = hashlib.md5(open(m2["seed_path"], "rb").read()).hexdigest()
    os.unlink(m2["seed_path"])
    m["merge_deterministic"] = (m2md5 == m["seed_md5"])
    state["merge4"] = m
    json.dump(state, open(state_path, "w"))
    print("[merge4] occupied_after=%s shared=%s conflicts=%s"
          % (m["occupied_after"], m["shared_total"],
             m["cross_conflicts"]))

    # ---- seedrun (merged 4-way seed, all 22 bits, ms24) ----
    sumS, _ = run_worker("seedrun4", 24, plan, all_bits, "700",
                         seed_path=seed_path)
    if sumS is None:
        sumS = wait_worker("seedrun4", timeout_s=2400)
    state["seedrun4"] = sumS
    json.dump(state, open(state_path, "w"))
    okS, mdS = verify_snapshots(manifest, "seedrun4", all_bits)

    # ---- record-identity gate on the seedrun dump ----
    ri = record_identity_pass("seedrun4", seed_path)
    state["record_identity"] = ri
    json.dump(state, open(state_path, "w"))

    # ---- gates ----
    per_bit_w1 = {p["bit"]: p["nodes_this_run"] for p in sums["workerW1"]["per_bit"]}
    first_bit_anchors = {
        "workerW2": (44, FRESH23_PER_BIT[44]),
        "workerW3": (89, FRESH23_PER_BIT[89]),
        "workerW4": (103, FRESH23_PER_BIT[103]),
    }
    anchor_ok = {}
    for tag, (bit, expect) in first_bit_anchors.items():
        got = [p["nodes_this_run"] for p in sums[tag]["per_bit"]
               if p["bit"] == bit][0]
        anchor_ok[tag] = (got == expect)
    bit95_nodes = [p["nodes_this_run"] for p in sums["workerW3"]["per_bit"]
                   if p["bit"] == 95][0]
    workers_total = sum(sums[t]["total_nodes"] for t, _ in worker_defs)
    seed = (sumS.get("seed") or {})
    gates = {
        "workerW1_per_bit_equals_band23_prefix":
            all(per_bit_w1[b] == BAND23_PER_BIT[b] for b in BITS_W1),
        "workerW1_total": sums["workerW1"]["total_nodes"] == W1_TOTAL,
        "workerW1_final_occupied":
            sums["workerW1"]["final_memo_occupied"] == BAND23_BIT41_OCCUPIED,
        "first_bit_fresh_anchors": all(anchor_ok.values()),
        "bit95_memo_state_invariant": bit95_nodes == 11857737,
        "internal_conflicts_zero":
            all(not distincts[t]["conflicts"] for t, _ in worker_defs),
        "cross_conflicts_zero": not m["cross_conflicts"],
        "worker_byte_identical":
            (oks["workerW1"] == 7 and oks["workerW2"] == 6 and
             oks["workerW3"] == 5 and oks["workerW4"] == 4),
        "seedrun_byte_identical": okS == 22,
        "seed_insert_failure_rate_below_0.1pct":
            (seed.get("failed", 0) / max(1, seed.get("seeded", 1))) < 0.001,
        "record_identity_no_violations": ri["value_violations"] == 0,
        "record_identity_missing_equals_seed_failed":
            ri["missing"] == seed.get("failed", 0),
        "merge_deterministic": m["merge_deterministic"],
    }

    doc = {
        "schema": "n11-class2-lane-worker-split4-memo-merge-73k-20261117-v1",
        "date": "2026-11-17",
        "lane": "n11 class2-lane long-term (cost73k)",
        "purpose": ("N-worker extension of the K0909 worker-split memo merge "
                    "measurement: 4-worker split of the cost-73k band, "
                    "KYOENWM1 dumps, N-way sort-based merge with key "
                    "incidence histogram and WIN/LOSS conflict detection, "
                    "merged-seed band run at MS=1<<24"),
        "inputs": {
            "extractor_blob": EXTRACTOR_BLOB,
            "manifest_blob": MANIFEST_BLOB,
            "legal_blob": LEGAL_BLOB,
            "engine_variants": ("verbatim + MS line substitution + dump/seed "
                                "export block only; no key-sign or "
                                "negative-bound fixes"),
            "worker_ms": 23, "seedrun_ms": 24,
            "bitsW1": BITS_W1, "bitsW2": BITS_W2,
            "bitsW3": BITS_W3, "bitsW4": BITS_W4,
            "split_rationale": ("node-count balanced at MS=1<<23 using the "
                                "published band/fresh per-bit values; W1 is "
                                "the band-ms23 prefix through bit 41"),
        },
        "workers": {
            t: {"total_nodes": sums[t]["total_nodes"],
                "final_occupied": sums[t]["final_memo_occupied"],
                "wall_ms": sums[t]["wall_ms"],
                "byte_identical": oks[t],
                "per_bit": sums[t]["per_bit"],
                "distinct": distincts[t]}
            for t, _ in worker_defs},
        "workers_total_nodes": workers_total,
        "vs_band23_total": workers_total / BAND23_TOTAL,
        "vs_two_way_workers_total":
            workers_total / TWO_WAY["workers_total_nodes"],
        "merge4": m,
        "two_way_comparison": {
            "two_way_occupied_after": TWO_WAY["occupied_after"],
            "occupied_after_delta_4way_minus_2way":
                m["occupied_after"] - TWO_WAY["occupied_after"],
            "two_way_shared_distinct": TWO_WAY["shared_distinct"],
            "two_way_workers_total_nodes": TWO_WAY["workers_total_nodes"],
            "two_way_merged_seed_md5": TWO_WAY["merged_seed_md5"],
            "two_way_seedrun_total_nodes": TWO_WAY["seedrun_total_nodes"],
        },
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
            "vs_two_way_seedrun_total":
                sumS["total_nodes"] / TWO_WAY["seedrun_total_nodes"],
        },
        "record_identity": ri,
        "first_bit_anchor_checks": anchor_ok,
        "gates": gates,
        "gates_all_pass": all(gates.values()),
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
        print("  gate %-44s %s" % (k, v))
    if not doc["gates_all_pass"]:
        print("GATES FAILED; see", out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
