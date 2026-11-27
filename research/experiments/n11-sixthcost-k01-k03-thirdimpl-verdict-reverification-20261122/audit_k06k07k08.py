#!/usr/bin/env python3
"""Fail-closed audit of the k06/k07/k08 third-implementation verdict addendum of
research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/
(declaration research/log/2026-11-26-n11-sixthcost-k06-k07-k08-thirdimpl-verdict-single-owner-note.md).

Reads only the k06/k07/k08 addendum raws in out/ plus the pinned replica raw copies
(out/k06-replica-raws/, out/k07-replica-raws/, out/k08-replica-raws/ in the published
layout, byte-identical to the sixth-cost probe lane originals consumed at HEAD
dc7f36e1; or the local kit layout's flat raws/ sibling), and recomputes every
acceptance gate of the addendum. Deterministic; byte-identical output across runs;
exits 1 on any gate failure.
"""
import hashlib, json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "out"
# replica raw copies: out/kNN-replica-raws/ when this script sits at the experiment
# dir root (published layout), or the flat raws/ sibling (local kit layout).
_CAND = [ROOT.parent / "raws"]
def _resolve(files):
    base = {"k06": _CAND + [ROOT / "out" / "k06-replica-raws", ROOT / "k06-replica-raws"],
            "k07": _CAND + [ROOT / "out" / "k07-replica-raws", ROOT / "k07-replica-raws"],
            "k08": _CAND + [ROOT / "out" / "k08-replica-raws", ROOT / "k08-replica-raws"]}
    return next((c for c in base[files] if c.exists() and
                 all((c / fn).exists() for fn in _FILES[files])), base[files][0])

_FILES = {
    "k06": ["at2m-k06.out.csv", "at15m-run1-k06.out.csv", "at15m-run2-k06.out.csv"],
    "k07": ["at2m-k07.out.csv", "at2m-run2-k07.out.csv", "at15m-run1-k07.out.csv", "at15m-run2-k07.out.csv"],
    "k08": ["at2m-k08.out.csv", "at15m-run1-k08.out.csv", "at15m-run2-k08.out.csv", "at15m-run3-verify-k08.out.csv"],
}
RAWS6 = _resolve("k06")
RAWS7 = _resolve("k07")
RAWS8 = _resolve("k08")

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

# ---- pinned replica raw copies (probe lane originals consumed at HEAD dc7f36e1) ----
# replay row layout: replay,id,stones,legal,is_or,budget,result,nodes,wall_s,key_lo,key_hi
def repl_gates(raws, key, files, stones, legal, lo, hi, expect_res, expect_nodes, label):
    rows = []
    for fname, (result, nodes, sha) in files.items():
        p = raws / fname
        s = sha256(p)
        gate(f"repl_sha_{fname}", s == sha, s)
        c = parse_row(p).split(",")
        ok = (c[0] == "replay" and c[2] == stones and c[3] == legal and c[4] == "0"
              and c[9] == lo and c[10] == hi and c[6] == result and c[7] == nodes)
        gate(f"repl_row_{fname}", ok, " | ".join(c))
        rows.append((c[6], c[7]))
    return rows

K06 = {
    "at2m-k06.out.csv": ("0", "2000000", "136dce33080d949cacc161e21abed9622420351737e61dd7fee847591c586259"),
    "at15m-run1-k06.out.csv": ("2", "8182231", "070095ec004b960dae1d90a6bc44660ab70f40cda3aaf7499a16923625eb171f"),
    "at15m-run2-k06.out.csv": ("2", "8182231", "b48f6816532585b4646bfada3b45a791b5c892caf216ab4d255e6e8644a88635"),
}
r6 = repl_gates(RAWS6, "k06", K06, "5", "89", "10376293541462675456", "65536", 2, 8182231, "k06")
gate("repl_k06_loss_2runs_unanimous", r6[1:] == [("2", "8182231")] * 2, str(r6))
gate("repl_k06_2m_unknown", r6[0] == ("0", "2000000"), str(r6[0]))

K07 = {
    "at2m-k07.out.csv": ("2", "1419823", "ac127dd0e3b651e51f45ec6fcf8a2079bd5322d43253a0160f69f54b0db99874"),
    "at2m-run2-k07.out.csv": ("2", "1419823", "ab41ce86955636be8f17ac1d1b1591baf0b54a7ec5f888ef68b952fea97d1fe9"),
    "at15m-run1-k07.out.csv": ("2", "1419823", "c0e75a93df64d71aa90b54647ce593c6de4766bf730f6179ea8e9d0c849fc2cf"),
    "at15m-run2-k07.out.csv": ("2", "1419823", "c0e75a93df64d71aa90b54647ce593c6de4766bf730f6179ea8e9d0c849fc2cf"),
}
r7 = repl_gates(RAWS7, "k07", K07, "5", "87", "10376293542535368704", "65536", 2, 1419823, "k07")
gate("repl_k07_loss_4runs_unanimous", r7 == [("2", "1419823")] * 4, str(r7))

K08 = {
    "at2m-k08.out.csv": ("0", "2000000", "274e02b011464194f397d5fda587aafe02b03d875d1c9e2f205438d9684f1c12"),
    "at15m-run1-k08.out.csv": ("1", "6195897", "b015a80c41c2aeb21c4c387c433d3a119569590c10907c8038d76e4e6c677044"),
    "at15m-run2-k08.out.csv": ("1", "6195897", "b015a80c41c2aeb21c4c387c433d3a119569590c10907c8038d76e4e6c677044"),
    "at15m-run3-verify-k08.out.csv": ("1", "6195897", "61d5379bccde66b43dc1bda2bf640a02152faeeeaa83cf982889ad4b8c732481"),
}
r8 = repl_gates(RAWS8, "k08", K08, "5", "89", "10376293610182148096", "68719476736", 1, 6195897, "k08")
gate("repl_k08_win_3runs_unanimous", r8[1:] == [("1", "6195897")] * 3, str(r8))
gate("repl_k08_2m_unknown", r8[0] == ("0", "2000000"), str(r8[0]))

# ---- C1 calibration (this session, this host, fresh) ----
vt = (OUT / "calib-verify-tbl-k06k07k08.txt").read_text()
gate("C1_verify_tbl_quads_equality",
     "replica quads 95670 mine quads 95670" in vt and "triples checked 195044 mismatches 0" in vt and "rc=0" in vt,
     vt.strip())
anch1 = parse_row(OUT / "calib-anchor-w2-k06k07k08.txt").split(",")
anch2 = parse_row(OUT / "calib-anchor-w2-run2-k06k07k08.txt").split(",")
gate("C1_anchor_w2_published_witness",
     anch1[5] == "1" and anch1[6] == "7583990" and "rc=0" in (OUT / "calib-anchor-w2-k06k07k08.txt").read_text(),
     " | ".join(anch1))
gate("C1_anchor_w2_run2_identical", (anch2[5], anch2[6]) == (anch1[5], anch1[6]) and
     "rc=0" in (OUT / "calib-anchor-w2-run2-k06k07k08.txt").read_text(),
     " | ".join(anch2))

# ---- C2/C3 third-impl rows (cold, independent processes) ----
def third_gates(files, legal, lo, hi):
    rows = []
    for f in files:
        c = parse_row(OUT / f).split(",")
        rows.append(c)
        gate(f"third_clean_{f}", c[11] == "clean", f"reason={c[11]}")
        gate(f"third_derivedlegal_{f}", c[3] == c[4] == legal, f"in={c[3]} derived={c[4]}")
        gate(f"third_key_{f}", c[9] == lo and c[10] == hi, " | ".join(c))
        gate(f"third_quads_{f}", "quads=95670" in (OUT / f).read_text(), "quads")
    return rows

k06 = third_gates(["k06-cold-a.txt", "k06-cold-b.txt"], "89", "10376293541462675456", "65536")
k07 = third_gates(["k07-cold-a.txt", "k07-cold-b.txt"], "87", "10376293542535368704", "65536")
k08 = third_gates(["k08-cold-a.txt", "k08-cold-b.txt", "k08-cold-v-legal.txt"],
                  "89", "10376293610182148096", "68719476736")

tok6 = [(c[5], c[6], c[7]) for c in k06]
tok7 = [(c[5], c[6], c[7]) for c in k07]
tok8 = [(c[5], c[6], c[7]) for c in k08]

gate("C2_k06_loss_verdict_level_vs_replica",
     all(c[5] == "2" for c in k06) and r6[1][0] == "2",
     f"third={set(c[5] for c in k06)} replica={r6[1][0]}")
gate("C2_k06_determinism_2runs_identical",
     len(set(tok6)) == 1 and tok6[0] == ("2", "9474431", "5163124"), f"{tok6}")
gate("C2_k06_ttoverwrites_pinned",
     all("ttOverwrites=5280127" in (OUT / f).read_text() for f in ["k06-cold-a.txt", "k06-cold-b.txt"]),
     "ttOverwrites=5280127")
gate("C2_k06_expansions_differ_from_replica_nodes_allowed",
     int(tok6[0][1]) != int(r6[1][1]),
     f"third_expansions={tok6[0][1]} replica_nodes={r6[1][1]} (different implementations; verdict-level agreement is the gate)")

gate("C2_k07_loss_verdict_level_vs_replica",
     all(c[5] == "2" for c in k07) and r7[0][0] == "2",
     f"third={set(c[5] for c in k07)} replica={r7[0][0]}")
gate("C2_k07_determinism_2runs_identical",
     len(set(tok7)) == 1 and tok7[0] == ("2", "1608994", "935234"), f"{tok7}")
gate("C2_k07_ttoverwrites_pinned",
     all("ttOverwrites=169" in (OUT / f).read_text() for f in ["k07-cold-a.txt", "k07-cold-b.txt"]),
     "ttOverwrites=169")
gate("C2_k07_expansions_differ_from_replica_nodes_allowed",
     int(tok7[0][1]) != int(r7[0][1]),
     f"third_expansions={tok7[0][1]} replica_nodes={r7[0][1]} (different implementations; verdict-level agreement is the gate)")

gate("C2_k08_win_verdict_level_vs_replica",
     all(c[5] == "1" for c in k08) and r8[1][0] == "1",
     f"third={set(c[5] for c in k08)} replica={r8[1][0]}")
gate("C2_k08_determinism_3runs_identical",
     len(set(tok8)) == 1 and tok8[0] == ("1", "7243596", "3873045"), f"{tok8}")
gate("C2_k08_ttoverwrites_pinned",
     all("ttOverwrites=3050565" in (OUT / f).read_text()
         for f in ["k08-cold-a.txt", "k08-cold-b.txt", "k08-cold-v-legal.txt"]),
     "ttOverwrites=3050565")
gate("C2_k08_expansions_differ_from_replica_nodes_allowed",
     int(tok8[0][1]) != int(r8[1][1]),
     f"third_expansions={tok8[0][1]} replica_nodes={r8[1][1]} (different implementations; verdict-level agreement is the gate)")

# ---- C4 negative gates (fail-closed input validation) ----
NG = {
    "C4_ng1_k06_legal90_gate_fail": ("neg-gate-k06-legal90.txt", "legal count mismatch: derived=89 declared=90"),
    "C4_ng2_k06_stones6_gate_fail": ("neg-gate-k06-stones6.txt", "stone count mismatch: bits=5 declared=6"),
    "C4_ng1_k07_legal88_gate_fail": ("neg-gate-k07-legal88.txt", "legal count mismatch: derived=87 declared=88"),
    "C4_ng2_k07_stones6_gate_fail": ("neg-gate-k07-stones6.txt", "stone count mismatch: bits=5 declared=6"),
    "C4_ng1_k08_legal90_gate_fail": ("neg-gate-k08-legal90.txt", "legal count mismatch: derived=89 declared=90"),
    "C4_ng2_k08_stones6_gate_fail": ("neg-gate-k08-stones6.txt", "stone count mismatch: bits=5 declared=6"),
}
for name, (fname, msg) in NG.items():
    t = (OUT / fname).read_text()
    gate(name, "GATE_FAIL" in t and msg in t and "rc=1" in t, t.strip())

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

# ---- row spec input pins (published batch inputs of the probe lane) ----
INPINS = {
    "k06.input.csv": ("e94c2ade1facf9de78b91936238acacc196770878c50bd84bfdd585d91e8e6a4",
                      "target,0,5,10376293541462675456,65536,89,0,0,0,0,0"),
    "k07.input.csv": ("1e3deebf9777b232e6dbec4cabf64a12039926f339b8ca9a91c95635e094bdb5",
                      "target,0,5,10376293542535368704,65536,87,0,0,0,0,0"),
    "k08.input.csv": ("6fcbf158817f25e82ebb73010c49638949aa2f8ff9d48713d4806a2d4426c35f",
                      "target,0,5,10376293610182148096,68719476736,89,0,0,0,0,0"),
}
for _name, (_sha, _spec) in INPINS.items():
    _p = next((c for c in [ROOT / "input" / _name, ROOT.parent / "inv" / _name] if c.exists()), None)
    gate(f"pin_input_{_name.replace('.', '_')}_sha256",
         _p is not None and sha256(_p) == _sha and _p.read_text().strip() == _spec,
         str(_p) if _p is not None else "not found in any candidate location")

summary = {
    "schema": "n11-sixthcost-k06k07k08-thirdimpl-audit-v1",
    "all_pass": all(g["pass"] for g in gates.values()),
    "gates": gates,
    "row_results": {
        "k06": {
            "third_impl_verdict": int(k06[0][5]),
            "third_impl_expansions": int(k06[0][6]),
            "third_impl_tt_hits": int(k06[0][7]),
            "third_impl_runs": len(k06),
            "third_impl_determinism_2runs_identical": len(set(tok6)) == 1,
            "replica_verdict": int(r6[1][0]),
            "replica_nodes_15m": int(r6[1][1]),
            "replica_2m_result_unknown": r6[0] == ("0", "2000000"),
            "verdict_level_agreement": all(c[5] == r6[1][0] for c in k06),
        },
        "k07": {
            "third_impl_verdict": int(k07[0][5]),
            "third_impl_expansions": int(k07[0][6]),
            "third_impl_tt_hits": int(k07[0][7]),
            "third_impl_runs": len(k07),
            "third_impl_determinism_2runs_identical": len(set(tok7)) == 1,
            "replica_verdict": int(r7[0][0]),
            "replica_nodes_allstages": int(r7[0][1]),
            "replica_runs_unanimous_4": r7 == [("2", "1419823")] * 4,
            "verdict_level_agreement": all(c[5] == r7[0][0] for c in k07),
        },
        "k08": {
            "third_impl_verdict": int(k08[0][5]),
            "third_impl_expansions": int(k08[0][6]),
            "third_impl_tt_hits": int(k08[0][7]),
            "third_impl_runs": len(k08),
            "third_impl_determinism_3runs_identical": len(set(tok8)) == 1,
            "replica_verdict": int(r8[1][0]),
            "replica_nodes_15m": int(r8[1][1]),
            "replica_2m_result_unknown": r8[0] == ("0", "2000000"),
            "verdict_level_agreement": all(c[5] == r8[1][0] for c in k08),
        },
    },
    "consumed": False,
    "claim": "verdict-level agreement only; no verdict consumed; 11x11 empty board / two-stone root {60,27} / third moves {100,108} remain UNKNOWN",
}
print(json.dumps(summary, indent=1, sort_keys=True))
sys.exit(0 if summary["all_pass"] else 1)
