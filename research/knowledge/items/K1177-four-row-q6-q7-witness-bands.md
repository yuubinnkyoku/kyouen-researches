---
id: K1177
title: "4xm q=6: witness band m=6..15, witness-free m=16..29; 4xm q=7: witness band m=7..12, witness-free m=13..85 — M_{4,6} = 16 or >= 30, M_{4,7} = 13 or >= 86"
kind: proposition
status: computed
topics: [rectangles, maximal-safe, variants]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "census (circleABC integer triples, line pairs) + sequential-counter/maximality core used verbatim (sat.js md5 0cc6021a…, sat2.js md5 282ae832… — same pins as the K0827/K1134 lanes); def-mode single clause 'some row <= q-2' is the complete encoding of 'not full capacity' for m >= q"
- type: depends_on
  target: K1134
  note: "band-sweep interpretation convention (M = a or >= first-unswept) and the --lex=H cross-encoding reliability check precedent"
- type: depends_on
  target: K0318
  note: "substitution upper bounds U_{4,6}=103, U_{4,7}=81 (curve-packing fixed-width JSON thresholds w=4) are quoted values, unchanged by this item"
artifacts:
- path: research/experiments/four-row-q6-q7-frontier-20261121/README.md
  role: proof
  note: "claims, band tables, 3-system verification protocol, resume/frontier information (initial sweep d6b2c948, band extension 433a8135)"
  commit: 433a813536071299f71accbc04c87de336388cb8
- path: research/experiments/four-row-q6-q7-frontier-20261121/output/records.jsonl
  role: data
  note: "108 append-only records: q=6 10 SAT (m=6..15) + 14 UNSAT (m=16..29; m=28,29 by same-day band extension) + capacity@16 SAT + lexH@16 UNSAT; q=7 6 SAT (m=7..12) + 73 UNSAT (m=13..85; m=73..85 by same-day band extension) + capacity@13/16 SAT + lexH@13 UNSAT. INDET 0; initial 93-record sweep commit d6b2c948, +15 band-extension records in 433a8135"
  commit: 433a813536071299f71accbc04c87de336388cb8
- path: research/experiments/four-row-q6-q7-frontier-20261121/README.md
  role: data
  note: "witness listing: 16 deficient-maximal witnesses (q=6: n=14..19; q=7: n=19..23) and 4 capacity configs (20 resp. 24 stones, all rows q-1) in output/witnesses/*.witness.json"
- path: research/experiments/four-row-q6-q7-frontier-20261121/scripts/runner.js
  role: solver
  note: "sweep / lexdef / rowfixed / cap orchestrator; idempotent by tag; 3-system verification wired in (deficient and capacity semantics)"
- path: research/experiments/four-row-q6-q7-frontier-20261121/scripts/verify3.py
  role: verifier
  note: "third independent verifier: subset-based, census-free; --capacity mode asserts safe+maximal+all rows exactly q-1"
- path: research/experiments/four-row-q6-q7-frontier-20261121/scripts/verify_witness.py
  role: verifier
  note: "python exact-arithmetic safety/maximality/deficiency verifier; --capacity mode added"
- path: research/log/2026-11-21-four-row-q6-q7-frontier-sweep.md
  role: log
  note: "session log: calibration, band construction, interpretation, unswept frontiers"
- path: research/log/2026-11-21-four-row-q6-q7-witness-frontier-single-owner-note.md
  role: log
  note: "single-owner lane declaration (commit 528ec9605bfe9bebf1978011c0c4affecde5e235, 2026-11-21T00:45Z)"
scope: "'finite machine verification (kissat 4.0.4 linux-amd64, md5 3a5eba830aa6008a604fcc9bbe99a325): 4xm q=6 widths 6..29 and 4xm q=7 widths 7..85, plus boundary cross-encodings and capacity instances. No claim about unswept widths >= 30 (q=6) resp. >= 86 (q=7; m=86 is an encoding resource wall, not a decided instance), no claim about the standard 11x11 board.'"
evidence: "'complete-enumeration-by-SAT: per-width def-mode UNSAT is a complete deterministic nonexistence proof for that width (INDET 0 among deciding instances); witnesses verified by 3 independent systems; positive control (6,16,6) reproduced bit-exact (CNF md5 22dd41ba…, conflicts 46).'"
---

# 4×m・q=6/7 行欠損極大 witness band と witness-free 帯 — M_{4,6} = 16 or >= 30, M_{4,7} = 13 or >= 86

## 主張

安定化長は M_{w,q} = least m0 such that P(m) for all m >= m0、
P(m) ⟺「4×m の全極大安全配置がちょうど (q−1)·4 石」とする（K1134 と同一の定式化）。

1. **(4,m,6)**: 幅 m ∈ {6,...,15} の各幅で行欠損極大安全配置（deficient witness）が存在
   （def-mode SAT・石数 14..19・行型 [4,5,5,5]/[5,5,5,4] 等〔m=6,7 は短い行で [1,3,5,5]/
   [1,4,5,5]〕・3系統検証 PASS）。
   幅 m ∈ {16,...,29} の各幅で def-mode インスタンスが **UNSAT（kissat 4.0.4・rc=20・
   INDET 0）**: 14幅すべて完全な決定論的証明（m=16..27 は初期掃引、m=28,29 は同日
   band extension）。conflicts は 1.42M (m=18) から 3.70M (m=27)、m=28,29 は
   2.46M/2.45M・140..141s/幅（cap 400s 内・生成側は `--max-old-space-size=2048` 必須）。
2. **(4,m,7)**: 幅 m ∈ {7,...,12} で deficient witness が存在（SAT・石数 19..23・
   m=7,8 は [6,1,6,6]/[6,2,6,6]、m >= 9 は最小行 5）。幅
   m ∈ {13,...,85} の **73幅すべてで def-mode UNSAT**（m=13..72 は初期掃引
   conflicts ~1,000..6,300・0.04..0.13s/幅、m=73..85 は band extension で
   conflicts 2,819..5,586・0.13..0.21s/幅。INDET 0）。kissat conflicts は幅に対して
   ほぼ非増加であり、UNSAT の理由が局所的（有限窓）構造である
   ことを示唆する（観察・未証明）。
3. **被覆論（K1134 claim 3 と同一）**: m >= q では各行は長さ m >= q の直線なので安全capは
   各行 q−1。よって「極大安全配置が満容量 (q−1)·4 でない」⟺「ある行が <= q−2 石」であり、
   これが def-mode の単一節そのもの。極大安全配置は空集合からの貪欲拡張で常に存在するので、
   def-mode UNSAT ⟹ P(m)。（非自明性の確認として満容量極大安全配置の実在も機械証明済み:
   (4,16,6) 20石 全行5、(4,13,7)・(4,16,7) 24石 全行6・3系統 capacity 検証 PASS。）
4. **K0821/K1134 規約の鋭い形**:
   **M_{4,6} = 16 or M_{4,6} >= 30**（witness band {6..15}・witness-free {16..29}。
   {16,...,29} すべてで P が成立し、30 以降は未掃引。安定化が幅 16..29 のどこかで
   始まるにはそれ以前の全幅に witness が必要だが 15 は最後の witness）。
   **M_{4,7} = 13 or M_{4,7} >= 86**（witness band {7..12}・witness-free {13..85}。
   m=86 は sat2.js 全三つ組 census 符号化の生成段階メモリ上限であって kissat 判定を
   得ておらず、UNSAT/SAT いずれの証拠でもない）。
   代入上界 U_{4,6}=103・U_{4,7}=81 は K0318 の引用値として不変。
   q>2w の自明分離（K0025）に含まれる q >= 9 は本項と無関係、q=8 は K0077 で解決済み
   （M_{4,8}=11・q=2w 境界）。
5. **境界幅の交差符号化確認**: (4,16,6) と (4,13,7) の def-mode + --lex=H（列鏡映
   lex-leader 節・別符号化）が双方 UNSAT（conflicts 1,351,887@45.6s・4,599@0.12s）。
   決定幅の符号化独立性を代表幅で確認した（K1134 と同じ手法）。

## 観察（予想として記録・未証明）

- q=7 の witness-free UNSAT が幅にほぼ非依存（73幅すべて 0.04..0.21s・conflicts
  1,000..6,300 ほぼ非増加）であることから、
  m >= 13 の全幅で欠損極大が存在しない可能性がある（**M_{4,7} = 13 全称予想**）。
  証明候補はブロッキング計数: 欠損行の <= q−2 石に対し、その行の各空点は >= q−1 石を含む
  census 曲線で塞がれなければならず、総石数 <= 4(q−1)−1 = 23 の制約下で幅 >= 13 では
  空点すべてを被覆できない、という類の計数。有限観察であり全称主張ではない。
- q=6 の UNSAT は幅とともに困難化したが（3.70M conflicts・220s@27幅）、m=28,29 は
  2.46M/2.45M conflicts・140s/幅程度に安定（ただし sat2.js census 生成側は
  `NODE_OPTIONS=--max-old-space-size=2048` 必須化）。延伸は引き続き計算資源
  （または rowY 分割・lex 強化）を要する。
- q=7 m=86 の符号化メモリ壁: sat2.js の全三つ組 census は幅 86 で生成段階に
  ヒープ上限到達（kissat 判定なし・INDET ではない）。six-row lane の genfast3.js 型
  弦対抽象円 census（q >= w+2 で完全性論つき・K1134 レーンで確立済み）の w=4 q=7
  移植が突破候補。

## 検証構造

- **較正**: pinned kissat（md5 3a5eba83…）で (6,16,6) 陽性対照を再現 — CNF md5
  `22dd41bae3f338713c8ed866b9a28f8e` 一致・conflicts 46 bit-exact・0.11s・29石 witness。
  sat.js（0cc6021a…）・sat2.js（282ae832…）は repo 正本（K1134/K0827 lane）と同一。
- **witness 3系統検証**: sat.js verifyConfig（安全+極大）・verify_witness.py（整数演算
  安全+極大+行欠損）・verify3.py（部分集合全列挙・census 非依存・第三相互検証）。
  capacity 配置は全系統に --capacity モードを追加して同水準で検証（安全+極大+全行 q−1）。
- **records**: append-only・tag 冪等（重複 skip）。108レコードすべてが mode/q/m/tag/CNF md5/
  kissat rc・conflicts・秒数・cap を記録。決定インスタンス中の INDET 0・SAT/UNSAT混在なし
  （witness band の SAT は witness、witness-free band の UNSAT は完全証明、それぞれ対応）。

## 解釈規約

- 各幅の UNSAT はその幅単体の完全証明であり、未掃引幅（q=6: 30 以降、q=7: 86 以降）に
  ついて一切主張しない。M の確定には残り全幅の UNSAT か十分大域の全称証明が必要。
  q=7 m=86 は符号化資源上限であって判定ではなく、未掃引幅と同様に主張対象外。
- M_{4,7}=13 予想の全称昇格には上記ブロッキング計数の定式化・証明が別途必要。
- 標準 11×11 空盤・二石root 等の未解決局面に本項は影響しない（固定幅 w=4 レーンは標準盤と無関係）。
