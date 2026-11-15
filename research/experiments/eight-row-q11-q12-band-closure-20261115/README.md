# eight-row-q11-q12-band-closure-20261115

IN FLIGHT (claim) — 高速レーン。w=8 の (8,11)/(8,12) 帯の def-mode SAT 掃引・witness 帯延長。

```json
{
  "schema": 1,
  "lane": "fixed-width fast lane (8,11)/(8,12) band closure",
  "status": "IN FLIGHT",
  "date": "2026-11-15",
  "scope": "def-mode SAT sweep of the (8,11) band m=16..907 and the (8,12) band m=15..882 with kissat 4.0.4, family-census CNF generator genfam12.js (rows + m-7 twelve-point F1 circles only, justified band-wide by eight-row-strip-classification-20261115 Theorem A + Corollary 4), upper bounds U_{8,11}=908 / U_{8,12}=883 by K0318 substitution",
  "calibration_done": [
    "genfam12 CNF byte-identical to sat2.js all-triples census CNF at 8x11..8x16 q11 and 8x12..8x16 q12 (11 widths)",
    "genfam12 CNF byte-identical to genfast.js chord-pair census CNF at 8x17/20/26/40/60 q11 and q12 (10 widths)",
    "all 8 published SA witnesses (8x11..8x15 q11, 8x12..8x14 q12) independently re-verified PASS by sat.js verifyConfig + verify_witness.py (dual system)"
  ],
  "early_findings": "kissat 4.0.4 def-mode SAT at the SA-resistant frontier widths: 8x15 q11 SAT (0 conflicts), 8x16 q11 SAT (14 conflicts), 8x17 q11 SAT (57 conflicts), 8x14 q12 SAT (32), 8x15 q12 SAT (66), 8x16 q12 SAT (194) - witnesses exist beyond the SA non-discovery record; M lower bounds will move; model decode + dual verification pending after a sandbox reset",
  "non_goals": "no 11x11 claims; witness-free width sets and M ranges only as established by verified witnesses and UNSAT instances; (8,9) 8x29 and other claimed frontiers untouched"
}
```

詳細な README・結果は掃引完了後に本ファイルを更新して記録する。
