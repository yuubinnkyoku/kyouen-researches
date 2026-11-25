#!/usr/bin/env python3
"""Fail-closed audit of the k01/k03 third-implementation verdict re-verification.

Reads only the raw output files of this experiment dir's out/ plus the pinned
replica raw CSVs consumed at their published paths (fetched at pinned commit),
and recomputes every acceptance gate of the declaration note
research/log/2026-11-22-n11-sixthcost-k01-k03-thirdimpl-verdict-single-owner-note.md
Deterministic; byte-identical output across runs; exits 1 on any gate failure.
"""
import hashlib, json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "out"
RAWS = ROOT.parent / "raws"

def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

gates = {}
def gate(name, ok, detail=""):
    gates[name] = {"pass": bool(ok), "detail": detail}
    return ok

# ---- C1a: verify_tbl ----
t = (OUT / "calib-verify-tbl.txt").read_text()
m1 = re.search(r"replica quads (\d+) mine quads (\d+)", t)
m2 = re.search(r"triples checked (\d+) mismatches (\d+)", t)
gate("C1a_quads_95670_eq", m1 is not None and m1.group(1) == "95670" and m1.group(2) == "95670",
     f"replica={m1.group(1) if m1 else '?'} mine={m1.group(2) if m1 else '?'}")
gate("C1a_triples_195044_0", m2 is not None and m2.group(1) == "195044" and m2.group(2) == "0",
     f"checked={m2.group(1) if m2 else '?'} mismatches={m2.group(2) if m2 else '?'}")

# ---- C1b: anchor w2 ----
def parse_third(path):
    for line in pathlib.Path(path).read_text().splitlines():
        if line.startswith("third,") or line.startswith("replay,"):
            return line
    return ""
def fields(line):
    # third,row,stones,legalIn,legalDerived,result,nodes,ttHits,wall,lo,hi,reason,...
    c = line.split(",")
    return c
anchor = parse_third(OUT / "calib-anchor-w2.txt")
ac = fields(anchor)
gate("C1b_anchor_w2_win", ac[5] == "1", f"result={ac[5]}")
gate("C1b_anchor_w2_expansions_eq_7583990", ac[6] == "7583990", f"expansions={ac[6]}")
gate("C1b_anchor_w2_clean_rc0", ac[11] == "clean" and "rc=0" in (OUT / "calib-anchor-w2.txt").read_text(), "")

# ---- replica expectations (published probe lane raws, pinned shas) ----
REPLICA = {
    "at15m-run1-k03.out.csv": ("10376293541461626880", "65792", "1", "9255414", "a1c51cdf3b4a7601b5afabf3c558127f3b762f1f3c87785c695a7ffe5d6b7151"),
    "at15m-run2-k03.out.csv": ("10376293541461626880", "65792", "1", "9255414", "b17652530797f7ecca37668ae22145ae538afc498c5795a58846c87902c5cd32"),
    "at15m-run3-verify-k03.out.csv": ("10376293541461626880", "65792", "1", "9255414", "27169f87a60b7600967e413433dc6fee12ca555b7a20f098ba61f09523e3b924"),
    "at2m-k03.out.csv": ("10376293541461626880", "65792", "0", "2000000", "ecd00db9ce475fda0adb57374c9c90624634387dd59eb51ccdca6b07713c3216"),
    "at15m-run1-k01.out.csv": ("1297036692683751424", "1114112", "2", "10369650", "8b923fffe30723a0ba5600ebbd3eb03bd5d30c2320d499746d1e0ef4d300447a"),
    "at15m-run2-k01.out.csv": ("1297036692683751424", "1114112", "2", "10369650", "9a51121df4a1e11264e74a0d403486f479842f2528a0fc9a28052822a76d485d"),
}
rep = {}
for fname, (lo, hi, result, nodes, sha) in REPLICA.items():
    p = RAWS / fname
    s = sha256(p)
    gate(f"repl_sha_{fname}", s == sha, f"{s}")
    line = parse_third(p)
    c = line.split(",")
    gate(f"repl_row_{fname}", c[0] == "replay" and c[6] == result and c[7] == nodes and c[9].strip('"') == lo and c[10] == hi,
         line.strip())
    if fname == "at2m-k03.out.csv":
        gate("repl_k03_2m_unknown_row", (result, nodes) == ("0", "2000000"), f"{result},{nodes}")
    else:
        rep.setdefault((lo, hi), []).append((result, nodes))

k03_rep = rep[("10376293541461626880", "65792")]
k01_rep = rep[("1297036692683751424", "1114112")]
gate("repl_k03_win_3runs_unanimous", k03_rep == [("1", "9255414")] * 3, str(k03_rep))
gate("repl_k01_loss_2runs_unanimous", k01_rep == [("2", "10369650")] * 2, str(k01_rep))

# ---- C2/C3 third-impl rows ----
runs = {}
for f in ["k03-cold-a.txt", "k03-cold-b.txt", "k03-cold-v-legal.txt", "k01-cold-a.txt", "k01-cold-b.txt"]:
    line = parse_third(OUT / f)
    c = fields(line)
    runs[f] = c
    gate(f"third_clean_{f}", c[11] == "clean", f"reason={c[11]}")
    gate(f"third_derivedlegal_{f}", c[4] == c[3], f"in={c[3]} derived={c[4]}")

k03 = [runs[f] for f in ["k03-cold-a.txt", "k03-cold-b.txt", "k03-cold-v-legal.txt"]]
tok = [(c[5], c[6], c[7]) for c in k03]
gate("C2_k03_win_verdict_level_vs_replica", all(c[5] == "1" for c in k03) and next(iter(k03_rep))[0] == "1",
     f"third={set(c[5] for c in k03)} replica={set(r[0] for r in k03_rep)}")
gate("C2_k03_determinism_3runs_identical", len(set(tok)) == 1 and tok[0] == ("1", "10896601", "5996958"),
     f"{tok}")
gate("C2_k03_is_or_stability", all(c for c in []), "")  # removed below
del gates["C2_k03_is_or_stability"]

k01 = [runs[f] for f in ["k01-cold-a.txt", "k01-cold-b.txt"]]
tok1 = [(c[5], c[6], c[7]) for c in k01]
gate("C3_k01_loss_verdict_level_vs_replica", all(c[5] == "2" for c in k01) and next(iter(k01_rep))[0] == "2",
     f"third={set(c[5] for c in k01)} replica={set(r[0] for r in k01_rep)}")
gate("C3_k01_determinism_2runs_identical", len(set(tok1)) == 1 and tok1[0] == ("2", "12033330", "6620470"),
     f"{tok1}")

# ---- C4 negative gates ----
ng1 = (OUT / "neg-gate-legal82.txt").read_text()
gate("C4_ng1_gate_fail", "GATE_FAIL" in ng1 and "legal count mismatch: derived=81 declared=82" in ng1 and "rc=1" in ng1, ng1.strip())
ng2 = (OUT / "neg-gate-stones6.txt").read_text()
gate("C4_ng2_gate_fail", "GATE_FAIL" in ng2 and "stone count mismatch: bits=5 declared=6" in ng2 and "rc=1" in ng2, ng2.strip())

# ---- pins of consumed scripts ----
INV = ROOT.parent / "inv"
gate("pin_third_impl_sha256", sha256(INV / "third_impl.js") == "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998", "")
gate("pin_verify_tbl_sha256", sha256(INV / "verify_tbl.js") == "c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251", "")
gate("pin_jsreplay_sha256", sha256(INV / "jsreplay.js") == "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df", "")

summary = {
    "schema": "n11-sixthcost-k01k03-thirdimpl-audit-v1",
    "all_pass": all(g["pass"] for g in gates.values()),
    "gates": gates,
    "row_results": {
        "k03": {"third_impl_verdict": int(k03[0][5]), "third_impl_expansions": int(k03[0][6]),
                 "third_impl_runs": len(k03), "replica_verdict": int(next(iter(k03_rep))[0]),
                 "replica_nodes_15m": int(next(iter(k03_rep))[1]),
                 "verdict_level_agreement": all(c[5] == next(iter(k03_rep))[0] for c in k03)},
        "k01": {"third_impl_verdict": int(k01[0][5]), "third_impl_expansions": int(k01[0][6]),
                 "third_impl_runs": len(k01), "replica_verdict": int(next(iter(k01_rep))[0]),
                 "replica_nodes_15m": int(next(iter(k01_rep))[1]),
                 "verdict_level_agreement": all(c[5] == next(iter(k01_rep))[0] for c in k01)},
    },
    "consumed": False,
    "claim": "verdict-level agreement only; no verdict consumed; 11x11 empty board / two-stone root {60,27} / third moves {100,108} remain UNKNOWN",
}
print(json.dumps(summary, indent=1, sort_keys=True))
sys.exit(0 if summary["all_pass"] else 1)
