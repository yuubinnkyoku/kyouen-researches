#!/usr/bin/env python3
"""Independent second verification of the y=14 fit published on main (K1233).

This lane (a second execution of the same hourly fast-lane task) derived a
cand14 closed form independently and BEFORE the winning declaration
(2026-11-22T18:42:55Z, commit e3a856ad9e; this lane's own declaration would
have been 2026-11-22T18:43:14Z), fitted it one-shot against its OWN raw
probe box (z=0..33, x=14..z+30, R<=x+z+28, 90,049 pts, mismatch 0, overlap 0)
and ran a 12-check audit battery (all bad 0). The fit publication was
YIELDED to the earlier declaration; this script re-targets all of that
work as independent second verification of the published K1233 artifacts:

  V1  our probe_rows.txt (raw double recursion, 90,049 pts, box complementary
      to theirs: z=31..33 rows, merge rows up to 15, x=z+30 edge rows) vs
      their published cand14: mismatch 0 expected (our raw data tests their
      closed form beyond their own probe box).
  V2  their probe regenerated from their published probe script:
      run our cand14 against their regenerated rows: mismatch 0 expected
      (their raw data, incl. the wider R cap x+z+30, tests our closed form).
  V3  verdict-equivalence of the two independently derived cand14
      implementations on a large no-engine grid (pure arithmetic):
      z=0..120, x=14..z+60, R=0..x+z+28.
  V4  fail-closed: tampering their cand14 module's Y constant must be
      caught by the V1-style comparison (patch anchored to the code line,
      not the docstring).

Usage: python3 y14_second_verification.py <their_dir>
  <their_dir> = research/experiments/<their experiment dir>, containing
  their cand14 module (cand*.py) and their probe*.py.
Deterministic, pure stdlib. Exit 1 on any failure. Writes
second_verification.json next to this script.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.setrecursionlimit(2_000_000)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cand14 import cand14 as my_cand14  # our local derivation (second lane)

OUR_PROBE = os.path.join(HERE, "probe_rows.txt")
OUR_PROBE_SHA = "8559dc59e4885414e6122b6cfbd2e15b34fc5fc52bf56fa96952cb8e454a4373"


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def find_file(d, predicate):
    for root, _, files in os.walk(d):
        for f in files:
            if predicate(f):
                return os.path.join(root, f)
    return None


def parse_rows(raw_text):
    for line in raw_text.splitlines():
        head, body = line.split('::')
        meta = dict(p.split('=') for p in head.split())
        z, x = int(meta['z']), int(meta['x'])
        vals = []
        for seg in body.split():
            v, c = seg.split('x')
            vals.extend([int(v)] * int(c))
        yield z, x, vals


def main():
    their_dir = sys.argv[1]
    their_cand_path = find_file(their_dir, lambda f: f.endswith(".py") and f.startswith("cand"))
    assert their_cand_path, "their cand module not found in " + their_dir
    their = load_module(their_cand_path, "their_cand14")

    # collect their cand entry function (cand14 or similar)
    fn = None
    for name in ("cand14", "cand", "cand14_val", "value"):
        if hasattr(their, name) and callable(getattr(their, name)):
            fn = getattr(their, name)
            break
    assert fn, "no callable candidate entry found in their module"

    out = {"their_dir": os.path.basename(their_dir.rstrip("/")),
           "their_cand_file": os.path.basename(their_cand_path),
           "checks": []}
    ok = True

    def check(name, points, bad, extra=None):
        nonlocal ok
        c = {"name": name, "points": points, "bad": bad}
        if extra:
            c.update(extra)
        out["checks"].append(c)
        if bad:
            ok = False

    # V1: our raw probe rows vs their cand14
    raw = open(OUR_PROBE, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == OUR_PROBE_SHA, "our probe sha drifted"
    n = bad = 0
    for z, x, vals in parse_rows(raw.decode()):
        for i, v in enumerate(vals):
            R = i + 1
            n += 1
            if fn(z, x, R) != v:
                bad += 1
    check("V1_our_raw_probe_vs_their_cand", n, bad)

    # V2: their probe script -> regenerate rows -> our cand14 self-consistency
    their_probe_path = find_file(their_dir, lambda f: f.endswith(".py") and f.startswith("probe"))
    their_rows_file = find_file(their_dir, lambda f: "probe_rows" in f and f.endswith(".txt"))
    if their_probe_path:
        tmp = tempfile.mkdtemp()
        shutil.copy(their_probe_path, os.path.join(tmp, os.path.basename(their_probe_path)))
        r = subprocess.run([sys.executable, os.path.basename(their_probe_path)],
                           cwd=tmp, capture_output=True, text=True, timeout=900)
        gen = os.path.join(tmp, "probe_rows.txt")
        if r.returncode == 0 and os.path.exists(gen):
            data = open(gen, "rb").read()
            n2 = bad2 = 0
            for z, x, vals in parse_rows(data.decode()):
                for i, v in enumerate(vals):
                    R = i + 1
                    n2 += 1
                    if my_cand14(z, x, R) != v:
                        bad2 += 1
            check("V2_their_regen_probe_vs_our_cand", n2, bad2,
                  {"rows_sha256": hashlib.sha256(data).hexdigest()})
            if their_rows_file:
                same = open(their_rows_file, "rb").read() == data
                check("V2b_their_rows_file_vs_regen", 0, 0 if same else 1)
        else:
            check("V2_their_probe_regen", 0, 1, {"stderr": r.stderr[-300:]})
        shutil.rmtree(tmp, ignore_errors=True)

    # V3: verdict equivalence on a large arithmetic grid (no engine)
    n3 = bad3 = 0
    for z in range(0, 121):
        for x in range(14, z + 61):
            for R in range(0, x + z + 29):
                n3 += 1
                if fn(z, x, R) != my_cand14(z, x, R):
                    bad3 += 1
    check("V3_verdict_equivalence_grid", n3, bad3)

    # V4 fail-closed: tamper their module's Y constant (patch anchored to the
    # code line, NOT the docstring mention) and require V1-style detection.
    tmpp = os.path.join(HERE, "_tamper_mod.py")
    src = open(their_cand_path).read()
    tam = src.replace("\nY = 14", "\nY = 15", 1)
    if tam != src:
        open(tmpp, "w").write(tam)
        tam_mod = load_module(tmpp, "their_cand_tampered")
        tfn = getattr(tam_mod, "cand14", None) or getattr(tam_mod, "cand", None)
        if tfn:
            n4 = bad4 = 0
            for z, x, vals in parse_rows(raw.decode()):
                for i, v in enumerate(vals):
                    R = i + 1
                    n4 += 1
                    if tfn(z, x, R) != v:
                        bad4 += 1
                if n4 > 20000:
                    break
            out["fail_closed"] = {"name": "V4_Y_tamper", "mismatch": bad4,
                                  "caught": bad4 > 0}
            if bad4 == 0:
                ok = False
        os.remove(tmpp)

    out["overall"] = "PASS" if ok else "FAIL"
    blob = json.dumps(out, sort_keys=True, indent=1, ensure_ascii=False) + "\n"
    print(blob)
    with open(os.path.join(HERE, "second_verification.json"), "w") as f:
        f.write(blob)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
