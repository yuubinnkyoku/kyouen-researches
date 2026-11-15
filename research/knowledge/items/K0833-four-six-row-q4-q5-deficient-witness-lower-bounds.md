---
id: K0833
title: "4〜6行 q=4,5 行欠損witness帯 — (4,4) m=4..34, (5,4) m=5..39, (6,4) m=6..40, (4,5) m=5..20, (5,5) m=5..23 全幅SAT; M_{4,4}>=35, M_{5,4}>=40, M_{6,4}>=41, M_{4,5}>=21, M_{5,5}>=24; sat3 OOM壁越えと rowY 分割で帯延伸"
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
  note: "26 records m=6..31 all SAT dual-verified: m=23以降単一欠損17石, m=31 4.1s/131 conflicts, 全インスタンス <7s; m>=32 census OOM"
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
   m≥32 census OOM。
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
## 追記 (2026-11-15 band-extension レーン: sat3 OOM壁越えと rowY 分割)

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
