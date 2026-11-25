# audit_cu.py -- fail-closed gate battery for Part CU: the published batch-29
# (closure class 2251) checkpoint-1/3 evidence (16 LOSS rows ab001..ab016, all
# UNCONSUMED honest labels, adoption candidates only) is (a) byte-pinned to the
# pre-declaration pins table, (b) internally consistent as published evidence
# (2-pass determinism, status reconciliation, batch-keys reconciliation,
# budget/verdict-shape), (c) reproduced on this host by a 2-pass fresh-cold
# pinned-replica using the byte-cloned published runbatch.sh + jsreplay.js
# (node-exact verdict and node counts), (d) corroborated by the pinned third
# implementation third_impl.js (16/16 LOSS verdict agreement, 2-run
# determinism pairs), (e) anchored by published third-impl anchors
# k02a (WIN 9106337/4991527) and l1a (LOSS 7660602/3951175) reproduced
# exactly, (f) negative-tested by published GATE_FAIL rows ng1/ng2, and
# (g) proven UNCONSUMED: none of the 16 keys occurs in the merged canonical
# cache 854800f3.. (6,301 rows). Every gate must PASS or the script exits
# rc=1 with the failing gate name; output/audit-summary.json is written on
# both paths. No verdict is consumed anywhere: the standard 11x11 empty
# board, the 19 central-reply roots, class 2251 and every batch-29 key stay
# UNKNOWN. Verdict adoption of these LOSS rows happens only in a separate
# declared adoption Part (pinned merger 90711961..); LOSS-row corroboration
# does NOT adopt them.
#
# Adapted from the published Part CR audit (audit_cr.py, sha256
# 2ab974c3..., itself from Part CM 3f9a29fa / CL / CC / BY / BX / BW / BV
# lineage). Deltas declared in the Part CU declaration note: pin table loaded
# from sources/pins-b29ckpt1.json (73 machine-generated entries, pinned in
# the declaration by its own sha256), the batch-29 checkpoint-1/3 wording, 16
# LOSS targets (0 WIN, 0 EXHAUSTED), replica outputs at output/raw/ (the
# published byte-cloned runbatch.sh convention) instead of output/replica/,
# published-evidence consistency gates G1a-G1e (row-audit delegation executed
# per the Part CI scaffold README), and the anchor/negative/unadopted-gate
# sources switched to the Part CU kit layout.
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = "n11-centralreply-class2251-b29ckpt1-audit-thirdimpl-20261124"
SCHEMA = "n11-centralreply-class2251-b29ckpt1-audit-v1"
ROWS_SCHEMA = "n11-centralreply-class2251-b29ckpt1-thirdimpl-input-v1"
PIN_MERGED_CANONICAL = "854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d"
PIN_PINS_TABLE = "59cd84093bac8a0e114913a6dedf38069ba27980a7fc20a59e606b9ddc1fb60f"
VALGATE_KEYS = [("at2m-s5-1152921504606851072-536870946", 2000000),
                ("at2m-s5-1188950301626860544-536870912", 2000000),
                ("first-15m-s5-1152921504606851072-536870946", 15000000),
                ("second-15m-s5-1188950301626860544-536870912", 15000000)]

gates = []
def gate(name, ok, detail=""):
    gates.append({"gate": name, "pass": bool(ok), "detail": str(detail)})
    if not ok:
        summary = {"schema": SCHEMA, "experiment": EXP, "all_pass": False, "gates": gates}
        with open(os.path.join(ROOT, "output", "audit-summary.json"), "w") as fh:
            json.dump(summary, fh, indent=1); fh.write("\n")
        print("GATE FAILED:", name, detail)
        sys.exit(1)
    print("PASS", name, detail)

def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

def parse_third_line(line):
    if not line.startswith("third,"):
        return None
    f = line.rstrip("\n").split(",")
    d = {"raw": line.rstrip("\n")}
    if f[5] == "GATE_FAIL" or (len(f) > 5 and f[5].startswith('"')):
        d["gate_fail"] = ",".join(f[5:]).strip('"')
        return d
    d["row"], d["legalIn"], d["legalDerived"] = f[1], int(f[3]), int(f[4])
    d["result"], d["expansion"], d["ttHits"], d["wall"] = int(f[5]), int(f[6]), int(f[7]), float(f[8])
    d["lo"], d["hi"] = int(f[9]), int(f[10])
    d["reason"] = f[11]
    for tail in f[12:]:
        if tail.startswith("quads="): d["quads"] = int(tail[6:])
        elif tail.startswith("ttOverwrites="): d["overwrites"] = int(tail[13:])
        elif tail.startswith("memoPower="): d["memoPower"] = int(tail[10:])
    return d

def read_run(kind, key, tag):
    p = os.path.join(ROOT, "output", kind, f"{key}.{tag}.out")
    if not os.path.isfile(p):
        return None
    with open(p) as fh:
        for line in fh:
            if line.startswith("third,"):
                return parse_third_line(line)
    return None

def parse_replay_out(path):
    if not os.path.isfile(path):
        return None, False, False
    row, done, quads = None, False, False
    with open(path) as fh:
        for line in fh:
            if line.startswith("replay,"):
                row = line.strip().split(",")
            if line.startswith("# replay_done"):
                done = True
            if line.startswith("# forbidden quadruples: 95670"):
                quads = True
    return row, done, quads

def main():
    rows = json.load(open(os.path.join(ROOT, "input", "rows.json")))

    # -- P0: pins table itself (sha pinned in the declaration note)
    pins_path = os.path.join(ROOT, "sources", "pins-b29ckpt1.json")
    gate("pin-pins-table", sha256(pins_path) == PIN_PINS_TABLE, sha256(pins_path))
    pins = json.load(open(pins_path))
    gate("pins-schema", pins.get("schema") == "n11-centralreply-class2251-b29ckpt1-pins-v1",
         pins.get("schema"))

    # -- P1: every pinned byte in the kit matches its pre-declaration sha256
    pin_miss = []
    for rel, want in sorted(pins["pinned"].items()):
        p = os.path.join(ROOT, rel)
        if not os.path.isfile(p) or sha256(p) != want:
            pin_miss.append(rel)
    gate("pin-all-73", not pin_miss and len(pins["pinned"]) == 73, pin_miss or f"{len(pins['pinned'])} entries")

    # -- G0: rows.json schema and structure (machine-regenerated agreement
    #        is re-checked below in G1e against sources)
    gate("rows-schema",
         rows["schema"] == ROWS_SCHEMA
         and rows.get("consumed_into_canonical_cache") is False
         and rows.get("unadopted_loss_rows") is True
         and rows.get("unadopted_win_rows") is True
         and rows.get("canonical_cache_sha256_unchanged") == PIN_MERGED_CANONICAL,
         rows.get("schema"))
    gate("rows-target-count", len(rows["targets"]) == 16,
         f"{len(rows['targets'])} (16 published ckpt-1/3 rows, all LOSS honest labels)")
    gate("rows-target-verdict-kind",
         sorted(t["expect_third"] for t in rows["targets"]) == [2] * 16
         and sorted(t["replica_result"] for t in rows["targets"]) == [2] * 16,
         "all 16 published rows are LOSS (result=2); 0 WIN / 0 EXHAUSTED")
    gate("rows-anchor-negative-counts",
         len(rows["anchors"]) == 2 and len(rows["negatives"]) == 2,
         f"{len(rows['anchors'])} anchors / {len(rows['negatives'])} negatives")

    # -- G1: published-evidence consistency (the delegated row-audit)
    # G1a: published 2-pass determinism and evidence shape
    for t in rows["targets"]:
        k = t["key_id"]
        f1, d1, q1 = parse_replay_out(os.path.join(ROOT, "sources", "raw", f"{k}.p1.out"))
        f2, d2, q2 = parse_replay_out(os.path.join(ROOT, "sources", "raw", f"{k}.p2.out"))
        gate(f"published-{k}-present-done", f1 is not None and f2 is not None and d1 and d2 and q1 and q2,
             f"p1={f1 is not None} p2={f2 is not None} done={d1 and d2}")
        if not (f1 and f2):
            continue
        gate(f"published-{k}-det-pair",
             all(f1[i] == f2[i] for i in (1, 2, 3, 4, 5, 6, 7, 9, 10)),
             f"p1={f1[5:8]} p2={f2[5:8]}")
        gate(f"published-{k}-key-scheme",
             f1[2] == "5" and f1[1] == "0" and f1[5] == "15000000" and int(f1[9]) == t["lo"]
             and int(f1[10]) == t["hi"] and int(f1[3]) == t["legal"],
             f"{f1[9]},{f1[10]},{f1[3]} vs {t['lo']},{t['hi']},{t['legal']}")
    # G1b: status.log reconciliation
    stat = open(os.path.join(ROOT, "sources", "status-ckpt13.log")).read().splitlines()
    gate("published-status-16-pass-lines",
         len(stat) == 16 and all(l.split()[2] == "PASS" for l in stat),
         f"{len(stat)} lines")
    st_bad = []
    for l in stat:
        m = l.split()
        key, budget, result, nodes = m[1], m[3].split(",")[0], m[3].split(",")[1], m[3].split(",")[2]
        f1, _, _ = parse_replay_out(os.path.join(ROOT, "sources", "raw", f"{key}.p1.out"))
        if (budget, result, nodes) != (f1[5], f1[6], f1[7]):
            st_bad.append(l)
    gate("published-status-reconciles-raw", not st_bad, st_bad or "16/16 (budget,result,nodes)")
    gate("published-status-no-halt-or-exhaustion",
         not any(("WIN-HALT" in l or "EXHAUSTED" in l or "MISMATCH" in l or "TRUNCATED" in l) for l in stat),
         "0 HALT/EXHAUSTED/MISMATCH/TRUNCATED lines")
    # G1c: batch-keys reconciliation
    bk = json.load(open(os.path.join(ROOT, "sources", "batch-keys-b29.json")))
    kmap = {k["key_id"]: k for k in bk["keys"]}
    kb_bad = []
    for t in rows["targets"]:
        t2 = kmap[t["key_id"]]
        if str(t["lo"]) != t2["lo"] or t["hi"] != 0 or t["legal"] != t2["legal"] or t["s5_index"] != t2["s5_index"]:
            kb_bad.append(t["key_id"])
    gate("published-batch-keys-reconcile", not kb_bad, kb_bad or "16/16")
    # G1d: published claim machine-check (commit a5a159d7 message: 16 LOSS / 0 WIN / 0 EXHAUSTED)
    all_res = set()
    for t in rows["targets"]:
        f1, _, _ = parse_replay_out(os.path.join(ROOT, "sources", "raw", f"{t['key_id']}.p1.out"))
        all_res.add(f1[6])
    gate("published-claim-16-loss",
         all_res == {"2"}, f"distinct results={sorted(all_res)}")
    # G1e: rows.json is a faithful machine derivation of sources (spot re-derivation)
    regen = {}
    for t in rows["targets"]:
        f1, _, _ = parse_replay_out(os.path.join(ROOT, "sources", "raw", f"{t['key_id']}.p1.out"))
        regen[t["key_id"]] = (int(f1[6]), int(f1[7]),
                              sha256(os.path.join(ROOT, "sources", "raw", f"{t['key_id']}.p1.out")),
                              sha256(os.path.join(ROOT, "sources", "raw", f"{t['key_id']}.p2.out")))
    e_bad = [t["key_id"] for t in rows["targets"]
             if (t["replica_result"], t["replica_nodes"],
                 t["published_raw_sha256_p1"], t["published_raw_sha256_p2"]) != regen[t["key_id"]]]
    gate("rows-regen-agrees-source", not e_bad, e_bad or "16/16 fields+sha re-derived")

    # -- G2: this-host pinned-replica (2-pass fresh-cold via byte-cloned
    #        published runbatch.sh): node-exact vs published rows
    rep_bad = []
    for t in rows["targets"]:
        k = t["key_id"]
        f1, d1, q1 = parse_replay_out(os.path.join(ROOT, "output", "raw", f"{k}.p1.out"))
        f2, d2, q2 = parse_replay_out(os.path.join(ROOT, "output", "raw", f"{k}.p2.out"))
        gate(f"replica-{k}-present", f1 is not None and f2 is not None, "p1/p2")
        if not (f1 and f2):
            continue
        gate(f"replica-{k}-done", d1 and d2, f"replay_done p1={d1} p2={d2}")
        gate(f"replica-{k}-quads", q1 and q2, f"quads-header p1={q1} p2={q2}")
        gate(f"replica-{k}-det-pair", all(f1[i] == f2[i] for i in (3, 4, 5, 6, 7, 9, 10)),
             f"p1={f1[5:8]} p2={f2[5:8]}")
        gate(f"replica-{k}-schema", f1[2] == "5" and f1[1] == "0" and f1[5] == "15000000",
             f"schema {f1[:6]}")
        gate(f"replica-{k}-key", int(f1[9]) == t["lo"] and int(f1[10]) == t["hi"] and int(f1[3]) == t["legal"],
             f"{f1[9]},{f1[10]},{f1[3]} vs {t['lo']},{t['hi']},{t['legal']}")
        gate(f"replica-{k}-node-exact-vs-published",
             int(f1[6]) == t["replica_result"] and int(f1[7]) == t["replica_nodes"],
             f"this-host result={f1[6]} nodes={f1[7]} vs published result={t['replica_result']} nodes={t['replica_nodes']}")
        if not (f1[6] == f2[6] and f1[7] == f2[7] and int(f1[6]) == t["replica_result"] and int(f1[7]) == t["replica_nodes"]):
            rep_bad.append(k)
    gate("replica-all-16-node-exact", not rep_bad, rep_bad or "16/16 (first independent-session reproduction of ckpt-1/3)")

    # -- G3: third-impl anchors reproduce the published deterministic counts
    for a in rows["anchors"]:
        ka = a["key_id"]
        ra, rb = read_run("anchors", ka, "a"), read_run("anchors", ka, "b")
        gate(f"anchor-{ka}-present", ra is not None and rb is not None, "a/b")
        if not (ra and rb):
            continue
        for r, tg in ((ra, "a"), (rb, "b")):
            gate(f"anchor-{ka}-{tg}-clean",
                 r["result"] == a["expect_third"] and r["reason"] == "clean" and r.get("quads") == 95670,
                 f"result={r['result']} reason={r['reason']} quads={r.get('quads')}")
            gate(f"anchor-{ka}-{tg}-expansions",
                 r["expansion"] == a["anchor_expansions"] and r["ttHits"] == a["anchor_ttHits"],
                 f"exp={r['expansion']} vs {a['anchor_expansions']}, ttH={r['ttHits']} vs {a['anchor_ttHits']}")
            gate(f"anchor-{ka}-{tg}-key", r["lo"] == a["lo"] and r["hi"] == a["hi"], f"{r['lo']}:{r['hi']}")
        gate(f"anchor-{ka}-det-pair",
             ra["expansion"] == rb["expansion"] and ra["ttHits"] == rb["ttHits"] and ra["result"] == rb["result"],
             f"a={ra['expansion']}/{ra['ttHits']} b={rb['expansion']}/{rb['ttHits']}")

    # -- G4: negatives fail closed with the published gate-fail text
    for n in rows["negatives"]:
        r = read_run("negative", n["key_id"], "a")
        gate(f"neg-{n['key_id']}-failclosed",
             r is not None and "gate_fail" in r and r["gate_fail"] == n["expect_gate_fail_text"],
             str(r))

    # -- G5: targets: 2-run determinism + three-implementation verdict agreement
    verdicts = []
    inconclusive = []
    exp_total = 0
    v_bad = []
    for t in rows["targets"]:
        k = t["key_id"]
        ra, rb = read_run("targets", k, "a"), read_run("targets", k, "b")
        gate(f"third-target-{k}-present", ra is not None and rb is not None, "a/b")
        if not (ra and rb):
            continue
        for r, tg in ((ra, "a"), (rb, "b")):
            gate(f"third-target-{k}-{tg}-key", r["lo"] == t["lo"] and r["hi"] == t["hi"], f"{r['lo']}:{r['hi']}")
            gate(f"third-target-{k}-{tg}-legal-derived", r["legalDerived"] == t["legal"],
                 f"{r['legalDerived']} vs {t['legal']}")
            gate(f"third-target-{k}-{tg}-quads", r.get("quads") == 95670, r.get("quads"))
        gate(f"third-target-{k}-det-pair",
             ra["result"] == rb["result"] and ra["expansion"] == rb["expansion"]
             and ra["ttHits"] == rb["ttHits"] and ra["reason"] == rb["reason"],
             f"a=({ra['result']},{ra['expansion']},{ra['reason']}) b=({rb['result']},{rb['expansion']},{rb['reason']})")
        if ra["reason"] == "clean" and ra["result"] == t["expect_third"]:
            verdicts.append({"key_id": k, "replica_result": t["replica_result"],
                              "replica_nodes": t["replica_nodes"],
                              "third_result": ra["result"], "third_expansion": ra["expansion"],
                              "third_ttHits": ra["ttHits"], "agree": True})
            exp_total += ra["expansion"]
            gate(f"third-target-{k}-verdict-agree", True, f"third={ra['result']} replica={t['replica_result']}")
        elif ra["reason"].startswith("runlimit"):
            inconclusive.append({"key_id": k, "reason": ra["reason"]})
            gate(f"third-target-{k}-verdict-agree", False, f"WALL-INCONCLUSIVE {ra['reason']} (not a verdict)")
        else:
            verdicts.append({"key_id": k, "replica_result": t["replica_result"],
                              "replica_nodes": t["replica_nodes"],
                              "third_result": ra["result"], "third_expansion": ra["expansion"],
                              "third_ttHits": ra["ttHits"], "agree": ra["result"] == t["replica_result"]})
            gate(f"third-target-{k}-verdict-agree",
                 ra["result"] == t["replica_result"] and ra["reason"] == "clean",
                 f"DIVERGENCE third=({ra['result']},{ra['reason']}) replica={t['replica_result']}")
        if not ("gate_fail" in ra or ra.get("result") != t["replica_result"] or "gate_fail" in rb):
            pass
        else:
            v_bad.append(k)
    gate("third-target-all-16-agree",
         not v_bad and len(verdicts) == 16 and all(v["agree"] for v in verdicts) and not inconclusive,
         f"16/16 three-implementation LOSS agreements (published df-pn + this-host replica + third impl)")

    # -- G6: unadopted-row guarantee: none of the 16 keys occurs in the merged
    #        canonical cache (verdict not consumed anywhere)
    merged_path = os.path.join(ROOT, "sources", "canonical-cache-co-merged-b28loss7.cache")
    gate("unadopted-pin-merged-cache", sha256(merged_path) == PIN_MERGED_CANONICAL, sha256(merged_path))
    s5rows = [l for l in open(merged_path).read().splitlines() if l.startswith("s5verdict,")]
    gate("unadopted-merged-cache-rowcount", len(s5rows) == 6301, f"{len(s5rows)} s5verdict rows")
    hits = []
    for t in rows["targets"]:
        row_would_be = f"s5verdict,{t['lo']},0,5,{t['replica_result']},{t['replica_nodes']}"
        keyprefix = f"s5verdict,{t['lo']},"
        if any(l == row_would_be for l in s5rows) or any(l.startswith(keyprefix) for l in s5rows):
            hits.append(t["key_id"])
    gate("unadopted-merged-cache-all-16-absent", not hits,
         f"{len(hits)} key-collision rows (expect 0: ckpt-1/3 rows never adopted)")

    # -- G7: val-gate this-host 4/4 node-exact vs the published baselines
    for vgkey, vgbudget in VALGATE_KEYS:
        base_path = os.path.join(ROOT, "val-gate", f"{vgkey}.published-baseline.out")
        host_path = os.path.join(ROOT, "val-gate", f"{vgkey}.cu-host.out")
        b, bd, _ = parse_replay_out(base_path)
        h, hd, hq = parse_replay_out(host_path)
        gate(f"valgate-{vgkey}-present", b is not None and h is not None and bd and hd and hq,
             f"baseline={b is not None} host={h is not None}")
        if not (b and h):
            continue
        gate(f"valgate-{vgkey}-budget", int(h[5]) == vgbudget, f"budget={h[5]} vs {vgbudget}")
        ok = all(b[i] == h[i] for i in (1, 2, 3, 4, 5, 6, 7, 9, 10))
        gate(f"valgate-{vgkey}-node-exact", ok, f"host={h[5:8]} baseline={b[5:8]}")

    n_loss = sum(1 for v in verdicts if v["replica_result"] == 2)
    n_agree = sum(1 for v in verdicts if v["agree"])
    summary = {"schema": SCHEMA,
               "experiment": EXP,
               "all_pass": all(g["pass"] for g in gates),
               "gate_count": len(gates),
               "targets_pass_one_total_third_expansions": exp_total,
               "verdict_agreements": verdicts,
               "wall_inconclusive": inconclusive,
               "gates": gates}
    with open(os.path.join(ROOT, "output", "audit-summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1); fh.write("\n")
    print(f"ALL {len(gates)} GATES PASS; verdict agreements {n_agree}/{len(verdicts)} "
          f"(LOSS={n_loss}); inconclusive={len(inconclusive)}; "
          f"total third-impl expansions pass-one={exp_total}")

if __name__ == "__main__":
    main()
