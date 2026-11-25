"""S1 pilot driver: multivalued WalkSAT over the fixed-d ternary CNF.

Builds, per d, the base-clause "problem" file for walksat.cpp, cross-checks the
walker's evaluation against the encoded CNF variable space, and runs the pilot
(warm / random init).

Problem-file semantics mirror ternary_general.clauses_for_pair and encode():
  - free pair v = min(t, p-t) in 1..h, v != d, remapped to 0..N-1;
  - side 0 = low (original literal +v), side 1 = high (original literal -v);
  - a clause is violated iff every listed (pair, side) currently matches;
  - state value 2 for a pair means empty (neither low nor high).
"""
from __future__ import annotations
import argparse
import json
import random
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(HERE))
from ternary_general import (base_clauses, encode, load_edges,  # noqa: E402
                             EDGES_GZ_SHA, EDGES_TXT_SHA)

P, H = 2647, 1323
TARGET = 1322
EMPTY_BOUND = H + 2 - TARGET  # 3
WARM = HERE.parent / "parabola-local-repair-20261109/output/walk-1000000-seed20261109/candidate.txt"


def build_problem(d, original, out_path):
    free = [v for v in range(1, H + 1) if v != d]
    idx = {v: i for i, v in enumerate(free)}
    assert all(len(c) >= 1 for c in original), "empty base clause"
    lines = [f"p {len(free)} {len(original)}\n"]
    for clause in original:
        parts = [str(len(clause))]
        for lit in clause:
            v = abs(lit)
            side = 1 if lit < 0 else 0  # -v requires high, +v requires low
            parts.append(str(idx[v]))
            parts.append(str(side))
        lines.append(" ".join(parts) + "\n")
    out_path.write_text("".join(lines), encoding="ascii", newline="\n")
    return free


def state_from_params(free, params):
    chosen = set(params)
    return [0 if v in chosen else 1 if (P - v) in chosen else 2 for v in free]


def reconstruct_params(free, d, state):
    params = {0, d, P - d}
    for v, s in zip(free, state):
        if s == 0:
            params.add(v)
        elif s == 1:
            params.add(P - v)
    return sorted(params)


def count_violations_literal(free, original, state):
    """A base clause is violated iff every requirement holds (negative clause)."""
    pos = dict(zip(free, state))
    bad = 0
    for clause in original:
        if all((lit > 0 and pos[abs(lit)] == 0) or (lit < 0 and pos[abs(lit)] == 1)
               for lit in clause):
            bad += 1
    return bad


def count_base_unsat_encoded(clauses, nbase, free, state):
    positive = set()
    for v, s in zip(free, state):
        positive.add(v if s == 0 else H + v if s == 1 else 2 * H + v)
    return sum(not any((lit > 0) == (abs(lit) in positive) for lit in clause)
               for clause in clauses[:nbase])


def save_state(path, state):
    path.write_text(" ".join(map(str, state)) + "\n", encoding="ascii", newline="\n")


def load_state(path):
    return list(map(int, path.read_text().split()))


def run_walker(exe, problem, *, init_state=None, random_init=False, eval_state=None,
               flips=None, seed=None, best_state=None, trace_every=None,
               lam=None, noise=None, bound=None, restart_every=None, stagnation=None):
    cmd = [str(exe), "--problem", str(problem)]
    if eval_state is not None:
        cmd += ["--eval", str(eval_state)]
    if random_init:
        cmd.append("--random")
    elif init_state is not None:
        cmd += ["--init", str(init_state)]
    if flips is not None:
        cmd += ["--flips", str(flips)]
    if seed is not None:
        cmd += ["--seed", str(seed)]
    if lam is not None:
        cmd += ["--lambda", str(lam)]
    if noise is not None:
        cmd += ["--noise", str(noise)]
    if bound is not None:
        cmd += ["--bound", str(bound)]
    if best_state is not None:
        cmd += ["--best-state", str(best_state)]
    if trace_every:
        cmd += ["--trace-every", str(trace_every)]
    run = subprocess.run(cmd, capture_output=True, text=True, check=True)
    trace = []
    result = None
    for line in run.stdout.splitlines():
        if line.startswith("trace "):
            _, step, v, e = line.split()
            trace.append([int(step), int(v), int(e)])
        elif line.strip():
            result = json.loads(line)
    if result is None:
        raise RuntimeError(f"no result from walker: {run.stderr}")
    if trace:
        result["trace"] = trace
    return result


def read_dimacs(path):
    import gzip
    if str(path).endswith(".gz"):
        text = gzip.decompress(Path(path).read_bytes()).decode("ascii")
    else:
        text = Path(path).read_text(encoding="ascii")
    clauses = []
    for line in text.splitlines():
        if not line or line[0] in "cp":
            continue
        clauses.append([int(x) for x in line.split()[:-1]])
    return clauses


def count_unsat(clauses, positive):
    return sum(not any((lit > 0) == (abs(lit) in positive) for lit in clause)
               for clause in clauses)


def cmd_check_eval(args):
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    exe = Path(args.exe)
    report = {"ds": args.ds, "seeds": args.seeds, "random_states_per_seed": args.states,
              "edges_gz_sha256": EDGES_GZ_SHA, "edges_txt_sha256": EDGES_TXT_SHA, "d": {}}
    all_ok = True
    warm = list(map(int, WARM.read_bytes().split()))
    assert warm[0] == P and warm[1] == len(warm) - 2 == 1292
    for d in args.ds:
        original = base_clauses(P, d, load_edges())
        assert len(original) == 53886
        clauses, _ = encode(P, d, original)
        free = build_problem(d, original, out / f"problem-d{d}.txt")
        # cross-check the encoded base prefix against the saved ladder CNF, if present
        saved = args.cnf_dir / f"ladder-d{d}-target1322-budget20000000/input.cnf.gz" if args.cnf_dir else None
        saved_ok = None
        if saved is not None and saved.exists():
            sc = read_dimacs(saved)
            saved_ok = (sc[:len(original)] == clauses[:len(original)])
            all_ok &= saved_ok
        checks = [("warm", state_from_params(free, warm[2:]))]
        for seed in args.seeds:
            rng = random.Random(seed * 1000003 + d)
            for k in range(args.states):
                checks.append((f"random-seed{seed}-{k}", [rng.randrange(3) for _ in free]))
        rows = []
        for name, state in checks:
            sp = out / f"state-d{d}-{name}.txt"
            save_state(sp, state)
            walker = run_walker(exe, out / f"problem-d{d}.txt", eval_state=sp)
            lit = count_violations_literal(free, original, state)
            enc = count_base_unsat_encoded(clauses, len(original), free, state)
            emp = sum(s == 2 for s in state)
            ok = walker["base_violations"] == lit == enc and walker["empties"] == emp
            all_ok &= ok
            rows.append({"case": name, "walker": walker["base_violations"],
                         "literal": lit, "encoded": enc,
                         "empties_walker": walker["empties"], "empties_py": emp, "ok": ok})
        report["d"][str(d)] = rows
        report.setdefault("saved_cnf_prefix_match", {})[str(d)] = saved_ok
    report["all_ok"] = all_ok
    report["states_total"] = sum(len(v) for v in report["d"].values())
    (out / "eval-check.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"all_ok": all_ok, "states_total": report["states_total"],
                      "saved_cnf_prefix_match": report["saved_cnf_prefix_match"]}))
    return 0 if all_ok else 1


def cmd_pilot(args):
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    exe = Path(args.exe)
    warm = list(map(int, WARM.read_bytes().split()))
    assert warm[0] == P and warm[1] == 1292
    rows = []
    for d in args.ds:
        original = base_clauses(P, d, load_edges())
        problem = out / f"problem-d{d}.txt"
        free = build_problem(d, original, problem)
        init_path = out / f"warm-d{d}.txt"
        save_state(init_path, state_from_params(free, warm[2:]))
        for kind in ("warm", "random"):
            for seed in args.seeds:
                best_state = out / f"beststate-d{d}-{kind}-seed{seed}.txt"
                res = run_walker(exe, problem,
                                 init_state=init_path if kind == "warm" else None,
                                 random_init=(kind == "random"),
                                 flips=args.flips, seed=seed, best_state=best_state,
                                 trace_every=args.trace_every,
                                 lam=args.lam, noise=args.noise, bound=args.bound)
                row = {"d": d, "kind": kind, "seed": seed, "flips": args.flips,
                       "lambda": args.lam, "noise": args.noise, "bound": args.bound,
                       "base_violations_best": res["base_violations_best"],
                       "empties_at_best": res["empties_at_best"], "best_step": res["best_step"],
                       "seconds": res["seconds"], "fps": args.flips / res["seconds"],
                       "solved": res["solved"], "trace": res.get("trace", [])}
                if res["solved"]:
                    st = load_state(best_state)
                    params = reconstruct_params(free, d, st)
                    row["params_size"] = len(params)
                    row["candidate"] = f"candidate-d{d}-{kind}-seed{seed}.txt"
                    (out / row["candidate"]).write_text(
                        f"{P} {len(params)}\n" + " ".join(map(str, params)) + "\n",
                        encoding="ascii", newline="\n")
                    row["empty_pairs"] = [v for v, s in zip(free, st) if s == 2]
                rows.append(row)
                print(json.dumps({k: v for k, v in row.items() if k != "trace"}), flush=True)
                (out / "pilot-results.json").write_text(
                    json.dumps(rows, indent=2) + "\n", encoding="utf-8", newline="\n")
                if res["solved"]:
                    print("SOLVED " + json.dumps(row), flush=True)
                    return 0
    return 0


def unit_path(out: Path, d: int, seed: int, noise: float, run: int) -> Path:
    """One (d, seed, noise, run) unit -> one JSON file. Resume = skip if present."""
    return out / f"deep-d{d}-seed{seed}-noise{noise:g}-run{run:02d}.json"


def block_stop_path(out: Path, d: int, seed: int, noise: float) -> Path:
    """Stop marker for one (d, seed, noise) block (W35 §2: 3 restarts without a
    d-level global-best improvement). Its presence makes --resume skip the block."""
    return out / f"deep-stop-d{d}-seed{seed}-noise{noise:g}.json"


def d_level_best(units_dir: Path, d: int) -> int | None:
    """Global best base violations over the finished units of d (None if none)."""
    best = None
    for r in load_units(units_dir, d):
        if best is None or r["base_violations_best"] < best:
            best = r["base_violations_best"]
    return best


def load_units(units_dir: Path, d: int) -> list[dict]:
    """All finished unit rows of d, in (seed, noise, run) order."""
    rows = []
    for p in units_dir.glob(f"deep-d{d}-seed*-noise*-run*.json"):
        try:
            r = json.loads(p.read_text())
        except json.JSONDecodeError:
            continue
        if r.get("d") == d:
            rows.append(r)
    rows.sort(key=lambda r: (r["seed"], r["noise"], r["run"]))
    return rows


def _same_noise(a: float, b: float) -> bool:
    return abs(float(a) - float(b)) < 1e-12


def block_progress(rows: list[dict], seed: int, noise: float, runs: int) -> tuple[int, int]:
    """Replay one (d, seed, noise) block in run order.

    Returns (next_run, consecutive_non_improve). The d-level best entering the
    block is the best over the *other* blocks' finished units, so a resume that
    replays the same files reaches the same streak counter as the live run
    (W35 §2: stop a block after 3 restarts without a d-level improvement).
    """
    cur = None
    for r in rows:
        if r["seed"] == seed and _same_noise(r["noise"], noise):
            continue
        if cur is None or r["base_violations_best"] < cur:
            cur = r["base_violations_best"]
    streak = 0
    next_run = 0
    for run in range(runs):
        row = next((x for x in rows if x["seed"] == seed
                    and _same_noise(x["noise"], noise) and x["run"] == run), None)
        if row is None:
            break
        b = row["base_violations_best"]
        if cur is None or b < cur:
            cur = b
            streak = 0
        else:
            streak += 1
        next_run = run + 1
    return next_run, streak


def cmd_deep(args):
    """Resumable D1 runner: one process per (d, seed, noise, run) unit.

    Each unit is `--flips-per-run` flips (one restart segment). Its init is
    warm when run is even, random when odd (W35 §2 restart policy), with the
    per-unit seed derived from (seed, run) so reruns are reproducible.
    A unit's JSON is written atomically after it finishes; an interrupted VM
    loses at most the unit in flight.

    `--max-seconds` bounds one job (W35 §3: jobs stay under the ~2 h VM restart
    window); the job exits cleanly with the remaining unit count and
    `--resume` continues from there. `--block-patience` stops a (d, seed,
    noise) block once that many consecutive restarts failed to improve the
    d-level best.
    """
    import time as _time
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    exe = Path(args.exe)
    warm = list(map(int, WARM.read_bytes().split()))
    assert warm[0] == P and warm[1] == 1292
    done = 0
    skipped_blocks = 0
    ran = []
    stopped_by_cap = False
    t_job = _time.monotonic()

    def out_of_time() -> bool:
        return args.max_seconds > 0 and (_time.monotonic() - t_job) >= args.max_seconds

    for d in args.ds:
        original = base_clauses(P, d, load_edges())
        problem = out / f"problem-d{d}.txt"
        if not problem.exists():
            free = build_problem(d, original, problem)
        else:
            free = [v for v in range(1, H + 1) if v != d]
        init_path = out / f"warm-d{d}.txt"
        if not init_path.exists():
            save_state(init_path, state_from_params(free, warm[2:]))
        for noise in args.noises:
            for seed in args.seeds:
                stop = block_stop_path(out, d, seed, noise)
                if stop.exists():
                    skipped_blocks += 1
                    continue
                rows = load_units(out, d)
                start_run, streak = block_progress(rows, seed, noise, args.runs)
                if start_run >= args.runs:
                    continue
                if streak >= args.block_patience:
                    _write_block_stop(stop, d, seed, noise, streak, start_run,
                                      d_level_best(out, d))
                    print(f"block-stop d={d} seed={seed} noise={noise:g} "
                          f"streak={streak}", flush=True)
                    continue
                for run in range(start_run, args.runs):
                    if out_of_time():
                        stopped_by_cap = True
                        break
                    up = unit_path(out, d, seed, noise, run)
                    if up.exists():
                        done += 1
                        continue
                    warm_run = (run % 2 == 0)
                    best_before = d_level_best(out, d)
                    best_state = out / f"beststate-d{d}-seed{seed}-noise{noise:g}-run{run:02d}.txt"
                    res = run_walker(exe, problem,
                                     init_state=init_path if warm_run else None,
                                     random_init=not warm_run,
                                     flips=args.flips_per_run,
                                     seed=seed * 1000003 + run,
                                     best_state=best_state,
                                     trace_every=args.trace_every,
                                     lam=args.lam, noise=noise, bound=args.bound,
                                     restart_every=args.restart_every,
                                     stagnation=args.stagnation)
                    row = {"d": d, "seed": seed, "noise": noise, "run": run,
                           "init": "warm" if warm_run else "random",
                           "flips": args.flips_per_run, "lambda": args.lam,
                           "bound": args.bound,
                           "base_violations_best": res["base_violations_best"],
                           "empties_at_best": res["empties_at_best"],
                           "best_step": res["best_step"],
                           "flips_run": res.get("flips_run", args.flips_per_run),
                           "restarts": res.get("restarts", 1),
                           "seconds": res["seconds"],
                           "fps": res.get("flips_run", args.flips_per_run) / res["seconds"],
                           "solved": res["solved"],
                           "best_state": best_state.name}
                    if res.get("trace"):
                        row["trace"] = res["trace"]
                    if res["solved"]:
                        st = load_state(best_state)
                        params = reconstruct_params(free, d, st)
                        row["params_size"] = len(params)
                        row["candidate"] = f"candidate-d{d}-seed{seed}-noise{noise:g}-run{run:02d}.txt"
                        (out / row["candidate"]).write_text(
                            f"{P} {len(params)}\n" + " ".join(map(str, params)) + "\n",
                            encoding="ascii", newline="\n")
                    tmp = up.with_suffix(".json.tmp")
                    tmp.write_text(json.dumps(row, indent=2) + "\n", encoding="utf-8", newline="\n")
                    tmp.replace(up)
                    ran.append(row)
                    print(json.dumps(row), flush=True)
                    if res["solved"]:
                        print("SOLVED " + json.dumps(row), flush=True)
                        return 0
                    improved = best_before is None or row["base_violations_best"] < best_before
                    streak = 0 if improved else streak + 1
                    if streak >= args.block_patience:
                        _write_block_stop(stop, d, seed, noise, streak, run + 1,
                                          d_level_best(out, d))
                        print(f"block-stop d={d} seed={seed} noise={noise:g} "
                              f"streak={streak}", flush=True)
                        break
                if stopped_by_cap:
                    break
            if stopped_by_cap:
                break
        if stopped_by_cap:
            break
    summary = {"units_ran": len(ran), "units_already_done": done,
               "blocks_skipped_done": skipped_blocks,
               "stopped_by_time_cap": stopped_by_cap,
               "job_seconds": round(_time.monotonic() - t_job, 1)}
    print(json.dumps(summary), flush=True)
    return 0


def _write_block_stop(path: Path, d: int, seed: int, noise: float, streak: int,
                      next_run: int, d_best: int | None) -> None:
    payload = {"d": d, "seed": seed, "noise": noise, "streak": streak,
               "next_run": next_run, "d_best": d_best}
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    tmp.replace(path)


def cmd_deep_report(args):
    """Aggregate finished deep units; compare measured fps with the W35 estimate."""
    out = Path(args.output)
    units = []
    for d in args.ds:
        for noise in args.noises:
            for seed in args.seeds:
                for run in range(args.runs):
                    up = unit_path(out, d, seed, noise, run)
                    if up.exists():
                        units.append(json.loads(up.read_text()))
    fps = [u["fps"] for u in units]
    by_d = {}
    for u in units:
        e = by_d.setdefault(u["d"], {"runs": 0, "best": None, "best_unit": None})
        e["runs"] += 1
        if e["best"] is None or u["base_violations_best"] < e["best"]:
            e["best"] = u["base_violations_best"]
            e["best_unit"] = {k: u[k] for k in ("seed", "noise", "run", "init")}
    report = {
        "ds": args.ds, "noises": args.noises, "seeds": args.seeds, "runs": args.runs,
        "units": len(units),
        "expected_units": len(args.ds) * len(args.noises) * len(args.seeds) * args.runs,
        "fps_min": min(fps) if fps else None,
        "fps_median": sorted(fps)[len(fps) // 2] if fps else None,
        "fps_max": max(fps) if fps else None,
        "flips_per_unit": args.flips_per_run,
        "by_d": {str(k): v for k, v in sorted(by_d.items())},
        "solved_any": any(u["solved"] for u in units),
    }
    if fps:
        median = report["fps_median"]
        conservative = report["fps_min"]
        total_flips = (len(args.ds) * len(args.noises) * len(args.seeds) * args.runs
                       * args.flips_per_run)
        report["projected_hours_median"] = total_flips / median / 3600
        report["projected_hours_conservative"] = total_flips / conservative / 3600
    (out / "deep-report.json").write_text(json.dumps(report, indent=2) + "\n",
                                          encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check-eval")
    c.add_argument("--ds", type=int, nargs="+", required=True)
    c.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3])
    c.add_argument("--states", type=int, default=3)
    c.add_argument("--output", required=True)
    c.add_argument("--exe", required=True)
    c.add_argument("--cnf-dir", type=Path, default=None)
    c.set_defaults(func=cmd_check_eval)

    p = sub.add_parser("pilot")
    p.add_argument("--ds", type=int, nargs="+", required=True)
    p.add_argument("--seeds", type=int, nargs="+", required=True)
    p.add_argument("--flips", type=int, default=1000000)
    p.add_argument("--lam", type=float, default=1000.0)
    p.add_argument("--noise", type=float, default=0.1)
    p.add_argument("--bound", type=int, default=3)
    p.add_argument("--trace-every", type=int, default=100000)
    p.add_argument("--output", required=True)
    p.add_argument("--exe", required=True)
    p.set_defaults(func=cmd_pilot)

    d = sub.add_parser("deep")
    d.add_argument("--ds", type=int, nargs="+", required=True)
    d.add_argument("--seeds", type=int, nargs="+", required=True)
    d.add_argument("--noises", type=float, nargs="+", default=[0.1, 0.2])
    d.add_argument("--runs", type=int, default=10)
    d.add_argument("--flips-per-run", type=int, default=10000000)
    d.add_argument("--lam", type=float, default=1000.0)
    d.add_argument("--bound", type=int, default=3)
    d.add_argument("--restart-every", type=int, default=0)
    d.add_argument("--stagnation", type=int, default=0)
    d.add_argument("--trace-every", type=int, default=0)
    d.add_argument("--max-seconds", type=int, default=0,
                   help="exit cleanly after this many seconds; --resume continues")
    d.add_argument("--block-patience", type=int, default=3,
                   help="stop a (d, seed, noise) block after N non-improving restarts")
    d.add_argument("--resume", action="store_true")
    d.add_argument("--output", required=True)
    d.add_argument("--exe", required=True)
    d.set_defaults(func=cmd_deep)

    r = sub.add_parser("deep-report")
    r.add_argument("--ds", type=int, nargs="+", required=True)
    r.add_argument("--seeds", type=int, nargs="+", required=True)
    r.add_argument("--noises", type=float, nargs="+", default=[0.1, 0.2])
    r.add_argument("--runs", type=int, default=10)
    r.add_argument("--flips-per-run", type=int, default=10000000)
    r.add_argument("--output", required=True)
    r.set_defaults(func=cmd_deep_report)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
