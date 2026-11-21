#!/usr/bin/env python3
"""n11 S5 wave-2 coordination refresh (Part A: measurement only, no searches).

Re-executes the published class-closure-priority measurement gates byte-exactly
(pinned inputs, published-output byte comparison), then registers the fixed
claimed key sets of the concurrent single-owner lanes from machine sources,
verifies the two known coordination facts, computes two static post-wave
scheduling scenarios (pure IF-scenarios; no probability, no verdict), and
ranks the wave-2 unclaimed targets with full machine-derived exclusive probe
orders for the next classes.

This script performs NO search and creates NO verdict.  Every number here is
a scheduling/measurement fact over published solver-trusted artifacts.
11x11, {60,27}, and third moves 100/108 remain UNKNOWN.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

# ---- pins (all fetched from main by bootstrap.sh) -------------------------
PIN = {
    "geometry_json_gz": "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54",
    "probe13_cache": "60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6",
    "supply_csv": "31f0d29b820a69508af0c352c22f09b244bff5b9ae79476679047cdb160ea954",
    "candidate_ledger_csv": "2a4c2382d812102f8132339c871b07ee998e933c80da876759e51e84f64fda80",
    "historical_profile_json": "6b2971e53059ac36af7bf161a61d90d65f85e604e27b93d013e7a2853fdceddc",
    "sbd_corpus_def_json": "779685a789dd2ab83266f685d26ffd6d25ab12ef33f2252320e4e6e1b0823585",
    "ccp_script_py": "2aa249d883d3948cf3c617d044f202eb0dac616005b7ce036658d8360a7d48b2",
    "ccp_published_json": "c837c52d252a632a2d247e0cac50222e2bf641062c8afd7ecdd4f839c67dcea6",
    "ccp_published_csv": "139eb0a0e3453309adcd617e9ca68ddd0615244c5e59f814d8c08bed5d69de87",
}

FOCUS_CLASS = "1188950301626859520:536870912"
CERT_CLASS = "1297036692683752448:0"
THIRD_CLASS = "1297036830122704896:0"
FOURTH_CLASS = "1297107061427929088:0"

REPLY27_LANE = {
    "lane": "reply27 two-target S5 candidate probe lane",
    "declaration_commit": "4e944105",
    "claim_kind": "open-ended ranked rule over supply keys with live_parents >= 2",
    "fixed_keyset": False,
    "reflected_keys": "probes 1..13 are already rows of the pinned probe-13 merged cache",
}


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def die(msg: str):
    print(f"GATE FAILED: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="workspace w2 dir")
    args = ap.parse_args()
    w = Path(args.dir)
    inp = w / "inputs"
    geo_p = inp / "geometry.json.gz"
    cache_p = inp / "merged-exact-s5-after-js-probe-13.cache"
    supply_p = inp / "shared-s5-tasks.csv"
    ledger_p = inp / "candidate-classes.csv"
    profile_p = inp / "historical-cost-profile.json"
    sbd_p = inp / "sbd-corpus-def.json"

    for p, s in PIN.items():
        f = {"geometry_json_gz": geo_p, "probe13_cache": cache_p,
             "supply_csv": supply_p, "candidate_ledger_csv": ledger_p,
             "historical_profile_json": profile_p,
             "sbd_corpus_def_json": sbd_p,
             "ccp_script_py": inp / "ccp-class_closure_priority.py",
             "ccp_published_json": inp / "ccp-published-class-closure-priority.json",
             "ccp_published_csv": inp / "ccp-published-class-closure-priority.csv"}[p]
        if digest(f) != s:
            die(f"pin mismatch {p} ({f})")

    # ---- Part A gate 1: byte-exact re-execution of the published ccp ---------
    reexec = w / "out/ccp-reexec"
    reexec.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        [sys.executable, str(inp / "ccp-class_closure_priority.py"),
         "--geometry", str(geo_p), "--cache", str(cache_p), "--supply",
         str(supply_p), "--candidate-ledger", str(ledger_p), "--profile",
         str(profile_p), "--out", str(reexec)],
        capture_output=True, text=True)
    if r.returncode != 0 or "ALL GATES PASS" not in r.stdout:
        die(f"ccp re-execution failed: {r.stdout} {r.stderr}")
    if digest(reexec / "class-closure-priority.json") != PIN["ccp_published_json"] or \
       digest(reexec / "class-closure-priority.csv") != PIN["ccp_published_csv"]:
        die("ccp re-execution not byte-identical to published outputs")

    # ---- census re-derivation (same invariants as the published ccp) --------
    geo = json.loads(gzip.open(geo_p, "rt", encoding="utf-8").read())
    if len(geo) != 3384:
        die("geometry class count")
    cache = {}
    for row in csv.reader(cache_p.open(encoding="utf-8-sig", newline="")):
        if not row or row[0].startswith("#"):
            continue
        k = (int(row[1]), int(row[2]))
        v = int(row[4])
        if k in cache and cache[k] != v:
            die(f"verdict conflict in pinned cache {k}")
        cache[k] = v

    def stage(vals):
        if 1 in vals:
            return "WIN"
        if all(v == 2 for v in vals):
            return "LOSS"
        return "UNKNOWN"

    active = []
    for g in geo:
        ch = {tuple(z) for z in g["children"]}
        vals = [cache.get(z, 0) for z in ch]
        st = stage(vals)
        if st == "UNKNOWN" and {100, 108}.intersection(g["coverage"]):
            active.append([tuple(g["key"]), g["coverage"], ch])
    if len(active) != 62:
        die(f"active class count {len(active)}")
    live_par = defaultdict(set)
    for k, cov, ch in active:
        for child in ch:
            if child not in cache:
                live_par[child].add(k)
    supply = {}
    for row in csv.DictReader(supply_p.open(newline="")):
        supply[(int(row["key"].split(":")[0]), int(row["key"].split(":")[1]))] = row
    if len(supply) != 4562 or set(supply) != set(live_par):
        die("supply/live-incidence mismatch")
    deg = defaultdict(int)
    for child in live_par:
        deg[len(live_par[child])] += 1
    if dict(deg) != {1: 2688, 2: 1874}:
        die(f"supply degree distribution {dict(deg)}")

    def dp(c):
        return int(supply[c]["truncated_cost_proxy_nodes"])

    def kof(c):
        return f"{c[0]}:{c[1]}"

    class_children = {}
    full_children = {}
    for k, cov, ch in active:
        full_children[k] = ch
        class_children[k] = [c for c in ch if c not in cache]

    # ---- claims registry (machine sources, fail-closed) ----------------------
    sbd = json.loads(sbd_p.read_text())
    sbd_corpus99 = {(a, b) for a, b in sbd["corpus99"]}
    sbd_extra2 = {(a, b) for a, b in sbd["unclaimed2"]}
    chain7 = {(a, b) for a, b in sbd["chain7"]}
    if len(sbd_corpus99) != 99 or len(sbd_extra2) != 2 or len(chain7) != 7:
        die("sbd corpus-def sizes")
    if set(map(tuple, sbd["children106"])) != sbd_corpus99 | chain7:
        die("sbd children106 != corpus99 + chain7")

    fk = tuple(map(int, FOCUS_CLASS.split(":")))
    ck = tuple(map(int, CERT_CLASS.split(":")))
    tk = tuple(map(int, THIRD_CLASS.split(":")))
    qk = tuple(map(int, FOURTH_CLASS.split(":")))
    if chain7 != (full_children[ck] & set(cache)):
        die("sbd chain7 != cached cert-class children")
    focus35 = sorted(c for c in class_children[fk] if len(live_par[c]) == 1)
    cert38 = sorted(c for c in class_children[ck] if len(live_par[c]) == 1)
    third39 = sorted(c for c in class_children[tk] if len(live_par[c]) == 1)
    if len(focus35) != 35:
        die(f"focus exclusive {len(focus35)}")
    if len(cert38) != 38:
        die(f"cert exclusive {len(cert38)}")
    if len(third39) != 39:
        die(f"third-cost exclusive {len(third39)}")
    if set(class_children[ck]) != sbd_corpus99:
        die("sbd corpus99 != cert-class unknown children")
    if set(focus35) & set(cert38):
        die("focus/cert exclusive overlap")

    fixed_claims = {
        "focus_lane_35_exclusive_of__1188950301626859520_536870912": set(focus35),
        "certificate_class_exclusive_38_of__1297036692683752448_0": set(cert38),
        "third_cost_class_exclusive_39_of__1297036830122704896_0": set(third39),
        "sbd_fresh_corpus_99_plus_2_of__1297036692683752448_0": sbd_corpus99 | sbd_extra2,
    }
    claimed_all = set()
    for name, s in fixed_claims.items():
        claimed_all |= s
    names = list(fixed_claims)
    pairwise = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            inter = fixed_claims[names[i]] & fixed_claims[names[j]]
            if inter:
                pairwise[f"{names[i]} & {names[j]}"] = sorted(kof(c) for c in inter)

    # ---- coordination fact gate ---------------------------------------------
    if not set(cert38) <= sbd_corpus99:
        die("coordination fact 1: cert38 not subset of sbd corpus99")
    for c in sbd_extra2:
        if c not in live_par:
            die(f"sbd extra row {kof(c)} not live")
    e1, e2 = sorted(sbd_extra2)
    if len(live_par[e1]) != 2 or len(live_par[e2]) != 2:
        die("sbd extra rows are not 2-live-parent children")
    coord_facts = {
        "fact_1_double_claim": {
            "finding": "certificate-class exclusive 38 keys (ccp lane) are fully "
                       "double-claimed inside the sbd fresh-corpus 99 (documented by "
                       "the third-cost lane note); evidence owners keep the decision",
            "intersection": sorted(kof(c) for c in set(cert38) & sbd_corpus99),
            "count": len(set(cert38) & sbd_corpus99),
        },
        "fact_2_sbd_extra_rows_are_shared_children": {
            "finding": "the sbd two extra backward-only rows are live shared children "
                       "of two active classes each; they are not exclusive to the "
                       "cert class, so a cert-class closure cannot consume them alone",
            "rows": {
                kof(e1): sorted(kof(x) for x in live_par[e1]),
                kof(e2): sorted(kof(x) for x in live_par[e2]),
            },
        },
    }

    # ---- per-class claim accounting + two static IF-scenarios ----------------
    per_class = []
    for k, cov, ch in sorted(active):
        unknown = class_children[k]
        unclaimed = [c for c in unknown if c not in claimed_all]
        claimed_here = [c for c in unknown if c in claimed_all]
        unc_excl = [c for c in unclaimed if len(live_par[c]) == 1]
        per_class.append({
            "class": kof(k),
            "coverage": [int(x) for x in sorted(cov)],
            "s5_children": len(ch),
            "s5_unknown": len(unknown),
            "claimed_unknown": len(claimed_here),
            "unclaimed_unknown": len(unclaimed),
            "unclaimed_exclusive": len(unc_excl),
            "unclaimed_shared": len(unclaimed) - len(unc_excl),
            "unclaimed_proxy_sum": sum(dp(c) for c in unclaimed),
            "unknown_proxy_sum": sum(dp(c) for c in unknown),
            "scenario_all_claimed_loss_closable": len(unclaimed) == 0,
            "scenario_all_claimed_parked_closable": len(claimed_here) == 0 and len(unknown) > 0,
        })
    by_class = {r["class"]: r for r in per_class}

    closable_loss = [r["class"] for r in per_class if r["scenario_all_claimed_loss_closable"]]
    if closable_loss != [CERT_CLASS]:
        die(f"scenario all-claimed-LOSS closable set {closable_loss}")
    if by_class[CERT_CLASS]["scenario_all_claimed_parked_closable"]:
        die("cert class parked-closable flag")

    # wave-2 unclaimed ranking: cheapest by unclaimed proxy among classes
    # with at least one unclaimed exclusive key
    w2 = [r for r in per_class if r["unclaimed_exclusive"] > 0]
    w2.sort(key=lambda r: (r["unclaimed_proxy_sum"], r["class"]))
    if w2[0]["class"] != FOURTH_CLASS:
        die(f"wave-2 top class {w2[0]['class']}")

    # fourth-cost class full exclusive machine list + declaration cross-check
    fourth_unk = class_children[qk]
    fourth_unc = [c for c in fourth_unk if c not in claimed_all]
    fourth_excl_unc = [c for c in fourth_unc if len(live_par[c]) == 1]
    fourth_order = sorted(fourth_excl_unc, key=lambda c: (dp(c), c))
    if len(fourth_unk) != 100 or len(fourth_unc) != 98 or len(fourth_order) != 41:
        die(f"fourth-cost accounting {len(fourth_unk)}/{len(fourth_unc)}/{len(fourth_order)}")

    # declaration note probe-order cross-check (fail-closed against drift)
    dec_p = w / "decl-note.md"
    decl_keys = []
    bands = []
    for line in dec_p.read_text(encoding="utf-8").splitlines():
        t = line.strip()
        if t.startswith("proxy band"):
            bands.append(int(t.split()[2].replace(",", "")))
        t2 = t.rstrip(";").rstrip(".")
        if t2.startswith("`") and ":" in t2:
            keys = [x.strip("` ") for x in t2.split(",")]
            if all(x and ":" in x for x in keys):
                decl_keys.extend((bands[-1] if bands else 0, k) for k in keys)
    if [k for _, k in decl_keys] != [kof(c) for c in fourth_order]:
        die("declaration-note 41-key enumeration != machine exclusive order")
    decl_band_hist = defaultdict(int)
    for b, _ in decl_keys:
        decl_band_hist[b] += 1
    mb = defaultdict(int)
    for c in fourth_order:
        mb[dp(c)] += 1
    if dict(decl_band_hist) != dict(mb):
        die(f"band histogram mismatch decl={dict(decl_band_hist)} machine={dict(mb)}")

    # ---- outputs ---------------------------------------------------------------
    outdir = w / "out/wave2-refresh"
    outdir.mkdir(parents=True, exist_ok=True)
    fcdir = w / "out/fourthcost-probe"
    fcdir.mkdir(parents=True, exist_ok=True)

    cols = list(per_class[0].keys())
    with (outdir / "wave2-priority.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        writer.writeheader()
        for r in sorted(per_class, key=lambda r: (r["unclaimed_proxy_sum"], r["class"])):
            writer.writerow(r)

    summary = {
        "part": "A (measurement only; no searches; no verdicts)",
        "input_pins": PIN,
        "ccp_reexecution": "byte-identical to the published class-closure-priority "
                           "outputs (json+csv); re-executed from the pinned script "
                           "and inputs; pinned by sha256 above",
        "claims_registry": {
            "reply27_lane_rule_4e944105": REPLY27_LANE,
            "fixed_claim_sets": {
                name: sorted(kof(c) for c in s) for name, s in fixed_claims.items()
            },
            "fixed_claim_counts": {name: len(s) for name, s in fixed_claims.items()},
            "pairwise_intersections": pairwise,
            "total_fixed_claimed_keys": len(claimed_all),
        },
        "coordination_facts": coord_facts,
        "scenarios": {
            "all_claimed_loss": {
                "statement": "IF every fixed-claimed unknown S5 child of the 62 live "
                             "classes is decided LOSS; static combinatorial "
                             "statement only, no probability used, no verdict made",
                "closable_classes": closable_loss,
                "note": "only the certificate class 1297036692683752448:0 becomes "
                        "closable under this scenario (all 99 of its unknowns are "
                        "claimed by the sbd fresh corpus); every other live class "
                        "still owns unclaimed unknowns",
            },
            "all_claimed_parked_unknown": {
                "statement": "IF every fixed-claimed unknown stays parked as UNKNOWN "
                             "(claimed-but-undecided); classes holding claimed "
                             "unknowns can never close under this scenario",
                "closable_classes": [r["class"] for r in per_class
                                     if r["scenario_all_claimed_parked_closable"]],
            },
        },
        "wave2_unclaimed_targets_top10": [
            {"class": r["class"], "unclaimed_unknown": r["unclaimed_unknown"],
             "unclaimed_exclusive": r["unclaimed_exclusive"],
             "unclaimed_proxy_sum": r["unclaimed_proxy_sum"]}
            for r in w2[:10]
        ],
        "fourth_cost_class_full_exclusive": {
            "class": FOURTH_CLASS,
            "coverage": by_class[FOURTH_CLASS]["coverage"],
            "s5_unknown": 100,
            "unclaimed_unknown": 98,
            "unclaimed_proxy_sum": by_class[FOURTH_CLASS]["unclaimed_proxy_sum"],
            "exclusive_unclaimed": 41,
            "exclusive_unclaimed_probe_order": [
                {"order": i + 1, "key": kof(c),
                 "legal": int(supply[c]["legal"]),
                 "truncated_cost_proxy_nodes": dp(c)}
                for i, c in enumerate(fourth_order)
            ],
            "known_shared_children_claims": {
                kof(c): sorted(kof(x) for x in live_par[c]) for c in fourth_unk
                if c in claimed_all
            },
            "declaration_cross_check": "41-key order matches the single-owner "
                                       "declaration note enumeration band-by-band "
                                       "(fail-closed gate)",
        },
        "status_guard": "the standard 11x11 empty board, the two-stone root {60,27}, "
                        "third moves 100/108 and every per-key S5 question remain "
                        "UNKNOWN; proxies, nodes and scenario flags are scheduling "
                        "quantities, never verdicts",
    }
    (outdir / "wave2-priority.json").write_text(
        json.dumps(summary, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    fc = {
        "experiment": "n11-fourthcost-class-s5-exclusive-probe-1297107061427929088",
        "class": FOURTH_CLASS,
        "claim_kind": "single-owner exclusive S5 probe batch (declaration "
                      "1f94f50139db6e6aef1a09a553506bcdcc65e1b4)",
        "key_count": len(fourth_order),
        "exclusive_unclaimed_probe_order": [
            {"order": i + 1, "key": kof(c), "legal": int(supply[c]["legal"]),
             "truncated_cost_proxy_nodes": dp(c)}
            for i, c in enumerate(fourth_order)
        ],
        "source": "machine-derived by n11-s5-wave2-refresh (claims registry over "
                   "pinned corpus-def + live incidence); cross-checked against the "
                   "declaration note enumeration",
        "status_guard": "no verdict yet; keys are search targets only; 11x11 "
                        "remains UNKNOWN",
    }
    (fcdir / "fourth-cost-exclusive-keys.json").write_text(
        json.dumps(fc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    print("WAVE2 REFRESH: ALL GATES PASS")
    print(f"fixed claims: focus35 cert38 third39 sbd99+2 = {len(claimed_all)} keys; "
          f"pairwise double-claims: {len(pairwise)}")
    print(f"scenario all-LOSS closable: {closable_loss}")
    print(f"scenario parked closable: "
          f"{[r['class'] for r in per_class if r['scenario_all_claimed_parked_closable']]}")
    print(f"wave-2 top: {w2[0]['class']} unclaimed_proxy="
          f"{w2[0]['unclaimed_proxy_sum']} excl={w2[0]['unclaimed_exclusive']}")
    print(f"fourth-cost: unknown=100 unclaimed=98 exclusive_unclaimed=41 "
          f"bands={dict(sorted((b, n) for b, n in mb.items()))}")


if __name__ == "__main__":
    main()
