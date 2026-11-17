#!/usr/bin/env python3
"""Cross-lane agreement check for the cost73k band memo extraction
capacity measurement (2026-11-17).

Background: the measurement (fresh MS=1<<24 battery -32.6% vs the published
fresh MS=1<<18 baseline, load-dependent band-wide sharing penalty
+11.69% at ms23 / +1.66% at ms24, bit-117 memo capacity sensitivity curve,
per-bit sharing ratios, 22/22 byte-identical certificate gates) was
published by a concurrent session at commits a3c27e9f / c170a4ef:
  output/class2-lane-band-memo-extraction-measurement-73k-20261117.json
  scripts/measure_band_memo_extraction_73k.ts
  scripts/measure_band_memo_extraction_73k_20261117.py
  research/log/2026-11-17-n11-class2-lane-band-memo-extraction-measurement-73k.md

A second session, unaware of that publication, rebuilt the pinned pubtest
environment from raw CDN pin 1da42ce0 (extractor engine
class4_child1_cert_extractor_exact.ts, blob 52bcaf509ea12fad4c936501d30d26b5b66c0085;
manifest blob 0892aed07d187ae2fb3b4b90a21c7adbc1002b62; candidate enumerator
legal_candidates.py, blob 8e97082c42838c7a4a4b6d2dd235276c8d43ab9a) and ran
an independently implemented orchestrator from scratch (different code from
the published measure_band_memo_extraction_73k.ts / _20261117.py driver,
same pinned engine), reproducing the whole measurement. At push time the
duplicate was detected (all four planned paths already published), so the
contribution was converted into this agreement check instead of a duplicate
publication (precedent: check_cost73j_reverification_cross_lane_
agreement_20261117.py; K0900 cross-lane agreement).

Independence of the two runs: different sessions, different machines, the
second run rebuilt the environment from source pins after an environment
reset, used a separately written orchestrator, and executed fresh Node.js
processes per configuration. Node counts are pure integer search accounting
over a deterministic engine, so independent fresh executions must agree
exactly; any mismatch would falsify the determinism claim.

This script fetches the published measurement JSON from the raw CDN at
pinned commit a3c27e9f, verifies its git blob sha, and compares it field by
field against the THIS_SESSION constants below (the second session's
independent re-run values): band-wide single-process runs at ms18/22/23/24
(totals, final memo occupancy, 22 per-bit node counts each), the fresh
per-process batteries at ms23 and ms24 (totals and 22 per-bit counts each),
the band-vs-fresh sharing decomposition at ms23 and ms24 (derived ratios
recomputed from the raw counts), and the bit-117 fresh sensitivity sweep at
six capacities. Derived percentages (vs_published, penalties, load) are
recomputed from this session's raw integers and compared to the published
rounded values.

Usage:
  python3 check_cost73k_memo_measurement_cross_lane_agreement_20261117.py \\
      [published.json] [out_dir]
Without arguments the pinned JSON is fetched from the raw CDN. The output
agreement JSON is written to out_dir (default: the script's ../output).

This check changes no verdicts, opens or closes no manifest row, and
modifies no certificate bytes. 11x11 remains UNKNOWN.
"""
import hashlib
import json
import pathlib
import sys
import urllib.request

PUBLISHED_URL = ("https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/"
                 "a3c27e9f/research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
                 "output/class2-lane-band-memo-extraction-measurement-73k-20261117.json")
PUBLISHED_BLOB = "ce625db014e0269fad48c573d29389e6f803310b"
PUBLISHED_COMMITS = {"artifacts": "a3c27e9f", "log_fix": "c170a4ef"}

# ---------------------------------------------------------------------------
# THIS_SESSION: the second session's independent re-run values (2026-11-17).
# Extracted verbatim from that session's measurement JSON run; see the
# agreement log entry for the runtime record (including the ERR_MODULE_NOT_FOUND
# failure on the first orchestrator pass, fixed by generating the ms22 driver
# variant, and the resume that preserved band_ms18).
# ---------------------------------------------------------------------------
BITS = [0, 7, 11, 15, 35, 39, 41, 44, 58, 62, 73, 76, 87, 89, 94, 95, 97, 98, 103, 105, 112, 117]
BASELINE_TOTAL = 155946109
BAND_TOTALS = {18: 205129712, 22: 142171197, 23: 121186659, 24: 106861135}
BAND_OCCUPIED = {18: 262144, 22: 4067454, 23: 7144086, 24: 10804024}
BAND_PER_BIT = {
    18: {
    0: 6442831, 7: 10234319, 11: 5610909, 15: 14807600, 35: 10437826,
    39: 4546407, 41: 4792669, 44: 9971167, 58: 10711461, 62: 4157751,
    73: 13705334, 76: 9113950, 87: 11639639, 89: 7683796, 94: 8360321,
    95: 11857737, 97: 10994220, 98: 9324844, 103: 10620467, 105: 7186388,
    112: 9791947, 117: 13138129,},
    22: {
    0: 4652905, 7: 5590458, 11: 3228612, 15: 9218400, 35: 5920392,
    39: 2390341, 41: 2233556, 44: 5595212, 58: 6082143, 62: 2881464,
    73: 9199078, 76: 6160288, 87: 9290759, 89: 5810915, 94: 6702780,
    95: 11857737, 97: 6108396, 98: 7217757, 103: 8533813, 105: 5222546,
    112: 7557478, 117: 10716167,},
    23: {
    0: 4303203, 7: 5039319, 11: 2910849, 15: 8159953, 35: 5045405,
    39: 1965979, 41: 1768864, 44: 4669878, 58: 4866570, 62: 2241220,
    73: 7510771, 76: 4815817, 87: 8054680, 89: 4928329, 94: 5625212,
    95: 11857737, 97: 4429190, 98: 6073176, 103: 7107709, 105: 4356101,
    112: 6167016, 117: 9289681,},
    24: {
    0: 4052092, 7: 4779818, 11: 2729113, 15: 7566378, 35: 4640168,
    39: 1807387, 41: 1567428, 44: 4301098, 58: 4256735, 62: 1811856,
    73: 6516009, 76: 3937754, 87: 6861735, 89: 4190038, 94: 4716565,
    95: 11857737, 97: 3508790, 98: 5190033, 103: 5918698, 105: 3696202,
    112: 5055110, 117: 7900391,},
}
FRESH23_TOTAL = 108499241
FRESH23_PER_BIT = {
    0: 4303203, 7: 4970943, 11: 2910026, 15: 8108353, 35: 4871692,
    39: 2037105, 41: 1868639, 44: 4617329, 58: 4567866, 62: 1771346,
    73: 7370204, 76: 4098489, 87: 6581793, 89: 3869180, 94: 4204274,
    95: 11857737, 97: 3815019, 98: 5336993, 103: 5828967, 105: 3641568,
    112: 4767520, 117: 7100995,}
FRESH24_TOTAL = 105117037
FRESH24_PER_BIT = {
    0: 4052092, 7: 4753185, 11: 2788279, 15: 7718508, 35: 4708548,
    39: 2013805, 41: 1854374, 44: 4527094, 58: 4511718, 62: 1739635,
    73: 7065611, 76: 3877225, 87: 6317339, 89: 3781817, 94: 4138931,
    95: 11857737, 97: 3788235, 98: 5097365, 103: 5540871, 105: 3548159,
    112: 4620105, 117: 6816404,
}
SENS_BIT117 = {18: 10635766, 20: 8768282, 21: 8103818, 22: 7599134, 23: 7100995, 24: 6816404}
SENS_SLOTS = {18: 262144, 20: 1048576, 21: 2097152, 22: 4194304, 23: 8388608, 24: 16777216}

# Session-2-only extras (not present in the published JSON; recorded here so
# the second run's additional instrumentation is reproducible and auditable):
UNION_ROWS = 682861
UNION_SUM_PER_BIT_ROWS = 966535
UNION_MD5 = "2133564406306fd1657af7ac11be6f5d"
BIT95_NODES_ALL_CONFIGS = 11857737  # identical in band ms18/22/23/24 and both fresh batteries
ANCHOR_BIT39_FRESH_MS18 = 2597243  # equals the published manifest value


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def check(published_path: pathlib.Path, out_dir: pathlib.Path) -> int:
    rb = published_path.read_bytes()
    got_blob = git_blob_sha(rb)
    assert got_blob == PUBLISHED_BLOB, f"published blob mismatch: {got_blob}"
    pub = json.loads(rb.decode("utf-8"))
    assert pub["schema"] == "n11-class2-lane-band-memo-extraction-measurement-73k-20261117-v1"

    checks: list = []  # (name, published, this_session, ok)

    def add(name, pv, mv):
        checks.append((name, pv, mv, pv == mv))

    # 0. baseline
    add("published_baseline.total",
        pub["published_baseline"]["per_bit_fresh_process_extraction_nodes_total"],
        BASELINE_TOTAL)

    # 1. band-wide runs: totals, occupancy, byte-identity, per-bit nodes
    for ms in (18, 22, 23, 24):
        r = pub["band_wide_runs"][str(ms)]
        add(f"band_ms{ms}.total_nodes", r["total_nodes"], BAND_TOTALS[ms])
        add(f"band_ms{ms}.final_occupied", r["final_occupied"], BAND_OCCUPIED[ms])
        add(f"band_ms{ms}.byte_identical_certificates", r["byte_identical"], 22)
        pb = {e["bit"]: e["nodes_this_run"] for e in r["per_bit"]}
        add(f"band_ms{ms}.per_bit_bits", sorted(pb), BITS)
        for b in BITS:
            add(f"band_ms{ms}.per_bit[{b}].nodes", pb[b], BAND_PER_BIT[ms][b])
        # derived: vs_published recomputed from this session's raw integers
        add(f"band_ms{ms}.vs_published(recomputed)",
            r["vs_published"], round(BAND_TOTALS[ms] / BASELINE_TOTAL, 6))

    # 2. fresh ms23 battery
    f23 = pub["attribution"]["fresh_per_bit_ms23"]
    add("fresh_ms23.total_nodes", f23["total_nodes"], FRESH23_TOTAL)
    add("fresh_ms23.vs_published(recomputed)", f23["vs_published"],
        round(FRESH23_TOTAL / BASELINE_TOTAL, 6))
    add("fresh_ms23.byte_identical_22_of_22", f23["byte_identical_22_of_22"], True)
    pb23 = {e["bit"]: e["fresh_ms23_nodes"] for e in f23["per_bit"]}
    add("fresh_ms23.per_bit_bits", sorted(pb23), BITS)
    for b in BITS:
        add(f"fresh_ms23.per_bit[{b}].nodes", pb23[b], FRESH23_PER_BIT[b])
    add("fresh_ms23.per_bit_sum(recomputed)", sum(pb23.values()), FRESH23_TOTAL)

    # 3. sharing decomposition at ms23 (band23 vs fresh23)
    sd = pub["attribution"]["sharing_decomposition_same_capacity_ms23"]
    add("sharing_ms23.band_wide_total", sd["band_wide_total"], BAND_TOTALS[23])
    add("sharing_ms23.fresh_total", sd["fresh_total"], FRESH23_TOTAL)
    add("sharing_ms23.penalty(recomputed)", sd["band_wide_penalty_vs_fresh"],
        round(BAND_TOTALS[23] / FRESH23_TOTAL, 6))
    for e in sd["per_bit"]:
        b = e["bit"]
        add(f"sharing_ms23.per_bit[{b}].fresh_nodes", e["fresh_ms23_nodes"], FRESH23_PER_BIT[b])
        add(f"sharing_ms23.per_bit[{b}].band_nodes", e["band_ms23_nodes"], BAND_PER_BIT[23][b])

    # 4. fresh ms24 battery
    f24 = pub["attribution"]["fresh_per_bit_ms24"]
    add("fresh_ms24.status", f24["status"], "complete")
    add("fresh_ms24.total_nodes", f24["total_nodes"], FRESH24_TOTAL)
    add("fresh_ms24.vs_published(recomputed)", f24["vs_published"],
        round(FRESH24_TOTAL / BASELINE_TOTAL, 6))
    pb24 = {e["bit"]: e["fresh_ms24_nodes"] for e in f24["per_bit"]}
    add("fresh_ms24.per_bit_bits", sorted(pb24), BITS)
    for b in BITS:
        add(f"fresh_ms24.per_bit[{b}].nodes", pb24[b], FRESH24_PER_BIT[b])
    add("fresh_ms24.per_bit_sum(recomputed)", sum(pb24.values()), FRESH24_TOTAL)

    # 5. band24 vs fresh24 sharing
    b24 = pub["attribution"]["band24_sharing_vs_fresh24_same_capacity"]
    add("band24_sharing.band_wide_total", b24["band_wide_total"], BAND_TOTALS[24])
    add("band24_sharing.fresh_total", b24["fresh_total"], FRESH24_TOTAL)
    add("band24_sharing.penalty_pct(recomputed)", b24["penalty_pct"],
        round((BAND_TOTALS[24] - FRESH24_TOTAL) / FRESH24_TOTAL * 100, 2))
    add("band24_sharing.band_final_occupied", b24["band_final_occupied"], BAND_OCCUPIED[24])
    add("band24_sharing.band_memo_slots", b24["band_memo_slots"], SENS_SLOTS[24])
    add("band24_sharing.band_final_load_pct(recomputed)", b24["band_final_load_pct"],
        round(BAND_OCCUPIED[24] / SENS_SLOTS[24] * 100, 1))
    for k, v in b24["per_bit_ratio_band_over_fresh"].items():
        b = int(k)
        add(f"band24_sharing.per_bit_ratio[{b}](recomputed)", v,
            round(BAND_PER_BIT[24][b] / FRESH24_PER_BIT[b], 4))

    # 6. bit-117 sensitivity sweep (fresh, six capacities)
    sens = {e["ms_shift"]: e for e in pub["sensitivity_bit117_fresh"]}
    add("sensitivity_bit117.capacities", sorted(sens), sorted(SENS_BIT117))
    for ms, nodes in SENS_BIT117.items():
        add(f"sensitivity_bit117.ms{ms}.memo_slots", sens[ms]["memo_slots"], SENS_SLOTS[ms])
        add(f"sensitivity_bit117.ms{ms}.nodes", sens[ms]["nodes"], nodes)
        add(f"sensitivity_bit117.ms{ms}.byte_identical", sens[ms]["byte_identical"], True)

    # 7. gates
    add("gates.failures", pub["gates"]["failures"], [])
    add("gates.all_expected_values_reproduced",
        pub["gates"]["all_expected_values_reproduced"], True)

    n_ok = sum(1 for c in checks if c[3])
    mismatches = [{"field": n, "published": p, "this_session": m}
                  for n, p, m, ok in checks if not ok]
    agreement = n_ok == len(checks)

    out = {
        "schema": "n11-class2-lane-cost73k-memo-measurement-cross-lane-agreement-20261117-v1",
        "date": "2026-11-17",
        "published_measurement": {
            "file": ("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/"
                     "class2-lane-band-memo-extraction-measurement-73k-20261117.json"),
            "git_blob_sha": PUBLISHED_BLOB,
            "pinned_commits": PUBLISHED_COMMITS,
            "fetch_url": PUBLISHED_URL,
        },
        "this_session": {
            "independence": ("separate concurrent session; environment rebuilt from raw "
                             "CDN pin 1da42ce0 after a reset; independently implemented "
                             "orchestrator (not the published driver), same pinned "
                             "engine blobs (extractor 52bcaf50..., manifest 0892aed0..., "
                             "enumerator 8e97082c...); fresh Node.js process per "
                             "configuration; ~50 min wall, all gates passed, FAILURES: 0"),
            "duplicate_publication_avoided": ("all four planned output paths were already "
                                              "published by the concurrent session; per "
                                              "the no-duplicate-publication policy the "
                                              "second run was converted into this "
                                              "agreement check (precedent 73j)"),
            "runtime_failure_recorded": ("first orchestrator pass failed at band_ms22 "
                                         "with ERR_MODULE_NOT_FOUND (ms22 driver variant "
                                         "not yet generated); fixed by generating the "
                                         "variant, band_ms18 preserved by resume; second "
                                         "pass re-verified every gate from the resumed "
                                         "state, FAILURES: 0"),
            "extras_not_in_published_json": {
                "union_rows": UNION_ROWS,
                "union_sum_per_bit_rows": UNION_SUM_PER_BIT_ROWS,
                "union_md5": UNION_MD5,
                "union_band_ms18_ms22_ms23_byte_equal": True,
                "union_fresh_battery_equal": True,
                "bit95_nodes_all_configurations": BIT95_NODES_ALL_CONFIGS,
                "anchor_bit39_fresh_ms18": ANCHOR_BIT39_FRESH_MS18,
            },
        },
        "compared": {
            "field_checks": len(checks),
            "checks_ok": n_ok,
            "mismatches": mismatches,
            "coverage": (
                "published fresh MS=1<<18 baseline total; band-wide single-process runs "
                "ms18/22/23/24 (totals, final memo occupancy, byte-identity, 22 per-bit "
                "node counts each, vs_published ratios); fresh per-process batteries "
                "ms23 and ms24 (status, totals, vs_published ratios, 22 per-bit counts "
                "each); ms23 sharing decomposition (band/fresh totals, penalty, per-bit "
                "band and fresh nodes); ms24 band-vs-fresh sharing (totals, penalty, "
                "occupancy, load, 22 per-bit ratios); bit-117 fresh sensitivity at six "
                "capacities (slots and nodes); gates"),
        },
        "verdict": ("AGREEMENT: every field of the published cost73k band memo extraction "
                    "capacity measurement reproduces exactly from the second session's "
                    "independent re-run (same pinned engine, independently implemented "
                    "orchestrator, fresh processes); no field disagrees"
                    ) if agreement else "DISAGREEMENT",
        "scope_guard": ("this is a measurement-reproducibility agreement between two "
                        "independent executions of the same deterministic engine; it is "
                        "not a game-theoretic result, closes no manifest row, changes no "
                        "certificate bytes and adds no verdict; WIN7-D10 proves a "
                        "first-player win within depth 10 from each individual 7-stone "
                        "root only; REFUTED-D10 is not a LOSS proof; 11x11 empty board, "
                        "two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 "
                        "remain UNKNOWN"),
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "class2-lane-cost73k-memo-measurement-cross-lane-agreement-20261117.json"
    text = json.dumps(out, indent=1, ensure_ascii=True) + "\n"
    dst.write_text(text)
    print(f"agreement JSON written: {dst} ({len(text)} bytes)")
    print(f"checks: {n_ok}/{len(checks)} ok; mismatches: {len(mismatches)}")
    print("verdict:", out["verdict"].split(":")[0])
    print("blob:", git_blob_sha(text.encode()))
    return 0 if agreement else 1


def main() -> None:
    args = sys.argv[1:]
    if len(args) >= 1:
        pub_path = pathlib.Path(args[0])
    else:
        print(f"fetching pinned published JSON: {PUBLISHED_URL}")
        with urllib.request.urlopen(PUBLISHED_URL) as resp:
            rb = resp.read()
        pub_path = pathlib.Path("_pinned_cost73k_measurement.json")
        pub_path.write_bytes(rb)
        got = git_blob_sha(rb)
        assert got == PUBLISHED_BLOB, f"blob mismatch on fetch: {got}"
    out_dir = pathlib.Path(args[1]) if len(args) >= 2 else (
        pathlib.Path(__file__).resolve().parent.parent / "output")
    sys.exit(check(pub_path, out_dir))


if __name__ == "__main__":
    main()
