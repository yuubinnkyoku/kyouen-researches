#!/usr/bin/env python3
"""Fault-injection validation of the worker-memo merge conflict detector
(2026-11-17, n11 class2-lane long-term lane).

TEST ONLY (synthetic corruption of measurement artifacts; no certificate
publication, no verdict changes, the natural merged seed is not affected).

The published K0909 2-worker measurement and the 4-worker measurement
(measure_worker_split4_memo_merge_73k_20261117.py) both observed ZERO
natural internal and cross conflicts.  A detector that has never fired is
itself unproven: this script injects deterministic synthetic corruptions
into copies of the real 4-worker dump/distinct tables and verifies that
the merge machinery detects EXACTLY the injected contradictions, with
zero false positives, and documents which corruption classes are
structurally absorbed by the unbound-sentinel combine rules.

MEMORY DESIGN (streaming everywhere): the first in-memory implementation
of this test loaded all four distinct tables into Python lists and was
OOM-killed twice by the ~1 GiB cgroup limit (dmesg: oom-kill pid ...,
total-vm ~1.0 GiB) before producing any output.  This rewrite streams:
scenario key selection is one heapq.merge pass over the sorted distinct
tables (O(1) memory per key group), corrupted table copies are streaming
line copies with a 10-entry substitution map, the F1 internal test reuses
the orchestrator's external-sort distinct_pass, and the cross test reuses
the orchestrator's streaming merge_pass_nway.  Peak python RSS stays far
below the limit.

Scenarios (2 distinct keys each, selected deterministically in sorted key
order over the heap-merged distinct tables, all keys pairwise disjoint
across scenarios; the internal test and the cross test use SEPARATE
corrupted copies so every gate is exact):

  F1 internal win_and_lose (dump-level duplicate): a duplicate record of
     an existing W2 key (win=w<255, lose=255) is appended to a copy of
     W2's raw dump with win=255, lose=3 (at a mirrored probe slot); the
     full sort+distinct pipeline must report exactly this key as an
     internal win_and_lose conflict.
  F2 cross win_and_lose: a key shared by W1 and W2 whose W2 record has
     win<255 and lose=255; W2's distinct record is corrupted to lose=3;
     the 4-way merge must report exactly this key as cross win_and_lose.
  F3 cross win_and_lose (reverse direction): a key shared by W3 and W4
     whose W4 record has win==255 and lose<255; W4's distinct record is
     corrupted to win=2; cross win_and_lose at exactly this key.
  F4 single-record win_le_nowin (worker-internal inconsistency visible
     only at merge time): a W4-only key (incidence 1) with win=w<255,
     nowin=255 is corrupted to nowin=w; the merge group check must fire
     win_le_nowin at exactly this key.
  F5 negative-bound retention: keys shared by W1 and W3; W3's record is
     corrupted to nowin=4 (the selected W1 win bound is 7) resp.
     nolose=2 (the selected W1 lose bounds are 6 and 4).  Since 255 means
     "no bound", it must be the identity for max-bound combination, not
     an absorbing value.  The merged records must retain nowin=4 /
     nolose=2.  These selected values are strictly below the matching
     positive bounds, so they must not trigger a logical conflict.

Gates: F1 internal conflicts == exactly the 2 injected keys; cross
conflicts == exactly the F2+F3 keys (win_and_lose) and F4 keys
(win_le_nowin); the F5 keys retain the injected finite negative bound
without a false conflict; the corrupted merge keeps the clean structural
counts (occupied_after 4,985,986 / shared_total 1,592,504 / incidence
histogram), so the corruptions changed values only; all other keys remain
conflict-free (zero false positives, via exact conflict totals and
samples); the natural (uncorrupted) merge conflicts remain zero (gated
against the main measurement JSON).

Interpretation guard: test only, synthetic data. No new WIN/LOSS
verdicts, no manifest row opened or closed, certificate bytes unchanged.
WIN7-D10 proves a first-player win within depth 10 from the individual
7-stone roots only; REFUTED-D10 is not a LOSS proof. The 11x11 empty
board, both two-stone roots {49,60} and {59,60}, S2 {59,60} and classes
1/2/4 all remain UNKNOWN.

Usage: python3 fault_inject_worker_merge_conflicts_20261117.py <out.json>
       (run after measure_worker_split4_memo_merge_73k_20261117.py has
       produced the four worker dumps and distinct tables)
"""
import hashlib
import heapq
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) or "."


def load_main_module():
    spec = importlib.util.spec_from_file_location(
        "m4main",
        os.path.join(HERE, "measure_worker_split4_memo_merge_73k_20261117.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def tagged_stream(tag, idx):
    """Yield (key4, worker_index, (win, lose, nowin, nolose)) in file order
    (the distinct tables are sorted by key)."""
    path = os.path.join(WORK, tag + ".distinct.txt")
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            f = line.split()
            if len(f) != 8:
                continue
            yield (f[:4], idx, (int(f[4]), int(f[5]), int(f[6]), int(f[7])))


def keystr(key):
    return " ".join(key)


def select_scenario_keys():
    """One streaming pass over the heap-merged distinct tables; pick 2
    keys per scenario in sorted key order, scenarios in priority order,
    pairwise disjoint."""
    quotas = {"F1": 2, "F2": 2, "F3": 2, "F4": 2, "F5a": 2, "F5b": 2}
    sel = {k: [] for k in quotas}
    streams = [tagged_stream(t, i) for i, t in enumerate(TAGS)]
    merged = heapq.merge(*streams, key=lambda x: x[0])
    group_key = None
    recs = {}
    groups = 0

    def flush_group(key, recs):
        has = lambda i: i in recs
        r = recs
        cands = []
        if has(1) and r[1][0] < 255 and r[1][1] == 255:
            cands.append("F1")
        if has(0) and has(1) and r[1][0] < 255 and r[1][1] == 255:
            cands.append("F2")
        if has(2) and has(3) and r[3][0] == 255 and r[3][1] < 255:
            cands.append("F3")
        if set(recs) == {3} and r[3][0] < 255 and r[3][2] == 255:
            cands.append("F4")
        # F5 absorption: verbatim-engine records never carry a real negative
        # bound (nowin/nolose are always 255, K0907) and a record with no
        # bound at all (win=lose=255 too) never occurs in the real tables
        # (the F5a pre-check found 0 such keys), so the negative bound is
        # injected into an otherwise-arbitrary W3 record; the other
        # workers' 255 sentinels do the absorbing (max rule).
        if (has(0) and has(2) and r[0][0] < 255 and r[0][2] == 255):
            cands.append("F5a")
        if (has(0) and has(2) and r[0][1] < 255 and r[0][3] == 255):
            cands.append("F5b")
        for sc in cands:
            if len(sel[sc]) < quotas[sc]:
                sel[sc].append({"key": keystr(key),
                                "worker_values": {t: list(recs[i])
                                                  for i, t in enumerate(TAGS)
                                                  if i in recs}})
                return  # one scenario per key keeps keys disjoint
    for key, idx, vals in merged:
        if key != group_key:
            if group_key is not None:
                flush_group(group_key, recs)
                groups += 1
            group_key = key
            recs = {}
        recs[idx] = vals
    if group_key is not None:
        flush_group(group_key, recs)
        groups += 1
    for sc in sel:
        if len(sel[sc]) != quotas[sc]:
            raise SystemExit("scenario %s selection failed (%d/%d)"
                             % (sc, len(sel[sc]), quotas[sc]))
    return sel, groups


def copy_with_substitutions(src, dst, subst):
    """subst: dict key-string -> dict field_index(4..7) -> new value."""
    n = 0
    with open(src, encoding="utf-8") as fi, \
            open(dst, "w", encoding="utf-8") as fo:
        for line in fi:
            f = line.split()
            k = " ".join(f[:4])
            s = subst.get(k)
            if s:
                for i, v in s.items():
                    f[i] = str(v)
                line = " ".join(f) + "\n"
                n += 1
            fo.write(line)
    return n


def find_dump_slots(dump_path, wanted):
    """Stream the raw dump; return {keystr: first slot} for wanted keys."""
    found = {}
    with open(dump_path, encoding="utf-8") as fh:
        fh.readline()  # KYOENWM1 header
        for line in fh:
            f = line.split()
            if len(f) != 9:
                continue
            k = " ".join(f[1:5])
            if k in wanted and k not in found:
                found[k] = int(f[0])
            if len(found) == len(wanted):
                break
    return found


def records_for_keys(path, wanted):
    """Stream a sorted table (distinct or merged seed, first line header
    if it starts with KYOENWM); return {keystr: (w,l,nw,nl)} for wanted."""
    out = {}
    with open(path, encoding="utf-8") as fh:
        first = fh.readline()
        if not first.startswith("KYOENWM"):
            fh.seek(0)
        for line in fh:
            f = line.split()
            if len(f) < 8:
                continue
            k = " ".join(f[:4])
            if k in wanted:
                out[k] = (int(f[4]), int(f[5]), int(f[6]), int(f[7]))
                if len(out) == len(wanted):
                    break
    return out


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "output", "fault-inject-worker-merge-conflicts-73k-20261117.json")
    m = load_main_module()
    for tag in TAGS:
        p = os.path.join(WORK, tag + ".distinct.txt")
        if not os.path.exists(p):
            raise SystemExit("missing %s; run the 4-worker measurement first" % p)
    main_json_path = os.path.join(
        HERE, "output", "worker-split4-memo-merge-73k-20261117.json")
    with open(main_json_path, encoding="utf-8") as fh:
        main_doc = json.load(fh)

    print("[select] streaming heap-merge over 4 distinct tables ...",
          flush=True)
    sel, groups = select_scenario_keys()
    total_sel = sum(len(v) for v in sel.values())
    print("[select] groups=%d selected=%d" % (groups, total_sel), flush=True)
    for sc in ("F1", "F2", "F3", "F4", "F5a", "F5b"):
        for e in sel[sc]:
            print("  %s key=%s vals=%s" % (sc, e["key"], e["worker_values"]),
                  flush=True)

    injections = {}
    for sc in sel:
        for e in sel[sc]:
            injections[e["key"]] = {"scenario": sc, "key": e["key"],
                                     "worker_values": e["worker_values"]}

    # ---- F1: internal duplicate appended to a copy of W2's raw dump ----
    f1_keys = [e["key"] for e in sel["F1"]]
    print("[F1] copying W2 raw dump + appending 2 injected records ...",
          flush=True)
    slots = find_dump_slots(os.path.join(WORK, "workerW2.dump.txt"),
                            set(f1_keys))
    if len(slots) != 2:
        raise SystemExit("F1 slot lookup failed: %r" % slots)
    dump_src = os.path.join(WORK, "workerW2.dump.txt")
    dump_dst = os.path.join(WORK, "faultW2.dump.txt")
    with open(dump_src, encoding="utf-8") as fi, \
            open(dump_dst, "w", encoding="utf-8") as fo:
        fo.write(fi.readline())  # header
        for line in fi:
            fo.write(line)
        for k in f1_keys:
            key = k.split()
            slot = (slots[k] + (1 << 22)) % (1 << 23)
            fo.write("%d %s 255 3 255 255\n" % (slot, k))
    for e in sel["F1"]:
        w = e["worker_values"]["workerW2"]
        e["orig"] = w
        e["injected"] = [255, 3, 255, 255]
        e["kind"] = "win_and_lose"
        e["mode"] = "internal_duplicate"
    print("[F1] external sort + distinct_pass (faultW2) ...", flush=True)
    f1_stats = m.distinct_pass("faultW2")
    print("[F1] conflicts=%s" % f1_stats["conflicts"], flush=True)

    # ---- corrupted copies of the distinct tables for the cross test ----
    print("[cross] writing corrupted distinct copies ...", flush=True)
    subst_w1 = {}  # W1 copy stays clean
    subst_w2 = {}
    for e in sel["F2"]:
        subst_w2[e["key"]] = {5: 3}  # lose -> 3
        w = e["worker_values"]["workerW2"]
        e["orig"] = w
        e["injected"] = [w[0], 3, w[2], w[3]]
        e["kind"] = "win_and_lose"
        e["mode"] = "cross_lose_injection"
    subst_w3 = {}
    for e in sel["F5a"]:
        subst_w3[e["key"]] = {6: 4}  # nowin -> 4
        w1 = e["worker_values"]["workerW1"]
        e["orig"] = e["worker_values"]["workerW3"]
        e["injected"] = [255, 255, 4, 255]
        e["kind"] = "absorbed_nowin"
        e["w1_record"] = w1
    for e in sel["F5b"]:
        subst_w3[e["key"]] = {7: 2}  # nolose -> 2
        w1 = e["worker_values"]["workerW1"]
        e["orig"] = e["worker_values"]["workerW3"]
        e["injected"] = [255, 255, 255, 2]
        e["kind"] = "absorbed_nolose"
        e["w1_record"] = w1
    subst_w4 = {}
    for e in sel["F3"]:
        subst_w4[e["key"]] = {4: 2}  # win -> 2
        w = e["worker_values"]["workerW4"]
        e["orig"] = w
        e["injected"] = [2, w[1], w[2], w[3]]
        e["kind"] = "win_and_lose"
        e["mode"] = "cross_win_injection"
    for e in sel["F4"]:
        w = e["worker_values"]["workerW4"]
        subst_w4[e["key"]] = {6: w[0]}  # nowin -> w
        e["orig"] = w
        e["injected"] = [w[0], w[1], w[0], w[3]]
        e["kind"] = "win_le_nowin"
        e["mode"] = "single_record_negative_bound"
    n_sub = {"faultW1": copy_with_substitutions(
                os.path.join(WORK, "workerW1.distinct.txt"),
                os.path.join(WORK, "faultW1.distinct.txt"), subst_w1),
             "faultW2c": copy_with_substitutions(
                os.path.join(WORK, "workerW2.distinct.txt"),
                os.path.join(WORK, "faultW2c.distinct.txt"), subst_w2),
             "faultW3": copy_with_substitutions(
                os.path.join(WORK, "workerW3.distinct.txt"),
                os.path.join(WORK, "faultW3.distinct.txt"), subst_w3),
             "faultW4": copy_with_substitutions(
                os.path.join(WORK, "workerW4.distinct.txt"),
                os.path.join(WORK, "faultW4.distinct.txt"), subst_w4)}
    print("[cross] substitutions applied: %s" % n_sub, flush=True)

    print("[cross] streaming 4-way merge over fault tables ...", flush=True)
    cross = m.merge_pass_nway(["faultW1", "faultW2c", "faultW3",
                               "faultW4"],
                              seed_name="faultmerged.kyoenwm2")
    print("[cross] conflicts=%s occupied_after=%d shared=%d"
          % (cross["cross_conflicts"], cross["occupied_after"],
             cross["shared_total"]), flush=True)

    # ---- F5 absorption gate: fault merged records == clean merged records
    print("[F5] extracting F5 keys from clean and fault merged seeds ...",
          flush=True)
    f5_keys = [e["key"] for e in sel["F5a"]] + [e["key"] for e in sel["F5b"]]
    clean_recs = records_for_keys(
        os.path.join(WORK, "merged_seed4.kyoenwm2"), set(f5_keys))
    fault_recs = records_for_keys(
        os.path.join(WORK, "faultmerged.kyoenwm2"), set(f5_keys))
    if len(clean_recs) != 4 or len(fault_recs) != 4:
        raise SystemExit("F5 record extraction failed: %d/%d"
                         % (len(clean_recs), len(fault_recs)))

    # ---- gates ----
    f1_expected = sorted(f1_keys)
    f1_conf_ok = (f1_stats["conflicts"] == {"win_and_lose": 2}
                  and sorted(f1_stats["conflict_samples"]
                             .get("win_and_lose", [])) == f1_expected)
    f2f3_expected = sorted([e["key"] for e in sel["F2"]] +
                           [e["key"] for e in sel["F3"]])
    f4_expected = sorted([e["key"] for e in sel["F4"]])
    samples = cross["conflict_samples"]
    cross_ok = (cross["cross_conflicts"].get("win_and_lose") == 4
                and cross["cross_conflicts"].get("win_le_nowin") == 2
                and "lose_le_nolose" not in cross["cross_conflicts"]
                and sorted(samples.get("win_and_lose", [])) == f2f3_expected
                and sorted(samples.get("win_le_nowin", [])) == f4_expected)
    f5_ok = True
    for e in sel["F5a"]:
        rec = fault_recs[e["key"]]
        expected = list(clean_recs[e["key"]])
        expected[2] = 4
        f5_ok = f5_ok and rec == tuple(expected) and 4 < e["w1_record"][0]
    for e in sel["F5b"]:
        rec = fault_recs[e["key"]]
        expected = list(clean_recs[e["key"]])
        expected[3] = 2
        f5_ok = f5_ok and rec == tuple(expected) and 2 < e["w1_record"][1]
    f5_not_fired = all(k not in samples.get("win_and_lose", [])
                       and k not in samples.get("win_le_nowin", [])
                       and k not in samples.get("lose_le_nolose", [])
                       for k in f5_keys)
    clean_merge = main_doc["merge4"]
    hist_f = {str(k): v for k, v in cross["incidence_histogram"].items()}
    structure_ok = (cross["occupied_after"] == clean_merge["occupied_after"]
                    and cross["shared_total"] == clean_merge["shared_total"]
                    and hist_f == clean_merge["incidence_histogram"])
    natural_ok = (clean_merge["cross_conflicts"] == {}
                  and main_doc["gates"]["internal_conflicts_zero"] is True
                  and main_doc["gates"]["cross_conflicts_zero"] is True)
    subst_ok = (n_sub["faultW1"] == 0 and n_sub["faultW2c"] == 2
                and n_sub["faultW3"] == 4 and n_sub["faultW4"] == 4)

    gates = {
        "f1_internal_exactly_injected": f1_conf_ok,
        "cross_exactly_injected": cross_ok,
        "f5_bounds_preserved_without_false_conflict": f5_ok,
        "f5_keys_not_flagged": f5_not_fired,
        "fault_merge_structure_equals_clean": structure_ok,
        "natural_merge_conflicts_zero": natural_ok,
        "substitution_counts_exact": subst_ok,
    }
    all_pass = all(gates.values())

    doc = {
        "schema": "n11-class2-lane-fault-inject-worker-merge-conflicts-73k-20261117-v2",
        "date": "2026-11-17",
        "lane": "n11 class2-lane long-term (cost73k)",
        "purpose": "fault-injection validation of the 4-worker memo merge conflict detector: injected contradictions detected, finite negative bounds retained across unbound sentinels, zero false positives",
        "design_note": ("streaming rewrite: the first in-memory implementation "
                        "(4 distinct tables in Python lists) was OOM-killed by "
                        "the ~1GiB cgroup limit twice before any output; this "
                        "version uses one heap-merge selection pass, streaming "
                        "table copies, and the orchestrator's external-sort "
                        "distinct_pass and streaming merge_pass_nway"),
        "inputs": {
            "measurement_json": "output/worker-split4-memo-merge-73k-20261117.json",
            "distinct_tables": [t + ".distinct.txt" for t in TAGS],
            "raw_dump_for_F1": "workerW2.dump.txt",
            "clean_merged_seed": "merged_seed4.kyoenwm2",
        },
        "selection_groups_scanned": groups,
        "scenarios": {
            "F1_internal_duplicate": sel["F1"],
            "F2_cross_lose_injection": sel["F2"],
            "F3_cross_win_injection": sel["F3"],
            "F4_single_record_negative_bound": sel["F4"],
            "F5a_absorbed_nowin": sel["F5a"],
            "F5b_absorbed_nolose": sel["F5b"],
        },
        "f1_result": {
            "conflicts": f1_stats["conflicts"],
            "conflict_samples": f1_stats["conflict_samples"],
            "records": f1_stats["records"],
            "distinct": f1_stats["distinct"],
            "dup_keys": f1_stats["dup_keys"],
            "max_copies": f1_stats["max_copies"],
        },
        "cross_result": {
            "cross_conflicts": cross["cross_conflicts"],
            "conflict_samples": cross["conflict_samples"],
            "occupied_after": cross["occupied_after"],
            "shared_total": cross["shared_total"],
            "incidence_histogram": cross["incidence_histogram"],
        },
        "f5_gate": {
            "clean_records": {k: list(clean_recs[k]) for k in f5_keys},
            "fault_records": {k: list(fault_recs[k]) for k in f5_keys},
            "equal": {k: clean_recs[k] == fault_recs[k] for k in f5_keys},
        },
        "gates": gates,
        "gates_all_pass": all_pass,
        "interpretation_guard": (
            "Test only, synthetic corruption of measurement artifacts. No new "
            "WIN/LOSS verdicts, no manifest row opened or closed, certificate "
            "bytes unchanged, the natural merged seed is not affected. "
            "WIN7-D10 proves a first-player win within depth 10 from the "
            "individual 7-stone roots only; REFUTED-D10 is not a LOSS proof. "
            "The 11x11 empty board, both two-stone roots {49,60} and {59,60}, "
            "S2 {59,60} and classes 1/2/4 all remain UNKNOWN."),
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    print("[gates] %s" % json.dumps(gates), flush=True)
    print("[done] all_pass=%s -> %s" % (all_pass, out_path), flush=True)
    return 0 if all_pass else 1


m = None
WORK = None
TAGS = ("workerW1", "workerW2", "workerW3", "workerW4")

if __name__ == "__main__":
    m = load_main_module()
    WORK = m.WORK
    sys.exit(main())
