#!/usr/bin/env python3
"""Fail-closed audit of the k05 third-implementation verdict addendum of
research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/
(declaration research/log/2026-11-26-n11-sixthcost-k05-thirdimpl-verdict-single-owner-note.md).

Reads only the k05 addendum raws in out/ plus the pinned replica raw copies in
out/k05-replica-raws/ (byte-identical to the sixth-cost probe lane originals
published at commit 704cb3ef; per-file pins enforced below), and recomputes
every acceptance gate of the addendum. Deterministic; byte-identical output
across runs; exits 1 on any gate failure.
"""
import hashlib, json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "out"
# replica raw copies: out/k05-replica-raws/ when this script sits at the experiment
# dir root (published layout), or a sibling k05-replica-raws/ (local kit layout).
_CAND = [ROOT / "out" / "k05-replica-raws", ROOT.parent / "k05-replica-raws"]
RAWS = next((c for c in _CAND if all((c / f).exists() for f in
             ["at2m-k05.out.csv", "at15m-run1-k05.out.csv", "at15m-run2-k05.out.csv",
              "at15m-run3-verify-k05.out.csv"])), _CAND[0])

def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

gates = {}
def gate(name, ok, detail=""):
    gates[name] = {"pass": bool(ok), "detail": detail}
    return ok

def parse_row(path):
    for line in pathlib.Path(path).read_text().splitlines():
        if line.startswith("third,") or line.startswith("replay,"):
            return line
    return ""

# ---- pinned replica raw copies (probe lane originals published at 704cb3ef) ----
# third/second,row,stones,legalIn,legalDerived,result,nodes/budget,ttHits/wall_s,wall,lo,hi,reason,...
# replay row layout: replay,id,stones,legal,is_or,budget,result,nodes,wall_s,key_lo,key_hi
REPLICA = {
    "at2m-k05.out.csv": ("0", "2000000", "6be638e623dcd3275cfb9cce04bebe447fbf3fa93dad33f8c30508b635f87297"),
    "at15m-run1-k05.out.csv": ("1", "13397611", "dde1e4f0eae6a0557f0a6da7fd54f43f8ab4749c0321c16eba8f4586ee743df8"),
    "at15m-run2-k05.out.csv": ("1", "13397611", "562e2c9d3cfd7596e63a4f4d101c40ea6ea7dd66abfe5339cc095c6a0e408a2c"),
    "at15m-run3-verify-k05.out.csv": ("1", "13397611", "1305562baff3d171ff24df0befd6dc519147b77dc3648f78580b7e039d6f9381"),
}
rep15 = []
for fname, (result, nodes, sha) in REPLICA.items():
    p = RAWS / fname
    s = sha256(p)
    gate(f"repl_sha_{fname}", s == sha, s)
    c = parse_row(p).split(",")
    ok = (c[0] == "replay" and c[2] == "5" and c[3] == "88" and c[4] == "0"
          and c[9] == "10376293541461757952" and c[10] == "65536"
          and c[6] == result and c[7] == nodes)
    gate(f"repl_row_{fname}", ok, " | ".join(c))
    if result == "1":
        rep15.append((c[6], c[7]))
gate("repl_k05_win_3runs_unanimous", rep15 == [("1", "13397611")] * 3, str(rep15))
gate("repl_k05_2m_unknown", parse_row(RAWS / "at2m-k05.out.csv").split(",")[6] == "0",
     parse_row(RAWS / "at2m-k05.out.csv"))

# ---- C2/C3 third-impl rows (cold, independent processes) ----
runs = {}
for f in ["k05-cold-a.txt", "k05-cold-b.txt", "k05-cold-v-legal.txt"]:
    c = parse_row(OUT / f).split(",")
    runs[f] = c
    gate(f"third_clean_{f}", c[11] == "clean", f"reason={c[11]}")
    gate(f"third_derivedlegal_{f}", c[3] == c[4] == "88", f"in={c[3]} derived={c[4]}")
    gate(f"third_key_{f}", c[9] == "10376293541461757952" and c[10] == "65536", " | ".join(c))
    gate(f"third_quads_{f}", "quads=95670" in (OUT / f).read_text(), "quads")
k05 = [runs[f] for f in ["k05-cold-a.txt", "k05-cold-b.txt", "k05-cold-v-legal.txt"]]
tok = [(c[5], c[6], c[7]) for c in k05]
gate("C2_k05_win_verdict_level_vs_replica",
     all(c[5] == "1" for c in k05) and rep15[0][0] == "1",
     f"third={set(c[5] for c in k05)} replica={set(r[0] for r in rep15)}")
gate("C2_k05_determinism_3runs_identical",
     len(set(tok)) == 1 and tok[0] == ("1", "15949585", "8391212"), f"{tok}")
gate("C2_k05_ttoverwrites_pinned",
     all("ttOverwrites=11755281" in (OUT / f).read_text() for f in runs), "ttOverwrites=11755281")
gate("C2_k05_expansions_differ_from_replica_nodes_allowed",
     int(tok[0][1]) != int(rep15[0][1]),
     f"third_expansions={tok[0][1]} replica_nodes={rep15[0][1]} (different implementations; verdict-level agreement is the gate)")

# ---- C4 negative gates (fail-closed input validation) ----
ng1 = (OUT / "neg-gate-k05-legal89.txt").read_text()
gate("C4_ng1_k05_legal89_gate_fail",
     "GATE_FAIL" in ng1 and "legal count mismatch: derived=88 declared=89" in ng1 and "rc=1" in ng1,
     ng1.strip())
ng2 = (OUT / "neg-gate-k05-stones6.txt").read_text()
gate("C4_ng2_k05_stones6_gate_fail",
     "GATE_FAIL" in ng2 and "stone count mismatch: bits=5 declared=6" in ng2 and "rc=1" in ng2,
     ng2.strip())

# ---- pins of consumed scripts (unchanged from the published k01/k03 experiment) ----
# candidates: published repo layout (this dir / probe-dir scripts) and the
# executable kit layout (sibling inv/ holding the at-commit pinned copies).
PROBE = ROOT.parent / "n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121"
PINS = {
    "third_impl.js": ([ROOT / "third_impl.js", ROOT.parent / "inv" / "third_impl.js"],
                     "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998"),
    "verify_tbl.js": ([ROOT / "verify_tbl.js", ROOT.parent / "inv" / "verify_tbl.js"],
                      "c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251"),
    "jsreplay.js":   ([PROBE / "scripts" / "jsreplay.js", ROOT.parent / "inv" / "jsreplay.js"],
                      "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"),
}
for _name, (_cands, _sha) in PINS.items():
    _p = next((c for c in _cands if c.exists()), None)
    gate(f"pin_{_name.replace('.', '_')}_sha256",
         _p is not None and sha256(_p) == _sha,
         str(_p) if _p is not None else "not found in any candidate location")

summary = {
    "schema": "n11-sixthcost-k05-thirdimpl-audit-v1",
    "all_pass": all(g["pass"] for g in gates.values()),
    "gates": gates,
    "row_results": {
        "k05": {
            "third_impl_verdict": int(k05[0][5]),
            "third_impl_expansions": int(k05[0][6]),
            "third_impl_tt_hits": int(k05[0][7]),
            "third_impl_runs": len(k05),
            "third_impl_determinism_3runs_identical": len(set(tok)) == 1,
            "replica_verdict": int(rep15[0][0]),
            "replica_nodes_15m": int(rep15[0][1]),
            "replica_2m_result_unknown": True,
            "verdict_level_agreement": all(c[5] == rep15[0][0] for c in k05),
        },
    },
    "consumed": False,
    "claim": "verdict-level agreement only; no verdict consumed; 11x11 empty board / two-stone root {60,27} / third moves {100,108} remain UNKNOWN",
}
print(json.dumps(summary, indent=1, sort_keys=True))
sys.exit(0 if summary["all_pass"] else 1)
