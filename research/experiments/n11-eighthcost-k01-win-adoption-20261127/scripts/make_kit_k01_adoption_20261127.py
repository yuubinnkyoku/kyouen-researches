#!/usr/bin/env python3
"""Eighth-cost k01 WIN row canonical adoption kit maker (2026-11-27).

Single-row form of the published Part SZ adoption maker (disclosed
structural clone): assembles the fail-closed adoption kit for consuming
exactly ONE published eighth-cost row, the k01 WIN row
(s5verdict,1297036692750860288,64,5,1,8514427), into the canonical head
of record BASE 5b6e77f7 (6,874 rows WIN 202 / LOSS 6,672). Declared in
research/log/2026-11-27-n11-eighthcost-k01-win-adoption-declaration.md
(publish-then-execute).

Gates (all must PASS; any failure -> rc=1, no emit):
  G0  BASE head sha + census + k01 pair ABSENT (freshness 1/1,
      WIN/LOSS conflicts 0).
  G1  replica pillar: eighth-cost kit batch-summary sha 2379dbe0,
      schema/class/counters; at15m cold pair sha 3be9db9b x2;
      WIN(1) nodes 8514427 inside budget; at2m stage pair pinned.
  G2  C++ gate pillar: published kit 24/24 byte-verified; gate-rows
      schema/pins; expected quadruple 84,15000000,1,8514427; LIVE audit
      re-run (audit_gate.py with the pinned head) rc=0.
  G3  third-impl pillar: kit 4/4 byte-verified; third_impl.js pin
      08ea958f; both raw rows result 1 WIN, expansions 9987963
      mutually identical.
  G4  merger byte-clone sha 90711961; increment emission (header +
      1 row) and adoption-manifest emission.

NO root verdict is consumed, NO class freed, NO class excluded; the
class-status flip review (win-hit census measurement of the serving
class 1297036692750860288:0) is a separately declared FOLLOW-UP Part.
The standard 11x11 empty board, every central-reply root, the
two-stone root {60,27}, its remaining third moves {100,108}, S2, class
1/2/4 and all closure classes stay UNKNOWN. Nodes are bookkeeping,
never verdicts.
"""
import hashlib, json, os, pathlib, subprocess, sys

KIT = pathlib.Path(__file__).resolve().parent.parent
SSOT = pathlib.Path(os.environ.get("ADOPT_SSOT", str(KIT.parent / "ssot")))

BASE = {
    "path": "research/experiments/n11-seventhcost-sz-adoption-20261127/output/merged/merged-exact-s5-chain-plus-seventhcost42-20261127.cache",
    "sha256": "5b6e77f7d7832d4ce84cb1f080a93e066eb052dcf8b817e5d560f95499fcdde2",
    "rows": 6874, "win": 202, "loss": 6672,
}
K01 = {"lo": "1297036692750860288", "hi": "64", "legal": "84",
       "nodes": 8514427, "budget": 15000000}
ROW = "s5verdict,1297036692750860288,64,5,1,8514427"
E8 = {
    "bs_sha256": "2379dbe031c59b368407a41a65c5366d5209234045c149d0ec2d40136698ba08",
    "raw_pair_sha256": "3be9db9b76f5dbd2756ffe51a2eb4e2c62c09f12d6999f7bc9a0376075479062",
    "class": "1297036692750860288:0",
}
GATE_KIT = "research/experiments/n11-eighthcost-k01-win-cppgate-20261127"
GATE_KIT_FILES = 24
GATE_EXPECT = "84,15000000,1,8514427"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
TI = {
    "manifest_lines": 4,
    "third_impl_sha256": "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998",
    "expansions": 9987963,
}

def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def replay_row(path):
    for line in pathlib.Path(path).read_text().splitlines():
        if line.startswith("replay,"):
            return line.split(",")
    return None

gates = {}
def gate(name, ok, detail=""):
    gates[name] = {"status": "PASS" if ok else "FAIL", "detail": str(detail)}
    return bool(ok)

ok = True

# G0: BASE head
head = SSOT / "head.cache"
ok &= gate("G0:base-head-sha", sha256(head) == BASE["sha256"], sha256(head))
data = [l for l in head.read_text().splitlines() if l.startswith("s5verdict,")]
wins = sum(1 for l in data if l.split(",")[4] == "1")
losses = sum(1 for l in data if l.split(",")[4] == "2")
ok &= gate("G0:base-head-census", len(data) == BASE["rows"] and wins == BASE["win"] and losses == BASE["loss"],
           "rows=%d WIN=%d LOSS=%d" % (len(data), wins, losses))
present = [l for l in data if l.split(",")[1] == K01["lo"] and l.split(",")[2] == K01["hi"]]
ok &= gate("G0:freshness-k01-absent", not present, "conflicts=0 freshness=1")
ok &= gate("G0:row-format", ROW == "s5verdict,%s,%s,5,1,%d" % (K01["lo"], K01["hi"], K01["nodes"]), "")

# G1: replica pillar
bs_path = SSOT / "e8" / "batch-summary.json"
ok &= gate("G1:batch-summary-sha", sha256(bs_path) == E8["bs_sha256"], sha256(bs_path))
bs = json.loads(bs_path.read_text())
ok &= gate("G1:batch-summary-schema", bs.get("schema") == "n11-eighthcost-batch-checkpoint-summary-v1", bs.get("schema"))
ok &= gate("G1:batch-summary-class", bs.get("class") == E8["class"], "")
ok &= gate("G1:batch-summary-counters", bs.get("batch_keys") == 43 and bs.get("resolved_exact_win") == 1
           and bs.get("win_resolved_keys") == ["1297036692750860288:64"] and bs.get("resolved_exact_loss") == 0
           and bs.get("parked_unknown_15m") == 0 and bs.get("win_stopping_rule_fired") is True, "")
r1 = SSOT / "e8" / "at15m-run1.k01.out.csv"
r2 = SSOT / "e8" / "at15m-run2.k01.out.csv"
ok &= gate("G1:at15m-pair-sha", sha256(r1) == E8["raw_pair_sha256"] and sha256(r2) == E8["raw_pair_sha256"], "")
f1 = replay_row(r1)
ok &= gate("G1:at15m-win-row", f1 and f1[3] == K01["legal"] and f1[6] == "1" and f1[7] == str(K01["nodes"])
           and int(f1[7]) <= int(f1[5]), "")
s1 = replay_row(SSOT / "e8" / "at2m-run1.k01.out.csv")
ok &= gate("G1:at2m-stage-unknown", s1 and s1[6] == "0" and s1[7] == "2000000", "")

# G2: C++ gate pillar (published kit copy)
gk = SSOT / "gatekit"
man = [l.split() for l in (gk / "MANIFEST-sha256.txt").read_text().splitlines() if l.strip()]
ok &= gate("G2:gatekit-manifest-count", len(man) == GATE_KIT_FILES, len(man))
bad = [r[2] for r in man if sha256(gk / r[2]) != r[0]]
ok &= gate("G2:gatekit-manifest-sha-all", not bad, str(bad[:2]))
gr = json.loads((gk / "input" / "gate-rows.json").read_text())
ok &= gate("G2:gate-rows-schema", gr.get("schema") == "n11-eighthcost-k01-win-cppgate-rows-v1", gr.get("schema"))
ok &= gate("G2:gate-rows-expected", gr.get("target", {}).get("k01", {}).get("expected") == GATE_EXPECT, "")
ok &= gate("G2:gate-rows-thirdimpl-recorded", gr.get("third_impl", {}).get("exists") is True, "")
audit = subprocess.run([sys.executable, str(gk / "scripts" / "audit_gate.py")],
                       capture_output=True, text=True, cwd=str(gk),
                       env=dict(os.environ, K01_HEAD=str(head)))
ok &= gate("G2:live-audit-rc0", audit.returncode == 0, (audit.stdout + audit.stderr).strip()[:200])

# G3: third-impl pillar
ti = SSOT / "ti"
tman = [l.split() for l in (SSOT / "ti-MANIFEST.txt").read_text().splitlines() if l.strip()]
ok &= gate("G3:ti-manifest-count", len(tman) == TI["manifest_lines"], len(tman))
bad = [r[2] for r in tman if sha256(ti / r[2]) != r[0]]
ok &= gate("G3:ti-manifest-sha-all", not bad, str(bad))
ok &= gate("G3:third-impl-pin", sha256(ti / "scripts" / "third_impl.js") == TI["third_impl_sha256"], "")
exp = []
for p in ("k01.p1.txt", "k01.p2.txt"):
    for line in (ti / "output" / "raw" / p).read_text().splitlines():
        if line.startswith("third,"):
            f = line.split(",")
            exp.append((f[3], f[5], f[6], f[9], f[10]))
ok &= gate("G3:ti-raws-win-expansions", len(exp) == 2 and all(
    e[0] == K01["legal"] and e[1] == "1" and e[2] == str(TI["expansions"]) and e[3] == K01["lo"] and e[4] == K01["hi"]
    for e in exp), str(exp))

# G4: merger byte-clone
merger = KIT / "scripts" / "s5_union_merge.py"
ok &= gate("G4:merger-byte-clone", sha256(merger) == MERGER_SHA, sha256(merger))

print(json.dumps({"gates": gates, "overall": "PASS" if ok else "FAIL"}, indent=1, sort_keys=True))
if not ok:
    for k, v in sorted(gates.items()):
        if v["status"] == "FAIL":
            print("FAIL", k, v["detail"])
    sys.exit(1)

# emit increment cache
hdr = """# n11 eighth-cost k01 WIN row canonical adoption increment
#   (n11-eighthcost-k01-win-adoption-20261127, 2026-11-27) - fresh
#   single-row increment: 1 WIN (k01 1297036692750860288:64, replica
#   nodes 8514427 at the 15M stage, cold pair 3be9db9b x2).
#   The canonical head of record advances from merged-exact-s5-chain-
#   plus-seventhcost42 (sha256 5b6e77f7..., 6,874 rows WIN 202 /
#   LOSS 6,672) by consuming exactly this one published row.
# Sources of record (all re-verified live by this maker against
#   published bytes): the eighth-cost ladder kit (batch-summary
#   2379dbe0, at15m cold pair 3be9db9b x2), the eighth-cost k01 WIN
#   C++ scrutiny gate kit (24/24 files, audit_gate.py live PASS),
#   the eighth-cost k01 third-implementation corroboration kit
#   (4/4 files, third_impl 08ea958f, WIN(1) expansions 9987963 x2).
# The adopted key is fresh to BASE 5b6e77f7 (absent, machine-
#   verified), WIN/LOSS conflicts 0 per the SV merger fail-closed
#   union; adopted node total 8514427 (bookkeeping, never verdicts).
# NO root verdict is consumed, NO class freed, NO class excluded;
#   the class-status flip review (win-hit census measurement of the
#   serving class 1297036692750860288:0) is a separately declared
#   follow-up Part; the standard 11x11 empty board, every
#   central-reply root, the two-stone root {60,27} and its remaining
#   third moves {100,108} stay UNKNOWN.
"""
inc_path = KIT / "output" / "increment-eighthcost-k01-win-adoption-20261127.cache"
inc_path.parent.mkdir(parents=True, exist_ok=True)
inc_path.write_text(hdr + ROW + "\n")

# emit adoption manifest
am = {
    "schema": "eighthcost-k01-win-adoption-manifest-v1",
    "kit": "n11-eighthcost-k01-win-adoption-20261127",
    "declaration_log": "research/log/2026-11-27-n11-eighthcost-k01-win-adoption-declaration.md",
    "base_head": {"path": BASE["path"], "sha256": BASE["sha256"], "rows": BASE["rows"],
                  "win": BASE["win"], "loss": BASE["loss"]},
    "pillars": {
        "replica": {"batch_summary_sha256": E8["bs_sha256"],
                    "at15m_pair_sha256": E8["raw_pair_sha256"],
                    "win_nodes": K01["nodes"], "stage": "15m"},
        "cpp_gate": {"kit": GATE_KIT, "files": GATE_KIT_FILES,
                     "gate_rows_sha256": sha256(gk / "input" / "gate-rows.json"),
                     "audit_live": "audit_gate: PASS"},
        "third_impl": {"kit": "n11-eighthcost-k01-win-thirdimpl-corroboration-20261127",
                       "files": TI["manifest_lines"],
                       "third_impl_sha256": TI["third_impl_sha256"],
                       "expansions": TI["expansions"]},
    },
    "adopted": {"rows": 1, "win": 1, "loss": 0, "nodes_total": K01["nodes"],
                "freshness": 1, "win_loss_conflicts": 0, "duplicates": 0,
                "row": ROW},
    "suppressed_not_adopted": {"keys": 42, "reason": "WIN stopping rule (pre-registered); they stay UNKNOWN-pair-at-2M only, fresh vs BASE"},
    "merger": {"path": "scripts/s5_union_merge.py", "sha256": MERGER_SHA, "runs": 3},
    "expected_merged": {"rows": 6875, "win": 203, "loss": 6672},
    "follow_up_declared": "class-status flip census measurement (win-hit mechanism, serving class 1297036692750860288:0 owner set) - separate Part",
    "gates": gates,
}
(KIT / "output" / "adoption-manifest.json").write_text(json.dumps(am, indent=1, sort_keys=True) + "\n")

# emit MANIFEST over kit files present now
man_out = []
for p in sorted(KIT.rglob("*")):
    if p.is_file() and p.name != "MANIFEST-sha256.txt":
        man_out.append("%s %d %s" % (sha256(p), p.stat().st_size, str(p.relative_to(KIT))))
(KIT / "MANIFEST-sha256.txt").write_text("\n".join(man_out) + "\n")
print("EMIT increment + adoption-manifest + MANIFEST")
