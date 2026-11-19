#!/usr/bin/env python3
"""n11 K1069 per-probe node-cost ledger re-derivation (39 roots x 2 orderings, depth 10).

Cost-ledger and published-aggregate cross-check only. The verdicts of all 39 roots
were published by K1069; this script does NOT judge, classify or close anything.
REFUTED-D10 is not a LOSS proof. The standard 11x11 empty board, two-stone roots
{49,60}/{59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN.

Usage:
  k1069_nodecost_ledger_20261120.py run <path-to-k1069-sweep-json>
  k1069_nodecost_ledger_20261120.py assemble <path-to-k1069-sweep-json> <path-to-ext-output-json>
"""
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent
RUNNER = EXP / "runner_v17.ts"
OUTD = EXP / "output"
RECORDS = OUTD / "probe-records-k1069ledger.jsonl"
OUTPUT = OUTD / "k1069-nodecost-ledger-20261120.json"
SCHEMA = "n11-k1069-nodecost-ledger-20261120-v1"

CAP = 30_000_000
TIMEOUT = 280
RUNNER_BLOB_PIN = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
PILOT_D6_NODES = 3402

REFUTED_SET_PIN = {
    "sha256": "22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc",
    "path": "research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/output/witness-39live-root-depth10-sweep-20261120.json",
}
EXT_OUTPUT_SHA = "8a584be6a145665c6230169bdc7edb51d453e9429dafe0ab9fd8fc0e579c7aa1"
EXT_OUTPUT_PATH = ("research/experiments/n11-depth11-cost-scaling-pilot-ext-20261120/"
                   "output/depth11-cost-scaling-pilot-ext-20261120.json")
DEPTH = 10
ORDERINGS = (1, 0)
PUBLISHED_PER_PROBE = {
    # root: {ordering: {nodes, loss, capped}}  (published values only)
    "00000000010000809002000040000080": {
        "andclose0": {"nodes": 14249420, "loss": False, "capped": False,
                      "ref": "K1069 summary.max_probe (ac1 non-published)"}},
    "00004000000000821082000000000100": {
        "andclose1": {"nodes": 1576372, "loss": True, "capped": False,
                      "ref": "K1069 knowledge item (17th WIN7-D10 certificate)"},
        "andclose0": {"nodes": 2544178, "loss": True, "capped": False,
                      "ref": "K1069 knowledge item (17th WIN7-D10 certificate)"}},
}
PUBLISHED_SUMMARY = {
    "total_nodes": 169615508, "max_probe_nodes": 14249420, "probes": 78,
    "roots": 39, "win": 1, "refuted": 38, "capped": 0, "order_conflicts": 0,
    "avg_nodes_per_probe": 2174557,
}


def runner_blob(raw=None):
    raw = raw if raw is not None else RUNNER.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def canon_child(root_hex):
    """生child hex rule: child = root minus its lowest set bit; bit = that index."""
    root = int(root_hex, 16)
    bit = (root & -root).bit_length() - 1
    return bit, f"{root & ~(1 << bit):032x}"


def root_map(k1069_path):
    doc = json.loads(Path(k1069_path).read_bytes())
    return {root: label for root, label in doc["classification"].items()}


def probe_list(k1069_path):
    out = []
    for root in sorted(root_map(k1069_path)):
        bit, child = canon_child(root)
        for ordering in ORDERINGS:
            out.append({
                "root": root, "child": child, "bit": bit,
                "ordering": f"andclose{ordering}", "order_n": ordering,
                "depth": DEPTH, "label": root_map(k1069_path)[root],
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


def cmd_run(k1069_path):
    done = load_done()
    todo = [p for p in probe_list(k1069_path) if (p["root"], p["depth"], p["ordering"]) not in done]
    if not todo:
        print("ALL PROBES DONE")
        return 0
    p = todo[0]
    rec_path = EXP / "output" / f".tmp-{p['root']}-{p['depth']}-{p['order_n']}.jsonl"
    if rec_path.exists():
        rec_path.unlink()
    cmd = ["node", "--experimental-strip-types", str(RUNNER),
           "--bits", str(p["bit"]), "--depth", str(DEPTH), "--cap", str(CAP),
           "--andclose", str(p["order_n"]), "--child", p["child"], "--out", str(rec_path)]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, cwd=EXP)
        rc, stdout, stderr = r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired as e:
        rc, stdout, stderr = "timeout", "", str(e.stderr or "")[-300:]
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
    rec = {"root": p["root"], "depth": DEPTH, "ordering": p["ordering"],
           "bit": p["bit"], "child": p["child"], "cap": CAP, "timeout_s": TIMEOUT,
           "k1069_label": p["label"], "wall_s": wall, "runner_blob": RUNNER_BLOB_PIN}
    if rc == "timeout":
        rec["error"] = f"timeout-{TIMEOUT}s"
        rec["control"] = control
    elif rc != 0:
        rec["error"] = f"exit-{rc}"
        rec["control"] = control
        rec["stderr_tail"] = stderr[-300:]
    elif result is None:
        rec["error"] = "missing-result"
        rec["control"] = control
        rec["stdout_tail"] = stdout[-300:]
        rec["stderr_tail"] = stderr[-300:]
    else:
        rec["control"] = control
        rec["result"] = result
    with RECORDS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
        f.flush()
    res = result or {}
    print(f"{rec.get('error', 'ok')} root={p['root'][:8]}… {p['ordering']} "
          f"wall={wall}s nodes={res.get('nodes')} loss={res.get('loss')} capped={res.get('capped')}", flush=True)
    return 0


def gate(gates, name, ok, detail):
    gates.append({"name": name, "pass": bool(ok), "detail": detail})


def cmd_assemble(k1069_path, ext_path):
    rm = root_map(k1069_path)
    done = load_done()
    gates = []
    gate(gates, "runner-blob-pin", runner_blob() == RUNNER_BLOB_PIN, {"git_blob": runner_blob()})

    ok = True
    for root in sorted(rm):
        bit, child = canon_child(root)
        ok = ok and (int(child, 16) | (1 << bit)) == int(root, 16)
    gate(gates, "raw-child-rebuild-39", ok, {"roots": len(rm)})

    raw = Path(k1069_path).read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    gate(gates, "k1069-classification-pin",
         sha == REFUTED_SET_PIN["sha256"] and len(rm) == PUBLISHED_SUMMARY["roots"],
         {"sha256": sha, "roots": len(rm),
          "refuted": sum(1 for l in rm.values() if l == "REFUTED-D10"),
          "win": sum(1 for l in rm.values() if l.startswith("WIN"))})

    planned = {(p["root"], p["depth"], p["ordering"]) for p in probe_list(k1069_path)}
    gate(gates, "all-probes-present", planned == set(done), {
        "planned": len(planned), "present": len(done),
        "missing": sorted(f"{r[:8]}…{o}" for r, d, o in planned - set(done))})

    ok = True
    bad = []
    for key, rec in done.items():
        c = rec.get("control")
        if not c or c.get("nodes") != PILOT_D6_NODES or c.get("loss") is not False or c.get("capped") is not False:
            ok = False
            bad.append([key, c])
    gate(gates, "pilot-d6-control-all-probes", ok and len(done) == len(probe_list(k1069_path)), {"bad": bad[:5]})

    # published per-probe pin checks (fail-closed on mismatch)
    pin_ok = True
    pin_detail = []
    for root, order_map in PUBLISHED_PER_PROBE.items():
        for ordering, pub in order_map.items():
            rec = done.get((root, DEPTH, ordering))
            entry = {"root": root, "ordering": ordering, "published": pub, "status": None,
                     "ref": pub["ref"]}
            if rec is None:
                entry["status"] = "missing-record"
                pin_ok = False
            elif rec.get("error"):
                entry["status"] = rec["error"]
                pin_ok = False
            else:
                r = rec["result"]
                match = (r["nodes"] == pub["nodes"] and r["loss"] is pub["loss"]
                         and r["capped"] is pub["capped"])
                entry["observed"] = {"nodes": r["nodes"], "loss": r["loss"], "capped": r["capped"]}
                entry["status"] = "exact-reproduction" if match else "MISMATCH"
                pin_ok = pin_ok and match
            pin_detail.append(entry)
    gate(gates, "published-per-probe-pins", pin_ok, pin_detail)

    # cross-check depth-10 nodes of the 4 roots measured by the landed ext experiment
    raw_ext = Path(ext_path).read_bytes()
    ext_sha = hashlib.sha256(raw_ext).hexdigest()
    ext = json.loads(raw_ext)
    ext_map = {(e["root"], e["ordering"]): e for e in ext["cost_scaling"]}
    cross = []
    cross_ok = ext_sha == EXT_OUTPUT_SHA
    for (ex_root, ordering), e in ext_map.items():
        rec = done.get((ex_root, DEPTH, ordering))
        obs = rec.get("result", {}).get("nodes") if rec and rec.get("result") else None
        ref = e["d10"].get("nodes")
        entry = {"root": ex_root, "ordering": ordering, "ext_nodes": ref, "observed_nodes": obs}
        if obs is None or ref is None or obs != ref:
            entry["status"] = "NO-MATCH"
            cross_ok = False
        else:
            entry["status"] = "exact"
        cross.append(entry)
    gate(gates, "ext-determinism-crosscheck", cross_ok,
         {"ext_sha256": ext_sha, "checks": cross})

    # summary aggregate re-derivation
    total_nodes = 0
    max_nodes = 0
    max_key = None
    capped = 0
    errors = 0
    order_conflicts = 0
    label_ok = True
    label_bad = []
    win_roots = 0
    refuted_roots = 0
    ledger = []
    for root in sorted(rm):
        losses = []
        root_nodes = 0
        for ordering in ("andclose1", "andclose0"):
            rec = done.get((root, DEPTH, ordering))
            if rec is None or rec.get("error"):
                errors += 1
                losses.append(None)
                ledger.append({"root": root, "ordering": ordering,
                               "status": (rec or {}).get("error", "missing")})
                continue
            r = rec["result"]
            total_nodes += r["nodes"]
            root_nodes += r["nodes"]
            capped += 1 if r["capped"] else 0
            if r["nodes"] > max_nodes:
                max_nodes, max_key = r["nodes"], (root, ordering)
            losses.append(r["loss"])
            ledger.append({"root": root, "ordering": ordering, "nodes": r["nodes"],
                           "loss": r["loss"], "capped": r["capped"], "ms": r.get("ms"),
                           "wall_s": rec["wall_s"], "k1069_label": rec["k1069_label"]})
        if len(losses) == 2 and losses[0] is not None and losses[1] is not None:
            if losses[0] != losses[1]:
                order_conflicts += 1
            lab = rm[root]
            expect = True if lab.startswith("WIN") else False
            if losses[0] != expect or losses[1] != expect:
                label_ok = False
                label_bad.append({"root": root, "label": lab, "losses": losses})
            if expect and losses[0] is True:
                win_roots += 1
            elif not expect:
                refuted_roots += 1
    gate(gates, "no-probe-errors", errors == 0, {"errors": errors})
    gate(gates, "summary-aggregate-rederivation",
         (total_nodes == PUBLISHED_SUMMARY["total_nodes"] and
          max_nodes == PUBLISHED_SUMMARY["max_probe_nodes"] and
          capped == PUBLISHED_SUMMARY["capped"] and
          order_conflicts == PUBLISHED_SUMMARY["order_conflicts"] and
          win_roots == PUBLISHED_SUMMARY["win"] and
          refuted_roots == PUBLISHED_SUMMARY["refuted"]),
         {"rederived": {"total_nodes": total_nodes, "max_probe_nodes": max_nodes,
                        "max_key": max_key, "capped": capped,
                        "order_conflicts": order_conflicts, "win": win_roots,
                        "refuted": refuted_roots},
          "published": PUBLISHED_SUMMARY})
    gate(gates, "label-consistency-all-39", label_ok, {"bad": label_bad[:5]})

    by_root = []
    for root in sorted(rm):
        recs = [l for l in ledger if l["root"] == root and l.get("nodes")]
        by_root.append({"root": root, "k1069_label": rm[root],
                        "nodes": {l["ordering"]: l["nodes"] for l in recs},
                        "sum_nodes": sum(l["nodes"] for l in recs),
                        "bit": canon_child(root)[0]})

    hard = [g for g in gates if not g["pass"]]
    out = {
        "schema": SCHEMA,
        "date": "2026-11-20",
        "cap": CAP,
        "timeout_s": TIMEOUT,
        "depth": DEPTH,
        "parallelism": 1,
        "runner_git_blob": RUNNER_BLOB_PIN,
        "protocol": ("per-probe node-cost ledger re-derivation of the K1069-published "
                     "depth-10 judgments; no judging, classification or closure; same "
                     "runner/argv form as the K1075 sweep driver; pilot_d6 control "
                     "required on every probe; fail-closed against published per-probe "
                     "pins, ext double-measurements, classification labels and summary "
                     "aggregates"),
        "inputs": {
            "k1069_classification": dict(REFUTED_SET_PIN, roots=len(rm)),
            "published_per_probe_pins": PUBLISHED_PER_PROBE,
            "published_summary": PUBLISHED_SUMMARY,
            "ext_output": {"sha256": EXT_OUTPUT_SHA, "path": EXT_OUTPUT_PATH},
        },
        "gates": gates,
        "ledger": ledger,
        "by_root": by_root,
        "rederived_summary": {
            "roots": len(rm), "probes": len([l for l in ledger if l.get("nodes")]),
            "total_nodes": total_nodes, "max_probe_nodes": max_nodes,
            "max_key": list(max_key) if max_key else None,
            "capped": capped, "order_conflicts": order_conflicts,
            "win": win_roots, "refuted": refuted_roots,
            "avg_nodes_per_probe": round(total_nodes / max(1, len([l for l in ledger if l.get("nodes")])), 0),
        },
        "interpretation_guard": (
            "This is a cost ledger and published-record cross-check, not a new verdict. "
            "REFUTED-D10 is not a LOSS proof. No row is closed by this ledger. The standard "
            "11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and classes "
            "1/2/4 all remain UNKNOWN."
        ),
    }
    OUTPUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    sha = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    print(f"gates: {len(gates) - len(hard)}/{len(gates)} pass")
    for g in hard:
        print("GATE FAIL:", g["name"], json.dumps(g["detail"])[:400])
    print("output sha256:", sha)
    return 1 if hard else 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "run" and len(sys.argv) > 2:
        sys.exit(cmd_run(sys.argv[2]))
    elif mode == "assemble" and len(sys.argv) > 3:
        sys.exit(cmd_assemble(sys.argv[2], sys.argv[3]))
    sys.exit(2)
