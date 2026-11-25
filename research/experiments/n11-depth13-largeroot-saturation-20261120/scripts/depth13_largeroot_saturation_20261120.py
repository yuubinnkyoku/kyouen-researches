#!/usr/bin/env python3
"""n11 depth-13 large-root saturation check (top-4 K1082-ledger roots, depths 10-13).

Cost measurement only. NOT a sweep undertaking, NOT a verdict change, NOT a
row closure. depth-13 loss values are recorded but not classified. REFUTED-D10 is not a LOSS proof. The standard 11x11 empty board,
two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 all remain
UNKNOWN.

Usage:
  depth13_largeroot_saturation_20261120.py run <path-to-ledger-output-json>
  depth13_largeroot_saturation_20261120.py assemble <k1069.json> <ledger.json> <large-root-scaling.json>
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
RECORDS = OUTD / "probe-records-d13largeroot.jsonl"
OUTPUT = OUTD / "depth13-largeroot-saturation-20261120.json"
SCHEMA = "n11-depth13-largeroot-saturation-20261120-v1"

CAP = 30_000_000
TIMEOUT = 280
RUNNER_BLOB_PIN = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
PILOT_D6_NODES = 3402

K1069_JSON_SHA = "22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc"
K1069_JSON_PATH = ("research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/"
                   "output/witness-39live-root-depth10-sweep-20261120.json")
LEDGER_SHA = "b55e5d83a0d25c06a8dcc8ffa06ce5d077bd6c225f6818423dafdf615fbf48a3"
LEDGER_PATH = ("research/experiments/n11-k1069-nodecost-ledger-20261120/"
               "output/k1069-nodecost-ledger-20261120.json")
SELECTION_RULE = ("top-4 by by_root.sum_nodes of the landed K1082 ledger, excluding the "
                  "max-probe root 00000000010000809002000040000080 already measured by the pilot")
LR_CANON_SHA = "c9927a2345edff7e6fe2e90ad1f3f255622aca7b35bb61d7876757d1fdbcecd0"
LR_CANON_PATH = ("research/experiments/n11-depth11-large-root-scaling-20261120/"
                 "output/depth11-large-root-scaling-20261120.json")

TARGETS = [
    {"root": "00000000000040809002000800100000", "bit": 20, "label": "K1082-ledger-rank1"},
    {"root": "00000000000000801202040000101000", "bit": 12, "label": "K1082-ledger-rank2"},
    {"root": "00000000000000003800000009080004", "bit": 2, "label": "K1082-ledger-rank3"},
    {"root": "00000000000000003800000009840000", "bit": 18, "label": "K1082-ledger-rank4"},
]
DEPTHS = (10, 11, 12, 13)
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


def cmd_run(ledger_path):
    ledger = json.loads(Path(ledger_path).read_bytes())
    lmap = {e["root"]: e for e in ledger["by_root"]}
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
           "label": p["label"], "wall_s": wall, "runner_blob": RUNNER_BLOB_PIN,
           "k1069_label": lmap[p["root"]]["k1069_label"] if p["root"] in lmap else None}
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
          f"wall={wall}s nodes={res.get('nodes')} loss={res.get('loss')} capped={res.get('capped')}", flush=True)
    return 0


def gate(gates, name, ok, detail):
    gates.append({"name": name, "pass": bool(ok), "detail": detail})


def cmd_assemble(k1069_path, ledger_path, lr_path):
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
    labels = doc["classification"]
    gate(gates, "k1069-classification-pin",
         sha == K1069_JSON_SHA and all(labels.get(t["root"]) == "REFUTED-D10" for t in TARGETS),
         {"sha256": sha, "labels": {t["root"]: labels.get(t["root"]) for t in TARGETS}})

    raw_led = Path(ledger_path).read_bytes()
    led_sha = hashlib.sha256(raw_led).hexdigest()
    led = json.loads(raw_led)
    ranked = [e["root"] for e in sorted(led["by_root"], key=lambda x: -x["sum_nodes"])
              if e["root"] != "00000000010000809002000040000080"][:4]
    gate(gates, "ledger-selection-pin",
         led_sha == LEDGER_SHA and ranked == [t["root"] for t in TARGETS],
         {"sha256": led_sha, "ranked": ranked, "rule": SELECTION_RULE})

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
    gate(gates, "pilot-d6-control-all-probes", ok and len(done) == len(probe_list()), {"bad": bad[:5]})

    # depth-10/11 re-measurement must equal the landed large-root scaling canonical
    raw_lr = Path(lr_path).read_bytes()
    lr_sha = hashlib.sha256(raw_lr).hexdigest()
    lr = json.loads(raw_lr)
    lr_map = {(e["root"], e["ordering"]): e for e in lr["cost_scaling"]}
    lr_cross = []
    lr_ok = lr_sha == LR_CANON_SHA
    for t in TARGETS:
        for ordering in ("andclose1", "andclose0"):
            e = lr_map.get((t["root"], ordering))
            if e is None:
                lr_ok = False
                lr_cross.append({"root": t["root"], "ordering": ordering, "status": "missing-in-canonical"})
                continue
            for depth in (10, 11):
                rec = done.get((t["root"], depth, ordering))
                obs = rec.get("result", {}).get("nodes") if rec and rec.get("result") else None
                ref = e[f"d{depth}"].get("nodes")
                entry = {"root": t["root"], "ordering": ordering, "depth": depth,
                         "canonical_nodes": ref, "observed_nodes": obs}
                if obs is None or ref is None or obs != ref:
                    entry["status"] = "NO-MATCH"
                    lr_ok = False
                else:
                    entry["status"] = "exact"
                lr_cross.append(entry)
    gate(gates, "largeroot-scaling-crosscheck", lr_ok,
         {"canonical_sha256": lr_sha, "checks": lr_cross})

    # depth-10 re-measurement must equal the landed ledger exactly
    lmap = {e["root"]: e for e in led["by_root"]}
    cross = []
    cross_ok = True
    for t in TARGETS:
        e = lmap.get(t["root"])
        if e is None:
            cross_ok = False
            continue
        for ordering in ("andclose1", "andclose0"):
            rec = done.get((t["root"], 10, ordering))
            obs = rec.get("result", {}).get("nodes") if rec and rec.get("result") else None
            ref = e["nodes"].get(ordering)
            loss_obs = rec.get("result", {}).get("loss") if rec and rec.get("result") else None
            entry = {"root": t["root"], "ordering": ordering, "ledger_nodes": ref,
                     "observed_nodes": obs, "loss": loss_obs}
            if obs is None or ref is None or obs != ref or loss_obs is not False:
                entry["status"] = "NO-MATCH"
                cross_ok = False
            else:
                entry["status"] = "exact"
            cross.append(entry)
    gate(gates, "ledger-determinism-crosscheck", cross_ok, cross)

    scaling = []
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
            n10 = ent["d10"].get("nodes")
            n11 = ent["d11"].get("nodes")
            n12 = ent["d12"].get("nodes")
            n13 = ent["d13"].get("nodes")
            if n10 and n11:
                ent["ratio_d11_d10"] = round(n11 / n10, 4)
            if n11 and n12:
                ent["ratio_d12_d11"] = round(n12 / n11, 4)
            if n12 and n13:
                ent["ratio_d13_d12"] = round(n13 / n12, 4)
            if n10 and n13:
                ent["ratio_d13_d10"] = round(n13 / n10, 4)
            losses = [ent[f"d{d}"].get("loss") for d in DEPTHS]
            if len({l for l in losses if l is not None}) > 1:
                ent["depth_cross_fact"] = "loss-differs-between-depths (fact, unclassified)"
            scaling.append(ent)

    hard = [g for g in gates if not g["pass"]]
    out = {
        "schema": SCHEMA,
        "date": "2026-11-20",
        "cap": CAP,
        "timeout_s": TIMEOUT,
        "parallelism": 1,
        "runner_git_blob": RUNNER_BLOB_PIN,
        "protocol": ("cost measurement only; top-4 large roots of the landed K1082 ledger; "
                     "depths {10,11,12,13} per (root, ordering); same runner/argv form as the "
                     "K1075 sweep driver; pilot_d6 control required; depth-10 re-measurement "
                     "must equal the published ledger node-exactly, and depth-10/11 must equal "
                     "the landed large-root scaling canonical node-exactly (fail-closed)"),
        "inputs": {
            "k1069_classification": {"sha256": K1069_JSON_SHA, "path": K1069_JSON_PATH},
            "ledger": {"sha256": LEDGER_SHA, "path": LEDGER_PATH},
            "selection_rule": SELECTION_RULE,
            "large_root_scaling_canonical": {"sha256": LR_CANON_SHA, "path": LR_CANON_PATH},
            "targets": {t["root"]: {"bit": t["bit"], "label": t["label"]} for t in TARGETS},
        },
        "gates": gates,
        "cost_scaling": scaling,
        "interpretation_guard": (
            "Node counts under cap are deterministic and machine-independent cost units. "
            "Capped/timeout probes are lower bounds of cost and evidence in NO direction. "
            "This measurement changes no verdict: a depth-11, depth-12 or depth-13 loss=false "
            "is not a closure proof nor a REFUTED-D11/D12/D13 classification. REFUTED-D10 is "
            "not a LOSS proof. The "
            "standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and "
            "classes 1/2/4 all remain UNKNOWN."
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
    elif mode == "assemble" and len(sys.argv) > 4:
        sys.exit(cmd_assemble(sys.argv[2], sys.argv[3], sys.argv[4]))
    sys.exit(2)
