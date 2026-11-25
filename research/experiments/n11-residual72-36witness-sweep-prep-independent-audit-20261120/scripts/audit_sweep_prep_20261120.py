#!/usr/bin/env python3
"""Independent audit of the sweep-prep commit 53b07ebe16 (36-witness depth-10 sweep inputs).

Single-owner lane declared in research/log/2026-11-20-n11-36witness-sweep-prep-independent-audit-single-owner-note.md.
Published-records-only. No new sweeps, no judgements, no folds, no row closures.

The machine rederives roots.json / residual72.json from the K1075 canonical record
(own D4 implementation, hand-checked unit tests), cross-checks every SHA pin that
assemble.py will enforce after the 72-probe sweep finishes, statically reviews the
driver's argv contract and partition/resume logic against the pinned runner source,
and runs a capped (non-judging) runner smoke test to prove the interface works.
Output is deterministic; two runs in different cwds must be byte-identical.
"""
import collections, hashlib, json, os, re, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPDIR = HERE.parents[0]
REPO = HERE.parents[3]

K1075 = REPO / "research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json"
K1075_SHA = "49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa"
SWEEP = REPO / "research/experiments/n11-residual72-36witness-depth10-sweep-20261120"
RUNNER_COPY = SWEEP / "runner_v17.ts"
RUNNER_ORIG = REPO / "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_runner_v17.ts"
RUNNER_BLOB_PIN = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
ROOTS_PIN = "3904041ea40c4e7c419d437046358eac7b91d169782e8d64abac0c9b044f160f"
RESID_PIN = "78e3ee7a8092dbca23fa3bf41491fdc666ba73a2e62c23f3da7570430bf28f9b"
PREP_SOURCE_SHA = "49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa"

# ---------------------------------------------------------------------------
# Independent D4 implementation (written from scratch; unit-tested below).
# Board cells are indexed 0..120 with cell = 11*y + x.
# ---------------------------------------------------------------------------
def pts(mask):
    return [(m % 11, m // 11) for m in range(121) if (mask >> m) & 1]

def transform_points(plist, t):
    out = []
    for (x, y) in plist:
        if t == 0:   X, Y = x, y            # identity
        elif t == 1: X, Y = 10 - y, x       # rotate 90 ccw
        elif t == 2: X, Y = 10 - x, 10 - y  # rotate 180
        elif t == 3: X, Y = y, 10 - x       # rotate 270
        elif t == 4: X, Y = 10 - x, y       # mirror vertical axis
        elif t == 5: X, Y = x, 10 - y       # mirror horizontal axis
        elif t == 6: X, Y = y, x            # transpose
        else:       X, Y = 10 - y, 10 - x   # anti-transpose
        out.append(11 * Y + X)
    return out

def transform(mask, t):
    m = 0
    for c in transform_points(pts(mask), t):
        m |= 1 << c
    return m

def orbit(mask):
    return [transform(mask, t) for t in range(8)]

def canon(mask):
    return min(orbit(mask))

def hx(mask):
    return f"{mask:032x}"

def cells(mask):
    return [c for c in range(121) if (mask >> c) & 1]

# ---------------------------------------------------------------------------
gates = []
def gate(name, ok, detail):
    gates.append({"name": name, "pass": bool(ok), "detail": detail})
    if not ok:
        print("GATE FAIL:", name, json.dumps(detail, ensure_ascii=False)[:400])

# ---- S: self-tests of the local D4 implementation (hand-derived expectations)
def self_tests():
    # corner pair (0,0)+(10,10) = cells {0,120}: the 8 dihedral images collapse
    # to exactly two sets: {0,120} (id/rot180/transpose/anti-transpose) and
    # {10,110} (rot90/rot270/mirror-x/mirror-y = cells (10,0),(0,10));
    # canon (integer min) is the {10,110} image.
    m = (1 << 0) | (1 << 120)
    orb = sorted(set(orbit(m)))
    exp_a = (1 << 0) | (1 << 120)   # {0,120}
    exp_c = (1 << 10) | (1 << 110)  # {(10,0),(0,10)}
    gate("self-d4-corner", orb == [exp_c, exp_a] and canon(m) == exp_c,
         {"orbit": [hx(u) for u in orb], "canon": hx(canon(m))})
    # center stone (5,5)=cell 60 is fixed by all 8 symmetries
    m2 = 1 << 60
    gate("self-d4-center", orbit(m2) == [m2] * 8, {"canon": hx(canon(m2))})
    # L-triomino {(0,0),(1,0),(0,1)}: rotate-90 gives cells {10,21,9}; transpose gives {0,110,12}
    m3 = (1 << 0) | (1 << 1) | (1 << 11)
    rot90 = transform(m3, 1)   # (x,y)->(10-y,x): (0,0)->10, (1,0)->21, (0,1)->9
    trans = transform(m3, 6)   # (x,y)->(y,x):    (0,0)->0, (1,0)->11, (0,1)->1
    gate("self-d4-triomino", rot90 == ((1 << 10) | (1 << 21) | (1 << 9))
         and trans == ((1 << 0) | (1 << 11) | (1 << 1)),
         {"rot90": sorted((c % 11, c // 11) for c in cells(rot90)),
          "transpose": sorted((c % 11, c // 11) for c in cells(trans))})
    # rotation composition: t1 twice equals t2; t1 composed with t3 equals identity
    m4 = 0
    for c in (3, 17, 42, 99, 118):
        m4 |= 1 << c
    comp = transform(transform(m4, 1), 1)
    gate("self-d4-composition", comp == transform(m4, 2) and transform(transform(m4, 1), 3) == m4,
         {"rot180": hx(comp), "identity_roundtrip": transform(transform(m4, 1), 3) == m4})

# ---- A: published-record pins
def pin_checks():
    k1075_bytes = K1075.read_bytes()
    roots_bytes = (SWEEP / "roots.json").read_bytes()
    resid_bytes = (SWEEP / "residual72.json").read_bytes()
    runner_bytes = RUNNER_COPY.read_bytes()
    orig_bytes = RUNNER_ORIG.read_bytes()
    gate("pin-k1075-canonical-json", hashlib.sha256(k1075_bytes).hexdigest() == K1075_SHA,
         {"sha256": hashlib.sha256(k1075_bytes).hexdigest()})
    gate("pin-roots-json-sha", hashlib.sha256(roots_bytes).hexdigest() == ROOTS_PIN,
         {"sha256": hashlib.sha256(roots_bytes).hexdigest()})
    gate("pin-residual72-json-sha", hashlib.sha256(resid_bytes).hexdigest() == RESID_PIN,
         {"sha256": hashlib.sha256(resid_bytes).hexdigest()})
    blob = hashlib.sha1(b"blob " + str(len(runner_bytes)).encode() + b"\x00" + runner_bytes).hexdigest()
    gate("pin-runner-v17-git-blob", blob == RUNNER_BLOB_PIN, {"git_blob_sha1": blob})
    gate("runner-copy-equals-pinned-original", runner_bytes == orig_bytes,
         {"copy_sha256": hashlib.sha256(runner_bytes).hexdigest(),
          "orig_sha256": hashlib.sha256(orig_bytes).hexdigest()})
    prepare_src = (SWEEP / "prepare_roots.py").read_text()
    gate("prepare-pins-k1075-sha", "EXPECTED = \"49b6f85f" in prepare_src
         and "assert actual == EXPECTED" in prepare_src,
         {"note": "prepare_roots.py fail-closes on the K1075 SHA-256 pin"})
    assemble_src = (SWEEP / "assemble.py").read_text()
    gate("assemble-pins-match-prep-artifacts",
         ('"' + ROOTS_PIN + '"') in assemble_src and ('"' + RESID_PIN + '"') in assemble_src
         and ('"' + RUNNER_BLOB_PIN + '"') in assemble_src,
         {"roots_pin_in_assemble": ('"' + ROOTS_PIN + '"') in assemble_src,
          "residual_pin_in_assemble": ('"' + RESID_PIN + '"') in assemble_src,
          "runner_blob_pin_in_assemble": ('"' + RUNNER_BLOB_PIN + '"') in assemble_src})
    return k1075_bytes, roots_bytes, resid_bytes, runner_bytes

# ---- B: source-record structure checks (independent)
def source_checks(data):
    residual_hex = data["base_state"]["residual_row_hex"]
    gate("source-residual-72-unique", len(residual_hex) == 72 and len(set(residual_hex)) == 72
         and data["base_state"]["residual_rows"] == 72,
         {"rows": len(residual_hex), "unique": len(set(residual_hex))})
    bad = [h for h in residual_hex
           if len(h) != 32 or int(h, 16).bit_count() != 6 or canon(int(h, 16)) != int(h, 16)]
    gate("source-residual-rows-canonical-s6", not bad, {"bad": bad[:5], "count": len(bad)})
    w = data["witness_full"]
    gate("source-witness-36", len(w) == 36 and data["candidate_supply"]["witness_size"] == 36,
         {"len": len(w)})
    keys_union = set().union(*[set(e) for e in w])
    roots = [e["root"] for e in w]
    gate("source-witness-roots-unique", len(set(roots)) == 36, {"unique": len(set(roots))})
    gate("source-witness-keys-and-safe",
         keys_union == {"covered", "root", "rows", "rule", "safe"} and all(e["safe"] is True for e in w),
         {"keys": sorted(keys_union)})
    rule = "live candidate: unjudged in the phase-2 full cache join over residual 72 (not REFUTED, not WIN, not a retired/dead root)"
    gate("source-witness-rule-string", all(e["rule"] == rule for e in w),
         {"rule": w[0]["rule"]})
    retired = set(data["candidate_supply"]["live38_killed_open_72row_supply"]["roots"])
    gate("source-witness-not-retired", len(retired) == 38 and not (set(roots) & retired),
         {"retired_listed": len(retired), "overlap": sorted(set(roots) & retired)})
    newwin = set(data["verdict_join"]["newly_judged_since_resolve6"]["win"])
    gate("source-witness-not-newly-win", not (set(roots) & newwin),
         {"newly_win": sorted(newwin)})
    rd = data["candidate_supply"]["row_demand"]
    gate("source-row-demand-covers-residual", set(rd) == set(residual_hex) and len(rd) == 72,
         {"row_demand": len(rd)})
    return residual_hex, w

# ---- C: independent rederivation of the prep artifacts
def rederive(residual_hex, witness, roots_bytes, resid_bytes):
    roots = {}
    row_use = collections.Counter()
    orbit_hist = []
    for e in witness:
        root = int(e["root"], 16)
        lo = root & -root
        bit = lo.bit_length() - 1
        child = root - lo
        rows = sorted(e["rows"])
        # structural fingerprint computed independently
        assert root.bit_count() == 7
        assert canon(root) == root
        assert sorted(e["covered"]) == rows and len(rows) == 2
        del_orbit = {hx(canon(root ^ (1 << p))) for p in cells(root)}
        assert set(rows) <= del_orbit
        for r in rows:
            assert int(r, 16).bit_count() == 6 and canon(int(r, 16)) == int(r, 16)
            row_use[r] += 1
        orbit_hist.append(len(del_orbit))
        roots[e["root"]] = {
            "root": e["root"], "child": hx(child), "bit": bit,
            "pcount": 7, "rows": rows, "safe": True,
        }
    res_set = set(residual_hex)
    gate("rederive-exact-1-cover",
         set(row_use) == res_set and all(row_use[r] == 1 for r in res_set)
         and sum(row_use.values()) == 72,
         {"memberships": sum(row_use.values()), "duplicates_or_missing":
          sum(1 for r in res_set if row_use[r] != 1)})
    gated_ok = True
    # every root: runner semantics roundtrip: child cells + bit == root cells
    roundtrip_bad = []
    for rh, it in roots.items():
        root = int(rh, 16)
        ch = int(it["child"], 16)
        if (ch | (1 << it["bit"])) != root or (ch & (1 << it["bit"])) != 0:
            roundtrip_bad.append(rh)
    gate("rederive-roundtrip-child-bit", not roundtrip_bad, {"bad": roundtrip_bad[:5]})
    my_roots = [roots[k] for k in sorted(roots)]
    my_roots_bytes = (json.dumps(my_roots, indent=1) + "\n").encode()
    my_resid_bytes = (json.dumps(sorted(set(residual_hex)), indent=1) + "\n").encode()
    gate("byteequal-roots-json", my_roots_bytes == roots_bytes,
         {"mine_sha256": hashlib.sha256(my_roots_bytes).hexdigest(),
          "pub_sha256": hashlib.sha256(roots_bytes).hexdigest(),
          "bytes": len(my_roots_bytes), "pub_bytes": len(roots_bytes)})
    gate("byteequal-residual72-json", my_resid_bytes == resid_bytes,
         {"mine_sha256": hashlib.sha256(my_resid_bytes).hexdigest(),
          "pub_sha256": hashlib.sha256(resid_bytes).hexdigest(),
          "bytes": len(my_resid_bytes), "pub_bytes": len(resid_bytes)})
    # root sort order + ascending residual order in published files
    pub_roots = json.loads(roots_bytes)
    gate("published-roots-sorted-and-fields",
         [r["root"] for r in pub_roots] == sorted(r["root"] for r in pub_roots)
         and all(r.get("pcount") == 7 and r.get("safe") is True and len(r["rows"]) == 2
                 for r in pub_roots),
         {"roots": len(pub_roots)})
    # deletion-orbit size histogram (structure observation, cheap)
    gate("rederive-orbit-histogram", True,
         {"orbit_sizes": dict(sorted(collections.Counter(orbit_hist).items()))})
    # cross: published rows per root equal record rows per root
    pub_map = {r["root"]: r for r in pub_roots}
    cross_bad = [e["root"] for e in witness if pub_map[e["root"]]["rows"] != sorted(e["rows"])]
    gate("cross-published-rows-equal-record", not cross_bad, {"bad": cross_bad[:5]})
    return pub_roots

# ---- D: driver/runner static consistency
def machinery_checks(pub_roots, runner_bytes):
    driver_src = (SWEEP / "driver.py").read_text()
    assemble_src = (SWEEP / "assemble.py").read_text()
    runner_src = runner_bytes.decode()

    # D1 partition roots[W::4]
    parts = [pub_roots[W::4] for W in range(4)]
    flat = [r["root"] for p in parts for r in p]
    gate("mach-partition-roots-w-slice-4",
         sorted(flat) == sorted(r["root"] for r in pub_roots) and len(flat) == 36
         and all(len(p) == 9 for p in parts)
         and len(set(flat)) == 36,
         {"sizes": [len(p) for p in parts]})
    # D2 both orderings enumerated for every root -> 72 unique keys
    keys = {(r["root"], o) for r in [x for p in parts for x in p] for o in ("andclose1", "andclose0")}
    gate("mach-72-unique-probe-keys", len(keys) == 72, {"keys": len(keys)})
    # D3 uniform cap in source
    m = re.search(r"CAP\s*=\s*([\d_]+)", driver_src)
    cap_ok = m and int(m.group(1).replace("_", "")) == 30_000_000
    m2 = re.search(r"TIMEOUT\s*=\s*(\d+)", driver_src)
    gate("mach-cap-30m-timeout-280", bool(cap_ok and m2 and int(m2.group(1)) == 280),
         {"cap": m.group(1) if m else None, "timeout": int(m2.group(1)) if m2 else None})
    # D4 argv contract
    driver_flags = set(re.findall(r'"(--[a-z]+)"', driver_src))
    runner_flags = set(re.findall(r"'(--[a-z]+)'", runner_src)) | set(re.findall(r'"(--[a-z]+)"', runner_src))
    gate("mach-argv-contract",
         driver_flags <= runner_flags and "--nocontrol" not in driver_flags
         and runner_flags <= {"--bits", "--depth", "--cap", "--andclose", "--child", "--out", "--nocontrol"},
         {"driver_flags": sorted(driver_flags), "runner_parse_flags": sorted(runner_flags)})
    gate("mach-andclose-threshold-depth8", "cfg.andcloseMode === 1 && d >= 8" in runner_src,
         {"note": "andclose ordering applies at d>=8; sweep depth 10 => both modes active"})
    # D5 resume predicate matches assemble ok predicate
    gate("mach-resume-predicate", '"result" in rec and rec.get("error") is None' in driver_src
         and 'r.get("result") is not None and r.get("error") is None' in assemble_src,
         {"note": "driver skips (root,ordering) only for records assemble counts as ok"})
    # D6 pilot gate agreement across runner and assemble
    gate("mach-pilot-gate-agreement",
         "expected loss=false nodes=3402" in runner_src
         and "PILOT_CELLS = hexCells('00000000000000003802000008000006')" in runner_src
         and "eng.solve(PILOT_CELLS.slice(), 6, 1e9, false)" in runner_src
         and '.get("control") == "pilot_d6"' in assemble_src
         and 'r["control"].get("nodes") == 3402' in assemble_src
         and 'r["control"].get("loss") is False' in assemble_src,
         {"runner_pilot_requirement": "loss=false nodes=3402 at depth 6",
          "assemble_expected_nodes": 3402})
    # D7 capped micro-probe semantics: capped result proves nothing (guard present)
    gate("mach-interpretation-guards",
         "capped => proves nothing either way" in runner_src
         and "REFUTED-D10 is not a LOSS proof" in assemble_src
         and "remain UNKNOWN" in assemble_src,
         {"note": "interpretation guards present in both runner and assemble"})

# ---- E: runner interface smoke test (cap 2000, non-judging)
SMOKE_CAP = 2000
def smoke_tests(pub_roots, runner_bytes):
    if "--no-smoke" in sys.argv:
        gate("smoke-skipped", True, {"note": "skipped by flag"})
        return
    sample = pub_roots[0]
    runner_copy = SWEEP / "runner_v17.ts"
    outs = {}
    with tempfile.TemporaryDirectory() as td:
        for ordering in ("1", "0"):
            outp = Path(td) / f"smoke-{ordering}.jsonl"
            cmd = ["node", "--experimental-strip-types", str(runner_copy),
                   "--bits", str(sample["bit"]), "--depth", "10", "--cap", str(SMOKE_CAP),
                   "--andclose", ordering, "--child", sample["child"], "--out", str(outp)]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if r.returncode != 0:
                gate(f"smoke-order{ordering}-exit", False,
                     {"rc": r.returncode, "stderr_tail": r.stderr[-300:]})
                continue
            lines = [json.loads(l) for l in outp.read_text().splitlines() if l.strip()]
            ctrl = lines[0]
            res = lines[1]
            ctrl_field = {"control": ctrl.get("control"), "loss": ctrl.get("loss"),
                          "nodes": ctrl.get("nodes"), "capped": ctrl.get("capped")}
            gate(f"smoke-order{ordering}-pilot-control",
                 ctrl_field == {"control": "pilot_d6", "loss": False, "nodes": 3402,
                                "capped": False} and len(lines) == 2, ctrl_field)
            res_field = {"bit": res.get("bit"), "loss": res.get("loss"),
                         "nodes": res.get("nodes"), "capped": res.get("capped"),
                         "depth": 10, "cap": SMOKE_CAP}
            gate(f"smoke-order{ordering}-capped-microprobe",
                 res_field["bit"] == sample["bit"] and res_field["loss"] is False
                 and res_field["capped"] is True and 0 < res_field["nodes"] <= SMOKE_CAP * 4,
                 res_field)
            outs[ordering] = {"control": ctrl_field, "result": res_field}
        gate("smoke-twoline-output-shape", set(outs) == {"1", "0"},
             {"note": "one control line + one result line per invocation, both orderings"})

# ---------------------------------------------------------------------------
def main():
    self_tests()
    k1075_bytes, roots_bytes, resid_bytes, runner_bytes = pin_checks()
    data = json.loads(k1075_bytes)
    residual_hex, witness = source_checks(data)
    pub_roots = rederive(residual_hex, witness, roots_bytes, resid_bytes)
    machinery_checks(pub_roots, runner_bytes)
    smoke_tests(pub_roots, runner_bytes)
    all_pass = all(g["pass"] for g in gates)
    out = {
        "schema": "n11-residual72-36witness-sweep-prep-independent-audit-20261120-v1",
        "date": "2026-11-20",
        "audited_prep_commit": "53b07ebe1647b2c966af098897290df243ba0d19",
        "audited_lane_declaration": "research/log/2026-11-20-n11-36witness-sweep-prep-independent-audit-single-owner-note.md",
        "inputs": {
            "k1075_canonical_json_sha256": K1075_SHA,
            "published_roots_json_sha256": ROOTS_PIN,
            "published_residual72_json_sha256": RESID_PIN,
            "runner_v17_git_blob": RUNNER_BLOB_PIN,
        },
        "gates": gates,
        "summary": {
            "gates_total": len(gates),
            "gates_pass": sum(1 for g in gates if g["pass"]),
            "roots": 36, "residual_rows": 72, "probe_keys": 72,
            "verdict": "audited-prep-consistent" if all_pass else "AUDIT-FAILED",
        },
        "interpretation_guard": [
            "This audit is candidate bookkeeping verification and implies nothing about game-theoretic values.",
            "The smoke test uses cap 2000; capped results prove nothing in either direction.",
            "REFUTED-D10 is not a LOSS proof; WIN7-D10 is a certificate-extraction candidate only.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
        ],
    }
    blob = json.dumps(out, indent=1, sort_keys=True) + "\n"
    if not all_pass:
        print("AUDIT FAILED; not writing output")
        for g in gates:
            if not g["pass"]:
                print("  FAIL:", g["name"], json.dumps(g["detail"])[:200])
        sys.exit(1)
    outdir = EXPDIR / "output"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "sweep-prep-independent-audit-20261120.json").write_text(blob, encoding="utf-8")
    print("all gates pass:", all_pass, f"({len(gates)} gates)")
    print("sha256:", hashlib.sha256(blob.encode()).hexdigest())

if __name__ == "__main__":
    main()
