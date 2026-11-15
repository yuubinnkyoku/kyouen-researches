---
id: K0833
title: "4〜6行 q=4,5 行欠損witness帯 — (4,4) m=4..34, (5,4) m=5..39, (6,4) m=6..46, (4,5) m=5..20, (5,5) m=5..25 全幅SAT; M_{4,4}>=35, M_{5,4}>=40, M_{6,4}>=47, M_{4,5}>=21, M_{5,5}>=26; sat3 OOM壁越えと rowY 分割・2クラス被覆で帯延伸"
kind: proposition
status: computed
topics: [rectangles, maximal-safe]
aliases: []
relations:
- type: depends_on
  target: K0810
  note: "sat2.js def-mode 完全符号化を verbatim 使用（全三つ組census・逐次カウンタ・極大性・lex=H,V,HVHV）; witness の検証にも sat.js verifyConfig（census不使用）を使用"
- type: depends_on
  target: K0068
  note: "q=4 の上界 T_4=237, T_5=567, T_6=1113（全局面偶奇式の一般上界; K0318 curve-packing 代入でも同一値）"
- type: depends_on
  target: K0318
  note: "q=5 の上界 U_{4,5}=140, U_{5,5}=336（curve-packing 代入上界; curve_packing_fixed_width.py bound() で本レーンで再計算・一致確認済み: w4q5 packing_U=140, w5q5 packing_U=336）"
- type: depends_on
  target: K0827
  note: "7行 q<=w 3ファミリーと同じ手法・同じ観察（m=q から連続帯・単一欠損 w(q-1)-1 石・構成的延伸は前線を一部だけ越える）; verify_independent.ts（第3系統）を verbatim 使用"
artifacts:
- path: research/experiments/four-six-row-q4-q5-witness-search-20261114/report.md
  role: proof
  note: "claims・手法・較正・honest negatives（OOM壁・INDET前線）・構造観察・次課題"
- path: research/experiments/four-six-row-q4-q5-witness-search-20261114/output/q4-w4-def-search/records.jsonl
  role: data
  note: "30 records: m=4..28 sat2+kissat SAT (m=8以降は単一欠損11石, conflicts 0..12,475 非単調), m=29/31/33/34 constructive SAT (空列追加/シフト, m=33 off=0, m=34 off=1, m=32ベース), m=30 SAT 105.1s/119,905, m=32 SAT 134.5s/122,164; m=29 60s INDET 38,235 は構成的SATで解決"
- path: research/experiments/four-six-row-q4-q5-witness-search-20261114/output/q4-w5-def-search/records.jsonl
  role: data
  note: "34 records m=5..36 all SAT dual-verified: 石数8..14（m=14以降 cap 14=w(q-1)-1）, m=25..33 は lex なし符号化でも SAT（witness としては等価に有効）, m=34 19.1s/2,623, m=35 72.6s/8,521, m=36 104.9s/10,644; m>=37 は sat2.js census CNF生成 OOM（rc=1 行は枝刈り済み）"
- path: research/experiments/four-six-row-q4-q5-witness-search-20261114/output/q4-w6-def-search/records.jsonl
  role: data
  note: "26 records m=6..31 al
l SAT dual-verified: m=23以降単一欠損17石, m=31 4.1s/131 conflicts, 全インスタンス <7s; m>=32 census OOM"
- path: research/experiments/four-six-row-q4-q5-witness-search-20261114/output/q5-w4-def-search/records.jsonl
  role: data
  note: "16 records: m=5..19 all SAT dual-verified (m=12以降単一欠損15石, m=19 14.2s/262,918), m=20 INDET 210s/3,296,257（未解決前線・不在主張ではない）; genfast.js PAIRTHRESH=12 は (4,5) で不正確なため sat2.js 全三つ組census を使用"
- path: research/experiments/four-six-row-q4-q5-witness-search-20261114/output/q5-w5-def-search/records.jsonl
  role: data
  note: "20 records: m=5..23 all SAT dual-verified (m=10以降単一欠損19石, m=23 62.9s/508,466), m=24 INDET 90s/698,672（前線）"
- path: research/experiments/four-six-row-q4-q5-witness-search-20261114/output/controls/records.jsonl
  role: data
  note: "較正11 records: 既知の確定閾値6件を全て再現（(3,5) 11SAT/12UNSAT, (3,6) 8/9, (4,6) 15/16, (4,7) 12/13, (4,8) 10/11, (3,4) m=23 SAT 8石 rows[3,2,3]）"
- path: research/experiments/four-six-row-q4-q5-witness-search-20261114/output/ts-verify-cross-family.json
  role: data
  note: "第3系統（純TS/BigInt, verify_independent.ts verbatim）で5前線 witness 全て PASS safe+maximal+row-deficient: (4,4) m=34 構成, (5,4) m=36, (6,4) m=31, (4,5) m=19, (5,5) m=23 — 3系統検証"
- path: research/experiments/four-six-row-q4-q5-band-extension-20261115/README.md
  role: proof
  note: "band-extension レーン（2026-11-15）: claim・較正（sat3=sat2 11対照バイト一致・kissat 閾値 7/8・lean5 端到端・ext_constructive 再現）・結果"
- path: research/experiments/four-six-row-q4-q5-band-extension-20261115/output/q4-w6/records.jsonl
  role: data
  note: "(6,4) m=32..38 def-mode SAT (782/445/265/332/744/487/932 conflicts, 全17石単一欠損, js+py 2系統検証) + m=39/40 def-mode 120s INDET (6,072/5,410) honest negatives - sat3 streaming census が sat2 census OOM 壁 (m>=32) を越えた初の (6,4) 記録"
- path: research/experiments/four-six-row-q4-q5-band-extension-20261115/output/q4-w6-rowY0/records.jsonl
  role: data
  note: "(6,4) m=39/40 rowY=0 固定分割 SAT (2,573/58.3s, 5,864/172.9s, 17石) - def-mode INDET 前線を解決し witness 帯は m=6..40 に"
- path: research/experiments/four-six-row-q4-q5-band-extension-20261115/output/q4-w5/records.jsonl
  role: data
  note: "(5,4) m=38 def-mode SAT 107.9s/8,626 (14石単一欠損) - 環境リセット前後で conflicts bit-exact"
- path: research/experiments/four-six-row-q4-q5-band-extension-20261115/output/q4-w5-rowY0/records.jsonl
  role: data
  note: "(5,4) m=37 rowY=0 固定分割 SAT 75.7s/8,351 (14石) - OOM 壁直後の幅を解決"
- path: research/experiments/four-six-row-q4-q5-band-extension-20261115/output/q4-w5-rowY0b/records.jsonl
  role: data
  note: "(5,4) m=39 rowY=0 260s INDET 64,737 conflicts の honest negative（不在主張ではない）"
- path: research/experiments/four-six-row-q4-q5-band-extension-20261115/output/q4-w5-rowY1/records.jsonl
  role: data
  note: "(5,4) m=39 rowY=1 固定分割 SAT 197.1s/21,147 (14石) - 帯は m=5..39 に"
- path: research/experiments/four-six-row-q4-q5-band-extension-20261115/output/q4-w4/records.jsonl
  role: data
  note: "(4,4) m=35 def-mode INDET 260s/317,151 conflicts (lex=H,V,HV) - (4,4) 初の cap 抵抗幅の honest negative（不在主張ではない）"
- path: research/experiments/four-row-q4-q5-frontier-20261115/README.md
  role: proof
  note: "frontier レーン（takeover・2026-11-15）: w=4 rowfixed 2クラス被覆補題（rowY=0/1 ∧ lex=H の2 UNSAT で witness-free が確定する行保存性論法・証明つき）・較正・結果"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/q4-w6-rowY0/records.jsonl
  role: data
  note: "(6,4) m=41 rowY=0 固定分割 SAT 245.2s/8,226 conflicts (17石) - witness 帯 m=6..41, M_{6,4} ∈ [42, 1113]"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/q4-w5-rowY1/records.jsonl
  role: data
  note: "(5,4) m=40 rowY=1 600s INDET 191,445 conflicts の honest negative（不在主張ではない）"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/q4-w4-rowY0H/records.jsonl
  role: data
  note: "(4,4) m=35 lex=H rowY=0 600s INDET 324,870 conflicts（2クラス被覆の前半・不在主張ではない）"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/q4-w4-rowY1H/records.jsonl
  role: data
  note: "(4,4) m=35 lex=H rowY=1 600s INDET 230,642 conflicts（2クラス被覆の後半・不在主張ではない）"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/q5-w4-rowY0H/records.jsonl
  role: data
  note: "(4,5) m=21 lex=H rowY=0 600s INDET 6,924,496 conflicts（2クラス被覆の前半・不在主張ではない）"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/q5-w4-rowY1H/records.jsonl
  role: data
  note: "(4,5) m=21 lex=H rowY=1 600s INDET 7,286,846 conflicts（2クラス被覆の後半・不在主張ではない）"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/q4-w6-rowY0-m42/records.jsonl
  role: data
  note: "(6,4) m=42 rowY=0 固定分割 SAT 461.6s/16,942 conflicts (17石 rows [2,3,3,3,3,3]) - witness 帯 m=6..42, M_{6,4} ∈ [43, 1113]"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/ts-verify-frontier.json
  role: data
  note: "(6,4) m=41 witness の第3系統検証 PASS・陽性対照（m=40 witness 再PASS）・陰性対照（1石移動で maxCirc=4 unsafe+10 uncovered を検出）"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/ts-verify-frontier-m42.json
  role: data
  note: "(6,4) m=42 witness の第3系統検証 PASS・陽性対照（m=40 再PASS・nCircles=670/nQ1Curves=690 が m=41 run と同一）・陰性対照（1石移動で maxCirc=4 unsafe+7 uncovered を検出）"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/q4-w6-rowY0-m43/records.jsonl
  role: data
  note: "(6,4) m=43 rowY=0 固定分割 SAT 900s-cap 34,728 conflicts/581s (17石 rows [2,3,3,3,3,3]; wrapper killed post-SAT by env reset, record honestly reconstructed from kissat.txt) - witness 帯 m=6..43, M_{6,4} ∈ [44, 1113]"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/ts-verify-frontier-m43.json
  role: data
  note: "(6,4) m=43 witness の第3系統検証 PASS・陽性対照（m=40 再PASS・nQ1Curves=690 が m=41/m=42 run と同一）・陰性対照（1石移動で maxCirc=4 unsafe+8 uncovered を検出）"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/q4-w6-rowY0-m44/records.jsonl
  role: data
  note: "(6,4) m=44 rowY=0 固定分割 SAT 1200s-cap 12,816 conflicts/493.9s (17石 rows [2,3,3,3,3,3], wrapper completed end-to-end incl. decode; conflicts < m=43's 34,728 - first local reversal of the difficulty trend) - witness 帯 m=6..44, M_{6,4} ∈ [45, 1113]"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/ts-verify-frontier-m44.json
  role: data
  note: "(6,4) m=44 witness の第3系統検証 PASS・陽性対照（m=40 再PASS・nCircles=670/nQ1Curves=690 が m=41/42/43 run と同一）・陰性対照（1石移動で maxCirc=4 unsafe+7 uncovered を検出）"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/q4-w6-rowY0-m45/records.jsonl
  role: data
  note: "(6,4) m=45 rowY=0 固定分割 SAT 1200s-cap 10,066 conflicts/272.1s (17石 rows [2,3,3,3,3,3], wrapper completed end-to-end; conflicts keeps decreasing 34,728 -> 12,816 -> 10,066, m=43 was a local peak) - witness 帯 m=6..45, M_{6,4} ∈ [46, 1113]"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/ts-verify-frontier-m45.json
  role: data
  note: "(6,4) m=45 witness の第3系統検証 PASS・陽性対照（m=40 再PASS・nCircles=670/nQ1Curves=690 が m=41..44 run と同一）・陰性対照（1石移動で maxCirc=4 unsafe+1 uncovered を検出）"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/q4-w6-construct-m46/records.jsonl
  role: data
  note: "(6,4) m=46 witness by constructive free-column append of the m=45 witness (solver-free): stones unchanged on the 6x46 board; pure-TS/BigInt full-board verification PASS (safe maxLine=3/maxCirc=3, uncovered=0, rows [2,3,3,3,3,3]); free append stops at m=47 (cell (46,0) uncovered); js+py verification pending bash recovery - witness 帯 m=6..46, M_{6,4} ∈ [47, 1113]"
- path: research/experiments/four-six-row-q4-q5-band-extension-20261115/output/ts-verify-band-extension.json
  role: data
  note: "第3系統（純TS/BigInt, verify_independent.ts verbatim・フラグメント照合18/18）で band-extension 全12 witness ((6,4) m=32..40, (5,4) m=37..39) が全て PASS safe+maximal+row-deficient・単一欠損; 陰性対照（石移動→unsafe検出）・陽性対照（前レーン3系統検証済み (6,31,4) witness の再PASS）つき — 3系統検証"

- path: research/experiments/four-row-q4-m35-surgery-20261115/README.md
  role: proof
  note: "高速レーン (2026-11-15): m=34 witness 両埋め込みからの bounded-edit surgery 完全列挙負 (offX=0/1: 20,277/21,824 最終状態葉・0 witness) と surgery4.js census 完全性修正 (q<=w の chord-pair census 欠陥: 非行直線・(1,1,1)/(2,1) 行分布円)・buildCensus4 == sat.js 全三つ組 8/8 PASS"
- path: research/experiments/four-row-q4-m35-class-split-20261115/README.md
  role: proof
  note: "高速レーン (2026-11-15) IN FLIGHT: 4×35 absence-capable 完全被覆掃引 (9 正準欠損クラス mod V・単一クラス k×minpos sound H-split・82インスタンス cap 700s resumable)。全 UNSAT なら M_{4,4}=35 or >=37・SAT なら M ∈ [36,237]"
- path: research/experiments/four-row-q4-m35-class-split-20261115/output/records.jsonl
  role: data
  note: "掃引進行記録 (1インスタンス1行・増分 push)。陽性対照 (4,34,4) class{1} k2 p7 は m=34 witness の V∘H 像を含む"
- path: research/experiments/six-row-q4-m47-rowY0-oom-20261115/README.md
  role: proof
  note: "高速レーン (2026-11-15): (6,4) m=47 rowY=0 は kissat RAM 壁 (rc=137/14.3s・sandbox RAM ~2.1GB)。CNF 生成は成功 (2,701,853 vars / 8,965,702 clauses / 259,412 curves)。INDET/OOM・不在主張ではない"

scope: "有限機械検証: kissat 4.0.4（公式静的バイナリ）による SAT 判定は符号化の完全性（def-mode = 行欠損極大安全配置の存在と同値, K0810）と lexer の正しさまで; 構成的延伸 witness は sat.js verifyConfig + Python Fraction の2系統; 前線5幅はさらに第3系統; 各ファミリーの記載幅のみ（未実施幅は不在主張ではない）"
evidence: "完全符号化 SAT インスタンス（sat2.js def-mode）+ 全 witness 2系統検証（jsVerify/pyVerify 全 records true）+ 前線5幅の第3系統検証（ts-verify-cross-family.json）+ 較正（確定閾値6件再現・(4,4) m=4..25 は環境リセット前後で conflicts bit-exact 一致）+ 構成的延伸（(4,4) m=29,31,33,34: cap 到達 witness の純粋空列追加/シフトを verifyConfig が直接検証, ソルバ不使用）"
---

# 4〜6行 q=4,5 行欠損witness帯 — 5ファミリー初の結果

## 主張

1. **(4,4)**: 行欠損の極大安全配置が **m=4..34 の全幅で存在**。
   m=8以降は単一欠損11石（=w(q-1)-1, rows [3,3,3,2] 型）。
   m=29,31,33,34 は SAT witness の**空列追加/シフト**による構成的延伸
   （ソルバ不使用・2系統検証）。**M_{4,4} ∈ [35, 237]**（上界 K0068 T_4）。
2. **(5,4)**: **m=5..36 の全幅で存在**（m=14以降14石）。m=36 は
   104.9s/10,644 conflicts。**M_{5,4} ∈ [37, 567]**。
   m≥37 は sat2.js census CNF生成 OOM（符号化上の壁・不在主張ではない）。
3. **(6,4)**: **m=6..31 の全幅で存在**（m=23以降17石）。**M_{6,4} ∈ [32, 1113]**。
   m≥32 census O
OM。
4. **(4,5)**: **m=5..19 の全幅で存在**（m=12以降15石）。**M_{4,5} ∈ [20, 140]**
   （上界 K0318 U_{4,5}=140）。前線 m=20 は 210s INDET / 3,296,257 conflicts
   — 本レーン最難の未掃引インスタンス。
5. **(5,5)**: **m=5..23 の全幅で存在**（m=10以降19石）。**M_{5,5} ∈ [24, 336]**
   （上界 K0318 U_{5,5}=336）。前線 m=24 は 90s INDET。
6. 検証: 全 witness 2系統検証。5前線 witness は第3系統（純TS/BigInt）
   でも PASS — **3系統検証**。較正として既知の確定閾値6件
   （M_{3,5}, M_{3,6}, M_{4,6}, M_{4,7}, M_{4,8}, M_{3,4} の SAT/UNSAT 対）
   を本レーンの符号化・ソルバで再現。

## 手法

K0810 sat2.js verbatim（q≤w でも (4,5) は genfast.js PAIRTHRESH=12 が
不正確なため全ファミリーで全三つ組census）+ kissat 4.0.4 公式バイナリ。
主符号化 lex=H,V,HVHV（lex なし def-mode は極端に難化: (3,23,4) 100s INDET
445k vs lex 17.7s SAT 66,895）。構成的延伸は cap 到達 witness
（spare=0）のシフト掃引を verifyConfig で直接検証。

## 構造観察

1. 全5ファミリーで **m=q から連続 witness 帯**（K0827 の7行 q≤w と一致）。
2. 十分大きな m で witness は**常に単一欠損** w(q-1)-1 石
   （行は q-2 を1行 + q-1 を w-1 行）— 偶奇式レジジム（K0068: 全極大が
   w(q-1) 石）への移行は、まさにこの単一欠損極大配置の絶滅で起こる。
   各前線は「最後の単一欠損配置」の探索である。
3. 純粋構成延伸（spare=0）は前線を**一部だけ**越える（(4,4) 29/31/33/34
   は越えたが 30 は越えられず、ソルバが 105s で解決）。7行レーンと同型。

## 次課題

(1) (4,5) m=20 rowY 分割（(7,5)/(7,6) 前線を解決した手法）— 小 w の q=5
で U=140 を大きく下回る確定閾値の候補; (2) sat3.js streaming census で
(6,4) m≥32・(5,4) m≥37 の OOM 壁を越える; (3) (4,4) m=35+, (5,5) m=24+;
(4) (4,4) m=32 ベースの blocking-coverage 分析（K0827 型の貪欲バンド延伸）。

## 追記 (2026-11-15 rowY 固定分割による (4,5) m=20 前線の解決)

1. **(4,5) m=20 SAT・3系統検証 PASS**（rowY=3 固定分割・36s・600,345
   conflicts・15石単一欠損 rows [4,4,4,3]）。def-mode OR は 210s INDET
   （3,296,257 conflicts）だった前線を解決し、**witness帯は m=5..20 に拡大、
   M_{4,5} ≥ 21**（M ∈ [21, 140]）。rowY 分割は (7,8)/(7,7)/(7,5)/(7,6)
   に続き5例目の成功。rowY=0/1/2 は 55s INDET（916,641/872,920/877,644）。
2. **前線は m=21**: rowY=0..3 すべて 55s INDET（871,503/796,043/806,981/
   853,465）、rowY=3 の 200s 再実行も INDET（2,714,555 conflicts）。
   いずれも不在主張ではない。
3. 上記で (4,5) の records.jsonl は 21 行（m=5..20 SAT 16幅 + m=20 INDET
   負記録 + m=21 rowY 負記録5件）、m=20 witness は
   ts-verify-cross-family.json で第3系統検証済み。
## 追記 (2026-11-15 band-extension レーン: sat3 OOM壁越えと r
owY 分割)

1. **(6,4): witness 帯 m=6..40 に延伸・M_{6,4} ∈ [41, 1113]**。sat3.js streaming
   census（sat2 と11対照で DIMACS バイト一致・repo (6,31,4) meta は --lex=H,V
   で完全一致）が sat2 の census OOM 壁（m≥32）を解消。m=32..38 は
   def-mode SAT（conflicts 782/445/265/332/744/487/932・全て 40s 未満・
   17石単一欠損）。m=39/40 は def-mode 120s INDET（6,072/5,410 conflicts）を
   **rowY=0 固定分割で解決**（2,573/58.3s・5,864/172.9s）。全 witness js+py
   2系統検証。環境リセット前後で m=32..36 の conflicts が bit-exact
   （決定性の傍証）。
2. **(5,4): witness 帯 m=5..39 に延伸・M_{5,4} ∈ [40, 567]**。m=37 は
   rowY=0 分割 SAT（75.7s/8,351）・m=38 は def-mode SAT（107.9s/8,626・
   再実行 bit-exact）・m=39 は rowY=1 分割 SAT（197.1s/21,147）。
   m=39 rowY=0 は 260s INDET 64,737 conflicts（honest negative）。
   全14石単一欠損・2系統検証。
3. **(4,4) m=35**: def-mode 260s INDET / 317,151 conflicts
   （lex=H,V,HV・sat3）— (4,4) 初の cap 抵抗幅（honest negative・
   不在主張ではない）。既知ベース（m≤34）からの構成的延伸は m=35 で失敗
   （ext_constructive.js の全オフセット掃引で verified 0）。
4. **符号化の訂正記録**: 前レーン m≥26 の lex "H,V,HVHV" は sat2/sat3 の
   SIG={H,V,HV} で "HVHV" がフィルタされ、**実効符号化は [H,V]** だった
   （(6,31,4) meta vars=797554/clauses=2651655 が --lex=H,V でのみ一致する
   ことで確認）。判定は等長不変なので結果に影響しない。本レーンは全記録に
   実効符号化（デフォルト H,V,HV）を明示。
5. 較正: kissat 既知閾値コントロール 8 点中 7 点再現（(3,5) 11/12・(4,8)
   10/11・(4,6) 15/16・(3,4) 23 SAT 66,895 bit-exact）。残る 1 点 (3,4)
   m=24 の 120s INDET は既知 honest negative と整合。
6. 上界は不変（K0068 T_4=237・T_5=567・T_6=1113）。INDET は cap 到達であり
   不在を意味しない。
7. **第3系統検証（追記）**: band-extension の全12 witness について、純TS/BigInt
   検証（verify_independent.ts を verbatim・sandbox 実行・フラグメント照合18/18）
   が全て PASS（safe: maxLine=maxCirc=3, maximal: uncovered=0, 単一欠損）。
   陰性対照（(6,32) witness の1石移動 → maxCirc=4 unsafe を検出）・陽性対照
   （前レーンで3系統検証済みの (6,31,4) witness が再PASS）。これにより
   band-extension の全 witness は js+py+TS の3系統検証済み
   （ts-verify-band-extension.json）。

## 追記 (2026-11-15 four-row-q4-q5-frontier-20261115: takeover と 2クラス被覆掃引)

1. **(6,4) m=41 SAT・3系統検証 PASS**（rowY=0 固定分割・245.2s・8,226 conflicts・
   17石単一欠損 rows [2,3,3,3,3,3]）。**witness 帯は m=6..41 に拡大、
   M_{6,4} ∈ [42, 1113]**。第3系統は純TS/BigInt verify_independent.ts verbatim
   （sandbox 実行・陽性対照 m=40 witness 再PASS・陰性対照 1石移動 unsafe 検出つき、
   ts-verify-frontier.json）。
1b. **(6,4) m=42 SAT・3系統検証 PASS**（rowY=0 固定分割・461.6s・16,942 conflicts・
   17石単一欠損 rows [2,3,3,3,3,3]）。第3系統は同一 verbatim 実行（ts-verify-frontier-m42.json・
   陽性対照 m=40 再PASS は nCircles=670/nQ1Curves=690 が m=41 run と同一・
   陰性対照 1石移動 unsafe 検出つき）。
1c. **(6,4) m=43 SAT・3系統検証 PASS**（rowY=0 固定分割・cap 900s で 581.1s・
   34,728 conflicts・17石単一欠損 rows [2,3,3,3,3,3]）。**witness 帯は m=6..43 に拡大、
   M_{6,4} ∈ [44, 1113]**。第3系統は同一 verbatim 実行（ts-verify-frontier-m43.json・
   陽性対照 m=40 再PASS は nQ1Curves=690 が m=41/m=42 run と同一・
   陰性対照 1石移動 unsafe 検出つき）。ラッパーが SAT 直後に環境リセットで
   殺されたため model は kissat.txt から手動復元し lean5.sh の SAT 分岐
   （decode + js/py 2系統検証）を手動再実行して record 構成（note に明記）。
   難化トレンド m=41 8,226/245s → m=42 16,942/462s →
   m=43 34,728/581s は conflicts ほぼ2倍ずつ・cap 900s が効いていた。
1d. **(6,4) m=44 SAT・3系統検証 PASS**（rowY=0 固定分割・cap 1200s で 493.9s・
   12,816 conflicts・17石単一欠損 rows [2,3,3,3,3,3]）。**witness 帯は m=6..44 に拡大、
   M_{6,4} ∈ [45, 1113]**。第3系統は同一 verbatim 実行（ts-verify-frontier-m44.json・
   陽性対照 m=40 再PASS は nCircles=670/nQ1Curves=690 が m=41/42/43 run と同一・
   陰性対照 1石移動で maxCirc=4 unsafe+7 uncovered を検出）。ラッパーが
   今回は decode・2系統検証まで完走し record は lean5.sh が直接生成
   （前線は m=45）。conflicts は m=43 の 34,728 から 12,816 に減少 —
   難化トレンドの初の反転。
1e. **(6,4) m=45 SAT・3系統検証 PASS**（rowY=0 固定分割・cap 1200s で 272.1s・
   10,066 conflicts・17石単一欠損 rows [2,3,3,3,3,3]）。**witness 帯は m=6..45 に拡大、
   M_{6,4} ∈ [46, 1113]**。第3系統は同一 verbatim 実行（ts-verify-frontier-m45.json・
   陽性対照 m=40 再PASS は nCircles=670/nQ1Curves=690 が m=41..44 run と同一・
   陰性対照 1石移動で maxCirc=4 unsafe+1 uncovered を検出）。conflicts は
   m=43 34,728 → m=44 12,816 → m=45 10,066 と減少が継続 — m=43 が局所ピーク
   だったことが確定。
1f. **(6,4) m=46 witness が構成的に確定**（free-column append: m=45 witness の
   石配置をそのまま 6×46 ボードに置く・ソルバ不使用）。純TS/BigInt 第3系統の
   full-board 走査で safe (maxLine=3/maxCirc=3)・全空点カバー (uncovered=0)・
   行欠損 (rows [2,3,3,3,3,3]) すべて PASS。**witness 帯は m=6..46、
   M_{6,4} ∈ [47, 1113]**。free append は m=47 で停止（(46,0) が未カバー）。
   js+py 2系統検証は bash 環境復旧後に実施予定。周辺分析（純TS）: 1石追加
   （63候補全滅・3 unsafe+60 nonmax）・1石移動（safe 77 組合せ全滅 nonmax）で
   は m=47 witness は出現せず。m=42..44 witness の free-append 到達幅は
   m0+1 で停止（m=42 witness → m=43, m=43/44 witness → m=44/45 の右端
   (m-1,0) が未カバー）— m=45 witness のみ m0+1 を到達。前線は m=47。
2. **w=4 rowfixed 2クラス被覆補題**（frontier レーン README に証明つき）:
   lex=H 単独の rowfixed(0)/rowfixed(1) の2 UNSAT で固定幅の witness-free が確定する
   （H は行を保存し、V は行 0↔3・1↔2 を送る。full-lex (H,V,HV) では V/HV が
   行を動かすため2クラスでは被覆しない）。これにより前レーンの rowY=0..3
   full-lex INDET と違い、2クラス掃引が absence-capable になった。
3. **(4,4) m=35**: 2クラス掃引（lex=H rowY=0/1）ともに 600s INDET
   （324,870 / 230,642 conflicts）。honest negative・不在主張ではない。
   M_{4,4} ∈ [35, 237] は不変。
4. **(4,5) m=21**: 2クラス掃引ともに 600s INDET（6,924,496 / 7,286,846 conflicts・
   合計 ~14.2M）。前レーン rowY=3 full-lex 2.7M@200s を大きく超える探索でも
   未解決。honest negative。M_{4,5} ∈ [21, 140] は不変。
5. **(5,4) m=40**: rowY=1 600s INDET 191,445 conflicts（m=39 rowY=1 SAT 21,147 の
   ~9倍の探索）。honest negative。M_{5,4} ∈ [40, 567] は不変・前線は m=40 のまま。
6. **(5,5) の表記更新**（class-split レーンの成果を反映・CSV と surgery レーン
   README の cross-lane convergence 記録に基づく）: witness 帯 m=5..25、
   M_{5,5} ∈ [26, 336]。
7. 環境運用: wrapper (lean5.sh) が cap 到達時に環境側で殺されても kissat 本体は
   cap まで完走し kissat.txt に最終 stats が残るため、記録を復元して records.jsonl
   に note 付きで保存した（conflicts は決定的値）。実効 CPU ~1コアのため逐次実行。

## 追記 (2026-11-15 高速レーン: 4×35 surgery 完全列挙負・class-split 掃引 IN FLIGHT・6×47 RAM 壁)

1. **(4,4) m=35 bounded-edit surgery 完全列挙 (負・局所)**: m=34 witness
   (rows [3,3,2,3]・11石) を4×35に2通りに移植 (offX=0: T′={(34,2)} /
   offX=1: T′={(0,2)}) し、追加≤2・除去≤2・石数≤11 の全編集を完全列挙
   (four-row-q4-m35-surgery-20261115)。offX=0 は 20,277・offX=1 は 21,824
   最終状態葉で、すべて safe・**0 witness**。**m=34 witness の両埋め込みから
   2+2石編集以内に 4×35 witness は存在しない (不在主張ではない)**。
   連続幅間の witness jump が大きい先行観察 ((5,6) sd≥7・(7,5) 2石移動)
   と整合。
2. **surgery.js census の q≤w 不完全性の発見と修正**: 従来の chord-pair
   census は q>w でのみ完全で、q≤w では非行直線と (1点,1点,1点)/(2点,1点)
   行分布の円が抜ける ((4,35,4) は q=w で該当)。surgery4.js は列挙コアを
   verbatim のまま census だけ buildCensus4 に差し替え (全直線 (L)・
   3行1点円 (E-a)・1行2点+他行1点円 (E-b)・chord-pair verbatim・列挙コアの
   空白正規化一致を機械検証)。
   **census 完全性検査 8/8 PASS**: buildCensus4(w,m,q) が sat.js 全三つ組
   buildCensus と点集合族として完全一致
   ((4,8,4) 485 / (4,20,4) 7,689 / (4,35,4) 41,607 / (5,12,4) 2,875 /
   (6,10,4) 2,735 / (3,24,4) 6,413 / (4,10,5) 89 / (4,20,5) 491)。
   (4,5) m=21 surgery への適用も正当化済み。
3. **(4,4) m=35 class-split 掃引 IN FLIGHT (absence-capable)**: 前線 m=35 の
   完全分解掃引を開始 (four-row-q4-m35-class-split-20261115)。9 正準欠損
   クラス mod V ({0},{1},{0,1},{0,2},{0,3},{1,2},{0,1,2},{0,1,3},{0,1,2,3})・
   単一クラス {0},{1} は正確な石数 k∈{0,1,2} と minpos p∈0..17
   (sound H-split: min(x₁,34−x_k)≤17) で分解・multi クラスは直接・
   計82インスタンス (cap 700s・resumable・全インスタンス lex なし)。
   **全 UNSAT ⟹ 4×35 欠損極大不在が確定し M_{4,4}=35 or ≥37**
   (K0821-audit 規約: 36..236 に witness があれば M ≥ 37)・
   **SAT ⟹ witness 帯は m=4..35 に拡大し M ∈ [36, 237]**。
   陽性対照 (4,34,4) class{1}k2p7 は m=34 witness の V∘H 像を含む
   (事前 probe 240s 1,052,475 conflicts 未決着・cap 700s で実行中)。
   census 41,607 曲線は sat3.js (sat.js 全三つ組) と surgery4.js で一致。
4. **(6,4) m=47 rowY=0 は kissat RAM 壁**: sat3 streaming 7r 版で CNF 生成
   成功 (2,701,853 vars / 8,965,702 clauses / 259,412 curves・
   md5 e2c7ab7255893ea4e974a479bd04c8f3) 後、kissat 4.0.4 が SIGKILL/OOM
   (rc=137) で 14.3s で死亡 (sandbox RAM ~2.1GB)
   (six-row-q4-m47-rowY0-oom-20261115)。INDET/OOM であり不在主張ではない。
   **M_{6,4} ∈ [47, 1113] は不変・前線は m=47 のまま**。決着にはメモリ効率
   符号化か外部実行が必要。
