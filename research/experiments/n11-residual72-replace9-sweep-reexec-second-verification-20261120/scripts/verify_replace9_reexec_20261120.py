#!/usr/bin/env python3
"""n11 residual-23 replace-9 depth-10 sweep: full probe re-execution second
verification (2026-11-20).

Single-owner undertaking per
research/log/2026-11-20-n11-residual72-replace9-d10-sweep-reexec-second-verification-single-owner-note.md
(commit 3f340466218bb47a08d1f7421947ff720bc52b85). This machine re-executes
EVERY published depth-10 probe record of the K1146 replace-9 sweep
(18 probes = 9 roots x 2 AND orderings) with the repo-pinned runner v17 in
two passes (A in this tree, B in an isolated cwd/HOME tree) and compares the
deterministic fields (nodes, loss, capped, terminalStoneRange) with the
published probe-records JSONL and the published sweep volume JSON:

  - K1146 replace9-d10-sweep record JSON sha256 e8f5d674...
  - K1146 probe-records-replace9.jsonl sha256 bdacf0e7...
    (computed from the publication commit e9ea153bc4...)

Independent re-derivations inside this machine (fail-closed):
  - pinned-input loading by SHA-256 (6 upstream record JSONs + the K1146
    volume + the K1146 probe-records JSONL)
  - runner v17 pinned by git blob SHA-1
  - probe plan re-derivation from the published records and, independently,
    from the pinned K1097 scope1 greedy_selection (roots, gained_rows,
    covered_rows, sweep_idx), with the raw child designation rule
    (child = root minus lowest set bit) re-derived per record
  - probe plan completeness (18 records, both AND orderings per root,
    depth 10, cap 30,000,000, timeout 280s, pilot_d6 control in every
    published record, runner blob + k1097 input sha in every record)
  - published internal consistency: probe-record JSONL values == volume
    per_root values for every probe
  - published classification pins (WIN8-D10 candidate 1 root /
    REFUTED-D10 8 roots / nodes total 3,574,172 / capped 0 / error 0)
  - residual-49/40/30/23 universe re-derivation from
    K1085+K1086+K1089+K1091+K1095 (NOT from K1097 or K1095 conclusions),
    with the K1097 bookkeeping crosscheck kept as a separate gate
  - replacement-plan geometry re-derivation (popcount 8, quadruple-free by
    exact 4x4 Bareiss determinants, D4 min-canonical, 23-row exactly-once
    coverage, claims are D4 orientations and stone subsets, gains hist
    {3:6,2:2,1:1})
  - fresh classification (win/refuted root sets, nodes totals) re-derived
    from the fresh pass results and compared with the published
    classification
  - pristine re-assembly check: the published sweep machine
    replace9_d10_sweep_20261120.py (sha256 d163b2a1...) re-assembled in an
    isolated tree on the published probe records must reproduce the
    published volume JSON byte-identically

This is a re-execution verification of published probe facts only:
NO row closure, NO receipt fold, NO certificate extraction, NO new probe
beyond re-running the published ones, NO verdict beyond depth 10, and NO
win/loss interpretation beyond the runner's depth-bounded probe semantics.
REFUTED-D10 is not a LOSS proof. node counts are not win/loss evidence.
The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}
and classes 1/2/4 all remain UNKNOWN.

Usage:
  verify_replace9_reexec_20261120.py run [budget_s] [--pass NAME] [--root DIR]
      [--workers N] [--k1085 PATH] [--k1086 PATH] [--k1089 PATH]
      [--k1091 PATH] [--k1095 PATH] [--k1097 PATH] [--records PATH]
      [--volume PATH]
  verify_replace9_reexec_20261120.py assemble [--pass-a DIR] [--pass-b DIR]
      [--k1085 PATH] [--k1086 PATH] [--k1089 PATH] [--k1091 PATH]
      [--k1095 PATH] [--k1097 PATH] [--records PATH] [--volume PATH]
      [--pristine PATH] [--out PATH]
"""
import hashlib
import itertools
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent
RUNNER = EXP / "runner_v17.ts"
OUTD = EXP / "output"
OUTPUT = OUTD / "replace9-sweep-reexec-second-verification-20261120.json"
SCHEMA = "n11-residual72-replace9-sweep-reexec-second-verification-20261120-v1"

CAP = 30_000_000
TIMEOUT = 280
RUNNER_BLOB_PIN = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
PILOT_D6_NODES = 3402
K1085_SHA256 = "5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e"
K1086_SHA256 = "3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced"
K1089_SHA256 = "808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc"
K1091_SHA256 = "edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25"
K1095_SHA256 = "335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707"
K1097_SHA256 = "2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40"
SWEEP_VOLUME_SHA256 = ("e8f5d6749032c4ad95136d2915c03ce7e997fe494b"
                       "f3eebf7f912cccc88ded1e")
SWEEP_RECORDS_SHA256 = ("bdacf0e7056093145bef917ad384220b70c06be68bdd892b56dd2"
                        "3b3a7d4cb06")
SWEEP_MACHINE_SHA256 = ("d163b2a120ac46abee40d0b9a32269bce14a73901a85a80e59"
                        "5b7d2512bcd41")

# published classification pins (from the published volume JSON)
PIN_WIN_ROOTS = ["00000000010000809002000040002001"]
PIN_REFUTED_ROOTS = [
    "00000000000000083800040048100000",
    "00000000000000143800000209000000",
    "00000000000000821082000000001018",
    "00000000000000821086800000000800",
    "00000000000040809002000800100200",
    "00000000000000103800000008080041",
    "00000000020000801202000800100001",
    "00000010000000801202000000000448",
]
PIN_PROBES = 18
PIN_ROOTS = 9
PIN_NODES_TOTAL = 3_574_172
PIN_TERMINAL_UNION = [14, 18]

# -------------------------------------------------------------------
# exact integer geometry (written independently for this verification)
# -------------------------------------------------------------------
N = 121


def cells_of(hexstr):
    v = int(hexstr, 16)
    return [i for i in range(N) if (v >> i) & 1]


def hex_of(cs):
    v = 0
    for c in cs:
        v |= 1 << c
    return f"{v:032x}"


def popcount_hex(hexstr):
    return bin(int(hexstr, 16)).count("1")


def _rot90(cell):
    x, y = cell % 11, cell // 11
    return (10 - x) * 11 + y


def _mirror(cell):
    x, y = cell % 11, cell // 11
    return y * 11 + (10 - x)


def d4_images(cs):
    """All 8 D4 images of a cell set, identity first, as sorted cell lists."""
    first = sorted(cs)
    out = [first]
    cur = first
    for _ in range(3):
        cur = sorted(_rot90(c) for c in cur)
        out.append(cur)
    cur = sorted(_mirror(c) for c in first)
    out.append(cur)
    for _ in range(3):
        cur = sorted(_rot90(c) for c in cur)
        out.append(cur)
    return out


def _det4_int(m):
    """Exact determinant of a 4x4 integer matrix by fraction-free
    (Bareiss) elimination; zero rows / zero pivots handled with swaps."""
    a = [row[:] for row in m]
    sign = 1
    prev = 1
    for k in range(3):
        if a[k][k] == 0:
            for i in range(k + 1, 4):
                if a[i][k] != 0:
                    a[k], a[i] = a[i], a[k]
                    sign = -sign
                    break
            else:
                return 0
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) // prev
            a[i][k] = 0
        prev = a[k][k]
    return sign * a[3][3]


def _four_on_one_conic_or_line(quad):
    pts = [(c % 11, c // 11) for c in quad]
    m = [[x * x + y * y, x, y, 1] for (x, y) in pts]
    return _det4_int(m) == 0


def quad_free(hexstr):
    cs = cells_of(hexstr)
    for comb in itertools.combinations(cs, 4):
        if _four_on_one_conic_or_line(comb):
            return False
    return True


# -------------------------------------------------------------------
# pinned inputs
# -------------------------------------------------------------------
def find_pinned(explicit, env, fallback):
    cands = []
    if explicit:
        cands.append(Path(explicit))
    if env and os.environ.get(env):
        cands.append(Path(os.environ[env]))
    cands.append(OUTD / fallback)
    for c in cands:
        if c.is_file():
            return c
    raise SystemExit(f"pinned input not found: {fallback} (pass an explicit path)")


def load_pinned(path, sha, label):
    raw = Path(path).read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got != sha:
        raise SystemExit(f"{label} sha256 pin FAIL: {got} != {sha}")
    return json.loads(raw.decode("utf-8")), got


def load_paths(args):
    def opt(flag):
        return args[args.index(flag) + 1] if flag in args else None
    return {
        "k1085": opt("--k1085") or os.environ.get("K1085_JSON"),
        "k1086": opt("--k1086") or os.environ.get("K1086_JSON"),
        "k1089": opt("--k1089") or os.environ.get("K1089_JSON"),
        "k1091": opt("--k1091") or os.environ.get("K1091_JSON"),
        "k1095": opt("--k1095") or os.environ.get("K1095_JSON"),
        "k1097": opt("--k1097") or os.environ.get("K1097_JSON"),
        "records": opt("--records") or os.environ.get("SWEEP_RECORDS_JSONL"),
        "volume": opt("--volume") or os.environ.get("SWEEP_VOLUME_JSON"),
    }


def load_all(paths):
    out = {}
    out["k1085"], out["sha_k1085"] = load_pinned(
        find_pinned(paths["k1085"], None, ".input-k1085.json"),
        K1085_SHA256, "K1085")
    out["k1086"], out["sha_k1086"] = load_pinned(
        find_pinned(paths["k1086"], None, ".input-k1086.json"),
        K1086_SHA256, "K1086")
    out["k1089"], out["sha_k1089"] = load_pinned(
        find_pinned(paths["k1089"], None, ".input-k1089.json"),
        K1089_SHA256, "K1089")
    out["k1091"], out["sha_k1091"] = load_pinned(
        find_pinned(paths["k1091"], None, ".input-k1091.json"),
        K1091_SHA256, "K1091")
    out["k1095"], out["sha_k1095"] = load_pinned(
        find_pinned(paths["k1095"], None, ".input-k1095.json"),
        K1095_SHA256, "K1095")
    out["k1097"], out["sha_k1097"] = load_pinned(
        find_pinned(paths["k1097"], None, ".input-k1097.json"),
        K1097_SHA256, "K1097")
    rec_path = find_pinned(paths["records"], None, "probe-records-replace9.jsonl")
    raw = Path(rec_path).read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got != SWEEP_RECORDS_SHA256:
        raise SystemExit(f"published probe-records jsonl sha256 pin FAIL: {got}")
    out["records"] = [json.loads(l) for l in raw.decode("utf-8").splitlines()
                      if l.strip()]
    out["volume"], out["sha_volume"] = load_pinned(
        find_pinned(paths["volume"], None, "replace9-d10-sweep-20261120.json"),
        SWEEP_VOLUME_SHA256, "K1146 volume")
    return out


def runner_blob(raw=None):
    raw = raw if raw is not None else RUNNER.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()


# -------------------------------------------------------------------
# plan re-derivation
# -------------------------------------------------------------------
def selection_of(k1097):
    sel = k1097["scope1_refsolve_residual23"]["greedy_selection"]
    if len(sel) != PIN_ROOTS:
        raise SystemExit(f"K1097 scope1 greedy_selection has {len(sel)} roots")
    return sel


def plan_from_selection(sel):
    plan = []
    for idx, t in enumerate(sel):
        root = t["root"]
        rv = int(root, 16)
        bit = (rv & -rv).bit_length() - 1
        child = f"{rv & ~(1 << bit):032x}"
        for ordering, order in (("andclose1", 1), ("andclose0", 0)):
            plan.append({
                "root": root, "idx": idx, "child": child, "bit": bit,
                "ordering": ordering, "order_n": order,
                "gained_rows": t["gained_rows"],
                "covered_rows": t["covered_rows"],
            })
    return plan


def cross_records_plan(records, plan):
    """fail-closed consistency: published records == plan re-derived from K1097."""
    if len(records) != PIN_PROBES:
        raise SystemExit(f"records count {len(records)} != {PIN_PROBES}")
    problems = []
    by_key = {}
    for r in records:
        key = (r["root"], r["ordering"])
        if key in by_key:
            problems.append({"key": key, "why": "duplicate"})
        by_key[key] = r
        if r.get("depth") != 10:
            problems.append({"key": key, "why": "depth"})
        if r.get("cap") != CAP or r.get("timeout_s") != TIMEOUT:
            problems.append({"key": key, "why": "cap/timeout"})
        if r.get("runner_blob") != RUNNER_BLOB_PIN:
            problems.append({"key": key, "why": "runner_blob"})
        if r.get("k1097_input_sha256") != K1097_SHA256:
            problems.append({"key": key, "why": "k1097_input_sha256"})
        rv = int(r["root"], 16)
        bit = (rv & -rv).bit_length() - 1
        if r.get("bit") != bit or int(r["child"], 16) != (rv & ~(1 << bit)):
            problems.append({"key": key, "why": "child-designation"})
        if popcount_hex(r["root"]) != 8 or popcount_hex(r["child"]) != 7:
            problems.append({"key": key, "why": "popcount"})
        c = r.get("control") or {}
        if (c.get("nodes") != PILOT_D6_NODES or c.get("loss") is not False
                or c.get("capped") is not False):
            problems.append({"key": key, "why": "pilot-control"})
    for p in plan:
        key = (p["root"], p["ordering"])
        r = by_key.get(key)
        if r is None:
            problems.append({"key": key, "why": "missing"})
            continue
        if (r.get("sweep_idx") != p["idx"] or r.get("gained_rows") != p["gained_rows"]
                or r.get("bit") != p["bit"] or r["child"] != p["child"]):
            problems.append({"key": key, "why": "plan-field"})
    return problems


def records_expect(records):
    exp = {}
    for r in records:
        res = r["result"]
        exp[(r["root"], r["ordering"])] = {
            "nodes": res["nodes"], "loss": res["loss"],
            "capped": res["capped"],
            "terminalStoneRange": res["terminalStoneRange"],
        }
    return exp


# -------------------------------------------------------------------
# run (fresh re-execution pass, resume-safe)
# -------------------------------------------------------------------
_RECORD_LOCK = threading.Lock()
_JOB_LOCK = threading.Lock()


def run_one_probe(p, rec_dir):
    rec_path = Path(rec_dir) / f".tmp-probe-{p['root']}-{p['order_n']}.jsonl"
    if rec_path.exists():
        rec_path.unlink()
    cmd = ["node", "--experimental-strip-types", str(RUNNER),
           "--bits", str(p["bit"]), "--depth", "10", "--cap", str(CAP),
           "--andclose", str(p["order_n"]), "--child", p["child"],
           "--out", str(rec_path)]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=TIMEOUT, cwd=str(RUNNER.parent))
        rc, stderr = r.returncode, r.stderr.strip()[-300:]
    except subprocess.TimeoutExpired:
        rc, stderr = "timeout", ""
    wall = round(time.time() - t0, 1)
    control = result = None
    if rec_path.exists():
        for line in rec_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                obj = json.loads(line)
                if obj.get("control"):
                    control = obj
                else:
                    result = obj
        rec_path.unlink()
    rec = {"root": p["root"], "ordering": p["ordering"], "depth": 10,
           "bit": p["bit"], "child": p["child"], "cap": CAP,
           "timeout_s": TIMEOUT, "wall_s": wall,
           "runner_blob": RUNNER_BLOB_PIN}
    if rc == "timeout":
        rec["error"] = f"timeout-{TIMEOUT}s"
        rec["control"] = control
    elif rc != 0:
        rec["error"] = f"exit-{rc}"
        rec["stderr_tail"] = stderr
    elif result is None:
        rec["error"] = "missing-result"
        rec["stderr_tail"] = stderr
    else:
        rec["control"] = control
        rec["result"] = result
    return rec


def cmd_run(argv):
    budget = 240.0
    workers = 4
    pass_name = os.environ.get("REEXEC_PASS", "A")
    root_dir = OUTD
    args = list(argv)
    i = 0
    while i < len(args):
        if args[i] == "--pass" and i + 1 < len(args):
            pass_name = args[i + 1]; i += 2; continue
        if args[i] == "--root" and i + 1 < len(args):
            root_dir = Path(args[i + 1]); i += 2; continue
        if args[i] == "--workers" and i + 1 < len(args):
            workers = max(1, min(4, int(args[i + 1]))); i += 2; continue
        try:
            budget = float(args[i])
        except ValueError:
            pass
        i += 1
    root_dir = Path(root_dir)
    root_dir.mkdir(parents=True, exist_ok=True)
    records_path = root_dir / f"probe-records-reexec-pass{pass_name}.jsonl"
    data = load_all(load_paths(args))
    if runner_blob() != RUNNER_BLOB_PIN:
        raise SystemExit("runner blob pin FAIL before probing")
    plan = plan_from_selection(selection_of(data["k1097"]))
    bad = cross_records_plan(data["records"], plan)
    if bad:
        raise SystemExit(f"published records vs plan cross-check FAIL: {bad[:3]}")
    done = set()
    if records_path.exists():
        for line in records_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                done.add((rec["root"], rec["ordering"]))
    todo = [p for p in plan if (p["root"], p["ordering"]) not in done]
    if not todo:
        print("ALL PROBES DONE", flush=True)
        return 0
    print(f"pass {pass_name}: {len(done)} done, {len(todo)} todo", flush=True)
    t_start = time.time()
    stats = {"ran": 0, "err": 0}
    jobs = list(todo)
    job_i = [0]

    def worker():
        while True:
            if time.time() - t_start > budget:
                return
            with _JOB_LOCK:
                if job_i[0] >= len(jobs):
                    return
                p = jobs[job_i[0]]
                job_i[0] += 1
            stats["ran"] += 1
            rec = run_one_probe(p, root_dir)
            with _RECORD_LOCK:
                with records_path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, sort_keys=True) + "\n")
                    f.flush()
            res = rec.get("result") or {}
            if rec.get("error"):
                stats["err"] += 1
            print(f"[pass{pass_name} {stats['ran']}/{len(jobs)}] "
                  f"{rec.get('error', 'ok')} {p['root'][:10]} {p['ordering']} "
                  f"nodes={res.get('nodes')} loss={res.get('loss')} "
                  f"capped={res.get('capped')} wall={rec['wall_s']}s", flush=True)

    threads = [threading.Thread(target=worker) for _ in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=budget + TIMEOUT + 30)
    print(f"pass {pass_name} budget {budget}s "
          f"elapsed={round(time.time() - t_start, 1)}s ran={stats['ran']} "
          f"err={stats['err']} remaining={len(jobs) - stats['ran']}", flush=True)
    return 0


# -------------------------------------------------------------------
# assemble (fail-closed gates + canonical audit JSON)
# -------------------------------------------------------------------
def gate(gates, name, ok, detail):
    gates.append({"name": name, "pass": bool(ok), "detail": detail})


def gate_resid_partition(gates, name, prior_set, win_roots, ref_roots,
                         doc, n_win, n_ref, n_win_rows, n_ref_rows, label_rows):
    claims_w, claims_r, unknown = [], [], []
    for root, info in doc["per_root"].items():
        if root not in win_roots and root not in ref_roots:
            continue
        tgt = claims_w if root in win_roots else claims_r
        for row_hex in info["covered_rows"]:
            canon = _canon_of(row_hex)
            if canon is None:
                unknown.append({"root": root, "row": row_hex})
            else:
                tgt.append(canon)
    detail = {
        "win_roots": len(win_roots), "refuted_roots": len(ref_roots),
        "win_claimed_rows": len(claims_w), "refuted_claimed_rows": len(claims_r),
        "unknown_claim_rows": unknown,
        "partition": {
            "win_claims_distinct": len(claims_w) == len(set(claims_w)),
            "refuted_claims_distinct": len(claims_r) == len(set(claims_r)),
            "disjoint": not (set(claims_w) & set(claims_r)),
            "union_is_prior_universe": (set(claims_w) | set(claims_r)) == prior_set,
            "refuted_claims_subset_of_prior": set(claims_r) <= prior_set,
        },
    }
    ok = (len(win_roots) == n_win and len(ref_roots) == n_ref
          and len(claims_w) == n_win_rows and len(claims_r) == n_ref_rows
          and not unknown
          and detail["partition"]["win_claims_distinct"]
          and detail["partition"]["refuted_claims_distinct"]
          and detail["partition"]["disjoint"]
          and detail["partition"]["union_is_prior_universe"])
    gate(gates, name, ok, detail)
    return set(claims_r)


# canonicalization table (populated by assemble before partition gates)
_CANON = {}


def _canon_of(row_hex):
    return _CANON.get(row_hex)


def build_canon_table(rows):
    _CANON.clear()
    for r in rows:
        for im in d4_images(cells_of(r)):
            _CANON[hex_of(im)] = r


def fresh_index(records_path):
    idx = {}
    for line in Path(records_path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            idx[(rec["root"], rec["ordering"])] = rec
    return idx


def cmp_fresh(plan, exp, fresh, tag, gates):
    mism = []
    got = 0
    nodes_sum = 0
    cap_err = 0
    loss_by_root = {}
    recs_by_root = {}
    for p in plan:
        key = (p["root"], p["ordering"])
        e = exp[key]
        rec = fresh.get(key)
        if rec is None:
            mism.append({"root": p["root"], "ordering": p["ordering"],
                         "why": "missing"})
            continue
        if rec.get("error"):
            cap_err += 1
            mism.append({"root": p["root"], "ordering": p["ordering"],
                         "why": rec["error"]})
            continue
        c = rec.get("control") or {}
        if (c.get("nodes") != PILOT_D6_NODES or c.get("loss") is not False
                or c.get("capped") is not False):
            cap_err += 1
            mism.append({"root": p["root"], "ordering": p["ordering"],
                         "why": "pilot-control"})
            continue
        r = rec["result"]
        if not all([r["nodes"] == e["nodes"], r["loss"] == e["loss"],
                    r["capped"] == e["capped"],
                    r["terminalStoneRange"] == e["terminalStoneRange"]]):
            mism.append({"root": p["root"], "ordering": p["ordering"],
                         "why": "value-mismatch",
                         "fresh": {k: r[k] for k in
                                   ("nodes", "loss", "capped",
                                    "terminalStoneRange")},
                         "published": e})
            continue
        got += 1
        nodes_sum += r["nodes"]
        loss_by_root.setdefault(p["root"], []).append(r["loss"])
        recs_by_root.setdefault(p["root"], []).append(r)
    conflicts = sorted(root for root, ls in loss_by_root.items()
                       if len(ls) == 2 and ls[0] != ls[1])
    win_roots = set()
    refuted_roots = set()
    for root, rrecs in recs_by_root.items():
        if len(rrecs) != 2:
            continue
        losses = [x["loss"] for x in rrecs]
        cappeds = [x["capped"] for x in rrecs]
        if any(l is True and c is False for l, c in zip(losses, cappeds)):
            win_roots.add(root)
        elif any(l is False and c is False for l, c in zip(losses, cappeds)):
            refuted_roots.add(root)
    stats = {
        "probes_compared_ok": got,
        "nodes_sum": nodes_sum,
        "cap_or_error_probes": cap_err,
        "ordering_conflicts": conflicts,
        "win_roots": sorted(win_roots),
        "refuted_roots": sorted(refuted_roots),
    }
    ok = (not mism and got == PIN_PROBES and nodes_sum == PIN_NODES_TOTAL
          and cap_err == 0 and not conflicts
          and sorted(win_roots) == sorted(PIN_WIN_ROOTS)
          and sorted(refuted_roots) == sorted(PIN_REFUTED_ROOTS))
    detail = dict(stats)
    if mism:
        detail["mismatch_count"] = len(mism)
        detail["mismatches"] = mism[:10]
    gate(gates, f"{tag}-fresh-vs-published-all-fields", ok, detail)
    return stats


def cmd_assemble(argv):
    args = list(argv)

    def opt(flag):
        return args[args.index(flag) + 1] if flag in args else None
    pass_a = Path(opt("--pass-a") or OUTD)
    pass_b = Path(opt("--pass-b")) if "--pass-b" in args else None
    pristine = Path(opt("--pristine")) if "--pristine" in args else None
    out_path = Path(opt("--out") or OUTPUT)
    data = load_all(load_paths(args))
    gates = []
    gate(gates, "runner-blob-pin", runner_blob() == RUNNER_BLOB_PIN,
         {"git_blob": runner_blob()})
    gate(gates, "k1085-sha-pin", data["sha_k1085"] == K1085_SHA256,
         {"sha256": data["sha_k1085"]})
    gate(gates, "k1086-sha-pin", data["sha_k1086"] == K1086_SHA256,
         {"sha256": data["sha_k1086"]})
    gate(gates, "k1089-sha-pin", data["sha_k1089"] == K1089_SHA256,
         {"sha256": data["sha_k1089"]})
    gate(gates, "k1091-sha-pin", data["sha_k1091"] == K1091_SHA256,
         {"sha256": data["sha_k1091"]})
    gate(gates, "k1095-sha-pin", data["sha_k1095"] == K1095_SHA256,
         {"sha256": data["sha_k1095"]})
    gate(gates, "k1097-sha-pin", data["sha_k1097"] == K1097_SHA256,
         {"sha256": data["sha_k1097"]})
    gate(gates, "sweep-volume-pin", data["sha_volume"] == SWEEP_VOLUME_SHA256,
         {"sha256": data["sha_volume"]})

    k1097 = data["k1097"]
    sel = selection_of(k1097)
    plan = plan_from_selection(sel)
    gate(gates, "probe-plan-rederivation-vs-published-records",
         not cross_records_plan(data["records"], plan),
         {"records": PIN_PROBES, "roots": PIN_ROOTS,
          "rule": "child = root minus lowest set bit; both AND orderings "
                  "per root; depth 10; cap 30M; timeout 280s; runner blob "
                  "and k1097 input sha stamped in every published record"})

    # published internal consistency: JSONL vs volume per_root
    volume = data["volume"]
    per_probes = {}
    for root, info in volume["per_root"].items():
        for ordering, ent in info["probes"].items():
            per_probes[(root, ordering)] = ent
    exp = records_expect(data["records"])
    bad_int = []
    for (root, ordering), e in exp.items():
        v = per_probes.get((root, ordering))
        if v is None:
            bad_int.append({"root": root, "ordering": ordering,
                            "why": "not-in-volume-per-root"})
            continue
        if (v["nodes"] != e["nodes"] or v["loss"] != e["loss"]
                or v["capped"] != e["capped"]
                or list(v["terminalStoneRange"]) != list(e["terminalStoneRange"])):
            bad_int.append({"root": root, "ordering": ordering,
                            "why": "value-mismatch",
                            "volume": v, "jsonl": e})
    sel_map = {t["root"]: t for t in sel}
    vol_map = {root: info for root, info in volume["per_root"].items()}
    for root in sel_map:
        v = vol_map.get(root)
        t = sel_map[root]
        if v is None:
            bad_int.append({"root": root, "why": "root-missing-in-volume"})
        elif (v["covered_rows"] != t["covered_rows"]
              or v["gained_rows"] != t["gained_rows"]):
            bad_int.append({"root": root, "why": "plan-coverage-mismatch"})
    gate(gates, "published-internal-consistency-jsonl-vs-volume-per-root",
         not bad_int, {"bad": bad_int[:5], "count": len(bad_int)})

    cls = volume["classification"]
    win_vol = sorted(w["root"] for w in cls["win8_d10_candidates"])
    ref_vol = sorted(r["root"] for r in cls["refuted_d10_facts"])
    ok_cls = (win_vol == sorted(PIN_WIN_ROOTS)
              and ref_vol == sorted(PIN_REFUTED_ROOTS)
              and cls["nodes_total"] == PIN_NODES_TOTAL
              and cls["capped_probes"] == 0 and cls["error_probes"] == 0
              and cls["unresolved"] == []
              and list(cls["terminalStoneRange_union"]) == PIN_TERMINAL_UNION
              and cls["win8_d10_candidates"][0]["gained_rows"] == 3
              and len(cls["win8_d10_candidates"][0]["covered_rows"]) == 3
              and sorted(cls["win8_d10_candidates"][0]["covered_rows"]) == sorted(
                  vol_map[PIN_WIN_ROOTS[0]]["covered_rows"]))
    lo = min(e["terminalStoneRange"][0] for e in exp.values())
    hi = max(e["terminalStoneRange"][1] for e in exp.values())
    ok_cls = ok_cls and [lo, hi] == PIN_TERMINAL_UNION
    gate(gates, "published-classification-pins", ok_cls,
         {"win_roots": win_vol, "refuted_roots": ref_vol,
          "nodes_total": cls["nodes_total"],
          "terminalStoneRange_union_from_records": [lo, hi],
          "gained_hist": {str(t["gained_rows"]):
                          sum(1 for u in sel if u["gained_rows"] == t["gained_rows"])
                          for t in sel}})

    # residual universe chain re-derivation (independent of K1097/K1095
    # conclusions), written for this verification from the published inputs
    build_canon_table(data["k1085"]["base_state"]["residual_row_hex"])
    rows72 = list(data["k1085"]["base_state"]["residual_row_hex"])
    if not (len(rows72) == data["k1085"]["base_state"]["residual_rows"] == 72):
        raise SystemExit("k1085 base_state residual rows sanity FAIL")
    resid49 = gate_resid_partition(
        gates, "residual49-rederived-from-k1085-k1086",
        set(rows72),
        {w["root"] for w in data["k1086"]["classification"]["win8_d10_candidates"]},
        {r["root"] for r in data["k1086"]["classification"]["refuted_d10_facts"]},
        data["k1086"], 7, 16, 23, 49, None)
    resid40 = gate_resid_partition(
        gates, "residual40-rederived-k1085-k1086-k1089", resid49,
        {w["root"] for w in data["k1089"]["classification"]["win8_d10_candidates"]},
        {r["root"] for r in data["k1089"]["classification"]["refuted_d10_facts"]},
        data["k1089"], 3, 13, 9, 40, None)
    resid30 = gate_resid_partition(
        gates, "residual30-rederived-k1085-k1086-k1089-k1091", resid40,
        {w["root"] for w in data["k1091"]["classification"]["win8_d10_candidates"]},
        {r["root"] for r in data["k1091"]["classification"]["refuted_d10_facts"]},
        data["k1091"], 3, 12, 10, 30, None)
    resid23 = gate_resid_partition(
        gates, "residual23-rederived-k1085-k1086-k1089-k1091-k1095", resid30,
        {w["root"] for w in data["k1095"]["classification"]["win8_d10_candidates"]},
        {r["root"] for r in data["k1095"]["classification"]["refuted_d10_facts"]},
        data["k1095"], 3, 9, 7, 23, None)
    k1097_rows = {r["row"] for r in k1097["per_row_residual23"]}
    s1 = [t["root"] for t in sel]
    s2 = [t["root"] for t in
          k1097["scope2_refsolve_need_new_providers"]["greedy_selection"]]
    gate(gates, "residual23-consistency-with-k1097-bookkeeping",
         k1097_rows == resid23 and s1 == s2 and len(resid23) == 23,
         {"k1097_per_row_residual23_rows": len(k1097_rows),
          "equal": k1097_rows == resid23,
          "k1097_scope1_scope2_same_selection": s1 == s2,
          "note": "the re-derivation above does not use K1097 for the "
                  "universe; this gate is a crosscheck only"})

    # replacement-plan geometry re-derivation
    geom_ok = True
    qf_roots = 0
    canon_roots = 0
    for t in sel:
        root = t["root"]
        geom_ok = geom_ok and popcount_hex(root) == 8
        geom_ok = geom_ok and quad_free(root)
        if quad_free(root):
            qf_roots += 1
        orb = [hex_of(im) for im in d4_images(cells_of(root))]
        if root == min(orb):
            canon_roots += 1
        geom_ok = geom_ok and root == min(orb)
    gate(gates, "replace9-plan-geometry-basic",
         geom_ok and qf_roots == PIN_ROOTS and canon_roots == PIN_ROOTS,
         {"popcount8_all": geom_ok, "quad_free_roots": qf_roots,
          "d4_min_canonical_roots": canon_roots})
    pair_ok = 0
    pair_bad = []
    cover_map = {}
    for t in sel:
        root = t["root"]
        for row_hex in t["covered_rows"]:
            canon = _canon_of(row_hex)
            sub = any((int(row_hex, 16) | int(hex_of(im), 16)) == int(hex_of(im), 16)
                      for im in d4_images(cells_of(root)))
            sub_rev = any((int(hex_of(im), 16) | int(root, 16)) == int(root, 16)
                          for im in d4_images(cells_of(row_hex)))
            if (canon is not None and canon in resid23 and (sub or sub_rev)
                    and canon not in cover_map):
                pair_ok += 1
                cover_map[canon] = root
            else:
                pair_bad.append({"root": root, "row": row_hex,
                                 "canon": canon,
                                 "in_resid23": canon in resid23 if canon else None,
                                 "sub": sub, "sub_rev": sub_rev,
                                 "dup": cover_map.get(canon) if canon else None})
    gate(gates, "replace9-claims-geometry-rederived",
         pair_ok == 23 and not pair_bad and len(t["covered_rows"]) == t["gained_rows"],
         {"pairs_ok": pair_ok, "bad": pair_bad[:5],
          "gains_equals_len_all": all(u["gained_rows"] == len(u["covered_rows"])
                                      for u in sel)})
    gate(gates, "coverage-23-exactly-once",
         set(cover_map) == resid23 and len(cover_map) == 23,
         {"covered_union": len(cover_map),
          "matches_rederived_residual23": set(cover_map) == resid23})
    gains_hist = {}
    for t in sel:
        gains_hist[str(t["gained_rows"])] = gains_hist.get(
            str(t["gained_rows"]), 0) + 1
    s1obj = k1097["scope1_refsolve_residual23"]
    gate(gates, "replace9-gains-hist-and-k1097-plan-agreement",
         gains_hist == {"3": 6, "2": 2, "1": 1}
         and s1obj["greedy_size"] == 9 and s1obj["leftover_rows"] == []
         and s1obj["stranded_rows"] == [] and s1obj["max_matching"] == 23
         and s1obj["gains_hist"] == {"1": 1, "2": 2, "3": 6},
         {"observed_hist": gains_hist,
          "k1097_scope1_greedy_size": s1obj["greedy_size"],
          "k1097_scope1_leftover": s1obj["leftover_rows"],
          "k1097_scope1_stranded": s1obj["stranded_rows"],
          "k1097_scope1_max_matching": s1obj["max_matching"],
          "k1097_scope1_gains_hist": s1obj["gains_hist"]})

    # fresh passes vs published
    rec_a = fresh_index(Path(pass_a) / "probe-records-reexec-passA.jsonl")
    stats_a = cmp_fresh(plan, exp, rec_a, "passA", gates)
    stats_b = None
    if pass_b is not None:
        rec_b = fresh_index(Path(pass_b) / "probe-records-reexec-passB.jsonl")
        stats_b = cmp_fresh(plan, exp, rec_b, "passB", gates)
        bad_ab = []
        for p in plan:
            key = (p["root"], p["ordering"])
            ra, rb = rec_a.get(key), rec_b.get(key)
            if ra is None or rb is None or ra.get("error") or rb.get("error"):
                bad_ab.append({"root": p["root"], "ordering": p["ordering"],
                               "why": "missing-or-error"})
                continue
            xa, xb = ra["result"], rb["result"]
            keys = ("nodes", "loss", "capped", "terminalStoneRange")
            if not all(xa[k] == xb[k] for k in keys):
                bad_ab.append({"root": p["root"], "ordering": p["ordering"],
                               "why": "value-mismatch",
                               "passA": {k: xa[k] for k in keys},
                               "passB": {k: xb[k] for k in keys}})
        gate(gates, "passA-vs-passB-deterministic-fields",
             not bad_ab, {"bad": bad_ab[:5], "count": len(bad_ab)})

    # pristine re-assembly check
    if pristine is not None:
        praw = pristine.read_bytes()
        psha = hashlib.sha256(praw).hexdigest()
        gate(gates, "pristine-reassemble-volume-byte-identical",
             psha == SWEEP_VOLUME_SHA256,
             {"pristine_output_sha256": psha,
              "published_volume_sha256": SWEEP_VOLUME_SHA256,
              "note": "published sweep machine replace9_d10_sweep_20261120.py "
                      "(machine sha256 d163b2a1...) re-assembled in an "
                      "isolated tree on the published probe records"})
    else:
        gate(gates, "pristine-reassemble-volume-byte-identical", False,
             {"why": "pristine output not provided to assemble"})

    total_fresh_nodes = stats_a["nodes_sum"]
    doc_out = {
        "schema": SCHEMA,
        "date": "2026-11-20",
        "cap": CAP,
        "timeout_s": TIMEOUT,
        "runner_git_blob": RUNNER_BLOB_PIN,
        "inputs": {
            "k1085_sha256": K1085_SHA256,
            "k1086_sha256": K1086_SHA256,
            "k1089_sha256": K1089_SHA256,
            "k1091_sha256": K1091_SHA256,
            "k1095_sha256": K1095_SHA256,
            "k1097_sha256": K1097_SHA256,
            "k1146_volume_sha256": SWEEP_VOLUME_SHA256,
            "k1146_probe_records_jsonl_sha256": SWEEP_RECORDS_SHA256,
            "k1146_sweep_machine_sha256": SWEEP_MACHINE_SHA256,
        },
        "single_owner_note": ("research/log/2026-11-20-n11-residual72-replace9-"
                              "d10-sweep-reexec-second-verification-single-owner-"
                              "note.md (commit 3f340466218bb47a08d1f7421947ff720bc52b85)"),
        "protocol": ("full re-execution second verification of the published "
                     "K1146 replace-9 sweep probe facts; runner v17 pinned by "
                     "git blob; depth 10; cap 30M; timeout 280s; both AND "
                     "orderings; pilot_d6 control required on every probe; "
                     "the raw child hex rule (child = root minus lowest set "
                     "bit) is re-derived per record and is bookkeeping only "
                     "(the engine receives the identical cell set); "
                     "deterministic comparison fields are nodes/loss/capped/"
                     "terminalStoneRange; ms/wall timings are excluded; "
                     "passA runs in this tree, passB in an isolated "
                     "cwd/HOME tree; the residual-23 universe and the "
                     "replacement-plan geometry are re-derived by this "
                     "machine from the pinned upstream inputs"),
        "targets": {
            "probes_total": PIN_PROBES,
            "replacement_roots": PIN_ROOTS,
            "published_nodes_total": PIN_NODES_TOTAL,
            "fresh_nodes_total_passA": total_fresh_nodes,
            "pass_b_included": stats_b is not None,
        },
        "passA_reexec_stats": stats_a,
        **({"passB_reexec_stats": stats_b} if stats_b is not None else {}),
        "gates": gates,
        "interpretation_guard": [
            "This verification re-executes published probe facts with the "
            "pinned engine and compares deterministic fields; it verifies "
            "NO win/loss claim beyond the runner's depth-bounded probe "
            "semantics.",
            "loss=true (uncapped) marks a WIN8-within-depth-10 candidate for "
            "that 8-stone root only; its certificate extraction is a separate "
            "declared undertaking and row closure semantics require the "
            "published extraction, triple-verification and receipt fold "
            "machines.",
            "loss=false (uncapped) is a REFUTED-D10 probe fact: it is NOT a "
            "LOSS proof of any earlier position and only erodes the "
            "replacement pool (safe8 120,474 - 58 = 120,416 roots).",
            "No row is closed by this verification; the residual-23 rows all "
            "remain open.",
            "Node counts and solved counts are not win/loss readings.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
            "S2 {59,60} and classes 1/2/4 all remain UNKNOWN.",
        ],
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(doc_out, indent=1, sort_keys=True) + "\n",
                        encoding="utf-8")
    sha = hashlib.sha256(out_path.read_bytes()).hexdigest()
    hard = [g for g in gates if not g["pass"]]
    print(f"gates: {len(gates) - len(hard)}/{len(gates)} pass")
    for g in hard:
        print("GATE FAIL:", g["name"], json.dumps(g["detail"])[:500])
    print("passA fresh nodes total:", total_fresh_nodes,
          "== published:", total_fresh_nodes == PIN_NODES_TOTAL)
    if stats_b is not None:
        print("passB fresh nodes total:", stats_b["nodes_sum"],
              "== published:", stats_b["nodes_sum"] == PIN_NODES_TOTAL)
    print("output sha256:", sha)
    return 1 if hard else 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    rest = sys.argv[2:]
    sys.exit(cmd_run(rest) if mode == "run" else
             cmd_assemble(rest) if mode == "assemble" else 2)
