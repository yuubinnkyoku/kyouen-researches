#!/usr/bin/env python3
"""Fail-closed audit of the k04 third-implementation verdict addendum of
research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/
(declaration research/log/2026-11-22-n11-sixthcost-k04-thirdimpl-verdict-single-owner-note.md).

Reads only the k04 addendum raws in out/ plus the pinned replica raw copies in
out/k04-replica-raws/ (byte-identical to the six-cost probe lane originals
published at commit cb7ffe05; per-file pins enforced below), and recomputes
every acceptance gate of the addendum. Deterministic; byte-identical output
across runs; exits 1 on any gate failure.
"""
import hashlib, json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "out"
# replica raw copies: out/k04-replica-raws/ when this script sits at the experiment
# dir root (published layout), or a sibling k04-replica-raws/ (local kit layout).
_CAND = [ROOT / "out" / "k04-replica-raws", ROOT.parent / "k04-replica-raws"]
RAWS = next((c for c in _CAND if all((c / f).exists() for f in
             ["at2m-k04.out.csv", "at15m-run1-k04.out.csv", "at15m-run2-k04.out.csv",
              "at15m-run3-verify-k04.out.csv"])), _CAND[0])

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

# ---- pinned replica raw copies (probe lane originals published at cb7ffe05) ----
# third/second,row,stones,legalIn,legalDerived,result,nodes/budget,ttHits/wall_s,wall,lo,hi,reason,...
# replay row layout: replay,id,stones,legal,is_or,budget,result,nodes,wall_s,key_lo,key_hi
REPLICA = {
    "at2m-k04.out.csv": ("0", "2000000", "e97fd079a6902287d992c68246b92817694f735f7273ef9f05e89b162b4a497e"),
    "at15m-run1-k04.out.csv": ("1", "9433024", "c10896543282f563deeddf31af994465c9f5fac465c734fa22339a47dc81ca61"),
    "at15m-run2-k04.out.csv": ("1", "9433024", "7c12138c13d8ff5f256a51d3a311994248e405e05f0780678e86a008daac1e8e"),
    "at15m-run3-verify-k04.out.csv": ("1", "9433024", "492f758e4b2a6e1eb1e7a48df697979b39a83f180ecc6d9aa124700c98e1a4ec"),
}
rep15 = []
for fname, (result, nodes, sha) in REPLICA.items():
    p = RAWS / fname
    s = sha256(p)
    gate(f"repl_sha_{fname}", s == sha, s)
    c = parse_row(p).split(",")
    ok = (c[0] == "replay" and c[2] == "5" and c[3] == "83" and c[4] == "0"
          and c[9] == "10376293541461626888" and c[10] == "65536"
          and c[6] == result and c[7] == nodes)
    gate(f"repl_row_{fname}", ok, " | ".join(c))
    if result == "1":
        rep15.append((c[6], c[7]))
gate("repl_k04_win_3runs_unanimous", rep15 == [("1", "9433024")] * 3, str(rep15))
gate("repl_k04_2m_unknown", parse_row(RAWS / "at2m-k04.out.csv").split(",")[6] == "0",
     parse_row(RAWS / "at2m-k04.out.csv"))

# ---- C2/C3 third-impl rows (cold, independent processes) ----
runs = {}
for f in ["k04-cold-a.txt", "k04-cold-b.txt", "k04-cold-v-legal.txt"]:
    c = parse_row(OUT / f).split(",")
    runs[f] = c
    gate(f"third_clean_{f}", c[11] == "clean", f"reason={c[11]}")
    gate(f"third_derivedlegal_{f}", c[3] == c[4] == "83", f"in={c[3]} derived={c[4]}")
    gate(f"third_key_{f}", c[9] == "10376293541461626888" and c[10] == "65536", " | ".join(c))
    gate(f"third_quads_{f}", "quads=95670" in (OUT / f).read_text(), "quads")
k04 = [runs[f] for f in ["k04-cold-a.txt", "k04-cold-b.txt", "k04-cold-v-legal.txt"]]
tok = [(c[5], c[6], c[7]) for c in k04]
gate("C2_k04_win_verdict_level_vs_replica",
     all(c[5] == "1" for c in k04) and rep15[0][0] == "1",
     f"third={set(c[5] for c in k04)} replica={set(r[0] for r in rep15)}")
gate("C2_k04_determinism_3runs_identical",
     len(set(tok)) == 1 and tok[0] == ("1", "11020407", "6092599"), f"{tok}")
gate("C2_k04_ttoverwrites_pinned",
     all("ttOverwrites=6826103" in (OUT / f).read_text() for f in runs), "ttOverwrites=6826103")
gate("C2_k04_expansions_differ_from_replica_nodes_allowed",
     int(tok[0][1]) != int(rep15[0][1]),
     f"third_expansions={tok[0][1]} replica_nodes={rep15[0][1]} (different implementations; verdict-level agreement is the gate)")

# ---- C4 negative gates (fail-closed input validation) ----
ng1 = (OUT / "neg-gate-k04-legal84.txt").read_text()
gate("C4_ng1_k04_legal84_gate_fail",
     "GATE_FAIL" in ng1 and "legal count mismatch: derived=83 declared=84" in ng1 and "rc=1" in ng1,
     ng1.strip())
ng2 = (OUT / "neg-gate-k04-stones6.txt").read_text()
gate("C4_ng2_k04_stones6_gate_fail",
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
    "schema": "n11-sixthcost-k04-thirdimpl-audit-v1",
    "all_pass": all(g["pass"] for g in gates.values()),
    "gates": gates,
    "row_results": {
        "k04": {
            "third_impl_verdict": int(k04[0][5]),
            "third_impl_expansions": int(k04[0][6]),
            "third_impl_tt_hits": int(k04[0][7]),
            "third_impl_runs": len(k04),
            "third_impl_determinism_3runs_identical": len(set(tok)) == 1,
            "replica_verdict": int(rep15[0][0]),
            "replica_nodes_15m": int(rep15[0][1]),
            "replica_2m_result_unknown": True,
            "verdict_level_agreement": all(c[5] == rep15[0][0] for c in k04),
        },
    },
    "consumed": False,
    "claim": "verdict-level agreement only; no verdict consumed; 11x11 empty board / two-stone root {60,27} / third moves {100,108} remain UNKNOWN",
}
print(json.dumps(summary, indent=1, sort_keys=True))
sys.exit(0 if summary["all_pass"] else 1)
