#!/usr/bin/env python3
"""Resumable, single-worker depth-10 sweep of K1041's 18-root witness.

Pinned inputs:
- K1041 refold JSON: Git blob dd2e8516c1b7424576a15bbbec6fcd38f4e0ba23
- runner v17: Git blob c132cc6425eee3feaeef1d697dd74f968cfedb59

The dedicated LXC has one vCPU, so probes run sequentially.
Each probe starts a fresh engine and must pass the pilot_d6 control.
"""
from __future__ import annotations
import hashlib, itertools, json, os, subprocess, sys, time
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[2]
INPUT = REPO / "research/experiments/n11-head1410-fifth-sixth-win7-receipt-fold-20261119/output/refuted-excluded-cover-refold-after-fifth-sixth-receipt-20261119.json"
RUNNER = REPO / "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_runner_v17.ts"
OUT = BASE / "output"
VERDICTS = OUT / "verdicts"
INPUT_BLOB = "dd2e8516c1b7424576a15bbbec6fcd38f4e0ba23"
RUNNER_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
CAP = 30_000_000
DEPTH = 10
MODES = (1, 0)
PILOT = {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}

def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()

def det_bareiss(a):
    a = [list(map(int, row)) for row in a]
    n = len(a)
    sign, prev = 1, 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot_row = next((i for i in range(k + 1, n) if a[i][k] != 0), None)
            if pivot_row is None:
                return 0
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = a[i][j] * pivot - a[i][k] * a[k][j]
                if num % prev:
                    raise ArithmeticError("Bareiss non-exact division")
                a[i][j] = num // prev
        for i in range(k + 1, n):
            a[i][k] = 0
        prev = pivot
    return sign * a[n - 1][n - 1]

def transform_xy(x, y, t):
    if t == 0: return x, y
    if t == 1: return 10-y, x
    if t == 2: return 10-x, 10-y
    if t == 3: return y, 10-x
    if t == 4: return 10-x, y
    if t == 5: return x, 10-y
    if t == 6: return y, x
    return 10-y, 10-x

def d4_canonical(mask):
    images = []
    for t in range(8):
        v = 0
        for i in range(121):
            if (mask >> i) & 1:
                x, y = i % 11, i // 11
                xx, yy = transform_xy(x, y, t)
                v |= 1 << (yy * 11 + xx)
        images.append(v)
    return mask == min(images)

def root_safety(mask):
    pts = [(i % 11, i // 11) for i in range(121) if (mask >> i) & 1]
    bad = []
    for q in itertools.combinations(pts, 4):
        mat = [[x, y, x*x + y*y, 1] for x, y in q]
        if det_bareiss(mat) == 0:
            bad.append(q)
    return len(pts), bad

def load_inputs():
    ib, rb = INPUT.read_bytes(), RUNNER.read_bytes()
    ish, rsh = git_blob_sha1(ib), git_blob_sha1(rb)
    if ish != INPUT_BLOB:
        raise RuntimeError(f"input Git blob mismatch: {ish} != {INPUT_BLOB}")
    if rsh != RUNNER_BLOB:
        raise RuntimeError(f"runner Git blob mismatch: {rsh} != {RUNNER_BLOB}")
    data = json.loads(ib)
    roots = data["witness_sweep_plan"]["untested_witness_roots"]
    checks = {x["root"]: x for x in data["root_checks"]}
    rows = {x["root"]: x["rows"] for x in data["witness"]}
    if len(roots) != 18 or data["witness_sweep_plan"]["untested_witness_rows_coverable"] != 30:
        raise RuntimeError("K1041 witness plan shape changed")
    if data["resolve"]["stranded_rows"] != 57 or data["resolve"]["stranded_classification"]["structural_rows"] != 53:
        raise RuntimeError("K1041 residual classification changed")
    preflight = []
    for h in roots:
        m = int(h, 16)
        n, bad = root_safety(m)
        c = checks[h]
        canonical = d4_canonical(m)
        ok = (len(h) == 32 and m < (1 << 121) and m.bit_count() == 7
              and n == 7 and not bad and c["stones"] == 7
              and c["unsafe_quadruples"] == 0 and c["d4_canonical"] is True
              and canonical and len(rows[h]) in (1, 2))
        preflight.append({"root":h,"stones":n,"unsafe_quadruples":len(bad),
                          "published_d4_canonical":c["d4_canonical"],
                          "independent_d4_canonical":canonical,"pass":ok})
        if not ok:
            raise RuntimeError(f"root preflight failed: {preflight[-1]}")
    return ib, rb, roots, rows, preflight

def read_probe(path, root, mode):
    try:
        d = json.loads(path.read_text())
        if (d.get("root") == root and d.get("andclose") == mode
            and d.get("engine_blob") == RUNNER_BLOB
            and d.get("input_blob") == INPUT_BLOB
            and d.get("pilot_control") == PILOT
            and isinstance(d.get("result"), dict)):
            return d
    except Exception:
        pass
    return None

def write_json_atomic(path, obj):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n")
    os.replace(tmp, path)

def summarize(roots, rows, done, preflight, failures, ib, rb):
    root_rows = []
    win = refuted = capped = pending = conflicts = 0
    for root in roots:
        a, b = done.get((root, 1)), done.get((root, 0))
        if a and b:
            ra, rb2 = a["result"], b["result"]
            if not ra["capped"] and not rb2["capped"] and ra["loss"] is True and rb2["loss"] is True:
                cls = "WIN7-D10"; win += 1
            elif not ra["capped"] and not rb2["capped"] and ra["loss"] is False and rb2["loss"] is False:
                cls = "REFUTED-D10"; refuted += 1
            elif ra["capped"] or rb2["capped"]:
                cls = "CAPPED"; capped += 1
            else:
                cls = "ORDERING_CONFLICT"; conflicts += 1
            root_rows.append({"root":root,"covered_residual_rows":rows[root],
                              "andclose1":ra,"andclose0":rb2,"classification":cls})
        else:
            pending += 1
            root_rows.append({"root":root,"covered_residual_rows":rows[root],
                              "andclose1":a["result"] if a else None,
                              "andclose0":b["result"] if b else None,
                              "classification":"PENDING"})
    total_nodes = sum(x["result"]["nodes"] for x in done.values())
    checks = [
        {"name":"pinned K1041 input Git blob matches","pass":git_blob_sha1(ib)==INPUT_BLOB},
        {"name":"pinned runner v17 Git blob matches","pass":git_blob_sha1(rb)==RUNNER_BLOB},
        {"name":"all 18 roots pass independent 7-stone, no-unsafe-quadruple and D4-canonical checks","pass":len(preflight)==18 and all(x["pass"] for x in preflight)},
        {"name":"all completed probes pass pilot_d6 control","pass":all(x["pilot_control"]==PILOT for x in done.values())},
        {"name":"no WIN/REFUTED ordering conflict","pass":conflicts==0},
        {"name":"all 36 probes completed","pass":len(done)==36 and pending==0},
    ]
    return {
        "schema":"n11-k1041-18-root-witness-depth10-sweep-20261119-v1",
        "date":"2026-11-19",
        "status":"sweep-complete" if len(done)==36 and pending==0 else "partial",
        "input":{"path":str(INPUT.relative_to(REPO)),"git_blob_sha1":INPUT_BLOB},
        "engine":{"path":str(RUNNER.relative_to(REPO)),"git_blob_sha1":RUNNER_BLOB,
                  "depth":DEPTH,"cap":CAP,"orderings":["andclose1","andclose0"],"workers":1},
        "candidate_pool":{"source":"K1041 witness_sweep_plan.untested_witness_roots",
                          "root_count":18,"coverable_rows":30,"eligible_candidates":32,
                          "stranded_rows":57,"structural_rows":53},
        "probe_count":len(done),"total_probes":36,"total_nodes":total_nodes,
        "classification":{"counted_roots":win+refuted+capped+conflicts,
                          "win7_d10":{"count":win},"refuted_d10":{"count":refuted},
                          "capped":{"count":capped},"ordering_conflicts":{"count":conflicts},
                          "pending_roots":pending},
        "root_preflight":preflight,"roots":root_rows,"failures":failures,
        "checks":checks,"all_pass":all(x["pass"] for x in checks),
        "interpretation_guard":[
            "WIN7-D10 is a constructive strategy result; it must be extracted and independently verified before receipt fold.",
            "REFUTED-D10 is only a complete no-win-within-depth-10 result at this seven-stone root; it is not a LOSS proof for an upstream S6/S5 parent.",
            "CAPPED, timeout, process failure, pilot failure, or ordering conflict supplies no verdict.",
            "A candidate witness root is not a certificate; only an independently verified WIN7-D10 certificate can close its declared S6 row.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
        ]
    }

def main():
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 3300.0
    OUT.mkdir(parents=True, exist_ok=True)
    VERDICTS.mkdir(parents=True, exist_ok=True)
    ib, rb, roots, rows, preflight = load_inputs()
    t0 = time.monotonic()
    done = {}
    for root in roots:
        for mode in MODES:
            p = VERDICTS / f"{root}.andclose{mode}.json"
            old = read_probe(p, root, mode)
            if old:
                done[(root, mode)] = old
    todo = [(root, mode) for mode in MODES for root in roots if (root, mode) not in done]
    print(json.dumps({"event":"start","roots":len(roots),"completed":len(done),
                      "remaining":len(todo),"cap":CAP,"depth":DEPTH,"workers":1,
                      "input_blob":INPUT_BLOB,"runner_blob":RUNNER_BLOB}), flush=True)
    for root, mode in todo:
        if time.monotonic() - t0 >= budget:
            print(json.dumps({"event":"budget_stop","completed":len(done),
                              "remaining":sum((r,m) not in done for r,m in todo)}), flush=True)
            break
        m = int(root, 16)
        bit = m.bit_length() - 1
        child = f"{m ^ (1 << bit):032x}"
        raw = OUT / "raw" / f"{root}.andclose{mode}.jsonl"
        raw.parent.mkdir(parents=True, exist_ok=True)
        if raw.exists(): raw.unlink()
        cmd = ["node","--experimental-strip-types",str(RUNNER),"--child",child,
               "--bits",str(bit),"--depth",str(DEPTH),"--cap",str(CAP),
               "--andclose",str(mode),"--out",str(raw)]
        started = time.monotonic()
        try:
            p = subprocess.run(cmd,capture_output=True,text=True,timeout=1800)
        except subprocess.TimeoutExpired:
            failures = {"root":root,"andclose":mode,"status":"TIMEOUT","child":child,"bit":bit}
            with open(OUT/"failures.jsonl","a") as f:
                f.write(json.dumps(failures,sort_keys=True)+"\n"); f.flush(); os.fsync(f.fileno())
            print(json.dumps(failures),flush=True)
            continue
        lines = [s for s in p.stdout.splitlines() if s.strip()]
        if p.returncode != 0 or len(lines) != 2:
            failure = {"root":root,"andclose":mode,"status":"PROCESS_FAIL",
                       "returncode":p.returncode,"stderr_tail":p.stderr[-1200:],
                       "stdout_lines":lines[-3:]}
            with open(OUT/"failures.jsonl","a") as f:
                f.write(json.dumps(failure,sort_keys=True)+"\n"); f.flush(); os.fsync(f.fileno())
            print(json.dumps(failure),flush=True)
            continue
        control, result = map(json.loads,lines)
        if control.get("control")!="pilot_d6" or control.get("loss") is not False or control.get("nodes")!=3402 or control.get("capped"):
            failure={"root":root,"andclose":mode,"status":"PILOT_FAIL","control":control,"result":result}
            with open(OUT/"failures.jsonl","a") as f:
                f.write(json.dumps(failure,sort_keys=True)+"\n"); f.flush(); os.fsync(f.fileno())
            print(json.dumps(failure),flush=True)
            continue
        if result.get("bit")!=bit or result.get("capped") not in (True,False) or not isinstance(result.get("loss"),bool):
            raise RuntimeError(f"malformed runner result {root} mode {mode}: {result}")
        rec={"root":root,"covered_residual_rows":rows[root],"andclose":mode,
             "ordering":f"andclose{mode}","child":child,"bit":bit,"cap":CAP,"depth":DEPTH,
             "engine_blob":RUNNER_BLOB,"input_blob":INPUT_BLOB,
             "pilot_control":control,"result":result,
             "elapsed_ms_observed":round((time.monotonic()-started)*1000)}
        write_json_atomic(VERDICTS/f"{root}.andclose{mode}.json",rec)
        done[(root,mode)]=rec
        failures=[]
        fp=OUT/"failures.jsonl"
        if fp.exists():
            failures=[json.loads(x) for x in fp.read_text().splitlines() if x.strip()]
        summary=summarize(roots,rows,done,preflight,failures,ib,rb)
        write_json_atomic(OUT/"summary.partial.json",summary)
        print(json.dumps({"event":"probe_done","root":root,"andclose":mode,
                          "loss":result["loss"],"nodes":result["nodes"],
                          "capped":result["capped"],
                          "terminal":result.get("terminalStoneRange"),
                          "elapsed_ms_observed":rec["elapsed_ms_observed"]}),flush=True)
    failures=[]
    fp=OUT/"failures.jsonl"
    if fp.exists():
        failures=[json.loads(x) for x in fp.read_text().splitlines() if x.strip()]
    summary=summarize(roots,rows,done,preflight,failures,ib,rb)
    records=[done[(root,mode)] for mode in MODES for root in roots if (root,mode) in done]
    (OUT/"probe-records.jsonl").write_text("".join(json.dumps(x,sort_keys=True,separators=(",",":"))+"\n" for x in records))
    write_json_atomic(OUT/("summary.json" if summary["status"]=="sweep-complete" else "summary.partial.json"),summary)
    print(json.dumps({"event":"finish_or_pause","completed_probes":len(done),
                      "total_probes":36,"completed_roots":summary["classification"]["counted_roots"],
                      "status":summary["status"],"all_pass":summary["all_pass"]}),flush=True)

if __name__=="__main__":
    main()
