#!/usr/bin/env python3
"""n11 residual-23 replace-9 depth-10 verdict sweep (2026-11-20).

Single-owner undertaking per
research/log/2026-11-20-n11-residual72-replace9-d10-sweep-single-owner-note.md
(commit 51bbb938809c36eafbf5a762f03bf729c097fe6f). Verdict probe facts only:
this machine records loss/nodes/capped/terminal-range per (root, ordering) for
the 9 round-4 replacement eight-stone roots of the pinned K1097 scope1 greedy
re-solve, at depth 10 with the repo-pinned runner v17. NO row closure, NO
receipt fold, NO certificate extraction, and NO loss/win interpretation beyond
the runner's depth-bounded probe semantics.

Independent re-derivation: the residual-49 row universe is re-derived inside
this machine from the pinned K1085 base state plus the pinned K1086 per-root
claimed coverage, the residual-40 universe is re-derived from those plus the
pinned K1089 per-root claimed coverage, the residual-30 universe is re-derived
from those plus the pinned K1091 per-root claimed coverage, and the residual-23
universe is re-derived from those plus the pinned K1095 per-root claimed
coverage (NOT taken from K1097 or K1095 conclusions), and the 9 replacement
roots' claimed coverage of those 23 rows is re-derived by exact integer
geometry (D4 images, Bareiss determinants) before any verdict is recorded.

REFUTED-D10 is not a LOSS proof. node counts are not win/loss evidence.
The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}
and classes 1/2/4 all remain UNKNOWN.

Usage:
  replace9_d10_sweep_20261120.py run [budget_s] [--k1085 PATH] [--k1086 PATH]
      [--k1089 PATH] [--k1091 PATH] [--k1095 PATH] [--k1097 PATH] [--workers N]
  replace9_d10_sweep_20261120.py assemble [--k1085 PATH] [--k1086 PATH]
      [--k1089 PATH] [--k1091 PATH] [--k1095 PATH] [--k1097 PATH]
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
RECORDS = OUTD / "probe-records-replace9.jsonl"
OUTPUT = OUTD / "replace9-d10-sweep-20261120.json"
SCHEMA = "n11-residual72-replace9-d10-sweep-20261120-v1"

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
DEPTHS = (10,)
ORDERINGS = (1, 0)

# ---------------------------------------------------------------------------
# exact integer geometry (independent of the runner engine)
# ---------------------------------------------------------------------------
N = 121

def cells(hexstr):
    v = int(hexstr, 16)
    return [i for i in range(N) if (v >> i) & 1]

def hexof(cs):
    v = 0
    for c in cs:
        v |= 1 << c
    return f"{v:032x}"

def popcount_hex(hexstr):
    return bin(int(hexstr, 16)).count("1")

def _rot(c):
    x, y = c % 11, c // 11
    return (10 - x) * 11 + y

def _flip(c):
    x, y = c % 11, c // 11
    return y * 11 + (10 - x)

def d4_images(cs):
    """All 8 D4 images of a cell set (identity first)."""
    out = [sorted(cs)]
    cur = sorted(cs)
    for _ in range(3):
        cur = sorted(_rot(c) for c in cur)
        out.append(cur)
    cur = sorted(_flip(c) for c in cs)
    out.append(cur)
    for _ in range(3):
        cur = sorted(_rot(c) for c in cur)
        out.append(cur)
    return out

def _det4(m):
    """Exact 4x4 determinant by Bareiss (integers stay small on 11x11)."""
    a = [row[:] for row in m]
    n = 4
    sign = 1
    prev = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            for i in range(k + 1, n):
                if a[i][k] != 0:
                    a[k], a[i] = a[i], a[k]
                    sign = -sign
                    break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) // prev
            a[i][k] = 0
        prev = a[k][k]
    return sign * a[n - 1][n - 1]

def _cyclic_or_linear(p):
    """4 cells concyclic-or-collinear iff the standard circle determinant is 0."""
    rows = []
    for (x, y) in p:
        rows.append([x * x + y * y, x, y, 1])
    return _det4(rows) == 0

def quad_free(cells_):
    """True iff no 4 stones of the position are concyclic or collinear."""
    for comb in itertools.combinations(cells_, 4):
        p = [(c % 11, c // 11) for c in comb]
        if _cyclic_or_linear(p):
            return False
    return True

# ---------------------------------------------------------------------------
# pinned inputs
# ---------------------------------------------------------------------------
def find_pinned(explicit=None, env=None, local=None):
    cands = []
    if explicit:
        cands.append(Path(explicit))
    if env and os.environ.get(env):
        cands.append(Path(os.environ[env]))
    cands.append(OUTD / local)
    for c in cands:
        if c.is_file():
            return c
    raise SystemExit(f"pinned input not found; pass explicit path for {local}")

def load_pinned(path, sha, label):
    data = path.read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if got != sha:
        raise SystemExit(f"{label} sha256 pin FAIL: {got}")
    return json.loads(data.decode("utf-8")), got

def load_k1085(explicit=None):
    p = find_pinned(explicit, "K1085_JSON", ".input-k1085.json")
    return load_pinned(p, K1085_SHA256, "K1085")

def load_k1086(explicit=None):
    p = find_pinned(explicit, "K1086_JSON", ".input-k1086.json")
    return load_pinned(p, K1086_SHA256, "K1086")

def load_k1089(explicit=None):
    p = find_pinned(explicit, "K1089_JSON", ".input-k1089.json")
    return load_pinned(p, K1089_SHA256, "K1089")


def load_k1091(explicit=None):
    p = find_pinned(explicit, "K1091_JSON", ".input-k1091.json")
    return load_pinned(p, K1091_SHA256, "K1091")


def load_k1095(explicit=None):
    p = find_pinned(explicit, "K1095_JSON", ".input-k1095.json")
    return load_pinned(p, K1095_SHA256, "K1095")


def load_k1097(explicit=None):
    p = find_pinned(explicit, "K1097_JSON", ".input-k1097.json")
    return load_pinned(p, K1097_SHA256, "K1097")

# ---------------------------------------------------------------------------
# probe plan (K1097 scope1 greedy_selection of 9 replacement roots)
# ---------------------------------------------------------------------------
def replacement_targets(k1097):
    sel = k1097["scope1_refsolve_residual23"]["greedy_selection"]
    assert len(sel) == 9, f"greedy_selection must be 9 roots, got {len(sel)}"
    return sel

def probe_plan(sel):
    out = []
    for idx, t in enumerate(sel):
        root = t["root"]
        rv = int(root, 16)
        bit = (rv & -rv).bit_length() - 1          # lowest set bit rule
        child = rv & ~(1 << bit)
        for depth in DEPTHS:
            for ordering in ORDERINGS:
                out.append({
                    "root": root, "idx": idx, "child": f"{child:032x}", "bit": bit,
                    "ordering": f"andclose{ordering}", "order_n": ordering, "depth": depth,
                    "gained_rows": t["gained_rows"],
                    "covered_rows": t["covered_rows"],
                })
    return out

def load_done():
    done = {}
    if RECORDS.exists():
        for line in RECORDS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                done[(rec["root"], rec["depth"], rec["ordering"])] = rec
    return done

def runner_blob(raw=None):
    raw = raw if raw is not None else RUNNER.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()

def run_one_probe(p, k_sha):
    rec_path = OUTD / f".tmp-{p['root']}-{p['depth']}-{p['order_n']}.jsonl"
    if rec_path.exists():
        rec_path.unlink()
    cmd = ["node", "--experimental-strip-types", str(RUNNER),
           "--bits", str(p["bit"]), "--depth", str(p["depth"]), "--cap", str(CAP),
           "--andclose", str(p["order_n"]), "--child", p["child"], "--out", str(rec_path)]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, cwd=EXP)
        rc, stderr = r.returncode, r.stderr.strip()
    except subprocess.TimeoutExpired as e:
        rc, stderr = "timeout", str(e.stderr or b"")[-300:]
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
    if rec_path.exists():
        rec_path.unlink()
    rec = {"root": p["root"], "depth": p["depth"], "ordering": p["ordering"],
           "bit": p["bit"], "child": p["child"], "cap": CAP, "timeout_s": TIMEOUT,
           "k1097_input_sha256": k_sha, "wall_s": wall, "runner_blob": RUNNER_BLOB_PIN,
           "sweep_idx": p["idx"], "gained_rows": p["gained_rows"]}
    if rc == "timeout":
        rec["error"] = f"timeout-{TIMEOUT}s"
        rec["control"] = control
    elif rc != 0:
        rec["error"] = f"exit-{rc}"
        rec["stderr_tail"] = stderr[-300:]
    elif result is None:
        rec["error"] = "missing-result"
        rec["stderr_tail"] = stderr[-300:]
    else:
        rec["control"] = control
        rec["result"] = result
    return rec

_RECORD_LOCK = threading.Lock()

def cmd_run(argv):
    budget = 240.0
    workers = 1
    paths = {"k1085": None, "k1086": None, "k1089": None, "k1091": None,
             "k1095": None, "k1097": None}
    args = list(argv)
    i = 0
    while i < len(args):
        m = False
        for key in paths:
            if args[i] == f"--{key}" and i + 1 < len(args):
                paths[key] = args[i + 1]; m = True; i += 2
        if m:
            continue
        if args[i] == "--workers" and i + 1 < len(args):
            workers = max(1, min(4, int(args[i + 1]))); i += 2
            continue
        try:
            budget = float(args[i])
        except ValueError:
            pass
        i += 1
    k1097, k_sha = load_k1097(paths["k1097"])
    _k1085_chk, _ = load_k1085(paths["k1085"])
    _k1086_chk, _ = load_k1086(paths["k1086"])
    _k1089_chk, _ = load_k1089(paths["k1089"])
    _k1091_chk, _ = load_k1091(paths["k1091"])
    _k1095_chk, _ = load_k1095(paths["k1095"])
    sel = replacement_targets(k1097)
    plan = probe_plan(sel)
    done = load_done()
    todo = [p for p in plan if (p["root"], p["depth"], p["ordering"]) not in done]
    if not todo:
        print("ALL PROBES DONE")
        return 0
    if runner_blob() != RUNNER_BLOB_PIN:
        raise SystemExit("runner blob pin FAIL before probing")
    t_start = time.time()
    stats = {"ran": 0, "ok": 0, "err": 0}
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
            rec = run_one_probe(p, k_sha)
            with _RECORD_LOCK:
                with RECORDS.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, sort_keys=True) + "\n")
                    f.flush()
            res = rec.get("result") or {}
            if rec.get("error"):
                stats["err"] += 1
            else:
                stats["ok"] += 1
            print(f"[{stats['ran']}/{len(jobs)}] {rec.get('error','ok')} root={p['root'][:8]}… "
                  f"d{p['depth']} {p['ordering']} wall={rec['wall_s']}s nodes={res.get('nodes')} "
                  f"loss={res.get('loss')} capped={res.get('capped')} term={res.get('terminalStoneRange')}",
                  flush=True)

    global _JOB_LOCK
    _JOB_LOCK = threading.Lock()
    threads = [threading.Thread(target=worker) for _ in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=budget + TIMEOUT + 30)
    print(f"budget {budget}s elapsed={round(time.time()-t_start,1)}s ran={stats['ran']} "
          f"ok={stats['ok']} err={stats['err']} remaining={len(jobs) - stats['ran']}")
    return 0

# ---------------------------------------------------------------------------
# assemble
# ---------------------------------------------------------------------------
def gate(gates, name, ok, detail):
    gates.append({"name": name, "pass": bool(ok), "detail": detail})

def cmd_assemble(argv):
    args = list(argv)
    paths = {"k1085": None, "k1086": None, "k1089": None, "k1091": None,
             "k1095": None, "k1097": None}
    for key in paths:
        if f"--{key}" in args:
            paths[key] = args[args.index(f"--{key}") + 1]
    k1085, k_sha5 = load_k1085(paths["k1085"])
    k1086, k_sha6 = load_k1086(paths["k1086"])
    k1089, k_sha9 = load_k1089(paths["k1089"])
    k1091, k_sha1 = load_k1091(paths["k1091"])
    k1095, k_sha15 = load_k1095(paths["k1095"])
    k1097, k_sha7 = load_k1097(paths["k1097"])
    sel = replacement_targets(k1097)
    plan = probe_plan(sel)
    done = load_done()
    gates = []
    gate(gates, "k1085-sha-pin", k_sha5 == K1085_SHA256, {"sha256": k_sha5})
    gate(gates, "k1086-sha-pin", k_sha6 == K1086_SHA256, {"sha256": k_sha6})
    gate(gates, "k1089-sha-pin", k_sha9 == K1089_SHA256, {"sha256": k_sha9})
    gate(gates, "k1091-sha-pin", k_sha1 == K1091_SHA256, {"sha256": k_sha1})
    gate(gates, "k1095-sha-pin", k_sha15 == K1095_SHA256, {"sha256": k_sha15})
    gate(gates, "k1097-sha-pin", k_sha7 == K1097_SHA256, {"sha256": k_sha7})
    gate(gates, "runner-blob-pin", runner_blob() == RUNNER_BLOB_PIN, {"git_blob": runner_blob()})

    # --- residual-49 re-derivation from K1085 + K1086 (NOT from K1088) ---
    rows72 = k1085["base_state"]["residual_row_hex"]
    assert len(rows72) == k1085["base_state"]["residual_rows"] == 72
    resid_forms = {}
    for r in rows72:
        for im in d4_images(cells(r)):
            resid_forms[hexof(im)] = r
    win8_roots = {w["root"] for w in k1086["classification"]["win8_d10_candidates"]}
    refuted_roots = {t["root"] for t in k1086["classification"]["refuted_d10_facts"]}
    claims_w, claims_r, unknown_rows = [], [], []
    for root, info in k1086["per_root"].items():
        tgt = claims_w if root in win8_roots else claims_r
        for row_hex in info["covered_rows"]:
            canon = resid_forms.get(row_hex)
            if canon is None:
                unknown_rows.append({"root": root, "row": row_hex})
            else:
                tgt.append(canon)
    rederiv = {
        "win8_roots": len(win8_roots), "refuted_roots": len(refuted_roots),
        "win8_claimed_rows": len(claims_w), "refuted_claimed_rows": len(claims_r),
        "unknown_claim_rows": unknown_rows,
        "partition": {
            "win8_claims_distinct": len(claims_w) == len(set(claims_w)),
            "refuted_claims_distinct": len(claims_r) == len(set(claims_r)),
            "disjoint": not (set(claims_w) & set(claims_r)),
            "union_is_residual72": set(claims_w) | set(claims_r) == set(rows72),
        },
    }
    ok_partition = (len(win8_roots) == 7 and len(refuted_roots) == 16
                    and len(claims_w) == 23 and len(claims_r) == 49
                    and not unknown_rows
                    and rederiv["partition"]["win8_claims_distinct"]
                    and rederiv["partition"]["refuted_claims_distinct"]
                    and rederiv["partition"]["disjoint"]
                    and rederiv["partition"]["union_is_residual72"])
    gate(gates, "residual49-rederived-from-k1085-k1086", ok_partition, rederiv)
    resid49 = set(claims_r)

    # --- residual-40 re-derivation from K1085 + K1086 + K1089 (NOT from K1090) ---
    win9_roots = {w["root"] for w in k1089["classification"]["win8_d10_candidates"]}
    ref13_roots = {r["root"] for r in k1089["classification"]["refuted_d10_facts"]}
    claims_w9, claims_r40, unknown_rows9 = [], [], []
    for root, info in k1089["per_root"].items():
        if root not in win9_roots and root not in ref13_roots:
            continue
        tgt = claims_w9 if root in win9_roots else claims_r40
        for row_hex in info["covered_rows"]:
            canon = resid_forms.get(row_hex)
            if canon is None:
                unknown_rows9.append({"root": root, "row": row_hex})
            else:
                tgt.append(canon)
    rederiv40 = {
        "win9_roots": len(win9_roots), "ref13_roots": len(ref13_roots),
        "win9_claimed_rows": len(claims_w9), "ref13_claimed_rows": len(claims_r40),
        "unknown_claim_rows": unknown_rows9,
        "partition": {
            "win9_claims_distinct": len(claims_w9) == len(set(claims_w9)),
            "ref13_claims_distinct": len(claims_r40) == len(set(claims_r40)),
            "disjoint": not (set(claims_w9) & set(claims_r40)),
            "union_is_residual49": set(claims_w9) | set(claims_r40) == resid49,
            "ref13_claims_subset_of_resid49": set(claims_r40) <= resid49,
        },
    }
    ok40 = (len(win9_roots) == 3 and len(ref13_roots) == 13
            and len(claims_w9) == 9 and len(claims_r40) == 40
            and not unknown_rows9
            and rederiv40["partition"]["win9_claims_distinct"]
            and rederiv40["partition"]["ref13_claims_distinct"]
            and rederiv40["partition"]["disjoint"]
            and rederiv40["partition"]["union_is_residual49"])
    gate(gates, "residual40-rederived-from-k1085-k1086-k1089", ok40, rederiv40)
    residual40 = set(claims_r40)

    # --- residual-30 re-derivation from K1085+K1086+K1089+K1091 (NOT from K1094 or K1097) ---
    win11_roots = {w["root"] for w in k1091["classification"]["win8_d10_candidates"]}
    ref12_roots = {r["root"] for r in k1091["classification"]["refuted_d10_facts"]}
    claims_w11, claims_r30, unknown_rows11 = [], [], []
    for root, info in k1091["per_root"].items():
        if root not in win11_roots and root not in ref12_roots:
            continue
        tgt = claims_w11 if root in win11_roots else claims_r30
        for row_hex in info["covered_rows"]:
            canon = resid_forms.get(row_hex)
            if canon is None:
                unknown_rows11.append({"root": root, "row": row_hex})
            else:
                tgt.append(canon)
    rederiv30 = {
        "win11_roots": len(win11_roots), "ref12_roots": len(ref12_roots),
        "win11_claimed_rows": len(claims_w11), "ref12_claimed_rows": len(claims_r30),
        "unknown_claim_rows": unknown_rows11,
        "partition": {
            "win11_claims_distinct": len(claims_w11) == len(set(claims_w11)),
            "ref12_claims_distinct": len(claims_r30) == len(set(claims_r30)),
            "disjoint": not (set(claims_w11) & set(claims_r30)),
            "union_is_residual40": set(claims_w11) | set(claims_r30) == residual40,
            "ref12_claims_subset_of_resid40": set(claims_r30) <= residual40,
        },
    }
    ok30 = (len(win11_roots) == 3 and len(ref12_roots) == 12
            and len(claims_w11) == 10 and len(claims_r30) == 30
            and not unknown_rows11
            and rederiv30["partition"]["win11_claims_distinct"]
            and rederiv30["partition"]["ref12_claims_distinct"]
            and rederiv30["partition"]["disjoint"]
            and rederiv30["partition"]["union_is_residual40"])
    gate(gates, "residual30-rederived-from-k1085-k1086-k1089-k1091", ok30, rederiv30)
    residual30 = set(claims_r30)

    # --- residual-23 re-derivation from K1085+K1086+K1089+K1091+K1095 (NOT from K1097) ---
    win12_roots = {w["root"] for w in k1095["classification"]["win8_d10_candidates"]}
    ref9_roots = {r["root"] for r in k1095["classification"]["refuted_d10_facts"]}
    claims_w12, claims_r23, unknown_rows12 = [], [], []
    for root, info in k1095["per_root"].items():
        if root not in win12_roots and root not in ref9_roots:
            continue
        tgt = claims_w12 if root in win12_roots else claims_r23
        for row_hex in info["covered_rows"]:
            canon = resid_forms.get(row_hex)
            if canon is None:
                unknown_rows12.append({"root": root, "row": row_hex})
            else:
                tgt.append(canon)
    rederiv23 = {
        "win12_roots": len(win12_roots), "ref9_roots": len(ref9_roots),
        "win12_claimed_rows": len(claims_w12), "ref9_claimed_rows": len(claims_r23),
        "unknown_claim_rows": unknown_rows12,
        "partition": {
            "win12_claims_distinct": len(claims_w12) == len(set(claims_w12)),
            "ref9_claims_distinct": len(claims_r23) == len(set(claims_r23)),
            "disjoint": not (set(claims_w12) & set(claims_r23)),
            "union_is_residual30": set(claims_w12) | set(claims_r23) == residual30,
            "ref9_claims_subset_of_resid30": set(claims_r23) <= residual30,
        },
    }
    ok23 = (len(win12_roots) == 3 and len(ref9_roots) == 9
            and len(claims_w12) == 7 and len(claims_r23) == 23
            and not unknown_rows12
            and rederiv23["partition"]["win12_claims_distinct"]
            and rederiv23["partition"]["ref9_claims_distinct"]
            and rederiv23["partition"]["disjoint"]
            and rederiv23["partition"]["union_is_residual30"])
    gate(gates, "residual23-rederived-from-k1085-k1086-k1089-k1091-k1095", ok23, rederiv23)
    residual23 = set(claims_r23)
    # consistency (non-independent) crosscheck against the pinned K1097 bookkeeping
    k1097_r23 = {r["row"] for r in k1097["per_row_residual23"]}
    scope1_sel = [t["root"] for t in k1097["scope1_refsolve_residual23"]["greedy_selection"]]
    scope2_sel = [t["root"] for t in k1097["scope2_refsolve_need_new_providers"]["greedy_selection"]]
    gate(gates, "residual23-consistency-with-k1097-bookkeeping",
         k1097_r23 == residual23 and scope1_sel == scope2_sel,
         {"k1097_per_row_residual23_rows": len(k1097_r23),
          "equal": k1097_r23 == residual23,
          "k1097_scope1_scope2_same_selection": scope1_sel == scope2_sel,
          "note": "equality expected: both enumerate the ref9 claimed rows in "
                  "residual30 canonical form; the independent derivation above does "
                  "not use K1097 for the universe"})

    # --- replacement-plan geometry re-derivation (independent of K1088's machine) ---
    geom = {}
    ok_pop = all(popcount_hex(t["root"]) == 8 for t in sel)
    qf_roots = [t["root"] for t in sel if quad_free(cells(t["root"]))]
    geom["quad_free_roots"] = len(qf_roots)
    canonical_roots = 0
    for t in sel:
        orb = [hexof(im) for im in d4_images(cells(t["root"]))]
        if t["root"] == min(orb):
            canonical_roots += 1
    geom["d4_min_canonical_roots"] = canonical_roots
    gate(gates, "replace9-geometry-basic",
         ok_pop and len(qf_roots) == 9 and canonical_roots == 9,
         {"popcount8": ok_pop, "quad_free": len(qf_roots), "d4_min_canonical": canonical_roots,
          "note": "each replacement root is 8 stones, quadruple-free, and the minimal "
                  "hex over its own D4 orbit"})
    pair_ok = 0
    pair_bad = []
    cover_map = {}
    for t in sel:
        for row_hex in t["covered_rows"]:
            canon = resid_forms.get(row_hex)
            sub = any((int(row_hex, 16) | int(hexof(im), 16)) == int(hexof(im), 16)
                      for im in d4_images(cells(t["root"])))
            sub2 = any((int(hexof(im), 16) | int(t["root"], 16)) == int(t["root"], 16)
                       for im in d4_images(cells(row_hex)))
            if canon is not None and canon in residual23 and (sub or sub2) and cover_map.get(canon) is None:
                pair_ok += 1
                cover_map[canon] = t["root"]
            else:
                pair_bad.append({"root": t["root"], "row": row_hex, "canon": canon,
                                 "in_residual23": canon in residual23 if canon else None,
                                 "sub": sub, "sub2": sub2,
                                 "dup": cover_map.get(canon) if canon else None})
    geom["claimed_pairs_ok"] = pair_ok
    geom["claimed_pairs_bad"] = pair_bad[:5]
    gate(gates, "replace9-pairs-rederived", pair_ok == 23 and not pair_bad,
         {"pairs_ok": pair_ok, "bad": pair_bad[:5],
          "note": "each claimed (root,row) pair: row hex is a D4 orientation of a "
                  "re-derived residual-23 row, row-set ⊆ some D4 image of the root "
                  "(in either orientation), and each residual-30 row is covered at "
                  "most once"})
    gate(gates, "coverage-23-exactly-once", set(cover_map) == residual23 and len(cover_map) == 23,
         {"covered_union": len(cover_map), "matches_rederived_residual23": set(cover_map) == residual23})
    gains_hist = {}
    for t in sel:
        gains_hist[str(t["gained_rows"])] = gains_hist.get(str(t["gained_rows"]), 0) + 1
    ok_gains = all(t["gained_rows"] == len(t["covered_rows"]) for t in sel)
    gate(gates, "replace9-gains-hist", ok_gains and gains_hist == {"3": 6, "2": 2, "1": 1},
         {"observed_hist": gains_hist, "per_root_claim_consistent": ok_gains,
          "k1097_scope1_greedy_size": k1097["scope1_refsolve_residual23"]["greedy_size"],
          "k1097_scope1_leftover": k1097["scope1_refsolve_residual23"]["leftover_rows"],
          "k1097_scope1_gains_hist": k1097["scope1_refsolve_residual23"]["gains_hist"],
          "k1097_scope1_stranded": k1097["scope1_refsolve_residual23"]["stranded_rows"],
          "k1097_scope1_max_matching": k1097["scope1_refsolve_residual23"]["max_matching"]})

    # --- raw child re-derivation ---
    ok_child = True
    for p in plan:
        rv = int(p["root"], 16)
        ok_child = ok_child and (int(p["child"], 16) | (1 << p["bit"])) == rv
        ok_child = ok_child and (rv & (1 << p["bit"])) != 0
        ok_child = ok_child and popcount_hex(p["child"]) == 7
    gate(gates, "raw-child-rebuild", ok_child,
         {"rule": "child = root minus lowest set bit; verdict is designation-independent "
                  "(engine receives the same cell set)"})

    # --- completeness ---
    planned = {(p["root"], p["depth"], p["ordering"]) for p in plan}
    gate(gates, "all-probes-present", planned == set(done), {
        "planned": len(planned), "present": len(done),
        "missing": sorted(f"{r[:8]}…d{d}{o}" for r, d, o in planned - set(done))})

    # --- pilot control on every record ---
    ctrl_ok = True
    ctrl_bad = []
    for key, rec in done.items():
        c = rec.get("control")
        if not c or c.get("nodes") != PILOT_D6_NODES or c.get("loss") is not False or c.get("capped") is not False:
            ctrl_ok = False
            ctrl_bad.append([key, c])
    gate(gates, "pilot-d6-control-all-probes", ctrl_ok and len(done) == len(plan), {"bad": ctrl_bad[:3]})

    # --- verdict table + ordering consistency ---
    per_root = {}
    for t in sel:
        per_root[t["root"]] = {"gained_rows": t["gained_rows"],
                               "covered_rows": t["covered_rows"],
                               "probes": {}}
    conflicts = []
    for (root, depth, ordering), rec in sorted(done.items()):
        ent = {"ordering": ordering, "wall_s": rec.get("wall_s")}
        if rec.get("error"):
            ent["status"] = rec["error"]
        else:
            r = rec["result"]
            ent.update({"nodes": r["nodes"], "loss": r["loss"], "capped": r["capped"],
                        "terminalStoneRange": r["terminalStoneRange"], "ms": r.get("ms")})
        per_root[root]["probes"][ordering] = ent
    for root, info in per_root.items():
        pr = info["probes"]
        losses = [pr[o].get("loss") for o in ("andclose1", "andclose0")
                  if o in pr and "loss" in pr[o]]
        if len(losses) == 2 and losses[0] != losses[1]:
            conflicts.append({"root": root, "losses": losses})
    gate(gates, "ordering-consistency-scan", not conflicts, {"conflicts": conflicts})

    # --- classification ---
    win8 = []
    refuted = []
    unresolved = []
    for root, info in per_root.items():
        pr = info["probes"]
        any_win_uncapped = any(pr[o].get("loss") is True and pr[o].get("capped") is False
                               for o in ("andclose1", "andclose0") if o in pr)
        full_refute = any(pr[o].get("loss") is False and pr[o].get("capped") is False
                          for o in ("andclose1", "andclose0") if o in pr)
        any_win_capped = any(pr[o].get("loss") is True for o in pr)
        if any_win_uncapped:
            win8.append({"root": root, "gained_rows": info["gained_rows"],
                         "covered_rows": info["covered_rows"]})
        elif full_refute:
            refuted.append({"root": root, "gained_rows": info["gained_rows"]})
        else:
            unresolved.append({"root": root, "status": "no-uncapped-completed-side",
                               "any_loss_true_capped": any_win_capped})
    nodes_total = 0
    capped_count = 0
    term_lo, term_hi = 121, 0
    error_count = 0
    for rec in done.values():
        if rec.get("error"):
            error_count += 1
        else:
            nodes_total += rec["result"]["nodes"]
            if rec["result"]["capped"]:
                capped_count += 1
            lo, hi = rec["result"]["terminalStoneRange"]
            term_lo = min(term_lo, lo)
            term_hi = max(term_hi, hi)
    if term_lo > term_hi:
        term_lo = term_hi = None

    hard = [g for g in gates if not g["pass"]]
    doc = {
        "schema": SCHEMA,
        "date": "2026-11-20",
        "cap": CAP,
        "timeout_s": TIMEOUT,
        "runner_git_blob": RUNNER_BLOB_PIN,
        "inputs": {"k1085_sha256": k_sha5, "k1086_sha256": k_sha6,
                   "k1089_sha256": k_sha9, "k1091_sha256": k_sha1,
                   "k1095_sha256": k_sha15, "k1097_sha256": k_sha7},
        "single_owner_note": ("research/log/2026-11-20-n11-residual72-replace9-d10-sweep-"
                              "single-owner-note.md (commit 51bbb938809c36eafbf5a762f03bf729c097fe6f)"),
        "protocol": ("verdict probe facts only; runner v17, depth 10, cap 30M, timeout 280s, "
                     "both AND orderings, pilot_d6 control required on every probe; "
                     "raw child hex rule (child = root minus lowest set bit) is bookkeeping "
                     "only, the engine receives the identical cell set; resume-safe sequential "
                     "records; capped/timeout probes are cost lower bounds and evidence in NO "
                     "direction"),
        "targets": {"replacement_roots": 9, "probes_planned": len(plan),
                    "base": "K1097 scope1_refsolve_residual23.greedy_selection "
                            "(pinned by sha256), residual-23 universe re-derived from "
                            "K1085+K1086+K1089+K1091+K1095 inside this machine"},
        "residual49_rederivation": rederiv,
        "residual40_rederivation": rederiv40,
        "residual30_rederivation": rederiv30,
        "residual23_rederivation": rederiv23,
        "replacement_plan_geometry_independent_rederivation": geom,
        "gates": gates,
        "per_root": per_root,
        "classification": {
            "win8_d10_candidates": win8,
            "refuted_d10_facts": refuted,
            "unresolved": unresolved,
            "nodes_total": nodes_total,
            "capped_probes": capped_count,
            "error_probes": error_count,
            "terminalStoneRange_union": [term_lo, term_hi],
        },
        "interpretation_guard": [
            "loss=true (uncapped) is a WIN8-within-depth-10 probe candidate: a certificate "
            "rebuild target whose extraction, fold and row-closure semantics are NOT "
            "established by this sweep and require a separate single-owner undertaking.",
            "loss=false with at least one uncapped ordering is a REFUTED-D10 probe fact for the "
            "8-stone root: it is NOT a LOSS proof of any earlier position, and it only erodes "
            "the replacement pool for the residual-49 rows.",
            "capped/timeout probes are cost lower bounds and evidence in NO direction.",
            "Node counts and solved counts are not win/loss readings.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and "
            "classes 1/2/4 all remain UNKNOWN.",
        ],
    }
    OUTD.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    sha = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    print(f"gates: {len(gates) - len(hard)}/{len(gates)} pass")
    for g in hard:
        print("GATE FAIL:", g["name"], json.dumps(g["detail"])[:400])
    print("classification:", json.dumps({k: (len(v) if isinstance(v, list) else v)
                                          for k, v in doc["classification"].items() if k != "win8_d10_candidates"}))
    print("win8 candidates:", len(win8))
    print("output sha256:", sha)
    return 1 if hard else 0

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    rest = sys.argv[2:]
    sys.exit(cmd_run(rest) if mode == "run" else cmd_assemble(rest) if mode == "assemble" else 2)
