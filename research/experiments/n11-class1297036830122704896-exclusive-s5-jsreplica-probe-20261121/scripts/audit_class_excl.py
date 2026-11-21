#!/usr/bin/env python3
"""Independent batch audit for the class-1297036830122704896:0 exclusive S5
probe (JS replica). Fails closed: any gate failure exits non-zero and writes
no OK audit. Batch adaptation of the reply27 probe-13 audit_probe.py gates,
re-derived entirely from the published raw rows (progress bookkeeping is
recomputed, not trusted). Dual layout via pub_paths."""
import csv, gzip, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pub_paths

P = pub_paths.resolve(__file__)
sys.path.insert(0, str(P["indep"].parent))
sys.path.insert(0, str(P["policy"].parent))
from independent import Board, mask_from_key  # noqa: E402
from s5_evidence_policy import is_canonical_safe_s5_key, quarantined_cache_keys  # noqa: E402

EXP = P["exp"]
RAW = EXP / "output" / "raw"
INP = EXP / "input"
GEOMETRY = P["geometry"]
BASE_CACHE = P["cache"]
QUARANTINE = P["quar"]
SUPPLY = P["supply"]
INDEP_SHA_EXPECT = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA_EXPECT = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
SEL = json.loads((EXP / "output" / "exclusive-selection.json").read_text(encoding="utf-8"))
MY_CLASS = (1297036830122704896, 0)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read_replay(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").split("\n"):
        if line.startswith("replay,"):
            f = line.split(",")
            rows.append(dict(id=int(f[1]), stones=int(f[2]), legal=int(f[3]),
                             is_or=int(f[4]), budget=int(f[5]), result=int(f[6]),
                             nodes=int(f[7]), key_lo=int(f[9]), key_hi=int(f[10])))
    return rows


def read_cache(p):
    data = Path(p).read_text(encoding="utf-8").split("\n")
    header, rows = data[0], [r for r in data[1:] if r]
    keys, entry = [], {}
    for r in rows:
        f = r.split(",")
        assert f[0] == "s5verdict" and int(f[3]) == 5 and int(f[4]) in (1, 2)
        k = (int(f[1]), int(f[2]))
        if k in entry and entry[k] != int(f[4]):
            raise ValueError(f"verdict conflict on {k}")
        entry[k] = int(f[4])
        keys.append(k)
    assert keys == sorted(keys), "cache not sorted"
    return header, entry, keys


gates = []
def gate(name, ok, detail=""):
    if not ok:
        print(f"GATE FAIL: {name} {detail}", file=sys.stderr)
        sys.exit(1)
    gates.append(name)


def main():
    out_path = EXP / "output" / "probe-audit.json"
    gate("independent_sha", sha(P["indep"]) == INDEP_SHA_EXPECT)
    gate("policy_sha", sha(P["policy"]) == POLICY_SHA_EXPECT)
    # ---- validation gate: replica vs every published two-target raw row ----
    expect = {
        "val-at2m-first": (98, 2_000_000, 0, 2_000_000, 1152921504606851072, 536870946),
        "val-at2m-second": (99, 2_000_000, 0, 2_000_000, 1188950301626860544, 536870912),
        "val-first-15m": (98, 15_000_000, 2, 3_651_923, 1152921504606851072, 536870946),
        "val-second-15m": (99, 15_000_000, 2, 5_040_200, 1188950301626860544, 536870912),
    }
    val_rows = {}
    for tag, e in expect.items():
        rep = read_replay(RAW / f"{tag}.out.csv")
        gate(f"validation_{tag}", len(rep) == 1 and
             (rep[0]["legal"], rep[0]["budget"], rep[0]["result"], rep[0]["nodes"],
              rep[0]["key_lo"], rep[0]["key_hi"]) == e)
        val_rows[tag] = rep[0]

    order_keys = [r["key"] for r in SEL["exclusive_probe_order"]]
    legal_by_key = {r["key"]: r["legal"] for r in SEL["exclusive_probe_order"]}
    supply = {}
    for row in csv.DictReader(SUPPLY.open(newline="")):
        lo, hi = row["key"].split(":")
        supply[(int(lo), int(hi))] = row

    per_key = {}
    done, parked = [], []
    win = None
    for k in order_keys:
        lo, hi = k.split(":")
        K = (int(lo), int(hi))
        r2 = read_replay(RAW / f"at2m-s5-{lo}-{hi}.out.csv")
        gate(f"{k}.at2m_row", len(r2) == 1 and (r2[0]["key_lo"], r2[0]["key_hi"]) == K
             and r2[0]["stones"] == 5 and r2[0]["is_or"] == 0 and r2[0]["budget"] == 2_000_000)
        gate(f"{k}.at2m_form", r2[0]["result"] in (0, 1, 2) and
             (r2[0]["result"] != 0 or r2[0]["nodes"] == 2_000_000))
        ip = INP / f"batch-s5-{lo}-{hi}.input.csv"
        line = [l for l in ip.read_text().split("\n") if l][0]
        f = line.split(",")
        gate(f"{k}.input_target", f[0] == "target" and int(f[2]) == 5 and
             (int(f[3]), int(f[4])) == K and int(f[5]) == legal_by_key[k])
        stages = {"at2m": {"result": r2[0]["result"], "nodes": r2[0]["nodes"], "budget": r2[0]["budget"]}}
        if r2[0]["result"] == 0:
            r15 = read_replay(RAW / f"at15m-s5-{lo}-{hi}.out.csv")
            r15b = read_replay(RAW / f"at15m-run2-s5-{lo}-{hi}.out.csv")
            gate(f"{k}.at15m_row", len(r15) == 1 and r15[0]["budget"] == 15_000_000
                 and (r15[0]["key_lo"], r15[0]["key_hi"]) == K)
            gate(f"{k}.at15m_run2_row", len(r15b) == 1 and r15b[0]["budget"] == 15_000_000
                 and (r15b[0]["key_lo"], r15b[0]["key_hi"]) == K)
            gate(f"{k}.determinism",
                 (r15[0]["result"], r15[0]["nodes"]) == (r15b[0]["result"], r15b[0]["nodes"]))
            gate(f"{k}.verdict_class", r15[0]["result"] in (0, 2), f"got {r15[0]['result']}")
            gate(f"{k}.nodes_within_budget", 0 < r15[0]["nodes"] <= 15_000_000)
            stages["at15m"] = {"result": r15[0]["result"], "nodes": r15[0]["nodes"], "budget": 15_000_000}
            stages["at15m_run2"] = {"result": r15b[0]["result"], "nodes": r15b[0]["nodes"], "budget": 15_000_000}
            verdict = {0: "UNKNOWN@15M", 2: "LOSS", 1: "WIN"}[r15[0]["result"]]
        else:
            r2b = read_replay(RAW / f"at2m-run2-s5-{lo}-{hi}.out.csv")
            gate(f"{k}.at2m_run2_row", len(r2b) == 1 and r2b[0]["budget"] == 2_000_000)
            gate(f"{k}.determinism2m",
                 (r2[0]["result"], r2[0]["nodes"]) == (r2b[0]["result"], r2b[0]["nodes"]))
            verdict = {1: "WIN@2M", 2: "LOSS@2M"}[r2[0]["result"]]
        lg = r2[0]["legal"]
        gate(f"{k}.legal_supply", int(supply[K]["legal"]) == lg == legal_by_key[k])
        board = Board(11)
        mask = mask_from_key(*K)
        gate(f"{k}.stone_count", len(board.points(mask)) == 5)
        gate(f"{k}.d4_canonical", board.canonical(mask) == mask)
        legal = board.legal(mask)
        gate(f"{k}.legal_count", len(board.points(legal)) == lg)
        gate(f"{k}.policy_canonical_safe", is_canonical_safe_s5_key(K))
        if verdict.startswith("LOSS"):
            done.append(k)
        elif verdict.startswith("WIN"):
            win = k
        else:
            parked.append(k)
        per_key[k] = {"stages": stages, "verdict": verdict, "legal": lg}
    gate("batch_complete", len(done) + len(parked) + (1 if win else 0) == 39)
    gate("win_none_or_witness", win is None or len(done) == 0,
         "a WIN halts the batch per stopping rule 1; earlier keys may exist")

    qkeys = quarantined_cache_keys()
    # verbatim row strings keyed by (lo,hi); nodes are never verdicts but the
    # base file must be byte-preserved (wave-2 union-merger norm)
    def read_cache_rows(p):
        data = Path(p).read_text(encoding="utf-8").split("\n")
        header = data[0]
        rows = {}
        for r in data[1:]:
            if not r:
                continue
            f = r.split(",")
            assert f[0] == "s5verdict" and int(f[3]) == 5 and int(f[4]) in (1, 2)
            k = (int(f[1]), int(f[2]))
            if k in rows and rows[k].split(",")[4] != f[4]:
                raise ValueError(f"verdict conflict on {k}")
            rows[k] = r
        return header, rows

    base_header, base_rowmap = read_cache_rows(BASE_CACHE)
    base_keys = sorted(base_rowmap)
    base_vals = {k: int(base_rowmap[k].split(",")[4]) for k in base_keys}
    gate("base_cache_rows", len(base_keys) == 5756)
    geo = json.loads(gzip.open(GEOMETRY, "rt", encoding="utf-8").read())
    gate("frozen_geometry_size", len(geo) == 3384)
    my_children = {tuple(z) for z in next(g for g in geo if tuple(g["key"]) == MY_CLASS)["children"]}
    for k in order_keys:
        lo, hi = k.split(":")
        K = (int(lo), int(hi))
        gate(f"{k}.quarantine_absent", K not in qkeys)
        gate(f"{k}.base_absent", K not in base_vals)
        gate(f"{k}.my_class_child", K in my_children)

    # ---- merged cache increment ----
    new_rows = []
    for k in done:
        lo, hi = k.split(":")
        stages = per_key[k]["stages"]
        nodes = stages.get("at15m", stages.get("at2m"))["nodes"]
        new_rows.append((int(lo), int(hi), 2, nodes))
    conflict = [(lo, hi) for lo, hi, v, _ in new_rows if (lo, hi) in base_vals and base_vals[(lo, hi)] != v]
    gate("no_conflict_with_base", not conflict, f"conflicts: {conflict}")
    gate("no_duplicate_new", len(set((lo, hi) for lo, hi, _, _ in new_rows)) == len(new_rows))
    merged_path = EXP / "output" / "merged-exact-s5-after-class-excl-1.cache"
    lines = dict(base_rowmap)
    dup_elided = []
    for lo, hi, v, nodes in new_rows:
        if (lo, hi) in lines:
            dup_elided.append((lo, hi))
            continue
        lines[(lo, hi)] = f"s5verdict,{lo},{hi},5,{v},{nodes}"
    out_lines = [base_header] + [lines[k] for k in sorted(lines)]
    merged_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    gate("dup_elision_ok", len(dup_elided) == 0 or all(base_vals[(lo, hi)] == 2 for lo, hi in dup_elided))
    gate("base_byte_preserved",
         all(lines[k] == base_rowmap[k] for k in base_keys),
         "base rows must appear verbatim (incl. original nodes fields)")
    hdr_n, new_rowmap = read_cache_rows(merged_path)
    new_vals = {k: int(new_rowmap[k].split(",")[4]) for k in new_rowmap}
    new_keys = sorted(new_rowmap)
    gate("merge_exactly_done",
         set(new_keys) - set(base_keys) == set((int(k.split(":")[0]), int(k.split(":")[1])) for k in done)
         and len(new_keys) == len(base_keys) + len(done))
    gate("parked_absent", all((int(k.split(":")[0]), int(k.split(":")[1])) not in new_vals for k in parked))
    gate("no_duplicate_keys", len(new_keys) == len(set(new_keys)))

    # ---- class status recomputation on the frozen geometry, before/after ----
    def classes_with(vals):
        out = {}
        for row in geo:
            ch = {tuple(z) for z in row["children"]}
            v = [vals.get(z, 0) for z in ch]
            st = "WIN" if 1 in v else ("LOSS" if all(x == 2 for x in v) else "UNKNOWN")
            out[tuple(row["key"])] = dict(status=st, win=v.count(1), loss=v.count(2),
                                          unknown=v.count(0), coverage=row["coverage"], total=len(ch))
        return out

    cb = classes_with(base_vals)
    cn = classes_with(new_vals)
    gate("my_class_before", cb[MY_CLASS]["status"] == "UNKNOWN"
         and cb[MY_CLASS]["unknown"] == 100 and cb[MY_CLASS]["loss"] == 7)
    gate("my_class_after", cn[MY_CLASS]["status"] == "UNKNOWN"
         and cn[MY_CLASS]["unknown"] == 100 - len(done)
         and cn[MY_CLASS]["loss"] == 7 + len(done))
    status_changes = []
    for k in cb:
        if cb[k]["status"] != cn[k]["status"]:
            status_changes.append({"key": list(k), "before": cb[k]["status"],
                                   "after": cn[k]["status"], "coverage": cb[k]["coverage"]})
    cand = [k for k in cb if {100, 108} & set(cb[k]["coverage"])]
    cand_changed = [k for k in cand if (cb[k]["status"], cb[k]["win"], cb[k]["loss"], cb[k]["unknown"]) !=
                    (cn[k]["status"], cn[k]["win"], cn[k]["loss"], cn[k]["unknown"])]
    cand_closures = [k for k in cand if cb[k]["status"] == "UNKNOWN" and cn[k]["status"] == "LOSS"]
    gate("no_candidate_closes", not cand_closures, f"{cand_closures}")
    secured_b = {v for k in cb if cb[k]["status"] == "LOSS" for v in cb[k]["coverage"]}
    secured_n = {v for k in cn if cn[k]["status"] == "LOSS" for v in cn[k]["coverage"]}
    gate("secured_unchanged", secured_b == secured_n)
    third = {v for k in cb for v in cb[k]["coverage"]}
    gate("remaining_third_moves_unchanged", third - secured_n == {100, 108})
    counts_b, counts_n = {}, {}
    for k in cb:
        counts_b[cb[k]["status"]] = counts_b.get(cb[k]["status"], 0) + 1
        counts_n[cn[k]["status"]] = counts_n.get(cn[k]["status"], 0) + 1
    gate("status_changes_only_recorded",
         (counts_b.get("WIN") == counts_n.get("WIN")) and
         (counts_n.get("LOSS", 0) - counts_b.get("LOSS", 0) == len(status_changes)))

    audit = {
        "schema": "n11-class-exclusive-s5-js-replica-probe-audit-v1",
        "all_gates_pass": True,
        "title": ("third-cost class 1297036830122704896:0 exclusive single-live-parent S5 probe "
                  f"(JS replica): {len(done)} LOSS / {len(parked)} UNKNOWN@15M / {1 if win else 0} WIN of "
                  "39 claimed keys"),
        "gates_passed_count": len(gates),
        "pins": {
            "pinned_cpp_kyouen_dfpn_root_sha256": "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e",
            "replica_jsreplay_sha256": sha(P["jsrelay"]),
            "independent_geometry_python_sha256": sha(P["indep"]),
            "geometry_sha256": sha(GEOMETRY),
            "base_merged_cache_sha256": sha(BASE_CACHE),
            "quarantine_sha256": sha(QUARANTINE),
            "supply_sha256": sha(SUPPLY),
            "policy_sha256": sha(P["policy"]),
        },
        "validation": {
            "published_raw_rows_reproduced": [
                {"tag": t, "row": {"stones": v["stones"], "legal": v["legal"], "is_or": v["is_or"],
                                   "budget": v["budget"], "result": v["result"], "nodes": v["nodes"]}}
                for t, v in val_rows.items()],
            "rule": "stones/legal/is_or/budget/result/nodes must match the published C++ raw rows; wall_s may differ",
        },
        "probe": {
            "class": f"{MY_CLASS[0]}:{MY_CLASS[1]}",
            "claimed_keys": 39,
            "resolved_loss": sorted(done),
            "parked_unknown_15m": sorted(parked),
            "win": win,
            "pinned_semantics": "exact_replay: 0 UNKNOWN (budget exhausted), 1 WIN, 2 LOSS (fixed first player)",
            "evidence_class": ("replica solver-trusted exact, node-exact against all four published C++ raw "
                               "rows; NOT terminal-only minimax"),
            "per_key": per_key,
            "determinism": ("every resolved stage executed twice with identical (result, nodes); parked keys "
                            "exhausted the 15M budget identically twice"),
        },
        "class_recomputation": {
            "before": cb[MY_CLASS], "after": cn[MY_CLASS],
            "candidate_classes_changed": [f"{k[0]}:{k[1]}" for k in cand_changed],
            "global_status_changes": status_changes,
            "status_counts_before": counts_b, "status_counts_after": counts_n,
        },
        "status_guard": ("evidence increment only; the 11x11 empty board, the two-stone root {60,27}, "
                         "and third moves 100/108 remain UNKNOWN; nodes and proxy values are never "
                         "verdicts; the class reaches 44 LOSS / 63 UNKNOWN of 107 children and is NOT closed"),
    }
    out_path.write_text(json.dumps(audit, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"ALL {len(gates)} GATES PASS")
    print(f"loss={len(done)} parked={parked} win={win}")
    print(f"class: {cb[MY_CLASS]['unknown']}->{cn[MY_CLASS]['unknown']} unknown")
    print(f"status_changes={[(c['key'], c['before'], c['after']) for c in status_changes]}")
    print("new merged cache sha256:", sha(merged_path))


if __name__ == "__main__":
    main()
