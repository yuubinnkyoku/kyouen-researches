#!/usr/bin/env python3
"""fixB worker-split memo merge measurement for the cost-73k lane
(2026-11-17, n11 class2-lane long-term lane).

MEASUREMENT ONLY (no certificate publication, no verdict changes).

This combines two published lanes for the first time:
  - K0907 fixB engine (both memo bugs fixed: Int32Array memo keys +
    sentinel-aware nowin/nolose updates; 22/22 certificates byte-identical,
    fresh-per-bit battery 28,290,025 nodes = 26.07% of verbatim fresh ms23),
  - K0909 worker-split merge configuration (2 workers at the published
    73/76 bit boundary, KYOENWM1 full-slot dumps, sort-based distinct+merge
    with sentinel-aware conflict detection, KYOENWM2 merged seed, seedrun).

Arms (all fixB, all deterministic, every certificate byte-compared):
  arm0 band23 : fixB band ms23 single process, all 22 bits, memo carried
                -> the FIRST fixB band-wide reference (per-bit series,
                   final occupied, full KYOENWM1 dump).
  arm1 workerA: fixB bits 0..73,  fresh process ms23 (band prefix).
  arm2 workerB: fixB bits 76..117, fresh process ms23.
  arm3 merge  : sort+distinct both worker dumps (duplicate-key census on
                the fixed engine: expect records == distinct, max copies 1,
                the full-band confirmation of the K0907 bug-A mechanism),
                then merge-join with LIVE nowin/nolose bounds: the
                win_le_nowin / lose_le_nolose conflict detectors of the
                published merge algebra are exercised on naturally live
                negative bounds for the first time.
  arm4 seedrun: fixB ms24 all 22 bits seeded with the merged table.
  arm5 band24 : fixB ms24 all 22 bits unseeded (seed-benefit reference).
  arm6 sim    : light_sim_seed_73k.mjs on the merged seed at MS=1<<24;
                engine seed failures must equal the sim prediction exactly.
  arm7 cmp    : band23 distinct table vs merged table (merge non-closure
                under the fixed engine: only_in_band / only_in_merged and
                shared-key value consistency).

Regression anchors (published, must reproduce):
  - fixB fresh battery per-bit (bit0 1,277,392 nodes; battery total
    28,290,025; byte-identical 22/22, blob-pinned inputs).
  - verbatim references for ratio reporting only: 2-way workers total
    119,962,147, merged occupied_after 4,291,899, band ms23 121,186,659,
    seedrun ms24 85,747,496, band ms24 106,861,135, fresh battery 108,499,241.

Interpretation guard: measurement only.  No new WIN/LOSS verdicts, no
manifest row opened or closed, certificate bytes unchanged.  The
repo-verbatim extractor is NOT modified in the repo (published determinism
chains); the fixB variants exist only in the work directory.  Adoption of
fixB as a production extractor is a separate lane decision.  WIN7-D10
proves a first-player win within depth 10 from the individual 7-stone
roots only; REFUTED-D10 is not a LOSS proof.  The 11x11 empty board, both
two-stone roots {49,60} and {59,60}, S2 {59,60} and classes 1/2/4 all
remain UNKNOWN.

Usage:  python3 measure_worker_split_fixb_memo_merge_73k_20261117.py <out.json>
        (env: KYOEN_NODE=node; every step resumes from
        output/fixb_worker_split_merge_73k_work/)
"""
import hashlib
import json
import os
import subprocess
import sys

from worker_memo_merge import bound_at_least, combine_values, conflict_kind

HERE = os.path.dirname(os.path.abspath(__file__)) or "."
OUT = os.path.join(HERE, "output")
CERTDIR = os.path.join(HERE, "class2-lane-cost73k-certificates")
WORK = os.path.join(OUT, "fixb_worker_split_merge_73k_work")
NODE = os.environ.get("KYOEN_NODE", "node")

EXTRACTOR = os.path.join(HERE, "class4_child1_cert_extractor_exact.ts")
DRIVER = os.path.join(HERE, "measure_worker_split_memo_73k.ts")
LEGAL = os.path.join(HERE, "legal_candidates.py")
SIM = os.path.join(HERE, "light_sim_seed_73k.mjs")
MANIFEST = os.path.join(
    CERTDIR, "class2-lane-cost73k-win7-certificates-20261117.json")

EXTRACTOR_BLOB = "52bcaf509ea12fad4c936501d30d26b5b66c0085"
MANIFEST_BLOB = "0892aed07d187ae2fb3b4b90a21c7adbc1002b62"
LEGAL_BLOB = "8e97082c42838c7a4a4b6d2dd235276c8d43ab9a"

VERBATIM_LINE = "const MS=1<<18, MM=MS-1;"
KEYS_LINE = ("const mK0=new Uint32Array(MS),mK1=new Uint32Array(MS),"
             "mK2=new Uint32Array(MS),mK3=new Uint32Array(MS);")
KEYS_LINE_FIXED = ("const mK0=new Int32Array(MS),mK1=new Int32Array(MS),"
                   "mK2=new Int32Array(MS),mK3=new Int32Array(MS);")
NOWIN_LINE = "if(h>=0&&d>mNoWin[h]) mNoWin[h]=d;"
NOWIN_LINE_FIXED = "if(h>=0&&(mNoWin[h]===255||d>mNoWin[h])) mNoWin[h]=d;"
NOLOSE_LINE = "if(h>=0&&e>mNoLose[h]) mNoLose[h]=e;"
NOLOSE_LINE_FIXED = "if(h>=0&&(mNoLose[h]===255||e>mNoLose[h])) mNoLose[h]=e;"
PATCH_ANCHOR = ("export function extractBatch(childHex: string, bit: number, "
                "killTable: Record<number, number>, moves: number[]) {")
PATCH_BLOCK = """// EXPERIMENT MODIFICATION (2026-11-17, fixB worker-split memo merge
// measurement only; not a replacement for the published extractor): fixB
// memo semantics (Int32Array keys + sentinel-aware negative bounds, see
// K0907) plus row-set reset, occupancy probe, full memo-table dump
// (KYOENWM1) and a streaming memo seed loader (KYOENWM2).
export function clearRows(): void { rows.clear(); }
export function memoStats(): { slots: number, occupied: number } {
  let c = 0; for (let i = 0; i < MS; i++) if (mOcc[i]) c++;
  return { slots: MS, occupied: c };
}
export function dumpMemo(path: string, header: string): void {
  const fd = fs.openSync(path, 'w');
  fs.writeSync(fd, header + NL);
  let buf = '';
  let written = 0;
  for (let i = 0; i < MS; i++) {
    if (!mOcc[i]) continue;
    buf += i + ' '
      + (mK0[i] >>> 0).toString(16).padStart(8, '0') + ' '
      + (mK1[i] >>> 0).toString(16).padStart(8, '0') + ' '
      + (mK2[i] >>> 0).toString(16).padStart(8, '0') + ' '
      + (mK3[i] >>> 0).toString(16).padStart(8, '0') + ' '
      + mWin[i] + ' ' + mLose[i] + ' ' + mNoWin[i] + ' ' + mNoLose[i] + NL;
    if (buf.length > (1 << 20)) { fs.writeSync(fd, buf); written += buf.length; buf = ''; }
    if (written >= (32 << 20)) { fs.fsyncSync(fd); written = 0; }
  }
  if (buf.length) fs.writeSync(fd, buf);
  fs.fsyncSync(fd);
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

# published references (ratio reporting only, no gates on these)
VERBATIM_REFS = {
    "band_ms23_total": 121186659,
    "band_ms24_total": 106861135,
    "fresh_ms23_total": 108499241,
    "two_way_workers_total": 119962147,
    "two_way_merged_occupied_after": 4291899,
    "two_way_seedrun_ms24_total": 85747496,
    "fixb_fresh_battery_total": 28290025,
}
# published fixB fresh-per-bit battery (K0907): per-bit regression anchor
FIXB_BATTERY_PER_BIT_NODES = {
    0: 1277392, 7: 1591792, 11: 865968, 15: 2032584, 35: 1458609,
    39: 559635, 41: 685117, 44: 1233735, 58: 1272331, 62: 529105,
    73: 1726317, 76: 1142104, 87: 1708980, 89: 989258, 94: 1097336,
    95: 1415400, 97: 1370585, 98: 1363204, 103: 1679848, 105: 976798,
    112: 1429015, 117: 1884912}


def git_blob_sha(path):
    data = open(path, "rb").read()
    h = hashlib.sha1()
    h.update(b"blob %d\x00" % len(data))
    h.update(data)
    return h.hexdigest()


def check_pin(name, path, expected):
    actual = git_blob_sha(path)
    if actual != expected:
        raise SystemExit("%s BLOB MISMATCH: %s != %s" % (name, actual,
                                                          expected))


def make_fixb_variant(ms_shift):
    """Verbatim engine + MS substitution + fixB (Int32Array memo keys,
    sentinel-aware negative bounds) + dump/seed export block.
    Exactly one line-level change per bug, asserted by exact counts."""
    os.makedirs(WORK, exist_ok=True)
    src = open(EXTRACTOR, "r", encoding="utf-8").read()
    for pat, what in [(VERBATIM_LINE, "MS line"),
                      (KEYS_LINE, "memo key arrays line"),
                      (NOWIN_LINE, "no-win update"),
                      (NOLOSE_LINE, "no-lose update"),
                      (PATCH_ANCHOR, "patch anchor")]:
        if src.count(pat) != 1:
            raise SystemExit("verbatim %s not found exactly once" % what)
    out = src.replace(VERBATIM_LINE, "const MS=1<<%d, MM=MS-1;" % ms_shift)
    out = out.replace(KEYS_LINE, KEYS_LINE_FIXED)
    out = out.replace(NOWIN_LINE, NOWIN_LINE_FIXED)
    out = out.replace(NOLOSE_LINE, NOLOSE_LINE_FIXED)
    out = out.replace(PATCH_ANCHOR, PATCH_BLOCK + PATCH_ANCHOR)
    dst = os.path.join(
        WORK, "class4_child1_cert_extractor_exact_fixbwm_ms%d.ts" % ms_shift)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(out)
    return dst


def make_driver(ms_shift):
    src = open(DRIVER, "r", encoding="utf-8").read()
    if DRIVER_IMPORT_TARGET not in src:
        raise SystemExit("driver import line not found")
    dst = os.path.join(
        WORK, "measure_worker_split_memo_73k_fixbwm_ms%d.ts" % ms_shift)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(src.replace(
            DRIVER_IMPORT_TARGET,
            "from './class4_child1_cert_extractor_exact_fixbwm_ms%d.ts'"
            % ms_shift))
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
    """Run one arm via background process + external poll.
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
    print("[start] %s -> %s" % (tag, log), flush=True)
    return None, dump


def wait_worker(tag, timeout_s=1800):
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
                tail = open(log, encoding="utf-8",
                             errors="replace").read()[-2000:]
            raise SystemExit("worker %s died without summary.\n%s"
                             % (tag, tail))
        time.sleep(5)
    raise SystemExit("worker %s timed out" % tag)


def _proc_alive(tag):
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


def published_cert_bytes(bit):
    c = [x for x in MANIFEST_CACHE["certificates"]
         if x["bit"] == bit][0]
    fn = c["file"]
    if c.get("split_cut_byte") is not None:
        return (open(os.path.join(CERTDIR, fn + ".part1of2"), "rb").read() +
                open(os.path.join(CERTDIR, fn + ".part2of2"), "rb").read())
    return open(os.path.join(CERTDIR, fn), "rb").read()


def verify_snapshots(tag, bits):
    ok = 0
    mds = {}
    for bit in bits:
        c = [x for x in MANIFEST_CACHE["certificates"]
             if x["bit"] == bit][0]
        snap = open(os.path.join(WORK, tag + ".certs", c["file"]),
                    "rb").read()
        pub = published_cert_bytes(bit)
        if snap == pub:
            ok += 1
        mds[str(bit)] = hashlib.md5(snap).hexdigest()
    return ok, mds


def sort_dump(tag):
    dump = os.path.join(WORK, tag + ".dump.txt")
    srt = os.path.join(WORK, tag + ".dump.sorted")
    if not os.path.exists(srt) or os.path.getsize(srt) == 0:
        env = dict(os.environ, LC_ALL="C")
        with open(dump, "rb") as fi, open(srt, "wb") as fo:
            subprocess.run(["sort", "-S", "200M", "-k2,5"], stdin=fi,
                           stdout=fo, env=env, check=True)
    return srt


def distinct_pass(tag):
    """Stream the sorted dump: combine duplicate keys, count internal
    conflicts, write the distinct table, and count LIVE-bound coverage
    (win/lose/nowin/nolose < 255) over distinct keys."""
    srt = sort_dump(tag)
    dst = os.path.join(WORK, tag + ".distinct.txt")
    n_records = 0
    distinct = 0
    dup_keys = 0
    max_copies = 0
    conflicts = {}
    bound = {"win": 0, "lose": 0, "nowin": 0, "nolose": 0,
             "win_and_lose": 0, "win_and_nowin_lt": 0, "all_unbound": 0}
    cur_key = None
    cur = None
    copies = 0

    def acc(rec):
        w, l, nw, nl = rec
        if w < 255:
            bound["win"] += 1
        if l < 255:
            bound["lose"] += 1
        if nw < 255:
            bound["nowin"] += 1
        if nl < 255:
            bound["nolose"] += 1
        if w < 255 and l < 255:
            bound["win_and_lose"] += 1
        if w < 255 and nw < 255 and nw < w:
            bound["win_and_nowin_lt"] += 1
        if w == 255 and l == 255 and nw == 255 and nl == 255:
            bound["all_unbound"] += 1

    with open(srt, "r", encoding="utf-8") as fi, \
            open(dst, "w", encoding="utf-8") as fo:
        for line in fi:
            if line.startswith("KYOENWM1"):
                continue
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
                    acc(cur)
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
            acc(cur)
            fo.write(" ".join(cur_key) + " %d %d %d %d\n" % cur)
    return {"records": n_records, "distinct": distinct,
            "dup_keys": dup_keys, "max_copies": max_copies,
            "conflicts": {k: len(v) for k, v in conflicts.items()},
            "conflict_samples": {k: v[:3] for k, v in conflicts.items()},
            "live_bound_coverage": bound}


def merge_pass(tagA, tagB, seed_name="merged_seed_fixb.kyoenwm2"):
    da = open(os.path.join(WORK, tagA + ".distinct.txt"), encoding="utf-8")
    db = open(os.path.join(WORK, tagB + ".distinct.txt"), encoding="utf-8")
    seed = os.path.join(WORK, seed_name)
    shared = 0
    conflicts = {}
    occupied_after = 0
    with open(seed, "w", encoding="utf-8") as fo:
        fo.write("KYOENWM2 merged fixb_worker_memo_tables cost73k "
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
    stats = distinct_pass(seedrun_tag)
    viol = []
    missing = 0
    present = 0
    with open(seed_path, encoding="utf-8") as fs_, \
            open(os.path.join(WORK, seedrun_tag + ".distinct.txt"),
                 encoding="utf-8") as ff:
        fs_.readline()  # header
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


def band_vs_merged_pass(band_tag, merged_seed_path):
    """Compare the unsplit band distinct table with the merged 2-way seed:
    only_in_band / only_in_merged counts and shared-key value consistency
    (combined record must be conflict-free; both tables are sound proofs)."""
    fb_path = os.path.join(WORK, band_tag + ".distinct.txt")
    shared = 0
    only_band = 0
    only_merged = 0
    conflicts = {}
    band_stronger = 0
    merged_stronger = 0
    with open(fb_path, encoding="utf-8") as fb, \
            open(merged_seed_path, encoding="utf-8") as fm:
        fm.readline()  # header
        rb = fb.readline()
        rm = fm.readline()
        while rb or rm:
            kb = rb.split()[:4] if rb else None
            km = rm.split()[:4] if rm else None
            if kb and (not km or kb < km):
                only_band += 1
                rb = fb.readline()
            elif km and (not kb or kb > km):
                only_merged += 1
                rm = fm.readline()
            else:
                fbd = [int(x) for x in rb.split()[4:]]
                fmd = [int(x) for x in rm.split()[4:]]
                cur = combine_values(fbd[0], fbd[1], fbd[2], fbd[3], fmd)
                ck = conflict_kind(*cur)
                if ck:
                    conflicts.setdefault(ck, []).append(" ".join(kb))
                # 255 is the largest value and means absent, so plain
                # integer comparison orders bounds correctly.
                if fbd[0] < fmd[0]:
                    band_stronger += 1
                if fmd[0] < fbd[0]:
                    merged_stronger += 1
                shared += 1
                rb = fb.readline()
                rm = fm.readline()
    return {"shared": shared, "only_in_band": only_band,
            "only_in_merged": only_merged,
            "shared_value_conflicts":
                {k: len(v) for k, v in conflicts.items()},
            "conflict_samples": {k: v[:3] for k, v in conflicts.items()},
            "band_strictly_better_win_examples": band_stronger,
            "merged_strictly_better_win_examples": merged_stronger}


MANIFEST_CACHE = None


def main():
    global MANIFEST_CACHE
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        OUT, "fixb-worker-split-memo-merge-73k-20261117.json")
    os.makedirs(WORK, exist_ok=True)
    check_pin("extractor", EXTRACTOR, EXTRACTOR_BLOB)
    check_pin("manifest", MANIFEST, MANIFEST_BLOB)
    check_pin("legal", LEGAL, LEGAL_BLOB)
    state_path = os.path.join(WORK, "state.json")
    state = {}
    if os.path.exists(state_path):
        state = json.load(open(state_path, encoding="utf-8"))

    manifest, plan = build_plan()
    MANIFEST_CACHE = manifest
    all_bits = [b["bit"] for b in json.load(open(plan))["bits"]]
    bitsA = [b for b in all_bits if b <= 73]
    bitsB = [b for b in all_bits if b >= 76]
    assert len(bitsA) == 11 and len(bitsB) == 11

    make_fixb_variant(23)
    make_fixb_variant(24)

    def arm(tag, ms_shift, bits, max_old, seed_path=""):
        if tag in state and isinstance(state[tag], dict) and \
                state[tag].get("total_nodes"):
            return state[tag]
        s, _ = run_worker(tag, ms_shift, plan, bits, max_old,
                          seed_path=seed_path)
        if s is None:
            s = wait_worker(tag)
        ok, mds = verify_snapshots(tag, bits)
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

    # ---- arm0: fixB band ms23 single-process reference ----
    band23 = arm("band23", 23, all_bits, "400")

    # ---- arm1/2: fixB workers ----
    wA = arm("workerA", 23, bitsA, "350")
    wB = arm("workerB", 23, bitsB, "350")

    # ---- arm3: distinct + merge (live bounds) ----
    if "distinctA" not in state:
        state["distinctA"] = distinct_pass("workerA")
        state["distinctB"] = distinct_pass("workerB")
        json.dump(state, open(state_path, "w"))
    dA, dB = state["distinctA"], state["distinctB"]
    if "merge" not in state:
        m = merge_pass("workerA", "workerB")
        m["seed_md5"] = hashlib.md5(
            open(m["seed_path"], "rb").read()).hexdigest()
        m2 = merge_pass("workerA", "workerB")
        m2md5 = hashlib.md5(
            open(m2["seed_path"], "rb").read()).hexdigest()
        m["merge_deterministic"] = (m2md5 == m["seed_md5"])
        state["merge"] = m
        json.dump(state, open(state_path, "w"))
    m = state["merge"]
    seed_path = m["seed_path"]

    # ---- arm4: fixB seedrun ms24 with merged seed ----
    seedrun = arm("seedrun", 24, all_bits, "500", seed_path=seed_path)

    # ---- arm5: fixB band ms24 unseeded reference ----
    band24 = arm("band24", 24, all_bits, "500")

    # ---- arm6: sim prediction on the merged seed ----
    if "sim_ms24" not in state:
        sim_out = os.path.join(WORK, "sim_ms24.json")
        proc = subprocess.run([NODE, SIM, seed_path, "24", "", sim_out],
                              capture_output=True, text=True, check=True)
        state["sim_ms24"] = json.loads(open(sim_out, encoding="utf-8").read())
        json.dump(state, open(state_path, "w"))
    sim = state["sim_ms24"]

    # ---- arm8: design-point seedrun at MS=1<<25 (K0909 seed capacity
    #      design rule: the 5.48M-key fixB merged seed sits above the
    #      MS=1<<24 knee, so the design point is MS=1<<25, load ~0.16;
    #      dumpMemo carries the published 32MiB-fsync strengthening so
    #      the ms25 full-table dump survives the cgroup page-cache cap) ----
    make_fixb_variant(25)
    seedrun25 = arm("seedrun25", 25, all_bits, "220", seed_path=seed_path)
    if "sim_ms25" not in state:
        sim_out = os.path.join(WORK, "sim_ms25.json")
        proc = subprocess.run([NODE, SIM, seed_path, "25", "", sim_out],
                              capture_output=True, text=True, check=True)
        state["sim_ms25"] = json.loads(open(sim_out, encoding="utf-8").read())
        json.dump(state, open(state_path, "w"))
    sim25 = state["sim_ms25"]
    if "record_identity25" not in state:
        state["record_identity25"] = record_identity_pass("seedrun25",
                                                          seed_path)
        json.dump(state, open(state_path, "w"))
    ri25 = state["record_identity25"]

    # ---- record identity + band-vs-merged comparison ----
    if "record_identity" not in state:
        state["record_identity"] = record_identity_pass("seedrun", seed_path)
        json.dump(state, open(state_path, "w"))
    ri = state["record_identity"]
    if "band_vs_merged" not in state:
        if "distinct_band23" not in state:
            state["distinct_band23"] = distinct_pass("band23")
            json.dump(state, open(state_path, "w"))
        state["band_vs_merged"] = band_vs_merged_pass("band23", seed_path)
        json.dump(state, open(state_path, "w"))
    bvm = state["band_vs_merged"]

    # ---- gates ----
    band23_pb = {p["bit"]: p["nodes_this_run"] for p in band23["per_bit"]}
    wA_pb = {p["bit"]: p["nodes_this_run"] for p in wA["per_bit"]}
    totA, totB = wA["total_nodes"], wB["total_nodes"]
    gates = {
        "band23_fixb_byte_identical": band23["byte_identical"] == 22,
        "workerA_byte_identical": wA["byte_identical"] == 11,
        "workerB_byte_identical": wB["byte_identical"] == 11,
        "seedrun_byte_identical": seedrun["byte_identical"] == 22,
        "band24_fixb_byte_identical": band24["byte_identical"] == 22,
        "workerA_per_bit_equals_band23_prefix":
            all(wA_pb[b] == band23_pb[b] for b in bitsA),
        "workerA_bit0_equals_fixb_battery":
            wA_pb[0] == FIXB_BATTERY_PER_BIT_NODES[0],
        "no_duplicate_keys_workerA":
            dA["dup_keys"] == 0 and dA["max_copies"] == 1,
        "no_duplicate_keys_workerB":
            dB["dup_keys"] == 0 and dB["max_copies"] == 1,
        "internal_conflicts_zero":
            not dA["conflicts"] and not dB["conflicts"],
        "cross_conflicts_zero": not m["cross_conflicts"],
        "merge_deterministic": m["merge_deterministic"],
        "seed_failed_equals_sim_prediction":
            (seedrun["seed"] or {}).get("failed") == sim["failed"],
        "record_identity_no_violations": ri["value_violations"] == 0,
        "record_identity_missing_equals_seed_failed":
            ri["missing"] == (seedrun["seed"] or {}).get("failed"),
        "seed_failure_rate_below_0.1pct":
            ((seedrun["seed"] or {}).get("failed", 0) /
             max(1, (seedrun["seed"] or {}).get("seeded", 1))) < 0.001,
        "band_vs_merged_shared_no_conflicts":
            not bvm["shared_value_conflicts"],
        "workers_total_sanity":
            (totA + totB) <= band23["total_nodes"] * 1.05,
        # ---- design point MS=1<<25 (K0909 seed capacity design rule) ----
        "seedrun25_byte_identical": seedrun25["byte_identical"] == 22,
        "seed25_failed_equals_sim25_prediction":
            (seedrun25["seed"] or {}).get("failed") == sim25["failed"],
        "record_identity25_no_violations":
            ri25["value_violations"] == 0,
        "record_identity25_missing_equals_seed25_failed":
            ri25["missing"] == (seedrun25["seed"] or {}).get("failed"),
        "seed25_failure_rate_below_0.1pct":
            ((seedrun25["seed"] or {}).get("failed", 0) /
             max(1, (seedrun25["seed"] or {}).get("seeded", 1))) < 0.001,
    }
    design_gates_ms25 = {
        "seedrun25_byte_identical": gates["seedrun25_byte_identical"],
        "seed25_failed_equals_sim25_prediction":
            gates["seed25_failed_equals_sim25_prediction"],
        "record_identity25_no_violations":
            gates["record_identity25_no_violations"],
        "record_identity25_missing_equals_seed25_failed":
            gates["record_identity25_missing_equals_seed25_failed"],
        "seed25_failure_rate_below_0.1pct":
            gates["seed25_failure_rate_below_0.1pct"],
    }

    workers_total = totA + totB
    doc = {
        "schema": "n11-class2-lane-fixb-worker-split-memo-merge-73k-20261117-v1",
        "date": "2026-11-17",
        "lane": "n11 class2-lane long-term (cost73k)",
        "purpose": ("fixB (K0907 both memo bugs fixed) worker-split memo "
                    "merge measurement in the K0909 2-way configuration: "
                    "fixB band ms23/ms24 references, 73/76 worker split, "
                    "KYOENWM1 dumps, live-bound distinct+merge, merged "
                    "KYOENWM2 seed, ms24 seedrun with sim cross-check"),
        "inputs": {
            "extractor_blob": EXTRACTOR_BLOB,
            "manifest_blob": MANIFEST_BLOB,
            "legal_blob": LEGAL_BLOB,
            "engine_variant": ("verbatim + MS substitution + Int32Array "
                               "memo keys + sentinel-aware nowin/nolose "
                               "updates (fixB, K0907) + dump/seed export "
                               "block; line-level changes asserted"),
            "worker_ms": 23, "seedrun_ms": 24, "band24_ms": 24,
            "bitsA": bitsA, "bitsB": bitsB,
        },
        "band23_fixb": band23,
        "workerA_fixb": wA,
        "workerB_fixb": wB,
        "workers_total_nodes": workers_total,
        "vs_band23_fixb": workers_total / band23["total_nodes"],
        "vs_verbatim_two_way_workers":
            workers_total / VERBATIM_REFS["two_way_workers_total"],
        "vs_fixb_fresh_battery":
            workers_total / VERBATIM_REFS["fixb_fresh_battery_total"],
        "distinct_pass": {"workerA": dA, "workerB": dB,
                          "band23": state.get("distinct_band23")},
        "merge": {k: v for k, v in m.items() if k != "seed_path"},
        "vs_verbatim_two_way_merged_occupied":
            m["occupied_after"] /
            VERBATIM_REFS["two_way_merged_occupied_after"],
        "seedrun_fixb": seedrun,
        "band24_fixb": band24,
        "sim_ms24": {k: v for k, v in sim.items() if k != "seed_path"},
        "seedrun25_fixb": seedrun25,
        "sim_ms25": {k: v for k, v in sim25.items() if k != "seed_path"},
        "record_identity25": ri25,
        "design_point_ms25": {
            "note": ("K0909 design rule applied to the 5.48M-key fixB "
                     "merged seed: MS=1<<24 sits above the published knee "
                     "(S~4.1-4.2M keys for the 0.1% gate) and the measured "
                     "0.44% failure rate matches the sim prediction "
                     "exactly; the design point MS=1<<25 (initial load "
                     "~0.16) is measured and gated separately"),
            "gates": design_gates_ms25,
            "gates_all_pass": all(design_gates_ms25.values()),
            "seedrun25_vs_seedrun24_nodes":
                seedrun25["total_nodes"] / seedrun["total_nodes"],
            "seed_failed_ms24_vs_ms25":
                [(seedrun["seed"] or {}).get("failed"),
                 (seedrun25["seed"] or {}).get("failed")],
        },
        "seed_benefit": {
            "seedrun_vs_band24_fixb":
                seedrun["total_nodes"] / band24["total_nodes"],
            "seedrun_vs_band23_fixb":
                seedrun["total_nodes"] / band23["total_nodes"],
            "seedrun_vs_fixb_fresh_battery":
                seedrun["total_nodes"] /
                VERBATIM_REFS["fixb_fresh_battery_total"],
            "seedrun_vs_verbatim_two_way_seedrun":
                seedrun["total_nodes"] /
                VERBATIM_REFS["two_way_seedrun_ms24_total"],
            "seedrun25_vs_band24_fixb":
                seedrun25["total_nodes"] / band24["total_nodes"],
            "seedrun25_vs_fixb_fresh_battery":
                seedrun25["total_nodes"] /
                VERBATIM_REFS["fixb_fresh_battery_total"],
        },
        "record_identity": ri,
        "band_vs_merged": bvm,
        "verbatim_refs": VERBATIM_REFS,
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


if __name__ == "__main__":
    sys.exit(main())
