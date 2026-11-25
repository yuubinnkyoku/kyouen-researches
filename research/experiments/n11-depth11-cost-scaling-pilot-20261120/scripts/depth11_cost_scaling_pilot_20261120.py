#!/usr/bin/env python3
"""n11 depth-11 cost-scaling pilot on published depth-10-judged roots.

Cost measurement only. This is NOT a depth-11 sweep undertaking, NOT a verdict
change, and NOT a row closure. REFUTED-D10 is not a LOSS proof. The standard
11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and classes
1/2/4 all remain UNKNOWN.

Usage:
  depth11_cost_scaling_pilot_20261120.py run       # run next unfinished probe (sequential)
  depth11_cost_scaling_pilot_20261120.py assemble   # evaluate gates, write output JSON
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
RECORDS = OUTD / "probe-records-d11pilot.jsonl"
OUTPUT = OUTD / "depth11-cost-scaling-pilot-20261120.json"
SCHEMA = "n11-depth11-cost-scaling-pilot-20261120-v1"

CAP = 30_000_000
TIMEOUT = 280
RUNNER_BLOB_PIN = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
PILOT_D6_NODES = 3402

# Published depth-10 references (main, fetched 2026-11-19):
# - K1069 39-live sweep正本 (fetched at repo pin 53b07ebe16) sha256
#   22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc
#   summary.max_probe = {root, bit 7, andclose false, nodes 14249420, capped false, loss false}
#   (REFUTED-D10; not a LOSS proof)
# - K1069 knowledge item (research/knowledge/README.md, 2026-11-20):
#   WIN7-D10 root ...0100 (bit 8, both orderings loss=true, uncapped, terminal [13,17],
#   nodes 1576372/2544178). Triple-verified certificate (K1070), receipt fold (K1071).
TARGETS = [
    {
        "root": "00000000010000809002000040000080",
        "bit": 7,
        "label": "K1069-max-probe-REFUTED-D10",
        "published_d10": {
            "andclose0": {"nodes": 14249420, "loss": False, "capped": False},
        },
        "published_refs": [
            "K1069 sweep output witness-39live-root-depth10-sweep-20261120.json summary.max_probe",
            "sha256 22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc (repo pin 53b07ebe16)",
        ],
    },
    {
        "root": "00004000000000821082000000000100",
        "bit": 8,
        "label": "K1069-K1070-WIN7-D10-seventeenth-certificate",
        "published_d10": {
            "andclose1": {"nodes": 1576372, "loss": True, "capped": False},
            "andclose0": {"nodes": 2544178, "loss": True, "capped": False},
        },
        "published_refs": [
            "K1069 knowledge item (research/knowledge/README.md 2026-11-20)",
            "K1070 seventeenth WIN7-D10 certificate triple verification",
        ],
    },
]
DEPTHS = (10, 11)
ORDERINGS = (1, 0)


def runner_blob(raw=None):
    raw = raw if raw is not None else RUNNER.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def canon_child(root_hex, bit):
    """生child hex rule: child = root minus its lowest set bit; bit = that index."""
    root = int(root_hex, 16)
    low = (root & -root).bit_length() - 1
    assert low == bit, f"bit {bit} != lowest set bit {low} of {root_hex}"
    child = root & ~(1 << bit)
    return f"{child:032x}"


def probe_list():
    out = []
    for t in TARGETS:
        child = canon_child(t["root"], t["bit"])
        t2 = dict(t)
        t2["child"] = child
        for depth in DEPTHS:
            for ordering in ORDERINGS:
                out.append({
                    "root": t["root"], "child": child, "bit": t["bit"],
                    "ordering": f"andclose{ordering}", "order_n": ordering,
                    "depth": depth, "label": t["label"],
                })
    # run cheap / reproduction probes first, expensive depth-11 last
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


def cmd_assemble():
    done = load_done()
    gates = []
    gate(gates, "runner-blob-pin", runner_blob() == RUNNER_BLOB_PIN, {"git_blob": runner_blob()})

    # raw-child rule re-derivation
    ok = True
    for t in TARGETS:
        child = canon_child(t["root"], t["bit"])
        ok = ok and (int(child, 16) | (1 << t["bit"])) == int(t["root"], 16)
        ok = ok and int(f"{t['root']}", 16) & (1 << t["bit"])
    gate(gates, "raw-child-rebuild", ok, {t["root"]: canon_child(t["root"], t["bit"]) for t in TARGETS})

    # completeness: every planned probe has exactly one record
    planned = {(p["root"], p["depth"], p["ordering"]) for p in probe_list()}
    gate(gates, "all-probes-present", planned == set(done), {
        "planned": len(planned), "present": len(done),
        "missing": sorted(f"{r[:8]}…d{d}{o}" for r, d, o in planned - set(done))})

    # pilot_d6 control on every record
    ok = True
    bad = []
    for key, rec in done.items():
        c = rec.get("control")
        if not c or c.get("nodes") != PILOT_D6_NODES or c.get("loss") is not False or c.get("capped") is not False:
            ok = False
            bad.append([key, c])
    gate(gates, "pilot-d6-control-all-probes", ok and len(done) == len(probe_list()), {"bad": bad})

    # depth-10 reproduction: exact match when the probe completed on this hardware;
    # environmental timeout is 'unverified-on-this-hardware', any value mismatch is FAIL
    repro = []
    repro_ok = True
    for t in TARGETS:
        for ordering, pub in t["published_d10"].items():
            rec = done.get((t["root"], 10, ordering))
            entry = {"root": t["root"], "ordering": ordering,
                     "published": pub, "status": None}
            if rec is None:
                entry["status"] = "missing-record"
                repro_ok = False
            elif rec.get("error") == f"timeout-{TIMEOUT}s":
                entry["status"] = "unverified-on-this-hardware-timeout"
            elif rec.get("error"):
                entry["status"] = rec["error"]
                repro_ok = False
            else:
                r = rec["result"]
                match = (r["nodes"] == pub["nodes"] and r["loss"] is pub["loss"]
                         and r["capped"] is pub["capped"])
                entry["observed"] = {"nodes": r["nodes"], "loss": r["loss"], "capped": r["capped"],
                                     "wall_s": rec["wall_s"], "ms": r.get("ms")}
                entry["status"] = "exact-reproduction" if match else "MISMATCH"
                repro_ok = repro_ok and match
            repro.append(entry)
    gate(gates, "depth10-exact-reproduction", repro_ok, repro)
    # published WIN node pair is order-ambiguous in prose; recorded mapping observed here
    win_recs = {o: done.get((TARGETS[1]["root"], 10, o)) for o in ("andclose1", "andclose0")}
    for o, rec in win_recs.items():
        if rec and rec.get("result"):
            repro.append({"root": TARGETS[1]["root"], "ordering": o,
                          "observed_nodes": rec["result"]["nodes"], "note": "order-mapping-evidence"})

    # depth-11: cost facts only, no gates on values; record conflicts as facts
    d11 = []
    for t in TARGETS:
        for ordering in ("andclose1", "andclose0"):
            rec10 = done.get((t["root"], 10, ordering))
            rec11 = done.get((t["root"], 11, ordering))
            ent = {"root": t["root"], "label": t["label"], "ordering": ordering}
            for depth, rec in ((10, rec10), (11, rec11)):
                if rec is None:
                    ent[f"d{depth}"] = {"status": "missing"}
                elif rec.get("error"):
                    ent[f"d{depth}"] = {"status": rec["error"], "wall_s": rec["wall_s"]}
                else:
                    r = rec["result"]
                    ent[f"d{depth}"] = {"nodes": r["nodes"], "loss": r["loss"],
                                        "capped": r["capped"], "ms": r.get("ms"),
                                        "wall_s": rec["wall_s"]}
            n10, n11 = ent["d10"].get("nodes"), ent["d11"].get("nodes")
            if n10 and n11:
                ent["ratio_nodes_d11_over_d10"] = round(n11 / n10, 4)
            elif n10 and ent["d11"].get("capped"):
                ent["ratio_lower_bound"] = round(CAP / n10, 4)
            l10, l11 = ent["d10"].get("loss"), ent["d11"].get("loss")
            if l10 is not None and l11 is not None and l10 != l11:
                ent["order_depth_cross_fact"] = "loss-differs-between-depths (fact, unclassified)"
            d11.append(ent)

    hard = [g for g in gates if not g["pass"]]
    doc = {
        "schema": SCHEMA,
        "date": "2026-11-20",
        "cap": CAP,
        "timeout_s": TIMEOUT,
        "parallelism": 1,
        "runner_git_blob": RUNNER_BLOB_PIN,
        "protocol": ("cost measurement only; sequential single probe per invocation; "
                      "same runner/argv form as the K1075 sweep driver with depth in {10,11}; "
                      "pilot_d6 control required on every probe; environmental timeout "
                      "recorded as unverified-on-this-hardware, never as evidence"),
        "inputs": {t["root"]: {"bit": t["bit"], "label": t["label"],
                                "published_d10": t["published_d10"],
                                "refs": t["published_refs"]} for t in TARGETS},
        "gates": gates,
        "reproduction": repro,
        "cost_scaling": d11,
        "interpretation_guard": (
            "Node counts under cap are deterministic and machine-independent cost units. "
            "Capped/timeout probes are lower bounds of cost and evidence in NO direction. "
            "This pilot changes no verdict: REFUTED-D10 is not a LOSS proof, a depth-11 "
            "loss=false is not a depth-11 closure proof, and this is not a depth-11 sweep "
            "undertaking. The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
            "S2 {59,60} and classes 1/2/4 all remain UNKNOWN."
        ),
    }
    OUTPUT.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    sha = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    print(f"gates: {len(gates) - len(hard)}/{len(gates)} pass")
    for g in hard:
        print("GATE FAIL:", g["name"], json.dumps(g["detail"])[:400])
    print("output sha256:", sha)
    return 1 if hard else 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    sys.exit(cmd_run() if mode == "run" else cmd_assemble() if mode == "assemble" else 2)
