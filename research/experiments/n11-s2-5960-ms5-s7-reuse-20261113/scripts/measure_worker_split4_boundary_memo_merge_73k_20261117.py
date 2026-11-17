#!/usr/bin/env python3
"""Boundary-respecting 4-worker split memo merge measurement for the
cost-73k lane (2026-11-17, n11 class2-lane long-term lane; K0909 N=4
extension; splits at the same 39/41, 73/76, 97/98 bit boundaries as the
published 2-way split, so the merged table is directly comparable to the
published 2-way seed).

MEASUREMENT ONLY (no certificate publication, no verdict changes).

Purpose (lane priority 3: safe worker-cache merge with immediate WIN/LOSS
conflict detection; priority 5: parallelization efficiency).  The published
K0909 measurement (commit f9e3acf8) split the published cost-73k WIN7-D10
band (22 roots, manifest blob 0892aed0...) into TWO workers at the 73/76
gap.  This measurement extends the split to FOUR workers:

  W0: bits 0,7,11,15,35,39    (6 bits, fresh process; prefix of worker A)
  W1: bits 41,44,58,62,73     (5 bits, fresh process)
  W2: bits 76,87,89,94,95,97  (6 bits, fresh process; prefix of worker B)
  W3: bits 98,103,105,112,117 (5 bits, fresh process)

and additionally REPRODUCES the published 2-worker split exactly
(workerA = bits 0..73, workerB = bits 76..117, verbatim engine, MS=1<<23,
band-wide memo carried within each worker, KYOENWM1 full-table dumps).

Offline merge (sort-based, streaming, no sqlite), all rules identical to
the published K0909 pipeline:
  1. per-worker dump externally sorted by key, stream-deduplicated
     (win=min lose=min nowin=max nolose=max), internal conflicts counted;
  2. all SIX pairwise merges among W0..W3 counted (shared keys, cross
     conflicts);
  3. cascade: M01 = merge(W0,W1), M23 = merge(W2,W3),
     FINAL4 = merge(M01,M23) - the 4-way merged seed table;
  4. 2-way reproduction check: merge(workerA,workerB) must reproduce the
     published merged-seed file BYTE-IDENTICALLY
     (md5 e7c2c17e7a91d8ea17f433f3bb482f29);
  5. subset/monotonicity check of FINAL4 vs the reproduced 2-way seed:
     every 2-way key must be present in FINAL4 (only_in_2way == 0) with
     equal-or-stronger combined values (win<=, lose<=, nowin>=, nolose>=
     under the published 255-sentinel comparison rules).

Seedrun: the verbatim engine at MS=1<<24 seeds its memo from FINAL4
(insertion in file order through the engine's own memoEntry(), verbatim
probe semantics), then extracts all 22 bits band-wide in one process.
Gates: 22/22 certificates byte-identical, seed insert failure rate
< 0.1%, record-identity check of the seedrun's final dump against FINAL4
(every seeded-and-inserted key present with equal-or-stronger values).

Regression gates (all from the published K0909 output JSON and the
published band ms23 per-bit table; the engine is deterministic, so a
fresh re-run must reproduce them):
  - workerA: per-bit nodes == published band ms23 per-bit values for bits
    0..73, total 48,482,011, final occupied 5,263,320, per-bit occupancy
    == published workerA occupancy series;
  - workerB: per-bit nodes/occupancy == published workerB values, total
    71,480,136, final occupied 6,242,804;
  - W0: per-bit nodes/occupancy == workerA's first six bits, total
    27,424,708, final occupied 3,705,871;
  - W2: per-bit nodes/occupancy == workerB's first six bits, total
    36,575,507, final occupied 4,869,649;
  - merged 2-way seed byte-identical to the published md5;
  - internal and cross conflicts == 0 everywhere;
  - 22/22 worker certificate snapshots byte-identical (W0+W1+W2+W3).

Interpretation guard: measurement only.  No new WIN/LOSS verdicts, no
manifest row opened or closed, certificate bytes unchanged.  The verbatim
extractor is NOT modified in the repo (published determinism chains); the
patched variants exist only in the work directory.  WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone roots only;
REFUTED-D10 is not a LOSS proof.  The 11x11 empty board, both two-stone
roots {49,60} and {59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN.

Usage: python3 measure_worker_split4_boundary_memo_merge_73k_20261117.py <out.json> <workdir>
       (env: KYOEN_NODE=node; every step resumes from <workdir>/)
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) or "."
CERTDIR = os.path.join(HERE, "class2-lane-cost73k-certificates")
NODE = os.environ.get("KYOEN_NODE", "node")

EXTRACTOR = os.path.join(HERE, "class4_child1_cert_extractor_exact.ts")
DRIVER = os.path.join(HERE, "measure_worker_split_memo_73k.ts")
LEGAL = os.path.join(HERE, "legal_candidates.py")
MANIFEST = os.path.join(
    CERTDIR, "class2-lane-cost73k-win7-certificates-20261117.json")

EXTRACTOR_BLOB = "52bcaf509ea12fad4c936501d30d26b5b66c0085"
DRIVER_BLOB = "2a95d9527afa3c1a24685b697c822f451aae58a5"
LEGAL_BLOB = "8e97082c42838c7a4a4b6d2dd235276c8d43ab9a"
MANIFEST_BLOB = "0892aed07d187ae2fb3b4b90a21c7adbc1002b62"

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
# class2-lane-band-memo-extraction-measurement-73k-20261117.json, blob ce625db0;
# identical to the dict in the published K0909 orchestrator)
BAND23_PER_BIT = {
    0: 4303203, 7: 5039319, 11: 2910849, 15: 8159953, 35: 5045405,
    39: 1965979, 41: 1768864, 44: 4669878, 58: 4866570, 62: 2241220,
    73: 7510771, 76: 4815817, 87: 8054680, 89: 4928329, 94: 5625212,
    95: 11857737, 97: 4429190, 98: 6073176, 103: 7107709, 105: 4356101,
    112: 6167016, 117: 9289681}
BAND23_TOTAL = 121186659
FRESH23_TOTAL = 108499241

# published K0909 constants (output worker-split-memo-merge-73k-20261117.json,
# commit f9e3acf8)
PUB = {
    "workerA_total": 48482011,
    "workerA_occ": 5263320,
    "workerA_nodes": [4303203, 5039319, 2910849, 8159953, 5045405,
                      1965979, 1768864, 4669878, 4866570, 2241220, 7510771],
    "workerA_occ_series": [710449, 1469800, 1882289, 2897951, 3473099,
                           3705871, 3816312, 4351136, 4733550, 4840253,
                           5263320],
    "workerB_total": 71480136,
    "workerB_occ": 6242804,
    "workerB_nodes": [4098489, 6656639, 4263829, 5108954, 11857737,
                      4589859, 6634071, 7351258, 4500217, 6410841, 10008242],
    "workerB_occ_series": [680933, 1698603, 2370024, 2984708, 4530953,
                           4869649, 5215260, 5555651, 5800305, 6012746,
                           6242804],
    "workers2_total": 119962147,
    "merged2_occupied_after": 4291899,
    "merged2_shared": 882089,
    "merged2_seed_md5": "e7c2c17e7a91d8ea17f433f3bb482f29",
    "seedrun2_total": 85747496,
    "seedrun2_final_occupied": 10614912,
    "seedrun2_seed": {"seeded": 4291899, "inserted": 4290451, "failed": 1448},
    "seedrun2_record_identity": {"present": 4290451, "missing": 1448,
                                  "value_violations": 0},
}

BITS_W0 = [0, 7, 11, 15, 35, 39]
BITS_W1 = [41, 44, 58, 62, 73]
BITS_W2 = [76, 87, 89, 94, 95, 97]
BITS_W3 = [98, 103, 105, 112, 117]
BITS_WA = BITS_W0 + BITS_W1           # published 2-way worker A
BITS_WB = BITS_W2 + BITS_W3           # published 2-way worker B
ALL_BITS = BITS_WA + BITS_WB
assert sorted(ALL_BITS) == ALL_BITS and len(ALL_BITS) == 22

PROGRESS = os.environ.get(
    "WM4_PROGRESS",
    "/home/user/knowledge/kyouen-research/_scratch/wm4-progress.md")


def progress(line):
    with open(PROGRESS, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


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


def make_variant(ms_shift):
    """Verbatim engine + MS substitution + dump/seed export block.
    No key-sign or negative-bound fixes: the workers and the seedrun run
    the verbatim memo semantics (published determinism)."""
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
            "from './class4_child1_cert_extractor_exact_wm_ms%d.ts'"
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
                     "published_rows": c["rows"],
                     "split": c.get("split_cut_byte") is not None})
    order = sorted(bits, key=lambda b: b["bit"])
    plan_path = os.path.join(WORK, "plan73k.json")
    with open(plan_path, "w", encoding="utf-8") as fh:
        json.dump({"child": child, "bits": order}, fh)
    return manifest, plan_path


def run_worker(tag, ms_shift, plan, bits, max_old, seed_path=""):
    """Launch one worker (or seedrun) via nohup background; resume from
    a saved summary when present."""
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
        if tag in cmd and "measure_worker_split" in cmd and \
                "measure_worker_split4_memo" not in cmd:
            return True
    return False


def wait_worker(tag, timeout_s=1800):
    import time
    summary = os.path.join(WORK, tag + ".summary.json")
    log = os.path.join(WORK, tag + ".runlog.txt")
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


def published_cert_bytes(bit):
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    c = [x for x in manifest["certificates"] if x["bit"] == bit][0]
    fn = c["file"]
    if c.get("split_cut_byte") is not None:
        return (open(os.path.join(CERTDIR, fn + ".part1of2"), "rb").read() +
                open(os.path.join(CERTDIR, fn + ".part2of2"), "rb").read())
    return open(os.path.join(CERTDIR, fn), "rb").read()


def verify_snapshots(tag, bits):
    ok = 0
    mds = {}
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    for bit in bits:
        c = [x for x in manifest["certificates"] if x["bit"] == bit][0]
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
    if not os.path.exists(srt):
        env = dict(os.environ, LC_ALL="C")
        with open(dump, "rb") as fi, open(srt, "wb") as fo:
            subprocess.run(["sort", "-S", "200M", "-k2,5"], stdin=fi,
                           stdout=fo, env=env, check=True)
    return srt


def combine_values(win, lose, nowin, nolose, rec):
    w = min(win, rec[0]); l = min(lose, rec[1])
    nw = max(nowin, rec[2]); nl = max(nolose, rec[3])
    return w, l, nw, nl


def conflict_kind(win, lose, nowin, nolose):
    if win < 255 and lose < 255:
        return "win_and_lose"
    if win < 255 and nowin < 255 and nowin >= win:
        return "win_le_nowin"
    if lose < 255 and nolose < 255 and nolose >= lose:
        return "lose_le_nolose"
    return None


def distinct_pass(tag):
    """Sorted dump -> distinct key table with combined values."""
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


def merge_join(inA, inB, out_path, header_line):
    """Merge-join two key-sorted distinct tables; returns stats.
    header_line: string WITHOUT trailing newline, or None for no header."""
    da = open(inA, encoding="utf-8")
    db = open(inB, encoding="utf-8")
    shared = 0
    conflicts = {}
    occupied_after = 0
    with open(out_path, "w", encoding="utf-8") as fo:
        if header_line is not None:
            fo.write(header_line + "\n")
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
            "conflict_samples": {k: v[:3] for k, v in conflicts.items()}}


SEED2_HEADER = ("KYOENWM2 merged worker_memo_tables cost73k "
                "A=workerA B=workerB "
                "combine=win_min_lose_min_nowin_max_nolose_max")
SEED4_HEADER = ("KYOENWM2 merged worker_memo_tables cost73k "
                "A=m01 B=m23 "
                "combine=win_min_lose_min_nowin_max_nolose_max")


def compare_final4_vs_seed2(seed4_path, seed2_path):
    """Stream both key-sorted seed tables (each with a header line):
    every 2-way key must be present in FINAL4 with equal-or-stronger
    values (published record-identity comparison rules)."""
    only4 = 0
    only2 = 0
    shared = 0
    viol = []
    with open(seed4_path, encoding="utf-8") as f4, \
            open(seed2_path, encoding="utf-8") as f2:
        f4.readline()  # header
        f2.readline()  # header
        r4 = f4.readline()
        r2 = f2.readline()
        while r4 or r2:
            k4 = r4.split()[:4] if r4 else None
            k2 = r2.split()[:4] if r2 else None
            if k2 and (not k4 or k2 < k4):
                only2 += 1
                r2 = f2.readline()
            elif k4 and (not k2 or k4 < k2):
                only4 += 1
                r4 = f4.readline()
            else:
                f4d = r4.split()
                f2d = r2.split()
                w4, l4 = int(f4d[4]), int(f4d[5])
                nw4, nl4 = int(f4d[6]), int(f4d[7])
                w2, l2 = int(f2d[4]), int(f2d[5])
                nw2, nl2 = int(f2d[6]), int(f2d[7])
                okw = w2 == 255 or w4 <= w2
                okl = l2 == 255 or l4 <= l2
                oknw = nw2 == 255 or nw4 >= nw2
                oknl = nl2 == 255 or nl4 >= nl2
                if not (okw and okl and oknw and oknl):
                    viol.append(" ".join(k2))
                shared += 1
                r4 = f4.readline()
                r2 = f2.readline()
    return {"shared": shared, "only_in_final4": only4,
            "only_in_seed2": only2,
            "value_violations": len(viol),
            "violation_samples": viol[:3]}


def record_identity_pass(seedrun_tag, seed_path):
    """Published record-identity gate: distinct-combine the seedrun's
    final dump and check every seeded record: present with equal-or-
    stronger values."""
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
                oknw = nowin == 255 or fnw >= nowin
                oknl = nolose == 255 or fnl >= nolose
                if not (okw and okl and oknw and oknl):
                    viol.append(" ".join(ks))
                present += 1
                rs = fs_.readline()
                rf = ff.readline()
    return {"present": present, "missing": missing,
            "value_violations": len(viol),
            "violation_samples": viol[:3], "seedrun_dump_stats": stats}


def strip_ms(per_bit):
    out = []
    for p in per_bit:
        q = dict(p)
        q.pop("ms", None)
        out.append(q)
    return out


WORK = "."
RUNTAG = "[run]"


def main():
    global WORK
    out_path = sys.argv[1] if len(sys.argv) > 1 else "wm4.json"
    WORK = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        HERE, "worker_split4_work")
    global RUNTAG
    RUNTAG = "[" + os.path.basename(out_path).replace(".json", "") + "]"
    os.makedirs(WORK, exist_ok=True)
    state_path = os.path.join(WORK, "state.json")
    state = json.load(open(state_path, encoding="utf-8")) if \
        os.path.exists(state_path) else {}

    for name, path, exp in [
            ("extractor", EXTRACTOR, EXTRACTOR_BLOB),
            ("driver", DRIVER, DRIVER_BLOB),
            ("legal", LEGAL, LEGAL_BLOB),
            ("manifest", MANIFEST, MANIFEST_BLOB)]:
        check_pin(name, path, exp)

    manifest, plan = build_plan()
    child = json.load(open(plan, encoding="utf-8"))["child"]

    make_variant(23)
    make_variant(24)

    # ---- step 1: the six workers ----
    specs = [("workerA", BITS_WA, "350"), ("workerB", BITS_WB, "350"),
             ("w0", BITS_W0, "350"), ("w1", BITS_W1, "350"),
             ("w2", BITS_W2, "350"), ("w3", BITS_W3, "350")]
    sums = {}
    for tag, bits, old in specs:
        s, _ = run_worker(tag, 23, plan, bits, old)
        if s is None:
            s = wait_worker(tag)
        sums[tag] = s
        state[tag] = {"total_nodes": s["total_nodes"],
                      "final_memo_occupied": s["final_memo_occupied"],
                      "all_bits_ok": s["all_bits_ok"]}
        json.dump(state, open(state_path, "w"))
        ok, mds = verify_snapshots(tag, bits)
        state[tag]["byte_identical"] = ok
        json.dump(state, open(state_path, "w"))
        print("[worker] %s nodes %d occ %d bytes_ok %d/%d"
              % (tag, s["total_nodes"], s["final_memo_occupied"], ok,
                 len(bits)), flush=True)
        progress(RUNTAG + " worker %s: nodes %d occ %d bytes_ok %d/%d"
                 % (tag, s["total_nodes"], s["final_memo_occupied"], ok,
                    len(bits)))

    # per-bit nodes/occupancy series (ms stripped)
    def series(tag):
        pb = sorted(sums[tag]["per_bit"], key=lambda p: p["bit"])
        return [p["nodes_this_run"] for p in pb], \
               [p["memo_occupied_after"] for p in pb]

    wa_nodes, wa_occ = series("workerA")
    wb_nodes, wb_occ = series("workerB")
    w0_nodes, w0_occ = series("w0")
    w1_nodes, w1_occ = series("w1")
    w2_nodes, w2_occ = series("w2")
    w3_nodes, w3_occ = series("w3")

    # ---- step 2: distinct passes ----
    dist = {}
    for tag, _, _ in specs:
        dist[tag] = distinct_pass(tag)
        state["distinct_" + tag] = dist[tag]
        json.dump(state, open(state_path, "w"))
        print("[distinct] %s: %s" % (tag, dist[tag]["distinct"]), flush=True)
        progress(RUNTAG + " distinct %s: records %d distinct %d dup %d"
                 % (tag, dist[tag]["records"], dist[tag]["distinct"],
                    dist[tag]["dup_keys"]))

    # ---- step 3: 2-way reproduction merge (published md5 gate) ----
    dpath = lambda t: os.path.join(WORK, t + ".distinct.txt")
    seed2_path = os.path.join(WORK, "merged_seed_2way.kyoenwm2")
    m2 = merge_join(dpath("workerA"), dpath("workerB"), seed2_path,
                    SEED2_HEADER)
    m2["seed_md5"] = hashlib.md5(open(seed2_path, "rb").read()).hexdigest()
    merge_join(dpath("workerA"), dpath("workerB"),
               seed2_path + ".tmp", SEED2_HEADER)
    tmp_md5 = hashlib.md5(open(seed2_path + ".tmp", "rb").read()).hexdigest()
    m2["merge_deterministic"] = (tmp_md5 == m2["seed_md5"])
    os.remove(seed2_path + ".tmp")
    state["merge2"] = m2
    json.dump(state, open(state_path, "w"))
    progress(RUNTAG + " merge2: shared %d occ_after %d md5 %s det %s"
             % (m2["shared_distinct"], m2["occupied_after"],
                m2["seed_md5"], m2["merge_deterministic"]))

    # ---- step 4: six pairwise merges among w0..w3 ----
    pairwise = {}
    for i in range(4):
        for j in range(i + 1, 4):
            ti = "w%d" % i
            tj = "w%d" % j
            out = os.path.join(WORK, "pair_%s_%s.kyoenwm2m" % (ti, tj))
            st = merge_join(dpath(ti), dpath(tj), out, None)
            pairwise["%s_%s" % (ti, tj)] = st
            os.remove(out)
    state["pairwise"] = pairwise
    json.dump(state, open(state_path, "w"))
    progress(RUNTAG + " pairwise: " + json.dumps(
        {k: [v["shared_distinct"], v["occupied_after"],
             v["cross_conflicts"]] for k, v in pairwise.items()}))

    # ---- step 5: cascade merge to FINAL4 ----
    m01_path = os.path.join(WORK, "m01.kyoenwm2m")
    m23_path = os.path.join(WORK, "m23.kyoenwm2m")
    m01 = merge_join(dpath("w0"), dpath("w1"), m01_path, None)
    m23 = merge_join(dpath("w2"), dpath("w3"), m23_path, None)
    seed4_path = os.path.join(WORK, "merged_seed_4way.kyoenwm2")
    mf = merge_join(m01_path, m23_path, seed4_path, SEED4_HEADER)
    mf["seed_md5"] = hashlib.md5(open(seed4_path, "rb").read()).hexdigest()
    merge_join(m01_path, m23_path, seed4_path + ".tmp", SEED4_HEADER)
    tmp_md5 = hashlib.md5(open(seed4_path + ".tmp", "rb").read()).hexdigest()
    mf["merge_deterministic"] = (tmp_md5 == mf["seed_md5"])
    os.remove(seed4_path + ".tmp")
    state["merge_cascade"] = {"m01": m01, "m23": m23, "final": mf}
    json.dump(state, open(state_path, "w"))
    progress(RUNTAG + " cascade: m01 %d m23 %d final occ %d shared %d md5 %s"
             % (m01["occupied_after"], m23["occupied_after"],
                mf["occupied_after"], mf["shared_distinct"], mf["seed_md5"]))

    # ---- step 6: FINAL4 vs seed2 subset/monotonicity ----
    cmp42 = compare_final4_vs_seed2(seed4_path, seed2_path)
    state["final4_vs_seed2"] = cmp42
    json.dump(state, open(state_path, "w"))
    progress(RUNTAG + " final4_vs_seed2: shared %d only4 %d only2 %d viol %d"
             % (cmp42["shared"], cmp42["only_in_final4"],
                cmp42["only_in_seed2"], cmp42["value_violations"]))

    # ---- step 7: seedrun (FINAL4 seed, all 22 bits, ms24) ----
    sumS, _ = run_worker("seedrun", 24, plan, ALL_BITS, "700",
                         seed_path=seed4_path)
    if sumS is None:
        sumS = wait_worker("seedrun", timeout_s=3000)
    state["seedrun"] = {"total_nodes": sumS["total_nodes"],
                        "final_memo_occupied": sumS["final_memo_occupied"],
                        "seed": sumS.get("seed")}
    json.dump(state, open(state_path, "w"))
    okS, mdS = verify_snapshots("seedrun", ALL_BITS)
    progress(RUNTAG + " seedrun: nodes %d occ %d seed %s bytes_ok %d/22"
             % (sumS["total_nodes"], sumS["final_memo_occupied"],
                json.dumps(sumS.get("seed")), okS))

    # ---- step 8: record identity on the seedrun dump ----
    ri = record_identity_pass("seedrun", seed4_path)
    state["record_identity"] = ri
    json.dump(state, open(state_path, "w"))
    progress(RUNTAG + " record_identity: present %d missing %d viol %d"
             % (ri["present"], ri["missing"], ri["value_violations"]))

    # ---- gates ----
    workers4_total = (sums["w0"]["total_nodes"] + sums["w1"]["total_nodes"]
                      + sums["w2"]["total_nodes"] + sums["w3"]["total_nodes"])
    gates = {
        # published 2-way reproduction (pipeline correctness anchor)
        "repro_workerA_total":
            sums["workerA"]["total_nodes"] == PUB["workerA_total"],
        "repro_workerA_occ":
            sums["workerA"]["final_memo_occupied"] == PUB["workerA_occ"],
        "repro_workerA_per_bit_nodes":
            wa_nodes == PUB["workerA_nodes"],
        "repro_workerA_per_bit_occ":
            wa_occ == PUB["workerA_occ_series"],
        "repro_workerB_total":
            sums["workerB"]["total_nodes"] == PUB["workerB_total"],
        "repro_workerB_occ":
            sums["workerB"]["final_memo_occupied"] == PUB["workerB_occ"],
        "repro_workerB_per_bit_nodes":
            wb_nodes == PUB["workerB_nodes"],
        "repro_workerB_per_bit_occ":
            wb_occ == PUB["workerB_occ_series"],
        "repro_merged2_seed_md5":
            m2["seed_md5"] == PUB["merged2_seed_md5"],
        "repro_merged2_occupied_after":
            m2["occupied_after"] == PUB["merged2_occupied_after"],
        "repro_merged2_shared":
            m2["shared_distinct"] == PUB["merged2_shared"],
        "merge2_deterministic": m2["merge_deterministic"],
        # 4-way worker determinism anchors (prefix reproductions)
        "w0_per_bit_nodes": w0_nodes == PUB["workerA_nodes"][:6],
        "w0_per_bit_occ": w0_occ == PUB["workerA_occ_series"][:6],
        "w0_total": sums["w0"]["total_nodes"] == 27424708,
        "w0_final_occ": sums["w0"]["final_memo_occupied"] == 3705871,
        "w2_per_bit_nodes": w2_nodes == PUB["workerB_nodes"][:6],
        "w2_per_bit_occ": w2_occ == PUB["workerB_occ_series"][:6],
        "w2_total": sums["w2"]["total_nodes"] == 36575507,
        "w2_final_occ": sums["w2"]["final_memo_occupied"] == 4869649,
        # conflict detection (priority 3)
        "internal_conflicts_zero":
            all(not d["conflicts"] for d in dist.values()),
        "pairwise_cross_conflicts_zero":
            all(not st["cross_conflicts"] for st in pairwise.values()),
        "cascade_cross_conflicts_zero":
            (not m01["cross_conflicts"] and not m23["cross_conflicts"]
             and not mf["cross_conflicts"]),
        "merge4_deterministic": mf["merge_deterministic"],
        # FINAL4 superset of the reproduced 2-way seed with
        # equal-or-stronger values
        "final4_superset": cmp42["only_in_seed2"] == 0,
        "final4_monotone": cmp42["value_violations"] == 0,
        # byte-identity gates
        "worker_byte_identical_w0": state["w0"]["byte_identical"] == 6,
        "worker_byte_identical_w1": state["w1"]["byte_identical"] == 5,
        "worker_byte_identical_w2": state["w2"]["byte_identical"] == 6,
        "worker_byte_identical_w3": state["w3"]["byte_identical"] == 5,
        "repro_byte_identical_A": state["workerA"]["byte_identical"] == 11,
        "repro_byte_identical_B": state["workerB"]["byte_identical"] == 11,
        "seedrun_byte_identical": okS == 22,
        "seed_insert_failure_rate_below_0.1pct":
            ((sumS.get("seed") or {}).get("failed", 0) /
             max(1, (sumS.get("seed") or {}).get("seeded", 1))) < 0.001,
        "record_identity_no_violations": ri["value_violations"] == 0,
    }

    doc = {
        "schema": "n11-class2-lane-worker-split4-boundary-memo-merge-73k-20261117-v1",
        "date": "2026-11-17",
        "lane": "n11 class2-lane long-term (cost73k)",
        "purpose": ("4-worker split memo merge measurement (K0909 N=4 "
                    "extension): 4-way split of the cost-73k band, exact "
                    "2-way reproduction of the published K0909 merge, "
                    "six pairwise + cascaded 4-way merge with WIN/LOSS "
                    "conflict detection, merged-seed band run at "
                    "MS=1<<24"),
        "inputs": {
            "extractor_blob": EXTRACTOR_BLOB,
            "driver_blob": DRIVER_BLOB,
            "manifest_blob": MANIFEST_BLOB,
            "legal_blob": LEGAL_BLOB,
            "engine_variants": ("verbatim + MS line substitution + dump/seed "
                                "export block only; no key-sign or "
                                "negative-bound fixes"),
            "worker_ms": 23, "seedrun_ms": 24,
            "bits_w0": BITS_W0, "bits_w1": BITS_W1,
            "bits_w2": BITS_W2, "bits_w3": BITS_W3,
            "bits_workerA": BITS_WA, "bits_workerB": BITS_WB,
            "published_k0909_commit": "f9e3acf8",
        },
        "repro_2way": {
            "workerA": {"total_nodes": sums["workerA"]["total_nodes"],
                        "final_occupied":
                            sums["workerA"]["final_memo_occupied"],
                        "byte_identical":
                            state["workerA"]["byte_identical"],
                        "per_bit": strip_ms(sums["workerA"]["per_bit"])},
            "workerB": {"total_nodes": sums["workerB"]["total_nodes"],
                        "final_occupied":
                            sums["workerB"]["final_memo_occupied"],
                        "byte_identical":
                            state["workerB"]["byte_identical"],
                        "per_bit": strip_ms(sums["workerB"]["per_bit"])},
            "workers_total_nodes": (sums["workerA"]["total_nodes"]
                                    + sums["workerB"]["total_nodes"]),
            "vs_band23_total": (sums["workerA"]["total_nodes"]
                                + sums["workerB"]["total_nodes"])
                               / BAND23_TOTAL,
            "merge": {"shared_distinct": m2["shared_distinct"],
                      "occupied_after": m2["occupied_after"],
                      "cross_conflicts": m2["cross_conflicts"],
                      "seed_md5": m2["seed_md5"],
                      "published_seed_md5": PUB["merged2_seed_md5"],
                      "merge_deterministic": m2["merge_deterministic"]},
        },
        "workers_4way": {
            "w0": {"total_nodes": sums["w0"]["total_nodes"],
                   "final_occupied": sums["w0"]["final_memo_occupied"],
                   "byte_identical": state["w0"]["byte_identical"],
                   "per_bit": strip_ms(sums["w0"]["per_bit"])},
            "w1": {"total_nodes": sums["w1"]["total_nodes"],
                   "final_occupied": sums["w1"]["final_memo_occupied"],
                   "byte_identical": state["w1"]["byte_identical"],
                   "per_bit": strip_ms(sums["w1"]["per_bit"])},
            "w2": {"total_nodes": sums["w2"]["total_nodes"],
                   "final_occupied": sums["w2"]["final_memo_occupied"],
                   "byte_identical": state["w2"]["byte_identical"],
                   "per_bit": strip_ms(sums["w2"]["per_bit"])},
            "w3": {"total_nodes": sums["w3"]["total_nodes"],
                   "final_occupied": sums["w3"]["final_memo_occupied"],
                   "byte_identical": state["w3"]["byte_identical"],
                   "per_bit": strip_ms(sums["w3"]["per_bit"])},
            "workers4_total_nodes": workers4_total,
            "vs_published_workers2_total": workers4_total
                                            / PUB["workers2_total"],
            "vs_band23_total": workers4_total / BAND23_TOTAL,
        },
        "distinct_pass": {t: dist[t] for t in
                          ["w0", "w1", "w2", "w3"]},
        "pairwise_merges": pairwise,
        "cascade_merge": {
            "m01": {"shared_distinct": m01["shared_distinct"],
                    "occupied_after": m01["occupied_after"],
                    "cross_conflicts": m01["cross_conflicts"]},
            "m23": {"shared_distinct": m23["shared_distinct"],
                    "occupied_after": m23["occupied_after"],
                    "cross_conflicts": m23["cross_conflicts"]},
            "final": {"shared_distinct": mf["shared_distinct"],
                      "occupied_after": mf["occupied_after"],
                      "cross_conflicts": mf["cross_conflicts"],
                      "seed_md5": mf["seed_md5"],
                      "merge_deterministic": mf["merge_deterministic"]},
            "published_2way_occupied_after": PUB["merged2_occupied_after"],
        },
        "final4_vs_seed2": cmp42,
        "seedrun": {
            "total_nodes": sumS["total_nodes"],
            "final_occupied": sumS["final_memo_occupied"],
            "seed": sumS.get("seed"),
            "byte_identical": okS,
            "per_bit": strip_ms(sumS["per_bit"]),
            "load_factor_final": sumS["final_memo_occupied"] / (1 << 24),
            "published_seedrun2_total": PUB["seedrun2_total"],
            "ratio_vs_published_seedrun2":
                sumS["total_nodes"] / PUB["seedrun2_total"],
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
        print("  gate %-38s %s" % (k, v), flush=True)
    progress(RUNTAG + " GATES all_pass=%s | workers4_total=%d (2way %d, "
             "band23 %d) | final4 occ=%d (2way %d) | seedrun=%d (pub %d)"
             % (doc["gates_all_pass"], workers4_total,
                PUB["workers2_total"], BAND23_TOTAL, mf["occupied_after"],
                PUB["merged2_occupied_after"], sumS["total_nodes"],
                PUB["seedrun2_total"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
