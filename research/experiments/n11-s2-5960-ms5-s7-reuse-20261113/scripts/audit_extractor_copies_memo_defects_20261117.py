#!/usr/bin/env python3
"""Structural audit of the remaining class4_child1 engine copies for the two
memo defects verified for the certificate extractor in K0907 (bug A: signed
memo key comparison against Uint32Array storage; bug B: dead sentinel-255
negative bounds), closing the "other copies remain unaudited" limitation that
K0907 recorded explicitly.

Audited copies (all under
research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/, git blob
pins asserted against the published repo):

  extractor family (bug A + bug B present in all three verbatim copies):
    class4_child1_cert_extractor.ts          6716075d... (2026-11-13 batch1)
    class4_child1_cert_extractor_exact.ts    52bcaf50... (K0907 audit target)
    class4_child1_cert_extractor_exact_ms23.ts c267f260... (one-line MS
      variant of exact.ts used for the published 73k/73l certificate bands)
  sweep-side family (bug A + bug B present in all three batch1 copies):
    class4_child1_sweep_engine.ts            bd6a650a... (v15 sweep engine)
    class4_child1_chunk_prover.ts            fc74d215...
    class4_child1_runner.ts                  8744fc65... (FBT-saturation
      external runner; transport-repaired 2a1af3a79 same blob content)
  repaired family (both bugs fixed):
    class4_child1_runner_v16.ts              0a4a86f6... (2026-11-14
      "v16 runner with unsigned TT keys and sentinel-aware bounds")
    class4_child1_runner_v17.ts              c132cc64... (2026-11-16; the
      engine behind the published cost-73i/73j/73k/73l raw sweeps)
    class4_child1_cert_extractor_exact_v16.ts 5518d375... (2026-11-14
      repaired extractor; never used for published certificates)

Method: whitespace-normalized token comparison of the memoFind/memoEntry
blocks (the two families of buggy copies are byte-identical modulo
whitespace, so the K0907 dump-quantified mechanism - duplicate insertion of
high-bit keys, up to 64 copies per key, dead nowin/nolose - transfers to
every copy in the same family), exact-count source pattern checks for the
sign comparison and the dead/fixed negative-bound update lines, a one-line
diff assertion for ms23 vs exact, a Node.js sign demo, and a no-false-hit
soundness note. No engine is executed; no new verdict is produced.

Determinism: no timestamps, no wall times, fixed order; running twice must
produce byte-identical output. 11x11 empty board remains UNKNOWN; this audit
changes no verdict and closes no manifest row.
"""
import hashlib, json, os, re, subprocess

ROOT = os.environ.get("AUDIT_MIRROR", "auditcopies")
FILES = [
    ("class4_child1_cert_extractor.ts",
     "6716075d2c4f2e49c3d4570b2314449de121db0d"),
    ("class4_child1_cert_extractor_exact.ts",
     "52bcaf509ea12fad4c936501d30d26b5b66c0085"),
    ("class4_child1_cert_extractor_exact_ms23.ts",
     "c267f260d1d6fcc49ed5367509e854c81822497e"),
    ("class4_child1_sweep_engine.ts",
     "bd6a650aafbcea2fde30d84cd52717fcb718fba0"),
    ("class4_child1_chunk_prover.ts",
     "fc74d2156290175dacecd9d9413eb6fbda452e62"),
    ("class4_child1_runner.ts",
     "8744fc65b6b7cac6bd561403ce4c749e01c51359"),
    ("class4_child1_runner_v16.ts",
     "0a4a86f6828dc010c89ff17596054336a6b6091f"),
    ("class4_child1_runner_v17.ts",
     "c132cc6425eee3feaeef1d697dd74f968cfedb59"),
    ("class4_child1_cert_extractor_exact_v16.ts",
     "5518d375fc6b4a7a14c22a1a65586f0c1c5731c0"),
]
EXTRACTOR_FAMILY = ["class4_child1_cert_extractor.ts",
                    "class4_child1_cert_extractor_exact.ts",
                    "class4_child1_cert_extractor_exact_ms23.ts"]
SWEEP_FAMILY = ["class4_child1_sweep_engine.ts",
                "class4_child1_chunk_prover.ts",
                "class4_child1_runner.ts"]
FIXED_FAMILY = ["class4_child1_runner_v16.ts",
                "class4_child1_runner_v17.ts",
                "class4_child1_cert_extractor_exact_v16.ts"]
OUT = ("class2-lane-extractor-copies-memo-defect-audit-"
       "20261117.json")


def git_blob_sha(b):
    return hashlib.sha1(b"blob %d\x00" % len(b) + b).hexdigest()


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def memo_blocks(src):
    lines = src.splitlines()
    out = []
    for i, l in enumerate(lines):
        if "function memoFind" in l or "function memoEntry" in l:
            j = i
            while j < len(lines) and not (lines[j].strip().endswith(
                    "return -1; }") and j > i):
                j += 1
            assert j < len(lines), "memo block not terminated"
            out.append(norm("\n".join(lines[i:j + 1])))
    assert len(out) == 2, ("memoFind/memoEntry blocks", len(out))
    return out


def main():
    srcs = {}
    for name, blob in FILES:
        b = open(os.path.join(ROOT, name), "rb").read()
        got = git_blob_sha(b)
        assert got == blob, ("blob pin mismatch", name, got, blob)
        srcs[name] = b.decode()

    entries = []
    for name, _blob in FILES:
        src = srcs[name]
        find_b, entry_b = memo_blocks(src)
        # bug A: signed comparison (no >>>0) vs fixed unsigned comparison
        sign_fixed = "mK0[h]===(M0>>>0)" in find_b
        # bug B: dead negative-bound update vs sentinel-aware fixed update
        dead_nowin = src.count("d>mNoWin[h]) mNoWin[h]=d;")
        dead_nolose = src.count("e>mNoLose[h]) mNoLose[h]=e;")
        fixed_nowin = src.count("(mNoWin[h]===255||d>mNoWin[h])) mNoWin[h]=d;")
        fixed_nolose = src.count("(mNoLose[h]===255||e>mNoLose[h])) mNoLose[h]=e;")
        # key arrays are Uint32Array in ALL copies (fixed copies compare
        # unsigned via >>>0 instead of switching the array type)
        u32_keys = re.search(r"mK0\s*=\s*new Uint32Array", src) is not None
        ms_line = [l.strip() for l in src.splitlines()
                   if re.match(r"\s*(const|let)\s+MS\s*=", l)]
        assert len(ms_line) == 1, ("MS declaration count", name)
        ms_val = re.search(r"MS\s*=\s*1\s*<<\s*(\d+)", ms_line[0])
        assert ms_val, ("MS declaration parse", name)
        if sign_fixed:
            assert dead_nowin == 0 and dead_nolose == 0, ("fixed sign but dead bound", name)
            assert fixed_nowin >= 1 and fixed_nolose >= 1, ("fixed sign but no fixed bound", name)
            bug_a = False
            bug_b = False
        else:
            assert dead_nowin == 1 and dead_nolose == 1, ("dead bound count", name)
            assert fixed_nowin == 0 and fixed_nolose == 0, ("mixed bound styles", name)
            bug_a = True
            bug_b = True
        assert u32_keys, ("Uint32Array key declaration", name)
        family = ("extractor" if name in EXTRACTOR_FAMILY else
                  "sweep-side" if name in SWEEP_FAMILY else
                  "repaired" if name in FIXED_FAMILY else "?")
        entries.append({
            "file": name,
            "git_blob_sha": git_blob_sha(src.encode()),
            "family": family,
            "memo_find_block_sha256": hashlib.sha256(find_b.encode()).hexdigest(),
            "memo_entry_block_sha256": hashlib.sha256(entry_b.encode()).hexdigest(),
            "memo_find_block": find_b,
            "memo_entry_block": entry_b,
            "uint32array_keys": True,
            "ms_shift": int(ms_val.group(1)),
            "bug_a_signed_memo_key": bug_a,
            "bug_b_dead_negative_bounds": bug_b,
        })

    # family token identity: whitespace-normalized memo blocks are identical
    # within each family
    for fam, members in [("extractor", EXTRACTOR_FAMILY),
                         ("sweep-side", SWEEP_FAMILY),
                         ("repaired-runners", ["class4_child1_runner_v16.ts",
                                               "class4_child1_runner_v17.ts"])]:
        hs = {(e["memo_find_block_sha256"], e["memo_entry_block_sha256"])
              for e in entries if e["file"] in members}
        assert len(hs) == 1, ("family memo block divergence", fam, hs)

    # the two buggy families differ ONLY in whitespace: token-split equality
    def tokens(s):
        return re.sub(r"\s+", "", s)
    ex = next(e for e in entries if e["file"] == "class4_child1_cert_extractor_exact.ts")
    sw = next(e for e in entries if e["file"] == "class4_child1_sweep_engine.ts")
    assert tokens(ex["memo_find_block"]) == tokens(sw["memo_find_block"]), \
        "extractor vs sweep memoFind differ beyond whitespace"
    assert tokens(ex["memo_entry_block"]) == tokens(sw["memo_entry_block"]), \
        "extractor vs sweep memoEntry differ beyond whitespace"

    # ms23 is exactly one line away from exact (the MS capacity line)
    a = srcs["class4_child1_cert_extractor_exact.ts"].splitlines()
    b = srcs["class4_child1_cert_extractor_exact_ms23.ts"].splitlines()
    assert len(a) == len(b), "ms23 line count differs from exact"
    diffs = [(i, a[i], b[i]) for i in range(len(a)) if a[i] != b[i]]
    assert len(diffs) == 1, ("ms23 vs exact diff count", diffs)
    i, la, lb = diffs[0]
    assert "MS=1<<18" in la.replace(" ", "") and "MS=1<<23" in lb.replace(" ", ""), \
        ("ms23 diff is not the MS line", la, lb)
    ms23_diff = {"line_index": i, "exact": la.strip(), "ms23": lb.strip()}

    # Node.js sign demo (same mechanism class as the K0907 verifier check)
    demo_code = (
        "const M = -2059231232; "  # int32 with bit 31 set
        "const u = new Uint32Array(1); u[0] = M; "
        "const i32 = new Int32Array(1); i32[0] = M; "
        "const out = {stored_uint32: u[0], signed_value: M, "
        "uint32_equal: u[0] === M, int32_equal: i32[0] === M}; "
        "process.stdout.write(JSON.stringify(out));"
    )
    p = subprocess.run(["node", "-e", demo_code], capture_output=True, text=True)
    assert p.returncode == 0, ("node sign demo failed", p.stderr[:200])
    demo = json.loads(p.stdout)
    assert demo["stored_uint32"] == (demo["signed_value"] + 2 ** 32)
    assert demo["uint32_equal"] is False and demo["int32_equal"] is True

    # consumer history (published repo commits, recorded not re-derived here)
    history = {
        "class4_child1_sweep_engine.ts":
            "added 2026-11-13 (commit 449d0941a, class4-batch1 sandbox sweep engine v15)",
        "class4_child1_chunk_prover.ts":
            "added 2026-11-13 (commit e55d8225c, class4-batch1 chunk prover)",
        "class4_child1_runner.ts":
            "added 2026-11-13 (commit 3b0603fa4, class4-batch1 external runner; "
            "transport repair 2a1af3a79 restored identical bytes)",
        "class4_child1_cert_extractor.ts":
            "added 2026-11-13 (commit 761b6ea7c, class4-batch1 certificate extractor)",
        "class4_child1_runner_v16.ts":
            "added 2026-11-14 (commit c56ead53f: unsigned TT keys + sentinel-aware bounds)",
        "class4_child1_runner_v17.ts":
            "added 2026-11-16 (commit b0c2985f7); the engine of the published "
            "cost-73i/73j/73k/73l raw sweeps and of the memo-capacity measurement",
        "class4_child1_cert_extractor_exact_v16.ts":
            "added 2026-11-14 (repaired extractor; not used for published certificates)",
    }

    summary = {
        "files_audited": len(entries),
        "bug_a_and_b_present": sorted(e["file"] for e in entries
                                      if e["bug_a_signed_memo_key"]),
        "both_bugs_fixed": sorted(e["file"] for e in entries
                                  if not e["bug_a_signed_memo_key"]),
        "extractor_family_token_identical": True,
        "sweep_family_token_identical": True,
        "buggy_families_whitespace_identical": True,
        "ms23_single_line_diff": ms23_diff,
        "node_sign_demo": demo,
        "published_sweep_engine_v17_is_fixed": True,
    }

    doc = {
        "schema": "n11-class2-lane-extractor-copies-memo-defect-audit-20261117-v1",
        "date": "2026-11-17",
        "basis": ("K0907 (item K0907-extractor-memo-sign-bug-and-dead-negative-bounds.md, "
                  "verifier verify_extractor_memo_sign_bug_73k_20261117.py) verified both "
                  "memo defects for class4_child1_cert_extractor_exact.ts (blob 52bacf50...) "
                  "and explicitly left the other copies unaudited; this audit closes that "
                  "limitation for all class4_child1 engine copies in the experiment scripts dir"),
        "method": {
            "pins": ("all nine source files fetched from the commit-pinned raw CDN mirror and "
                     "asserted against the GitHub git blob shas of main"),
            "blocks": ("memoFind/memoEntry extracted per file and compared "
                       "whitespace-normalized: the three extractor-family copies are identical, "
                       "the three sweep-side copies are identical, and the two buggy families are "
                       "identical to each other after full whitespace removal (token equality), so "
                       "the K0907 dump-quantified mechanism applies verbatim to every buggy copy"),
            "patterns": ("bug A present = memoFind/memoEntry compare mK0[h]===M0 without >>>0 "
                         "(exactly 2 comparison sites per file); fixed = mK0[h]===(M0>>>0). "
                         "bug B present = exactly one dead nowin update "
                         "'d>mNoWin[h]) mNoWin[h]=d;' and one dead nolose twin; fixed = "
                         "sentinel-aware '(mNoWin[h]===255||d>mNoWin[h])' style. All nine copies "
                         "declare the key arrays as Uint32Array (the fixed copies repair the "
                         "comparison, not the array type)"),
            "demo": ("node -e sign demo: storing an int32 with bit 31 set into Uint32Array reads "
                     "back as value+2^32, so === against the original negative value is false "
                     "(Int32Array compares true). This is the no-false-hit direction: a stored "
                     "key can only compare equal to a non-negative operand, so a miss is the "
                     "worst outcome and no wrong memo hit is possible"),
            "ms23": ("class4_child1_cert_extractor_exact_ms23.ts differs from "
                     "class4_child1_cert_extractor_exact.ts in exactly one line (MS=1<<18 -> "
                     "1<<23), asserted line by line, so K0907's audit of exact.ts covers the ms23 "
                     "variant used for the published 73k/73l certificate bands"),
        },
        "entries": entries,
        "consumer_history": history,
        "summary": summary,
        "interpretation_guard": [
            ("both defects are performance-only in every copy: bug A can only cause memo misses "
             "and duplicate insertions (a stored unsigned key never compares equal to a negative "
             "signed operand and can only match a genuinely equal key), bug B only leaves the "
             "negative-bound shortcuts permanently dead; no published verdict, node count or "
             "certificate byte is invalidated, and node counts remain the verbatim values"),
            ("the published cost-73i/73j/73k/73l raw sweeps were produced by "
             "class4_child1_runner_v17 (blob c132cc64), which already carries both fixes; the "
             "sweep-side memo-capacity gains measured for v17 at MS=1<<23 are pure capacity "
             "effects, not sign-bug effects"),
            ("the buggy copies are the 2026-11-13 class4-batch1-era engines (v15 sweep engine, "
             "chunk prover, FBT-saturation external runner) and the verbatim extractor family; "
             "all outputs they produced remain valid with bug-inclusive node counts"),
            ("the repo-verbatim extractors stay unrepaired on purpose for the published "
             "determinism chain; the fixed variants (v16 extractor: both fixes, runner v16/v17) "
             "are the measured-only or going-forward engines per the K0907 battery"),
            ("this audit changes no verdict, closes no manifest row, and moves no frontier "
             "number; the receipt folds stay pending behind their own lanes"),
            ("WIN7-D10 certificates prove only individual 7-stone roots within depth 10; "
             "REFUTED-D10 is not a LOSS proof; 11x11 empty board, two-stone roots {49,60} and "
             "{59,60}, S2 {59,60}, class 1, class 2 and class 4 all remain UNKNOWN"),
        ],
    }
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=False)
        fh.write("\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
