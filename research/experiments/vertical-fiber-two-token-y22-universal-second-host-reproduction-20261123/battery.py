#!/usr/bin/env python3
"""Fail-closed tamper battery for the second-host own-build y=22 machine.

Runs on throwaway copies in /tmp only: the canonical own build
(mybuild/verify_y22_universal.py), the scratch run tree and the published
corpus bytes are never modified. After each probe the canonical bytes are
re-hashed and the scratch outputs are cmp'd against the frozen baseline to
prove the probe touched nothing.

12 probes mirroring the published fail-closed battery of the declaration
(e1e60cd4 / runlog): each must be CAUGHT (rc != 0 with an explicit
FAIL-CLOSED message or a bad-count audit FAIL). Expected bad counts are
recorded from the published battery outcomes for comparison; any deviation
is reported honestly, never silently fit.
"""
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("/home/user/kr-exec/y22repro")
BUILD = ROOT / "mybuild" / "verify_y22_universal.py"
BUILD_SHA = "88ce3ed17baf162bb7efebbceb63d028dbe605be0eedcf6117b51cb3fcea60e4"
PUB = ROOT / "published" / "verify_y22_universal.py"
PUB_SHA = "96d9787fae441a39c1cf0475e446b9dfef9bcc8297818afc1bd82a9f3c19ec6b"
SRC_EXP = ROOT / "scratch" / "research" / "experiments" / "vertical-fiber-two-token-y22-universal-proof-20261123"
BASE = SRC_EXP / "baseline"
TMP = Path("/tmp/y22-battery")


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def integrity(tag):
    errs = []
    if sha256(BUILD) != BUILD_SHA:
        errs.append("own build bytes changed")
    if sha256(PUB) != PUB_SHA:
        errs.append("published bytes changed")
    if (SRC_EXP / "verify_y22_universal.py").read_bytes() != BUILD.read_bytes():
        errs.append("scratch machine bytes changed")
    for f in sorted(BASE.iterdir()):
        if f.name == "hashes.txt":
            continue
        if f.name in ("census.txt", "census-ordered.json", "census-canonical.json",
                      "preflight-c1d-y22.json"):
            # cmp scratch live output vs frozen baseline copy
            live = SRC_EXP / "output" / f.name
            if not live.exists() or live.read_bytes() != f.read_bytes():
                errs.append(f"scratch output/{f.name} diverged from baseline")
    return errs


def fresh_exp(tag):
    d = TMP / tag
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(SRC_EXP, d, ignore=shutil.ignore_patterns("baseline"))
    return d


def tamper_machine(d, old, new, count=1):
    p = d / "verify_y22_universal.py"
    s = p.read_text()
    c = s.count(old)
    assert c == count, f"tamper pattern {old!r} found {c}x (expected {count})"
    p.write_text(s.replace(old, new))
    return sha256(p)


def run_checks(d, args, timeout=280):
    t0 = time.time()
    r = subprocess.run([sys.executable, d.name + "/verify_y22_universal.py"] + args,
                       cwd=d.parent, capture_output=True, text=True, timeout=timeout)
    return r, time.time() - t0


def parse_out(out):
    """Extract printed per-check bad counts, merge/tail corollary dicts, overall."""
    res = {"checks": {}, "merge_bad": None, "tail_bad": None, "overall": None,
           "failclosed": None}
    for ln in out.splitlines():
        ln = ln.strip()
        if ln.startswith("FAIL-CLOSED"):
            res["failclosed"] = ln
        if ln.startswith("overall:"):
            res["overall"] = ln
        elif ":" in ln and ln.split(":")[0].strip() in (
                "C1", "C1b", "C1d", "C2", "C2b", "C3", "C4", "C4t", "C7",
                "C8", "C9", "C11", "C11r", "C12"):
            name, rest = ln.split(":", 1)
            res["checks"][name.strip()] = rest.strip()
        elif ln.startswith("merge: "):
            res["merge_bad"] = ln
    return res


PROBES = [
    # (tag, kind, mutation, checks, expectation)
    ("P01-census-missing", "shutil", ("rm", "output/census.txt"), ["C11r"],
     {"failclosed_sub": "census.txt is missing"}),
    ("P02-census-row-deleted", "census", "drop_first_row", ["C11r"],
     {"failclosed_sub": "census rows 3919 != 3920"}),
    ("P03-census-duplicate", "census", "dup_first_row", ["C11r"],
     {"failclosed_sub": "duplicate census row (0,22)"}),
    ("P04-census-P-tamper", "census", "drop_last_P_first_row", ["C11r"],
     {"check": "C11r", "bad": 1}),
    ("P05-census-T-inject", "census", "inject_T_first_row", ["C11r"],
     {"check": "C11r", "bad": 1}),
    ("P06-C11r-tail-flip", "sed",
     ("        tail = (x + 22) % 2", "        tail = (x + 23) % 2", 1), ["C11r"],
     {"check": "C11r", "bad": 3920}),
    ("P07-anchor-misbind", "sed",
     ("(17, A17u)", "(17, A10u)", 1), ["C1d"],
     {"check": "C1d", "bad": 14869}),
    ("P08-lowR-shift", "sed",
     ("!= single_token(x + 22, z0, R):", "!= single_token(x + 22, z0, R + 1):", 1),
     ["C1d"], {"check": "C1d", "bad": 9108}),
    ("P09-merge-boundary", "sed",
     ("\n    if x <= z - 23:", "\n    if x <= z - 22:", 1), ["C2"],
     {"merge_bad": 59}),
    ("P10-clip-window", "sed",
     ("CLIP, SENT = 46, 47", "CLIP, SENT = 44, 45", 1), ["C4", "C4t"],
     {"check": "C4", "bad": 945}),
    ("P11-tail-parity-flip", "sed",
     ("    tail = x % 2 == 1 and R >= x + z + Y + 1",
      "    tail = x % 2 == 0 and R >= x + z + Y + 1", 1), ["C1", "C2"],
     {"checks": {"C1": 4898, "C2": 24024}}),
    ("P12-band-parity-flip", "sed",
     ("off % 2 == 0 and 2 * Y + 2 <= off <= x + Y",
      "off % 2 == 1 and 2 * Y + 2 <= off <= x + Y", 1), ["C1", "C2"],
     {"checks": {"C1": 1763, "C2": 24451}}),
]


def apply_census(d, what):
    p = d / "output" / "census.txt"
    lines = p.read_text().splitlines(keepends=True)
    if what == "drop_first_row":
        # find first data row (after any header) - format is "z=... " rows only
        idx = next(i for i, ln in enumerate(lines) if ln.startswith("z="))
        del lines[idx]
    elif what == "dup_first_row":
        idx = next(i for i, ln in enumerate(lines) if ln.startswith("z="))
        lines.insert(idx + 1, lines[idx])
    elif what == "drop_last_P_first_row":
        # census set syntax has NO space after commas: P={1,3,...,43}.
        # An earlier harness attempt searched ', 43' (with space), which is
        # absent -> ln[:-1] silently dropped the newline instead, appending a
        # stray brace (machine still failed closed on int parse, rc=1, but the
        # mutation itself was invalid). Recorded honestly; re-probed with the
        # valid pattern below.
        for i, ln in enumerate(lines):
            if ln.startswith("z="):
                assert ln.rstrip().endswith(",43}"), ln[-12:]
                lines[i] = ln[: ln.rfind(",43")] + "}\n"
                break
    elif what == "inject_T_first_row":
        for i, ln in enumerate(lines):
            if ln.startswith("z=") and "T={} " in ln:
                lines[i] = ln.replace("T={}", "T={5}", 1)
                break
    else:
        raise AssertionError(what)
    p.write_text("".join(lines))
    return sha256(p)


def run_probe(spec, results):
    tag, kind, mut, checks, exp = spec
    d = fresh_exp(tag)
    if kind == "shutil":
        (d / mut[1]).unlink()
        mut_sha = "removed"
    elif kind == "census":
        mut_sha = apply_census(d, mut)
    elif kind == "sed":
        old, new, cnt = mut
        mut_sha = tamper_machine(d, old, new, cnt)
    try:
        r, wall = run_checks(d, checks)
        out = r.stdout + r.stderr
        po = parse_out(out)
        caught = r.returncode != 0 and (
            po["failclosed"] is not None or "overall: FAIL" in out)
        detail = {"failclosed": po["failclosed"], "overall": po["overall"],
                  "checks": po["checks"], "merge": po["merge_bad"]}
    except subprocess.TimeoutExpired as e:
        caught, wall = False, None
        detail = {"error": "timeout", "partial": (e.stdout or b"").decode() if e.stdout else ""}
        r = None
    errs = integrity(tag)
    ok_exp = True
    exp_report = {}
    if exp.get("failclosed_sub"):
        hit = (po["failclosed"] or "") if r is not None else ""
        exp_report = {"expected_sub": exp["failclosed_sub"],
                      "observed": po["failclosed"] if r is not None else None}
        ok_exp = exp["failclosed_sub"] in hit
    if exp.get("check"):
        want = exp["bad"]
        gotline = po["checks"].get(exp["check"], "") if r is not None else ""
        got = None
        for tok in gotline.split():
            if tok.startswith("bad="):
                got = int(tok[4:])
        exp_report["expected_bad"] = want
        exp_report["observed"] = got
        ok_exp = ok_exp and got == want
    if exp.get("checks"):
        exp_report["expected_bads"] = exp["checks"]
        got_map = {}
        ok = True
        for k, want in exp["checks"].items():
            got = None
            gl = po["checks"].get(k, "") if r is not None else ""
            for tok in gl.split():
                if tok.startswith("bad="):
                    got = int(tok[4:])
            got_map[k] = got
            ok = ok and got == want
        exp_report["observed"] = got_map
        ok_exp = ok_exp and ok
    if exp.get("merge_bad") is not None:
        got = None
        if r is not None and po["merge_bad"]:
            import re as _re
            m = _re.search(r"'bad':\s*(\d+)", po["merge_bad"])
            if m:
                got = int(m.group(1))
        exp_report = {"expected_merge_bad": exp["merge_bad"], "observed": got}
        ok_exp = ok_exp and got == exp["merge_bad"]
    rec = {"tag": tag, "checks": checks, "mutated_sha": mut_sha,
           "caught": caught, "rc": r.returncode if r is not None else None,
           "wall_s": round(wall, 1) if wall else None,
           "expectation": exp_report, "expectation_match": ok_exp,
           "baseline_integrity": "OK" if not errs else errs,
           "stdout_tail": (r.stdout or "")[-400:] if r is not None else detail.get("partial", "")[-400:]}
    results[tag] = rec
    sch = "PASS" if (caught and ok_exp and not errs) else (
        "CAUGHT-but-mismatch" if caught else "NOT-CAUGHT")
    print(f"[{tag}] {sch} rc={rec['rc']} wall={rec['wall_s']}s "
          f"exp_match={ok_exp} integrity={'OK' if not errs else errs}")
    if rec["stdout_tail"]:
        print("   last output:", rec["stdout_tail"].replace("\n", " | ")[-280:])
    shutil.rmtree(TMP / tag, ignore_errors=True)
    return caught and not errs


def main():
    TMP.mkdir(parents=True, exist_ok=True)
    only = sys.argv[1:]
    results = {}
    all_ok = True
    for spec in PROBES:
        if only and not any(o in spec[0] for o in only):
            continue
        if not run_probe(spec, results):
            all_ok = False
    outp = ROOT / "mybuild" / ("battery-results-%s.json" % ("-".join(only).replace(":", "") if only else "full"))
    outp.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
    print("results ->", outp.name, "all_ok =", all_ok)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
