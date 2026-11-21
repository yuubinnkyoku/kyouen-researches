#!/usr/bin/env python3
"""True-vs-adaptive cost re-measurement for the n11 S5 chain (measurement only).

Re-derives, from published pinned bytes only, the current out-of-sample
relationship between observed resolution node counts ("true cost") and the
adaptive truncated-cost proxy (legal-decile historical mean, censored at 15M
in its source corpus), on the four fully published post-supply cohorts:

  cohort reply27      : 42 rows of the pinned reconciliation-findings.json
                        (27 resolved LOSS at 15M)
  cohort reply27_late : the 15 rows exhausted at the 2M row stage, all later
                        resolved LOSS inside the probe-13 base pin 60e0dc34
                        (true cost re-read from the base pin; strict disjoint
                        from every other cohort, machine-gated)
  cohort thirdcost    : 37 resolved LOSS rows (chain-cache bb4495e0 minus
                        probe-13 base 60e0dc34) + 2 parked UNKNOWN@15M
  cohort fourthcost   : 33 resolved LOSS + 8 parked UNKNOWN@15M of the pinned
                        fourth-cost pass-1 complete note (41 keys, authoritative
                        order pinned in fourth-cost-exclusive-keys.json)

and produces the allocation table for the 63 unknown children of the
third-cost class 1297036830122704896:0 (per-key legal/proxy/incidence/priors
+ ratio-quantile node estimates + cheapest-first order). Scheduling hints
only: no verdict, no probability calibration, no cache write.
Fail-closed: any gate failure exits non-zero and writes no output.
Deterministic: byte-identical on re-run.
"""
import csv, gzip, hashlib, json, re, statistics, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pub_paths

P = pub_paths.resolve(__file__)
OUT = P["out"]
MY_CLASS = (1297036830122704896, 0)
PARKED = [("1297036830122704896", "67108864", 91), ("10376294091217440768", "33554432", 94)]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


gates = []
def gate(name, ok, detail=""):
    if not ok:
        print(f"GATE FAIL: {name} {detail}", file=sys.stderr)
        sys.exit(1)
    gates.append(name)


def qstats(xs):
    if not xs:
        return {"n": 0}
    xs = sorted(xs)
    n = len(xs)
    def pick(f):
        i = min(n - 1, max(0, int(f * (n - 1) + 0.5)))
        return xs[i]
    return {"n": n, "min": xs[0], "q25": pick(0.25), "median": pick(0.5),
            "q75": pick(0.75), "max": xs[-1],
            "mean": round(sum(xs) / n, 4)}


def read_cache(p):
    rows = {}
    order = []
    data = Path(p).read_text(encoding="utf-8").split("\n")
    header = data[0]
    for r in data[1:]:
        if not r:
            continue
        f = r.split(",")
        assert f[0] == "s5verdict" and int(f[3]) == 5 and int(f[4]) in (1, 2)
        k = (int(f[1]), int(f[2]))
        assert k not in rows, f"duplicate {k}"
        rows[k] = (int(f[4]), int(f[5]))
        order.append(k)
    gate_order = order == sorted(order)
    return header, rows, gate_order


def parse_note_sections(text):
    """Split the fourth-cost pass-1 note into its three key-list bullets."""
    m = {}
    secs = {"at2m": r"- LOSS at 2M stage \(5\):(.*?)(?=- LOSS at 15M stage)",
            "at15m": r"- LOSS at 15M stage \(28[^:]*:?(.*?)(?=- UNKNOWN@15M parked)",
            "parked": r"- UNKNOWN@15M parked \(8[^:]*:?(.*?)\n\n"}
    for tag, pat in secs.items():
        mm = re.search(pat, text, re.S)
        gate(f"note.section.{tag}", mm is not None)
        m[tag] = mm.group(1) if mm else ""
    return m


def parse_keys(block):
    """Extract (key, paren-int) pairs from a bullet block."""
    out = []
    for k, val in re.findall(r"(\d{10,20}:\d{1,20})\s*\(([^)]*)\)", block):
        val = val.strip()
        v = None
        if val.endswith(" n"):
            v = int(val[:-2].replace(",", ""))
        elif val.startswith("legal "):
            v = ("legal", int(val[6:].replace(",", "")))
        else:
            v = int(val.replace(",", ""))
        out.append((k, v))
    return out


def main():
    # ---- pins ----
    gate("geometry_sha", sha(P["geometry"]) == pub_paths.GEOM_SHA)
    gate("profile_sha", sha(P["profile"]) == pub_paths.PROFILE_SHA)
    gate("supply_sha", sha(P["supply"]) == pub_paths.SUPPLY_SHA)
    gate("ledger_sha", sha(P["ledger"]) == pub_paths.LEDGER_SHA)
    gate("probe13_sha", sha(P["probe13"]) == pub_paths.PROBE13_SHA)
    gate("chain_sha", sha(P["chain"]) == pub_paths.CHAIN_SHA)
    gate("selection_sha", sha(P["sel"]) == pub_paths.SELECT_SHA)
    gate("recfind_sha", sha(P["recfind"]) == pub_paths.RECFIND_SHA)
    gate("fourthkeys_sha", sha(P["fourthkeys"]) == pub_paths.FOURTHKEYS_SHA)
    gate("fourthnote_sha", sha(P["fourthnote"]) == pub_paths.FOURTHNOTE_SHA)
    gate("indep_sha", sha(P["indep"]) == pub_paths.INDEP_SHA)
    gate("policy_sha", sha(P["policy"]) == pub_paths.POLICY_SHA)

    # ---- caches ----
    _, p13, sorted13 = read_cache(P["probe13"])
    _, ch, sortedch = read_cache(P["chain"])
    gate("probe13_rows", len(p13) == 5756)
    gate("chain_rows", len(ch) == 5793)
    gate("probe13_sorted", sorted13)
    gate("chain_sorted", sortedch)
    gate("chain_superset_byte_preserved", all(k in ch and ch[k] == v for k, v in p13.items()))
    added = {k: ch[k] for k in ch if k not in p13}
    gate("chain_added_37_loss", len(added) == 37 and all(v[0] == 2 for v in added.values()))

    # ---- supply / profile ----
    supply = {}
    for row in csv.DictReader(P["supply"].open(newline="")):
        lo, hi = row["key"].split(":")
        supply[(int(lo), int(hi))] = row
    gate("supply_rows", len(supply) == 4562)
    profile = json.loads(Path(P["profile"]).read_text(encoding="utf-8"))
    prof = profile["profile"]
    gate("profile_bins_n", sum(b["n"] for b in prof.values()) == profile["unique_s5_15m"] == 2629)

    def bin_mean(legal):
        d = str(legal // 10 * 10)
        gate(f"profile.bin.{d}", d in prof)
        return prof[d]["mean_truncated_nodes"]

    def proxy_of(key):
        gate(f"supply.has.{key}", key in supply)
        row = supply[key]
        legal = int(row["legal"])
        gm = bin_mean(legal)
        gate(f"proxy_bins_agree.{key}",
             int(row["truncated_cost_proxy_nodes"]) == int(gm + 0.5),
             f"{row['truncated_cost_proxy_nodes']} vs {gm}")
        return legal, float(row["truncated_cost_proxy_nodes"]), gm

    # ---- cohort reply27 (pinned reconciliation-findings rows) ----
    recf = json.loads(Path(P["recfind"]).read_text(encoding="utf-8"))
    rows27 = recf["proxy_calibration"]["rows"]
    gate("recf_rows_42", len(rows27) == 42)
    for r in rows27:
        gate(f"recf.ratio.{r['key']}", abs(r["nodes_over_proxy"] - r["nodes"] / r["proxy"]) < 1e-3)
    rep_resolved = [r for r in rows27 if r["result"] != 0]
    rep_parked = [r for r in rows27 if r["result"] == 0]
    gate("recf_resolved_27", len(rep_resolved) == 27 and all(r["result"] == 2 for r in rep_resolved))
    gate("recf_parked_15_at2m", len(rep_parked) == 15 and all(r["nodes"] == 2_000_000 for r in rep_parked))
    # All 15 rows censored at the 2M row stage were later resolved (LOSS) inside the
    # probe-13 base pin itself (the 13-probe campaign continued past row publication).
    # Their true cost is a fresh out-of-sample observation: cohort reply27_late.
    rep_late = []
    for r in sorted(rep_parked, key=lambda r: r["key"]):
        k = tuple(int(x) for x in r["key"].split(":"))
        gate(f"recf.late.in_probe13_base.{r['key']}", k in p13)
        gate(f"recf.late.verdict_loss.{r['key']}", p13[k][0] == 2)
        gate(f"recf.late.above_row_censor.{r['key']}", p13[k][1] > r["nodes"])
        gate(f"recf.late.not_in_chain_diff.{r['key']}", k not in added)
        rep_late.append({"key": r["key"], "legal": r["legal"], "nodes": p13[k][1],
                         "proxy": float(r["proxy"]), "ratio": round(p13[k][1] / float(r["proxy"]), 8),
                         "row_censored_at": r["stage_budget"],
                         "resolved_in": "probe-13 base pin 60e0dc34"})

    # ---- cohort thirdcost ----
    sel = json.loads(Path(P["sel"]).read_text(encoding="utf-8"))
    sel_rows = {r["key"]: r for r in sel["exclusive_probe_order"]}
    gate("sel_39", len(sel_rows) == 39)
    tc_resolved, tc_parked = [], []
    for k, v in sorted(added.items()):
        kstr = f"{k[0]}:{k[1]}"
        gate(f"tc.sel.has.{kstr}", kstr in sel_rows)
        legal, proxy_i, pmean = proxy_of(k)
        tc_resolved.append({"key": kstr, "legal": legal, "nodes": v[1],
                            "proxy": pmean, "ratio": round(v[1] / pmean, 8)})
    for lo, hi, legal in PARKED:
        k = (int(lo), int(hi))
        kstr = f"{lo}:{hi}"
        gate(f"tc.parked.not_in_chain.{kstr}", k not in ch and k not in p13)
        gate(f"tc.sel.parked.{kstr}", kstr in sel_rows)
        legal2, proxy_i, pmean = proxy_of(k)
        gate(f"tc.parked.legal.{kstr}", legal2 == legal)
        tc_parked.append({"key": kstr, "legal": legal, "censored_at": 15_000_000,
                          "proxy": pmean})

    # ---- cohort fourthcost ----
    fkeys = json.loads(Path(P["fourthkeys"]).read_text(encoding="utf-8"))
    gate("fourth.key_count", fkeys["key_count"] == 41 == len(fkeys["exclusive_unclaimed_probe_order"]))
    fourth_order = [r["key"] for r in fkeys["exclusive_unclaimed_probe_order"]]
    note = Path(P["fourthnote"]).read_text(encoding="utf-8")
    secs = parse_note_sections(note)
    fc_resolved, fc_parked = [], []
    for tag, rows_like in (("at2m", parse_keys(secs["at2m"])), ("at15m", parse_keys(secs["at15m"]))):
        gate(f"fourth.parse.{tag}", len(rows_like) == (5 if tag == "at2m" else 28))
        for kstr, nodes in rows_like:
            gate(f"fourth.parse.int.{tag}.{kstr}", isinstance(nodes, int))
            legal, proxy_i, pmean = proxy_of(tuple(int(x) for x in kstr.split(":")))
            fc_resolved.append({"key": kstr, "legal": legal, "nodes": nodes,
                                "proxy": pmean, "ratio": round(nodes / pmean, 8),
                                "stage_budget": 2_000_000 if tag == "at2m" else 15_000_000})
    pk = parse_keys(secs["parked"])
    gate("fourth.parse.parked", len(pk) == 8)
    for kstr, lv in pk:
        if isinstance(lv, int):
            # line-wrapped form: legal count without the "legal " prefix
            lv = ("legal", lv)
        gate(f"fourth.parse.legal.{kstr}", isinstance(lv, tuple) and lv[0] == "legal")
        legal, proxy_i, pmean = proxy_of(tuple(int(x) for x in kstr.split(":")))
        gate(f"fourth.parked.legal_agree.{kstr}", legal == lv[1])
        fc_parked.append({"key": kstr, "legal": legal, "censored_at": 15_000_000, "proxy": pmean})
    gate("fourth.cover_all_41",
         set(k["key"] for k in fc_resolved + fc_parked) == set(fourth_order))
    # notes' headline sanity: 0 WIN anywhere
    gate("fourth.zero_win_claim", "WIN: 0" in note)
    gate("thirdcost.zero_win_recompute", all(v[0] == 2 for v in added.values()))

    # ---- disjointness between cohorts (fresh machine re-verification) ----
    ks27 = set(r["key"] for r in rows27)
    ks_tc = set(k["key"] for k in tc_resolved + tc_parked)
    ks_fc = set(k["key"] for k in fc_resolved + fc_parked)
    gate("disjoint_reply27_thirdcost", not (ks27 & ks_tc))
    gate("disjoint_reply27_fourthcost", not (ks27 & ks_fc))
    gate("disjoint_thirdcost_fourthcost", not (ks_tc & ks_fc))

    # ---- combined out-of-sample ratio stats ----
    all_res = []
    for r in rep_resolved:
        all_res.append({"cohort": "reply27", "key": r["key"], "legal": r["legal"],
                        "nodes": r["nodes"], "proxy": r["proxy"],
                        "ratio": round(r["nodes"] / r["proxy"], 8),
                        "stage_budget": r["stage_budget"]})
    # tc rows come from the chain diff without an explicit stage field; the stage
    # is inferred from the node count relative to the 2M stage budget.
    for r in tc_resolved:
        stage = 2_000_000 if r["nodes"] <= 2_000_000 else 15_000_000
        all_res.append({"cohort": "thirdcost", "key": r["key"], "legal": r["legal"],
                        "nodes": r["nodes"], "proxy": r["proxy"], "ratio": r["ratio"],
                        "stage_budget": stage})
    for r in rep_late:
        all_res.append({"cohort": "reply27_late", "key": r["key"], "legal": r["legal"],
                        "nodes": r["nodes"], "proxy": r["proxy"],
                        "ratio": r["ratio"], "stage_budget": 15_000_000,
                        "row_censored_at": r["row_censored_at"]})
    for r in fc_resolved:
        all_res.append({"cohort": "fourthcost", **r})
    gate("all_resolved_112", len(all_res) == 112)
    gate("ratios_sane", all(0.05 <= r["ratio"] <= 100 for r in all_res))

    per_cohort = {}
    for c in ("reply27", "reply27_late", "thirdcost", "fourthcost"):
        per_cohort[c] = qstats([r["ratio"] for r in all_res if r["cohort"] == c])
    per_bin = {}
    for r in all_res:
        d = str(r["legal"] // 10 * 10)
        per_bin.setdefault(d, []).append(r["ratio"])
    per_bin_stats = {d: qstats(v) for d, v in sorted(per_bin.items(), key=lambda kv: int(kv[0]))}
    combined = qstats([r["ratio"] for r in all_res])

    censoring = {
        "reply27": {"rows_total": 42, "resolved_in_rows": len(rep_resolved),
                    "censored_at_2m_row_stage": len(rep_parked),
                    "later_resolved_in_probe13_base": len(rep_late),
                    "remaining_censored_after_pins": 0,
                    "note": ("every row censored at the 2M row stage was later resolved (LOSS) "
                             "inside the probe-13 base pin; that censoring is superseded and "
                             "recovered as the reply27_late cohort")},
        "thirdcost": {"rows_total": 39,
                      "resolved_2m": sum(1 for r in tc_resolved if r["nodes"] <= 2_000_000),
                      "resolved_15m": sum(1 for r in tc_resolved if r["nodes"] > 2_000_000),
                      "parked_15m": len(tc_parked), "parked_keys": tc_parked},
        "fourthcost": {"rows_total": 41,
                       "resolved_2m": sum(1 for r in fc_resolved if r["stage_budget"] == 2_000_000),
                       "resolved_15m": sum(1 for r in fc_resolved if r["stage_budget"] == 15_000_000),
                       "parked_15m": len(fc_parked), "parked_keys": fc_parked},
    }
    gate("thirdcost_rows_39", censoring["thirdcost"]["resolved_2m"]
         + censoring["thirdcost"]["resolved_15m"] + censoring["thirdcost"]["parked_15m"] == 39)
    gate("fourthcost_rows_41", censoring["fourthcost"]["resolved_2m"]
         + censoring["fourthcost"]["resolved_15m"] + censoring["fourthcost"]["parked_15m"] == 41)
    gate("thirdcost_parks_2", censoring["thirdcost"]["parked_15m"] == 2)
    gate("fourthcost_parks_8", censoring["fourthcost"]["parked_15m"] == 8)
    gate("reply27_censoring_superseded",
         censoring["reply27"]["later_resolved_in_probe13_base"] == 15
         and censoring["reply27"]["remaining_censored_after_pins"] == 0)

    # ---- class-focus: the 63 unknown children of MY_CLASS ----
    geo = json.loads(gzip.open(P["geometry"], "rt", encoding="utf-8").read())
    gate("frozen_geometry_size", len(geo) == 3384)
    myrow = next(g for g in geo if tuple(g["key"]) == MY_CLASS)
    children = {tuple(z) for z in myrow["children"]}
    gate("my_children_107", len(children) == 107)
    resolved_children = {k: v for k, v in ch.items() if k in children}
    gate("my_loss_44", sum(1 for v in resolved_children.values() if v[0] == 2) == 44)
    gate("my_win_0", sum(1 for v in resolved_children.values() if v[0] == 1) == 0)
    unknown = sorted(children - set(resolved_children))
    gate("my_unknown_63", len(unknown) == 63)
    single, shared = [], []
    for k in unknown:
        kstr = f"{k[0]}:{k[1]}"
        legal, proxy_i, pmean = proxy_of(k)
        srow = supply[k]
        ent = {"key": kstr, "legal": legal, "proxy": pmean,
               "live_parents": int(srow["live_parents"]),
               "parent_unknown_min": int(srow["parent_unknown_min"]),
               "parent_unknown_inverse_sum": float(srow["parent_unknown_inverse_sum"]),
               "if_loss_progress": int(srow["if_loss_progress"]),
               "if_win_classes_eliminated": int(srow["if_win_classes_eliminated"]),
               "historical_observations": int(srow["historical_observations"]),
               "historical_nodes": int(srow["historical_nodes"]),
               "bin_sample_size": int(srow["bin_sample_size"]),
               "bin_win_count": int(srow["bin_win_count"]),
               "bin_loss_count": int(srow["bin_loss_count"]),
               "bin_unknown_count": int(srow["bin_unknown_count"]),
               "est_nodes_ratio_q50": int(pmean * combined["median"]),
               "est_nodes_ratio_q75": int(pmean * combined["q75"]),
               "est_nodes_ratio_max": int(pmean * combined["max"])}
        (single if ent["live_parents"] == 1 else shared).append(ent)
    gate("unknown_single_2", len(single) == 2 and {e["key"] for e in single} == {f"{a}:{b}" for a, b, _ in PARKED})
    gate("unknown_shared_61", len(shared) == 61)
    for e in single:
        e["claimed_by"] = ("parked-pair L50M ladder lane (single-owner declaration b1a38144)")
    allocation = sorted(shared + single, key=lambda e: (e["proxy"], e["key"]))
    for i, e in enumerate(allocation, 1):
        e["rank_cheapest_first"] = i
    shared_sum_proxy = sum(e["proxy"] for e in shared)
    shared_sum_q50 = sum(e["est_nodes_ratio_q50"] for e in shared)
    shared_sum_q75 = sum(e["est_nodes_ratio_q75"] for e in shared)

    # ---- output ----
    OUT.mkdir(parents=True, exist_ok=True)
    measurement = {
        "schema": "n11-s5-true-vs-adaptive-remeasurement-v2",
        "all_gates_pass": True,
        "title": ("true-vs-adaptive cost re-measurement: 112 out-of-sample resolved rows "
                  "(reply27 27 / reply27_late 15 / thirdcost 37 / fourthcost 33) + 10 parked keys; "
                  "allocation table for the 63 unknown children of class 1297036830122704896:0"),
        "gates_passed_count": len(gates),
        "pins": {"geometry_sha256": sha(P["geometry"]),
                 "profile_sha256": sha(P["profile"]),
                 "supply_sha256": sha(P["supply"]),
                 "ledger_sha256": sha(P["ledger"]),
                 "probe13_cache_sha256": sha(P["probe13"]),
                 "chain_cache_sha256": sha(P["chain"]),
                 "selection_sha256": sha(P["sel"]),
                 "reconciliation_findings_sha256": sha(P["recfind"]),
                 "fourthcost_keys_sha256": sha(P["fourthkeys"]),
                 "fourthcost_note_sha256": sha(P["fourthnote"]),
                 "independent_sha256": sha(P["indep"]),
                 "policy_sha256": sha(P["policy"])},
        "proxy_definition": ("adaptive proxy = legal-decile mean truncated nodes of the frozen "
                             "historical-cost-profile corpus (2,629 unique S5 keys censored at "
                             "15M; selection bias documented upstream in the profile caveat)"),
        "cohorts": {
            "reply27": {"source": "pinned reconciliation-findings.json (frontier census lane)",
                        "resolved": rep_resolved,
                        "censored_at_2m_row_stage": rep_parked,
                        "superseded_note": ("these 15 rows were censored at the 2M row stage; "
                                            "all 15 keys were later resolved inside the probe-13 "
                                            "base pin and are recovered in the reply27_late cohort "
                                            "with their true resolution cost")},
            "reply27_late": {"source": ("the 15 censored rows; true cost re-read from the probe-13 "
                                        "base pin 60e0dc34, verdicts LOSS"),
                             "resolved": rep_late},
            "thirdcost": {"source": "chain cache bb4495e0 minus probe-13 base (37 rows) + 2 parked publication",
                          "resolved": tc_resolved, "parked": tc_parked},
            "fourthcost": {"source": "pinned fourth-cost pass-1 complete note (compiled raws)",
                           "resolved": fc_resolved, "parked": fc_parked},
        },
        "combined_ratio_stats_resolved_only": combined,
        "per_cohort_ratio_stats": per_cohort,
        "per_legal_decile_ratio_stats": per_bin_stats,
        "censoring_table": censoring,
        "previous_reference": {"reply27_calibration": "min 0.698 / mean 1.347 / max 2.490 (27 rows)",
                               "reply27_censored_15_followup": ("all 15 keys censored at the 2M row stage "
                                                               "resolved later in the probe-13 base (LOSS, "
                                                               "3,651,923-12,626,043 nodes), confirming the "
                                                               "row-era censoring direction"),
                               "this_measurement_supersedes": ("adds 85 resolved rows over the 27-row "
                                                               "calibration, recovers the 15 censored rows "
                                                               "as true observations, and adds per-decile structure")},
        "class_focus": {
            "class": f"{MY_CLASS[0]}:{MY_CLASS[1]}",
            "children": 107, "loss": 44, "unknown": 63,
            "unknown_single_live_parent_keys": [e["key"] for e in single],
            "unknown_single_live_parent_claimed_by":
                "parked-pair L50M ladder lane (single-owner declaration b1a38144)",
            "unknown_shared": 61,
            "shared_proxy_sum": shared_sum_proxy,
            "shared_est_sum_ratio_q50": shared_sum_q50,
            "shared_est_sum_ratio_q75": shared_sum_q75,
            "allocation_ranked_proxy_asc": allocation,
        },
        "scheduling_guard": ("all outputs are scheduling estimates on resolved-only ratio "
                              "distributions (selection-biased toward cheap keys); historical bins are "
                              "censored at 15M; no calibrated resolution probability is claimed; "
                              "ranks and estimates are never verdicts and never authorize skipping any key"),
        "status_guard": ("measurement only: no solver run, no cache write, no verdict claim; the "
                         "standard 11x11 empty board, the two-stone root {60,27}, and third moves "
                         "100/108 remain UNKNOWN; nodes and proxies are not verdicts"),
    }
    out_path = OUT / "measurement.json"
    out_path.write_text(json.dumps(measurement, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"ALL {len(gates)} GATES PASS")
    print("combined ratio stats:", json.dumps(combined))
    print("per-cohort medians:", json.dumps({k: v["median"] for k, v in per_cohort.items()}))
    print("per-decile:", json.dumps({k: v["median"] for k, v in per_bin_stats.items()}))
    print("reply27_late nodes range:", min(r["nodes"] for r in rep_late), "-",
          max(r["nodes"] for r in rep_late), "ratios:",
          sorted(r["ratio"] for r in rep_late))
    print("class 63: single", len(single), "shared", len(shared),
          "proxy_sum(shared)", shared_sum_proxy)
    print("output sha256:", sha(out_path))


if __name__ == "__main__":
    main()
