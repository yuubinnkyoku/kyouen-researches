---
id: K1183
title: "3×m・q=4: witness band m=4..23・m=24..27 は witness-free（P(24..27)） — M_{3,4} ∈ [24, 69]（m≥28 未掃引）"
kind: proposition
status: computed
topics: [rectangles, maximal-safe, variants]
aliases: []
relations:
- type: depends_on
  target: K0024
  note: "十分長さ T_{3,4} = min(A,B) = 69 が上界 69 を与える（引用値）"
- type: depends_on
  target: K0318
  note: "packing 境界の q=4 での非改善 d1=C(2,3)=0・cross_cost=C(2,2)-1=0・U_{3,4}=69=old_T（正本スクリプトの独立実行で確認・引用値）"
- type: depends_on
  target: K1177
  note: "band-sweep 解釈規約・def-mode 符号化（sat.js md5 0cc6021a…, sat2.js md5 282ae832…・w 代入のみ）・witness 2/3系統検証プロトコル"
- type: generalizes
  target: K0071
  note: "3行固定幅 q≤5 家族（M_{3,5}=12, M_{3,6}=9）の q=4 メンバーの band 確立"
artifacts:
- path: research/experiments/three-row-q4-frontier-20261121/README.md
  role: proof
  note: "主張・band 表・row-split 部分問題の健全性・検証プロトコル・レジューム（単一オーナー宣言 72fdd106 レーン・2026-11-21）"
- path: research/experiments/three-row-q4-frontier-20261121/output/records.jsonl
  role: data
  note: "67レコード: 24 SAT (m=4..23 band〔m=23 は中央行系 wit_3x23_4 と外側行系 wit_3x23_outer_4 の両 witness・2系統検証 PASS〕+ 較正 sat3 kex=2 piece + m=23 (2,3,3) 外側 piece + V鏡像交差 (3,3,2)) + 35 UNSAT (m=24 行和63分割 16 piece〔決定打 (2,3,3) 2,671,271 conflicts〕+ m=23 外側分割 17 piece + 交差符号化 2件) + 8 INDET プローブ (m=23 plain/lexH/row0-lexH, m=24 plain/row1-lexH/row1-lexHV/row0-lexH, m=25 plain・cap下 conflicts 参考値)。全分割ピースは第二環境で conflicts bit-exact 再検証済み"
- path: research/experiments/three-row-q4-frontier-20261121/output/brute_3x4_4.json
  role: data
  note: "m=4..8 完全分類（brute_3x{4..8}_4.json・安全集合全列挙に基づく極大・欠損台帳・第三独立系）"
- path: research/experiments/three-row-q4-frontier-20261121/scripts/verify34.py
  role: verifier
  note: "独立 witness 検証器（K0318 curve_key 幾何・安全/極大/欠損の計数意味論）"
- path: research/experiments/three-row-q4-frontier-20261121/scripts/brute34.py
  role: verifier
  note: "安全集合枝刈り全列挙と極大分類（小盤 m<=8）"
- path: research/experiments/three-row-q4-frontier-20261121/output/partition_closure.json
  role: data
  note: "m=24 63-triple / m=23 外側 48-triple の完全被覆台帳（各 triple を殺す piece と conflicts・pending/uncovered 0・exactly-once）"
- path: research/experiments/three-row-q4-frontier-20261121/scripts/sat3.js
  role: verifier
  note: "row-k 分割 piece 符号器（rowfixed-kex: 不足行の石数を厳密に固定・sat2.js 正本に依存）"
- path: research/experiments/three-row-q4-frontier-20261121/scripts/sat4.js
  role: verifier
  note: "row-sum 分割 piece 符号器（rspec: 3行の石数完全指定・V不変性の機械検査つき）"
- path: research/experiments/three-row-q4-frontier-20261121/scripts/parity_lemmas.py
  role: verifier
  note: "S/X/Y 被覆円パリティ補題（有限剰余証明・machine-complete）+ witness 794円交差検査"
- path: research/experiments/three-row-q4-frontier-20261121/output/wit_3x23_outer_4.witness.json
  role: data
  note: "m=23 外側行欠損 witness (2,3,3)型 8石 rows [2,3,3]・両系統検証 PASS（part4/5 で出版済み・本項目は台帳完結のため再掲）"
- path: research/log/2026-11-21-three-row-q4-frontier.md
  role: log
  note: "セッション log（census 交差検証・band 構成・row-split による m=23 判定・境界 INDET・verify34.py 初版バグと修正）"
- path: research/experiments/three-row-q4-enumeration-20261121/README.md
  role: proof
  note: "独立第二方法（列挙閉包・SAT 非依存）: 63プロファイル完全分割（family 9 / fast 13 / lemma 41）の主張表・検証チェーン・再現手順（単一オーナー宣言 7b5bdfec レーン・2026-11-21）"
- path: research/experiments/three-row-q4-enumeration-20261121/output/crossval_summary.json
  role: data
  note: "列挙閉包検証チェーン総括 (overall PASS): dx34 direct ≡ brute m=4..8 全プロファイル一致・fast ≡ direct m=4..12 mismatch 0・wsearch ≡ brute family 15実行一致・m=23 witness 陽性対照（先行出版 wit_3x23_outer_4 と byte-exact 再発見・2系統検証 PASS）・補題キル ↔ 全数列挙 矛盾 0"
- path: research/experiments/three-row-q4-enumeration-20261121/output/family_sweep_23_27.jsonl
  role: data
  note: "family (3,3,a) 9プロファイル構造完全探索: m=23 陽性対照（witness 再発見）・m=24..27 × Y∈{0,1,2} 全 0 witness"
- path: research/experiments/three-row-q4-enumeration-20261121/output/dx_sweep_24_27.jsonl
  role: data
  note: "fast 13プロファイル（(3,a,b) 置換 + (2,2,2)）: m=24..27 全 count 0（52/52）"
- path: research/experiments/three-row-q4-enumeration-20261121/output/closure_check_13_27.jsonl
  role: data
  note: "crossing-supply 補題による lemma 41プロファイル算術キル台帳（D(m)=Σ(m−rᵢ) > 2·nDef·C(k,3)・m≥22 で41/41・m=4..12 で全数列挙と矛盾 0 を validate）"
- path: research/experiments/three-row-q4-enumeration-20261121/scripts/wsearch34.js
  role: verifier
  note: "family (3,3,a) 円表構造完全探索器（md5 526cf1c3・最終正本 commit 01ac240c）"
- path: research/experiments/three-row-q4-enumeration-20261121/scripts/dx34.js
  role: verifier
  note: "def-mode 列挙器 direct/fast（md5 b02235a9・fast は family・(3,a,b)・(2,2,2) を circle-class 表で厳密処理・selftest m=4..12 で direct == fast）"
scope: "'有限機械検証: (SAT 側・kissat 4.0.4 linux-amd64 md5 3a5eba830aa6008a604fcc9bbe99a325) 3×m q=4 幅 4..23 の def-mode SAT 判定と witness、幅 4..8 の全数分類、9幅の census 2実装一致、m=24 の行和63分割全滅による witness-free 判定（較正1件含む35分割ピースは第二環境 bit-exact 再検証）。(列挙閉包側・SAT 非依存) 63プロファイル完全分割（family 9: wsearch34.js 構造完全探索 / fast 13: dx34.js circle-class 列挙 / lemma 41: crossing-supply 算術キル）で m=24..27 を掃引し全て witness-free: P(25), P(26), P(27) はこちらの方法のみで確定・P(24) は両方法で一致。m≥28 は未掃引であり一切主張しない。上界 69 は K0024 引用。標準 11×11 空盤等には無関係。'"
evidence: "'SAT 側: 各幅の判定は決定論的 kissat run・witness は 2系統独立検証 (sat.js verifyConfig + verify34.py・21/21 PASS〔中央行系20+外側行系1・witness 794円の独立交差検査は parity_lemmas.py で機械確認〕)・m=4..8 では独立全数列挙 (brute34.py) が欠損極大の存在件数まで一致。m=23 は中央行系 row-split と外側行系行和分割の両面で判定。census は JS/Python 2実装で 9幅 byte-identical。UNSAT 側: m=24 の行和63分割 ({0..3}^3 ∖ (3,3,3)) は row-k piece (sat3) 4件 + row-sum piece (sat4) 12件の計16件で exactly-once 被覆 (partition_closure.py 機械検査・pending/uncovered 0) し全 UNSAT・決定打は (2,3,3) rs=2,671,271 conflicts。全35分割ピース+較正1件は第二環境で CNF 再生成・kissat 再実行され conflicts が出版台帳と bit-exact 一致・交差符号化 (m=24 lexH-only 再判定 x2 UNSAT・m=23 V鏡像 rspec (3,3,2) 交差で同一 witness 型再現) で verdict 一致。S/X/Y パリティ補題は有限剰余列挙で機械完証明・被覆円家族 identity は exact-rational 2,124 checks 0 mismatch。列挙閉包側: m=24..27 で fast 52/52 count 0・family 12掃引 0 witness・lemma 41/41 算術キル(m≥22)。検証チェーン (crossval_summary.json overall PASS): dx34 direct ≡ brute34.py m=4..8 全プロファイル一致（def totals 182/674/1724/4607/11542）・fast ≡ direct m=4..12（selftest・mismatch 0）・wsearch34 ≡ brute family 15実行一致・m=23 陽性対照 witness は sat.js verifyConfig + witness_check.py (整数行列式) の2系統 PASS かつ先行出版 wit_3x23_outer_4 と石集合 byte-exact 再発見・補題キル台帳は m=4..12 全数列挙と矛盾 0。'"
---

# 3×m・q=4 行欠損極大 witness band — M_{3,4} ∈ [24, 69]

## 主張

安定化長は M_{w,q} = least m0 such that P(m) for all m >= m0、
P(m) ⟺「3×m の全極大安全配置がちょうど (q−1)·3 = 9 石」（K1177 と同一の定式化）。

1. **witness band m ∈ {4,...,23}**: 各幅で行欠損（ある行 ≤ 2 石）かつ極大な安全配置が
   存在する（def-mode SAT・全幅決着・INDET 0）。witness 石数は m=4: 5・m=5: 6・
   m ≥ 6: 8（= 満容量−1・行型 (3,3,2) の置換）。**M_{3,4} ≥ 24。**
   m=4..22 は plain 符号化の定理的 CNF、**m=23 は不足行固定の row-split 部分問題**
   （--rowY=1・中央行欠損 + --lex=H・行を保存する列鏡映対称性との併用は健全・
   SAT 471,357 conflicts@106.83s）で判定。抽出 witness（8石・rows [3,2,3]）は
   plain board 上で sat.js verifyConfig (ok) + verify34.py (pass) を直接通るため、
   band 主張は witness 自身に立脚し部分問題の意味論には依存しない。
   m=23 の外側行系（行0欠損・(2,3,3)型 8石 rows [2,3,3]・wit_3x23_outer_4）も
   行和分割 sat4 (2,3,3) piece SAT（1,004,683 conflicts）で判定し、witness は
   両系統検証 PASS。**両行系とも m=23 まで witness が存在する。**
2. **m=24..27 は witness-free（P(24), P(25), P(26), P(27)）**: m=24 は行和分割（3行の石数 (a,b,c) ∈ {0..3}^3 ∖
   (3,3,3) の 63 triple を exactly-once に被覆）で掃引した。row-k piece（sat3・
   不足行の石数 k ∈ {0,1} を共有する 4 グループ ×(H,V鏡像)=4件〔rowY=1系2件+隣接
   行约束なしの対角鏡像2件〕…実際の構成は「いずれかの行が石数 ≤ 1」を殺す 4 piece
   ＋「各行 2..3 石かつ 3行和 ≠ 9」を rspec 完全指定で殺す 12 piece の 16 件で
   63 triple を exactly-once 被覆（partition_closure.py 台帳・pending/uncovered 0）。
   全 16 piece が UNSAT（決定打 (2,3,3) 2,671,271 conflicts@476s・V鏡像 (3,3,2)
   も同値）→ m=24 の 3×24 板に行欠損かつ極大な安全配置は存在しないことに加え、
   **SAT に依存しない独立の列挙閉包（第二方法）が m=24..27 全幅を確定した**
   〔three-row-q4-enumeration-20261121〕: 安全配置の各行各石数 ≤ 3（水平禁止曲線）より
   欠損極大の行プロファイルは (r0,r1,r2) ∈ {0..3}³ ∖ {(3,3,3)} の 63 通り、これを
   family（9: 2行満杯・残る行 a ∈ {0,1,2}・wsearch34.js 円表構造完全探索）/
   fast（13: (3,a,b) 置換 12 + (2,2,2)・dx34.js fast circle-class 列挙）/
   lemma（41: 石数和 k ≤ 5・crossing-supply 補題 D(m) > 2·nDef·C(k,3) の算術キル・
   m ≥ 22 で41/41）に exactly-once 分割し、m=24..27 で family・fast とも全 0
   （family: 12掃引全 0 witness・fast: 52/52 count 0）。よって
   **witness band（欠損極大の存在幅）はちょうど {4,...,23} で終端**し、
   P(24) は SAT 分割と列挙閉包の 2 方法で一致、P(25), P(26), P(27) は
   列挙閉包単独で確定（新規）。
   ただし P は単調でない（m=27 witness-free でも m≥28 での witness 復活は否定
   されない）。**M_{3,4} ∈ [24, 69]（不変）**: M=24 ⟺ P(m) が m ≥ 28 でもすべて
   成立、残る不確定幅は 28..68 の 41 幅の掃引である。
3. **上界 69 は K0024 の引用値のまま**: K0318 の三つ組・点対充填は q=4 では改善を
   与えない（r = 3 で d1 = C(2,3) = 0・cross_cost = C(2,2) − 1 = 0）。K0318 正本の
   curve_packing_fixed_width.py を実行して U_{3,4} = 69 = min(A,B) を確認
   （整数最適化解 [x=18, y=30]）。閉包掃引の目標幅は 69。
4. **小盤完全分類 (m = 4..8)**: 第三の独立系（枝刈り全列挙）が全極大安全配置を決定。
   m=4,5,6 では全極大が欠損（満容量極大は 0 個）、満容量 (3,3,3) 極大は m=7 で
   初出（64 個）し m=8 で 976 個。最小欠損極大は全幅 5 石。
   kissat の SAT 判定（欠損極大の存在）と全幅で一致。

## 観察（予想として記録・未証明）

- m ≥ 6 の witness が一様に 8 石・(3,3,2)/(2,3,3) 型であることから、欠損極大は
  「不足行の空点すべてを、残る2行の ≤ 6 石によって張られる円（3行板上 ≤ 6 点・各行
  ≤ 2 点）で被覆する」パターンに帰着していると観察される。かつて「m=23 が被覆破綻の
  候補幅」という予想を記録していたが m=23 witness（中央行系・外側行系とも）により
  反証され、**m=24 の行和分割全滅により被覆破綻はちょうど幅 24 で初めて成立する**
  ことが機械証明された。決定打が (2,3,3)（外側行欠損型）であることから、
  バンド終端は中央行系より外側行系で先に来る: 中央行欠損系の m=24 掃引は
  rowY=1+lexH piece（1.16M conflicts cap下）が未決で、外側行系が先に尽きた形。
  幅 25..27 は列挙閉包で witness-free・28 以降での witness 復活の有無は open。
- 証明候補は K0077 型の「円の局所形分類 + 一般計数」（3行板上の 4 点以上円は
  3行への切り方で有限分類可能）あるいは K1177 観察と同型のブロッキング計数。
  q=4 は r=3 の境界形状で K0318 型の被覆計数の項が全て退化するため、
  固定幅 q=4 は packing 定理の力が最も弱い領域である。

## 解釈規約

- 各幅の SAT は実在 witness（2系統検証済み）による存在証明。m=24 の witness-free
  （P(24)）は 63 分割 piece の全 UNSAT + exactly-once 被覆台帳による有限機械証明
  （witness が無いので witness 検証方式ではなく台帳検査方式）。m=25..27 の
  witness-free（P(25), P(26), P(27)）は SAT 非依存の列挙閉包（63プロファイル完了分割・
  同じく witness が無いので検証は検証チェーン一致・陽性対照・全数列挙交差による）。
  m ≥ 28 にはいかなる存在/非存在主張もしない（未掃引）。M_{3,4} ∈ [24,69] は
  K0024 上界の引用と witness band + P(24..27) による区間であって、M の確定値の
  主張ではない。
- 決定インスタンスの conflicts は pinned kissat の決定論的再現対象。
  INDET の cap 下 conflicts は環境依存の参考値。
- 標準 11×11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま（固定幅 w=3 レーンは標準盤と無関係）。
