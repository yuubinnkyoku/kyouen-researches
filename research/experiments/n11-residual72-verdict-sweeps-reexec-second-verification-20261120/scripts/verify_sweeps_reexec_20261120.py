#!/usr/bin/env python3
"""n11 residual-72 four verdict sweeps: probe re-execution second verification
(2026-11-20).

Single-owner undertaking per
research/log/2026-11-20-n11-residual72-verdict-sweeps-reexec-second-verification-single-owner-note.md
(commit 259e4019db88395a1b8ca48fda9d0b842665653a). This machine re-executes
EVERY published depth-10 probe record of the four residual-72 candidate-supply
sweeps with the repo-pinned runner v17 and compares the deterministic fields
(nodes, loss, capped, terminalStoneRange) against the published records:

  - K1086 addtwo-greedy23-d10-sweep: 46 probes (record JSON sha256 3045e152...)
  - K1089 replace16-d10-sweep:      32 probes (record JSON sha256 808fbda1...)
  - K1091 replace15-d10-sweep:      30 probes (record JSON sha256 edd7ac84...)
  - K1095 replace12-d10-sweep:      24 probes (record JSON sha256 335eca5e...)

Independent re-derivations inside this machine (fail-closed):
  - pinned-input loading by SHA-256 (4 record JSONs + 4 probe-record JSONLs)
  - runner v17 pinned by git blob SHA-1
  - raw child designation rule re-derivation (child = root minus lowest set
    bit; bookkeeping only, the engine receives the same cell set)
  - probe plan completeness (46/32/30/24, both AND orderings, depth 10,
    cap 30,000,000, timeout 280s, pilot_d6 control in every published record)
  - published internal consistency: probe-record JSONL values == record JSON
    per_root values for every probe
  - fresh re-execution (two passes: A in this tree, B in an isolated tree)
  - fresh classification and nodes totals re-derived from fresh results and
    compared with the published classification

This is a re-execution verification of published probe facts only:
NO row closure, NO receipt fold, NO certificate extraction, NO new probe
beyond re-running the published ones, NO verdict beyond depth 10, and NO
win/loss interpretation beyond the runner's depth-bounded probe semantics.
REFUTED-D10 is not a LOSS proof. node counts are not win/loss evidence.
The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}
and classes 1/2/4 all remain UNKNOWN.

Usage:
  verify_sweeps_reexec_20261120.py run [budget_s] [--pass NAME] [--root DIR]
      [--workers N] [--inputs DIR]
  verify_sweeps_reexec_20261120.py assemble [--pass-a DIR] [--pass-b DIR]
      [--inputs DIR] [--out PATH]
"""
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent
REPO_EXPERIMENTS = EXP.parent
RUNNER = EXP / "runner_v17.ts"
OUTD = EXP / "output"
OUTPUT = OUTD / "verdict-sweeps-reexec-second-verification-20261120.json"
SCHEMA = "n11-residual72-verdict-sweeps-reexec-second-verification-20261120-v1"

CAP = 30_000_000
TIMEOUT = 280
RUNNER_BLOB_PIN = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
PILOT_D6_NODES = 3402

# published artifacts: sweep label -> pinned protocol constants
SWEEPS = {
    "k1086_greedy23": {
        "dir": "n11-residual72-addtwo-greedy23-d10-sweep-20261120",
        "json": ("addtwo-greedy23-d10-sweep-20261120.json",
                 "3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced"),
        "jsonl": ("probe-records-add2greedy23.jsonl",
                  "773fef4262a9c69766402d3c0f846f5569ce095107efedaa02a76690ab35b8f3"),
        "probes": 46, "win": 7, "refuted": 16, "nodes_total": 18_032_471,
    },
    "k1089_replace16": {
        "dir": "n11-residual72-replace16-d10-sweep-20261120",
        "json": ("replace16-d10-sweep-20261120.json",
                 "808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc"),
        "jsonl": ("probe-records-replace16.jsonl",
                  "75fda6ade767e731ba4e42049230bcea6498eee6e9b2348a9d909a1832f329f6"),
        "probes": 32, "win": 3, "refuted": 13, "nodes_total": 6_339_079,
    },
    "k1091_replace15": {
        "dir": "n11-residual72-replace15-d10-sweep-20261120",
        "json": ("replace15-d10-sweep-20261120.json",
                 "edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25"),
        "jsonl": ("probe-records-replace15.jsonl",
                  "47165331b68f10684db9217a18fd3a2aab6748ecf1191f0216905981737a773a"),
        "probes": 30, "win": 3, "refuted": 12, "nodes_total": 7_383_022,
    },
    "k1095_replace12": {
        "dir": "n11-residual72-replace12-d10-sweep-20261120",
        "json": ("replace12-d10-sweep-20261120.json",
                 "335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707"),
        "jsonl": ("probe-records-replace12.jsonl",
                  "89e2c30d93fc26b5f760c3f9f00c6190595e6adc2fd6320fd2ac69a2603f9c56"),
        "probes": 24, "win": 3, "refuted": 9, "nodes_total": 5_700_222,
    },
}


# ---------------------------------------------------------------------------
# pinned inputs
# ---------------------------------------------------------------------------
def inputs_root(explicit=None):
    if explicit:
        return Path(explicit)
    env = os.environ.get("REEXEC_INPUT_ROOT")
    if env:
        return Path(env)
    return REPO_EXPERIMENTS


def load_pinned(path, sha, label):
    data = path.read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if got != sha:
        raise SystemExit(f"{label} sha256 pin FAIL: {got} != {sha}")
    return json.loads(data.decode("utf-8"))


def load_sweeps(root):
    out = {}
    for label, meta in SWEEPS.items():
        base = Path(root) / meta["dir"] / "output"
        doc = load_pinned(base / meta["json"][0], meta["json"][1],
                          f"{label} record json")
        recs = []
        raw = (base / meta["jsonl"][0]).read_bytes()
        got = hashlib.sha256(raw).hexdigest()
        if got != meta["jsonl"][1]:
            raise SystemExit(f"{label} probe-records jsonl sha256 pin FAIL: {got}")
        for line in raw.decode("utf-8").splitlines():
            if line.strip():
                recs.append(json.loads(line))
        out[label] = {"doc": doc, "recs": recs}
    return out


def runner_blob(raw=None):
    raw = raw if raw is not None else RUNNER.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()


def popcount_hex(h):
    return bin(int(h, 16)).count("1")


def plan_from_records(recs, label):
    """Build the re-execution plan and re-derive the child designation rule."""
    plan = []
    for r in recs:
        if r.get("depth") != 10:
            raise SystemExit(f"{label}: non-d10 record in probe-records")
        root = r["root"]
        rv = int(root, 16)
        bit = (rv & -rv).bit_length() - 1
        child = rv & ~(1 << bit)
        if r.get("bit") != bit or int(r["child"], 16) != child:
            raise SystemExit(f"{label} {root}: child designation re-derivation FAIL")
        if popcount_hex(root) != 8 or popcount_hex(r["child"]) != 7:
            raise SystemExit(f"{label} {root}: popcount sanity FAIL")
        if r.get("ordering") not in ("andclose1", "andclose0"):
            raise SystemExit(f"{label} {root}: unknown ordering {r.get('ordering')}")
        if r.get("cap") != CAP or r.get("timeout_s") != 280:
            raise SystemExit(f"{label} {root}: cap/timeout not as pinned protocol")
        if r.get("runner_blob") != RUNNER_BLOB_PIN:
            raise SystemExit(f"{label} {root}: runner blob in record != pin")
        c = r.get("control") or {}
        if (c.get("nodes") != PILOT_D6_NODES or c.get("loss") is not False
                or c.get("capped") is not False):
            raise SystemExit(f"{label} {root}: published pilot_d6 control FAIL")
        res = r["result"]
        plan.append({
            "label": label, "root": root, "bit": bit, "child": r["child"],
            "andclose": 1 if r["ordering"] == "andclose1" else 0,
            "ordering": r["ordering"],
            "expect": {"nodes": res["nodes"], "loss": res["loss"],
                       "capped": res["capped"],
                       "terminalStoneRange": res["terminalStoneRange"]},
        })
    return plan


def doc_per_probes(doc):
    """per_root probes table from the sweep record JSON."""
    per = doc["per_root"]
    out = {}
    for root, info in per.items():
        probes = info["probes"]
        for ordering, ent in probes.items():
            out[(root, ordering)] = {
                "nodes": ent["nodes"], "loss": ent["loss"],
                "capped": ent["capped"],
                "terminalStoneRange": ent["terminalStoneRange"],
            }
    return out


# ---------------------------------------------------------------------------
# run (fresh re-execution pass, resume-safe)
# ---------------------------------------------------------------------------
_RECORD_LOCK = threading.Lock()
_JOB_LOCK = threading.Lock()


def run_one_probe(p, rec_path):
    tmp = rec_path.parent / f".tmp-probe-{os.getpid()}-{time.time_ns()}.jsonl"
    if tmp.exists():
        tmp.unlink()
    cmd = ["node", "--experimental-strip-types", str(RUNNER),
           "--bits", str(p["bit"]), "--depth", "10", "--cap", str(CAP),
           "--andclose", str(p["andclose"]), "--child", p["child"],
           "--out", str(tmp)]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=TIMEOUT, cwd=str(RUNNER.parent))
        rc, stderr = r.returncode, r.stderr.strip()[-300:]
    except subprocess.TimeoutExpired:
        rc, stderr = "timeout", ""
    wall = round(time.time() - t0, 1)
    control = result = None
    if tmp.exists():
        for line in tmp.read_text(encoding="utf-8").splitlines():
            if line.strip():
                obj = json.loads(line)
                if obj.get("control"):
                    control = obj
                else:
                    result = obj
        tmp.unlink()
    rec = {"label": p["label"], "root": p["root"], "ordering": p["ordering"],
           "depth": 10, "bit": p["bit"], "child": p["child"], "cap": CAP,
           "timeout_s": TIMEOUT, "wall_s": wall}
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
    inc_root = None
    args = list(argv)
    i = 0
    while i < len(args):
        if args[i] == "--pass" and i + 1 < len(args):
            pass_name = args[i + 1]; i += 2; continue
        if args[i] == "--root" and i + 1 < len(args):
            root_dir = Path(args[i + 1]); i += 2; continue
        if args[i] == "--inputs" and i + 1 < len(args):
            inc_root = args[i + 1]; i += 2; continue
        if args[i] == "--workers" and i + 1 < len(args):
            workers = max(1, min(4, int(args[i + 1]))); i += 2; continue
        try:
            budget = float(args[i])
        except ValueError:
            pass
        i += 1
    root_dir = Path(root_dir)
    root_dir.mkdir(parents=True, exist_ok=True)
    records = root_dir / f"probe-records-reexec-pass{pass_name}.jsonl"
    sweeps = load_sweeps(inputs_root(inc_root))
    if runner_blob() != RUNNER_BLOB_PIN:
        raise SystemExit("runner blob pin FAIL before probing")
    plan = []
    for label, s in sweeps.items():
        if len(s["recs"]) != SWEEPS[label]["probes"]:
            raise SystemExit(f"{label}: probe-records count != pin "
                             f"({len(s['recs'])} != {SWEEPS[label]['probes']})")
        plan.extend(plan_from_records(s["recs"], label))
    done = set()
    if records.exists():
        for line in records.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                done.add((rec["label"], rec["root"], rec["ordering"]))
    todo = [p for p in plan
            if (p["label"], p["root"], p["ordering"]) not in done]
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
            rec = run_one_probe(p, records)
            with _RECORD_LOCK:
                with records.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, sort_keys=True) + "\n")
                    f.flush()
            res = rec.get("result") or {}
            if rec.get("error"):
                stats["err"] += 1
            print(f"[pass{pass_name} {stats['ran']}/{len(jobs)}] {rec.get('error','ok')} "
                  f"{p['label']} {p['root'][:10]} {p['ordering']} "
                  f"nodes={res.get('nodes')} loss={res.get('loss')} "
                  f"capped={res.get('capped')} wall={rec['wall_s']}s", flush=True)

    threads = [threading.Thread(target=worker) for _ in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=budget + TIMEOUT + 30)
    print(f"pass {pass_name} budget {budget}s elapsed={round(time.time()-t_start,1)}s "
          f"ran={stats['ran']} err={stats['err']} "
          f"remaining={len(jobs) - stats['ran']}", flush=True)
    return 0


# ---------------------------------------------------------------------------
# assemble (fail-closed gates + canonical audit JSON)
# ---------------------------------------------------------------------------
def gate(gates, name, ok, detail):
    gates.append({"name": name, "pass": bool(ok), "detail": detail})


def fresh_index(records_path):
    idx = {}
    for line in Path(records_path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            idx[(rec["label"], rec["root"], rec["ordering"])] = rec
    return idx


def cmp_fresh(plans, fresh, tag, gates):
    """Compare a fresh pass against published probe facts. Fail-closed."""
    total_mismatch = []
    per_label_stats = {}
    for label, meta in SWEEPS.items():
        plan = plans[label]
        got = 0
        nodes_sum = 0
        cap_or_err = 0
        loss_by_root = {}
        recs_by_root = {}
        for p in plan:
            rec = fresh.get((label, p["root"], p["ordering"]))
            if rec is None:
                total_mismatch.append({"label": label, "root": p["root"],
                                       "ordering": p["ordering"], "why": "missing"})
                continue
            if rec.get("error"):
                cap_or_err += 1
                total_mismatch.append({"label": label, "root": p["root"],
                                       "ordering": p["ordering"],
                                       "why": rec.get("error")})
                continue
            c = rec.get("control") or {}
            if (c.get("nodes") != PILOT_D6_NODES or c.get("loss") is not False
                    or c.get("capped") is not False):
                cap_or_err += 1
                total_mismatch.append({"label": label, "root": p["root"],
                                       "ordering": p["ordering"],
                                       "why": "pilot-control"})
                continue
            r = rec["result"]
            ok = all([r["nodes"] == p["expect"]["nodes"],
                      r["loss"] == p["expect"]["loss"],
                      r["capped"] == p["expect"]["capped"],
                      r["terminalStoneRange"] == p["expect"]["terminalStoneRange"]])
            if not ok:
                total_mismatch.append({
                    "label": label, "root": p["root"],
                    "ordering": p["ordering"], "why": "value-mismatch",
                    "fresh": {k: r[k] for k in
                              ("nodes", "loss", "capped", "terminalStoneRange")},
                    "published": p["expect"]})
                continue
            got += 1
            nodes_sum += r["nodes"]
            loss_by_root.setdefault(p["root"], []).append(r["loss"])
            recs_by_root.setdefault(p["root"], []).append(r)
        order_conflicts = sorted(root for root, ls in loss_by_root.items()
                                 if len(ls) == 2 and ls[0] != ls[1])
        win_roots = set()
        refuted_roots = set()
        for root, rrecs in recs_by_root.items():
            if len(rrecs) != 2:
                continue
            losses = [x["loss"] for x in rrecs]
            capped = [x["capped"] for x in rrecs]
            if any(l is True and c is False for l, c in zip(losses, capped)):
                win_roots.add(root)
            elif any(l is False and c is False for l, c in zip(losses, capped)):
                refuted_roots.add(root)
        per_label_stats[label] = {
            "probes_compared_ok": got,
            "nodes_sum": nodes_sum,
            "cap_or_error_probes": cap_or_err,
            "ordering_conflicts": order_conflicts,
            "win_roots": len(win_roots),
            "refuted_roots": len(refuted_roots),
        }
    ok_all = (not total_mismatch
              and all(s["probes_compared_ok"] == SWEEPS[l]["probes"]
                      and s["nodes_sum"] == SWEEPS[l]["nodes_total"]
                      and s["win_roots"] == SWEEPS[l]["win"]
                      and s["refuted_roots"] == SWEEPS[l]["refuted"]
                      and s["cap_or_error_probes"] == 0
                      and not s["ordering_conflicts"]
                      for l, s in per_label_stats.items()))
    detail = dict(per_label_stats)
    if total_mismatch:
        detail["mismatches"] = total_mismatch[:10]
        detail["mismatch_count"] = len(total_mismatch)
    gate(gates, f"{tag}-fresh-vs-published-all-fields", ok_all, detail)
    return per_label_stats


def cmd_assemble(argv):
    pass_a = OUTD
    pass_b = None
    inc_root = None
    out_path = OUTPUT
    args = list(argv)
    i = 0
    while i < len(args):
        if args[i] == "--pass-a" and i + 1 < len(args):
            pass_a = Path(args[i + 1]); i += 2; continue
        if args[i] == "--pass-b" and i + 1 < len(args):
            pass_b = Path(args[i + 1]); i += 2; continue
        if args[i] == "--inputs" and i + 1 < len(args):
            inc_root = args[i + 1]; i += 2; continue
        if args[i] == "--out" and i + 1 < len(args):
            out_path = Path(args[i + 1]); i += 2; continue
        i += 1
    sweeps = load_sweeps(inputs_root(inc_root))
    gates = []
    gate(gates, "runner-blob-pin", runner_blob() == RUNNER_BLOB_PIN,
         {"git_blob": runner_blob()})

    plans = {}
    pub_internal_bad = []
    cls_pins_ok = True
    for label, meta in SWEEPS.items():
        s = sweeps[label]
        doc = s["doc"]
        per = doc_per_probes(doc)
        cls = doc["classification"]
        if len(s["recs"]) != meta["probes"]:
            raise SystemExit(f"{label}: records count {len(s['recs'])} != pin")
        plan = plan_from_records(s["recs"], label)
        plans[label] = plan
        for p in plan:
            key = (p["root"], p["ordering"])
            if key not in per:
                pub_internal_bad.append({"label": label, "key": key,
                                         "why": "not-in-per_root"})
                continue
            d = per[key]
            e = p["expect"]
            if (d["nodes"] != e["nodes"] or d["loss"] != e["loss"]
                    or d["capped"] != e["capped"]
                    or d["terminalStoneRange"] != e["terminalStoneRange"]):
                pub_internal_bad.append({"label": label, "key": key,
                                         "why": "value-mismatch",
                                         "per_root": d, "jsonl": e})
        ok_cls = (len(cls.get("win8_d10_candidates", [])) == meta["win"]
                  and len(cls.get("refuted_d10_facts", [])) == meta["refuted"]
                  and cls.get("nodes_total") == meta["nodes_total"]
                  and cls.get("capped_probes") == 0
                  and cls.get("error_probes") == 0)
        if not ok_cls:
            cls_pins_ok = False
        lo = min(p["expect"]["terminalStoneRange"][0] for p in plan)
        hi = max(p["expect"]["terminalStoneRange"][1] for p in plan)
        if cls.get("terminalStoneRange_union") not in ([lo, hi], None):
            cls_pins_ok = False
    gate(gates, "published-internal-consistency-jsonl-vs-per-root",
         not pub_internal_bad,
         {"bad": pub_internal_bad[:5], "count": len(pub_internal_bad)})
    gate(gates, "published-classification-pins", cls_pins_ok,
         {"pins": {l: {"win": m["win"], "refuted": m["refuted"],
                       "nodes_total": m["nodes_total"]} for l, m in SWEEPS.items()}})

    rec_a = fresh_index(Path(pass_a) / "probe-records-reexec-passA.jsonl")
    stats_a = cmp_fresh(plans, rec_a, "passA", gates)
    stats_b = None
    if pass_b is not None:
        rec_b = fresh_index(Path(pass_b) / "probe-records-reexec-passB.jsonl")
        stats_b = cmp_fresh(plans, rec_b, "passB", gates)
        cmp_ab_bad = []
        for label in SWEEPS:
            for p in plans[label]:
                ra = rec_a.get((label, p["root"], p["ordering"]))
                rb = rec_b.get((label, p["root"], p["ordering"]))
                if ra is None or rb is None or ra.get("error") or rb.get("error"):
                    cmp_ab_bad.append({"label": label, "root": p["root"],
                                       "ordering": p["ordering"],
                                       "why": "missing-or-error"})
                    continue
                xa, xb = ra["result"], rb["result"]
                keys = ("nodes", "loss", "capped", "terminalStoneRange")
                if not all(xa[k] == xb[k] for k in keys):
                    cmp_ab_bad.append({"label": label, "root": p["root"],
                                       "ordering": p["ordering"],
                                       "why": "value-mismatch",
                                       "passA": {k: xa[k] for k in keys},
                                       "passB": {k: xb[k] for k in keys}})
        gate(gates, "passA-vs-passB-deterministic-fields", not cmp_ab_bad,
             {"bad": cmp_ab_bad[:5], "count": len(cmp_ab_bad)})

    total_fresh_nodes = sum(s["nodes_sum"] for s in stats_a.values())
    total_pub_nodes = sum(m["nodes_total"] for m in SWEEPS.values())
    doc_out = {
        "schema": SCHEMA,
        "date": "2026-11-20",
        "cap": CAP,
        "timeout_s": TIMEOUT,
        "runner_git_blob": RUNNER_BLOB_PIN,
        "inputs": {
            "k1086_record_sha256": SWEEPS["k1086_greedy23"]["json"][1],
            "k1086_records_jsonl_sha256": SWEEPS["k1086_greedy23"]["jsonl"][1],
            "k1089_record_sha256": SWEEPS["k1089_replace16"]["json"][1],
            "k1089_records_jsonl_sha256": SWEEPS["k1089_replace16"]["jsonl"][1],
            "k1091_record_sha256": SWEEPS["k1091_replace15"]["json"][1],
            "k1091_records_jsonl_sha256": SWEEPS["k1091_replace15"]["jsonl"][1],
            "k1095_record_sha256": SWEEPS["k1095_replace12"]["json"][1],
            "k1095_records_jsonl_sha256": SWEEPS["k1095_replace12"]["jsonl"][1],
        },
        "single_owner_note": ("research/log/2026-11-20-n11-residual72-verdict-sweeps-"
                              "reexec-second-verification-single-owner-note.md "
                              "(commit 259e4019db88395a1b8ca48fda9d0b842665653a)"),
        "protocol": ("probe re-execution second verification; runner v17 pinned by "
                     "git blob, depth 10, cap 30M, timeout 280s, both AND orderings, "
                     "pilot_d6 control required on every probe; raw child hex rule "
                     "(child = root minus lowest set bit) re-derived per record and "
                     "is bookkeeping only (the engine receives the identical cell set); "
                     "deterministic comparison fields are nodes/loss/capped/"
                     "terminalStoneRange; ms/wall timings are excluded; passA runs "
                     "in this tree and passB in an isolated cwd/HOME/EXPERIMENT_ROOT"),
        "targets": {
            "sweeps": {l: {"probes": m["probes"], "win": m["win"],
                           "refuted": m["refuted"], "nodes_total": m["nodes_total"]}
                       for l, m in SWEEPS.items()},
            "probes_total": sum(m["probes"] for m in SWEEPS.values()),
            "fresh_nodes_total_passA": total_fresh_nodes,
            "published_nodes_total": total_pub_nodes,
            "pass_b_included": stats_b is not None,
        },
        "passA_reexec_stats": stats_a,
        **({"passB_reexec_stats": stats_b} if stats_b is not None else {}),
        "gates": gates,
        "interpretation_guard": [
            "This verification re-executes published probe facts with the pinned "
            "engine and compares deterministic fields; it verifies NO win/loss "
            "claim beyond the runner's depth-bounded probe semantics.",
            "loss=true (uncapped) marks a WIN8-within-depth-10 candidate for that "
            "8-stone root only; row closure semantics require the separate "
            "published extraction, triple-verification and receipt fold machines.",
            "loss=false (uncapped) is a REFUTED-D10 probe fact: it is NOT a LOSS "
            "proof of any earlier position and only erodes the replacement pool.",
            "capped/timeout probes are cost lower bounds and evidence in NO "
            "direction (none occurred).",
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
          "== published:", total_fresh_nodes == total_pub_nodes)
    print("output sha256:", sha)
    return 1 if hard else 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    rest = sys.argv[2:]
    sys.exit(cmd_run(rest) if mode == "run" else
             cmd_assemble(rest) if mode == "assemble" else 2)
