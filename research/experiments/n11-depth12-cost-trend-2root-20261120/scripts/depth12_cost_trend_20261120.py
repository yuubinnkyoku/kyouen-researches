#!/usr/bin/env python3
"""n11 depth-12 second-difference cost trend (2 K1069 REFUTED-D10 roots, depths 10/11/12).

Cost measurement only. NOT a sweep undertaking, NOT a verdict change, NOT a
row closure. REFUTED-D10 is not a LOSS proof. The standard 11x11 empty board,
two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 all remain
UNKNOWN.

Usage:
  depth12_cost_trend_20261120.py run
  depth12_cost_trend_20261120.py assemble <path-to-k1069-sweep-json> <path-to-ext-output-json>
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
RECORDS = OUTD / "probe-records-d12trend.jsonl"
OUTPUT = OUTD / "depth12-cost-trend-2root-20261120.json"
SCHEMA = "n11-depth12-cost-trend-2root-20261120-v1"

CAP = 30_000_000
TIMEOUT = 280
RUNNER_BLOB_PIN = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
PILOT_D6_NODES = 3402

REFUTED_SET_PIN = {
    "sha256": "22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc",
    "path": "research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/output/witness-39live-root-depth10-sweep-20261120.json",
    "selection": [0, 12],
    "selection_rule": ("sorted 38 REFUTED-D10 roots of the K1069 classification, indices "
                       "{0,12} = the two cheapest roots of the landed ext measurement"),
}

TARGETS = [
    {"root": "00000000000000003800000008001220", "bit": 5, "label": "K1069-REFUTED-D10-idx0"},
    {"root": "00000000000000801202000000880100", "bit": 8, "label": "K1069-REFUTED-D10-idx12"},
]
EXT_OUTPUT_SHA = "8a584be6a145665c6230169bdc7edb51d453e9429dafe0ab9fd8fc0e579c7aa1"
EXT_OUTPUT_PATH = ("research/experiments/n11-depth11-cost-scaling-pilot-ext-20261120/"
                   "output/depth11-cost-scaling-pilot-ext-20261120.json")
DEPTHS = (10, 11, 12)
ORDERINGS = (1, 0)


def runner_blob(raw=None):
    raw = raw if raw is not None else RUNNER.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def canon_child(root_hex, bit):
    """生child hex rule: child = root minus its lowest set bit; bit = that index."""
    root = int(root_hex, 16)
    low = (root & -root).bit_length() - 1
    assert low == bit, f"bit {bit} != lowest set bit {low} of {root_hex}"
    return f"{root & ~(1 << bit):032x}"


def probe_list():
    out = []
    for t in TARGETS:
        child = canon_child(t["root"], t["bit"])
        for depth in DEPTHS:
            for ordering in ORDERINGS:
                out.append({
                    "root": t["root"], "child": child, "bit": t["bit"],
                    "ordering": f"andclose{ordering}", "order_n": ordering,
                    "depth": depth, "label": t["label"],
                })
    out.sort(key=lambda p: (p["depth"], p["order_n"]))
    return out


def load_done():
    done = {}
    if RECORDS.exists():
        for line in RECORDS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                done[(rec["root"], rec["depth"], rec["ordering"])] = rec
    return done


def cmd_run():
    done = load_done()
    todo = [p for p in probe_list() if (p["root"], p["depth"], p["ordering"]) not in done]
    if not todo:
        print("ALL PROBES DONE")
        return 0
    p = todo[0]
    rec_path = EXP / "output" / f".tmp-{p['root']}-{p['depth']}-{p['order_n']}.jsonl"
    if rec_path.exists():
        rec_path.unlink()
    cmd = ["node", "--experimental-strip-types", str(RUNNER),
           "--bits", str(p["bit"]), "--depth", str(p["depth"]), "--cap", str(CAP),
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
    rec = {"root": p["root"], "depth": p["depth"], "ordering": p["ordering"],
           "bit": p["bit"], "child": p["child"], "cap": CAP, "timeout_s": TIMEOUT,
           "label": p["label"], "wall_s": wall, "runner_blob": RUNNER_BLOB_PIN}
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
    print(f"{rec.get('error', 'ok')} root={p['root'][:8]}… d{p['depth']} {p['ordering']} "
          f"wall={wall}s nodes={res.get('nodes')} loss={res.get('loss')} capped={res.get('capped')}")
    return 0


def gate(gates, name, ok, detail):
    gates.append({"name": name, "pass": bool(ok), "detail": detail})


def cmd_assemble(k1069_path, ext_path):
    done = load_done()
    gates = []
    gate(gates, "runner-blob-pin", runner_blob() == RUNNER_BLOB_PIN, {"git_blob": runner_blob()})

    ok = True
    for t in TARGETS:
        child = canon_child(t["root"], t["bit"])
        ok = ok and (int(child, 16) | (1 << t["bit"])) == int(t["root"], 16)
    gate(gates, "raw-child-rebuild", ok,
         {t["root"]: canon_child(t["root"], t["bit"]) for t in TARGETS})

    raw = Path(k1069_path).read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    doc = json.loads(raw)
    refuted = sorted(r for r, lab in doc["classification"].items() if lab == "REFUTED-D10")
    expected = [refuted[i] for i in REFUTED_SET_PIN["selection"]]
    gate(gates, "k1069-classification-pin",
         sha == REFUTED_SET_PIN["sha256"] and len(refuted) == 38 and
         expected == [t["root"] for t in TARGETS],
         {"sha256": sha, "refuted_n": len(refuted), "selected": expected})

    # cross-check against the published ext measurement (independent re-measurement
    # of depths 10/11 must be node-exact: determinism double-measurement evidence)
    raw_ext = Path(ext_path).read_bytes()
    ext_sha = hashlib.sha256(raw_ext).hexdigest()
    ext = json.loads(raw_ext)
    ext_map = {(e["root"], e["ordering"]): e for e in ext["cost_scaling"]}
    cross = []
    cross_ok = ext_sha == EXT_OUTPUT_SHA
    for t in TARGETS:
        for ordering in ("andclose1", "andclose0"):
            e = ext_map.get((t["root"], ordering))
            if e is None:
                cross_ok = False
                cross.append({"root": t["root"], "ordering": ordering, "status": "missing-in-ext"})
                continue
            for depth in (10, 11):
                rec = done.get((t["root"], depth, ordering))
                obs = rec.get("result", {}).get("nodes") if rec and rec.get("result") else None
                ref = e[f"d{depth}"].get("nodes")
                entry = {"root": t["root"], "ordering": ordering, "depth": depth,
                         "ext_nodes": ref, "observed_nodes": obs}
                if obs is None or ref is None or obs != ref:
                    cross_ok = False
                    entry["status"] = "NO-MATCH"
                else:
                    entry["status"] = "exact"
                cross.append(entry)
    gate(gates, "ext-determinism-crosscheck", cross_ok,
         {"ext_sha256": ext_sha, "checks": cross})

    planned = {(p["root"], p["depth"], p["ordering"]) for p in probe_list()}
    gate(gates, "all-probes-present", planned == set(done), {
        "planned": len(planned), "present": len(done),
        "missing": sorted(f"{r[:8]}…d{d}{o}" for r, d, o in planned - set(done))})

    ok = True
    bad = []
    for key, rec in done.items():
        c = rec.get("control")
        if not c or c.get("nodes") != PILOT_D6_NODES or c.get("loss") is not False or c.get("capped") is not False:
            ok = False
            bad.append([key, c])
    gate(gates, "pilot-d6-control-all-probes", ok and len(done) == len(probe_list()), {"bad": bad})

    label = []
    label_ok = True
    for t in TARGETS:
        for ordering in ("andclose1", "andclose0"):
            rec = done.get((t["root"], 10, ordering))
            entry = {"root": t["root"], "ordering": ordering, "status": None}
            if rec is None:
                entry["status"] = "missing-record"
                label_ok = False
            elif rec.get("error") == f"timeout-{TIMEOUT}s":
                entry["status"] = "unverified-on-this-hardware-timeout"
            elif rec.get("error"):
                entry["status"] = rec["error"]
                label_ok = False
            else:
                r = rec["result"]
                good = r["loss"] is False and r["capped"] is False
                entry["observed"] = {"nodes": r["nodes"], "loss": r["loss"], "capped": r["capped"],
                                     "wall_s": rec["wall_s"], "ms": r.get("ms")}
                entry["status"] = "consistent-with-REFUTED-D10" if good else "MISMATCH"
                label_ok = label_ok and good
            label.append(entry)
    gate(gates, "d10-label-consistency", label_ok, label)

    trend = []
    for t in TARGETS:
        for ordering in ("andclose1", "andclose0"):
            ent = {"root": t["root"], "label": t["label"], "ordering": ordering}
            for depth in DEPTHS:
                rec = done.get((t["root"], depth, ordering))
                if rec is None:
                    ent[f"d{depth}"] = {"status": "missing"}
                elif rec.get("error"):
                    ent[f"d{depth}"] = {"status": rec["error"], "wall_s": rec["wall_s"]}
                else:
                    r = rec["result"]
                    ent[f"d{depth}"] = {"nodes": r["nodes"], "loss": r["loss"],
                                        "capped": r["capped"], "ms": r.get("ms"),
                                        "wall_s": rec["wall_s"]}
            n = {d: ent[f"d{d}"].get("nodes") for d in DEPTHS}
            if n[10] and n[11]:
                ent["ratio_d11_d10"] = round(n[11] / n[10], 4)
            if n[11] and n[12]:
                ent["ratio_d12_d11"] = round(n[12] / n[11], 4)
            if n[10] and n[12]:
                ent["ratio_d12_d10"] = round(n[12] / n[10], 4)
            losses = [ent[f"d{d}"].get("loss") for d in DEPTHS]
            if len({l for l in losses if l is not None}) > 1:
                ent["depth_cross_fact"] = "loss-differs-between-depths (fact, unclassified)"
            trend.append(ent)

    hard = [g for g in gates if not g["pass"]]
    out = {
        "schema": SCHEMA,
        "date": "2026-11-20",
        "cap": CAP,
        "timeout_s": TIMEOUT,
        "parallelism": 1,
        "runner_git_blob": RUNNER_BLOB_PIN,
        "protocol": ("cost measurement only; depths {10,11,12} per (root, ordering); same "
                     "runner/argv form as the K1075 sweep driver; pilot_d6 control required "
                     "on every probe; K1069 REFUTED-D10 label consistency gated at depth 10; "
                     "depths 10/11 re-measured here must equal the landed ext measurement "
                     "(determinism double-measurement); environmental timeout recorded as "
                     "unverified-on-this-hardware, never as evidence"),
        "inputs": {
            "k1069_classification": REFUTED_SET_PIN,
            "targets": {t["root"]: {"bit": t["bit"], "label": t["label"]} for t in TARGETS},
            "ext_output": {"sha256": EXT_OUTPUT_SHA, "path": EXT_OUTPUT_PATH},
        },
        "gates": gates,
        "d10_label_check": label,
        "cost_trend": trend,
        "interpretation_guard": (
            "Node counts under cap are deterministic and machine-independent cost units. "
            "Capped/timeout probes are lower bounds of cost and evidence in NO direction. "
            "This measurement changes no verdict: REFUTED-D10 is not a LOSS proof, a depth-11 "
            "or depth-12 loss=false is not a closure proof nor a REFUTED-D11/D12 classification, "
            "and this is not a sweep undertaking. The standard 11x11 empty board, two-stone "
            "roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN."
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
    if mode == "run":
        sys.exit(cmd_run())
    elif mode == "assemble" and len(sys.argv) > 3:
        sys.exit(cmd_assemble(sys.argv[2], sys.argv[3]))
    sys.exit(2)
