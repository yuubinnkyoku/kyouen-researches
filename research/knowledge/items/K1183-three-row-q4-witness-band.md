---
id: K1183
title: "3×m・q=4: witness band m=4..23 — M_{3,4} ∈ [24, 69]（m=24,25 は cap下INDET）"
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
  note: "29レコード: 21 SAT (m=4..23・witness 2系統検証 PASS・m=23 は rowY=1+lexH で判定し lexHV 陽性対照で同一 witness 再生・m=4..22 は plain) + 8 INDET プローブ (m=23 plain/lexH/row0-lexH, m=24 plain/row1-lexH/row1-lexHV/row0-lexH, m=25 plain・cap下 conflicts 参考値)"
- path: research/experiments/three-row-q4-frontier-20261121/output/brute_3x4_4.json
  role: data
  note: "m=4..8 完全分類（brute_3x{4..8}_4.json・安全集合全列挙に基づく極大・欠損台帳・第三独立系）"
- path: research/experiments/three-row-q4-frontier-20261121/scripts/verify34.py
  role: verifier
  note: "独立 witness 検証器（K0318 curve_key 幾何・安全/極大/欠損の計数意味論）"
- path: research/experiments/three-row-q4-frontier-20261121/scripts/brute34.py
  role: verifier
  note: "安全集合枝刈り全列挙と極大分類（小盤 m<=8）"
- path: research/log/2026-11-21-three-row-q4-frontier.md
  role: log
  note: "セッション log（census 交差検証・band 構成・row-split による m=23 判定・境界 INDET・verify34.py 初版バグと修正）"
scope: "'有限機械検証 (kissat 4.0.4 linux-amd64 md5 3a5eba830aa6008a604fcc9bbe99a325): 3×m q=4 幅 4..23 の def-mode SAT 判定と witness、幅 4..8 の全数分類、9幅の census 2実装一致。未決幅 24,25 は cap 下 INDET であり一切主張しない。上界 69 は K0024 引用。標準 11×11 空盤等には無関係。'"
evidence: "'SAT 側: 各幅の判定は決定論的 kissat run・witness は 2系統独立検証 (sat.js verifyConfig + verify34.py・20/20 PASS)・m=4..8 では独立全数列挙 (brute34.py) が欠損極大の存在件数まで一致。m=23 は不足行固定 row-split 部分問題 (rowY=1+lex=H・列鏡映は行保存なので分割は健全・SAT は plain 実例の SAT を含意) で判定し、抽出 witness は plain board 上で両検証器を直接通る。census は JS/Python 2実装で 9幅 byte-identical。--lex=H 交差符号化で (3,12,4)/(3,22,4) の SAT を再現。UNSAT 幅はまだ存在しないため UNSAT 側の brute 照合・交差は未実施（witness-free帯の主張なし）。'"
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
2. **m=24, 25 は未決**: m=24 は plain（100s cap・481k conflicts）に加え全
   row-split 分割（rowY=1+lexH 285s・1.16M／rowY=1+lexH,V 285s・1.23M／
   rowY=0+lexH 285s・1.60M）が判定に至らず、m=25 plain は 115s cap
   （507k conflicts）未決。(3,23,4) rowY=0+lexH（外側行欠損の代表・行2は行0と
   V 同型）も 140s cap（1.00M conflicts）未決で、**m ≥ 23 での外側行欠損 witness
   の存在は open**。witness-free 幅は未確定。**M_{3,4} ∈ [24, 69]**
   （Γ の内側は open）。
3. **上界 69 は K0024 の引用値のまま**: K0318 の三つ組・点対充填は q=4 では改善を
   与えない（r = 3 で d1 = C(2,3) = 0・cross_cost = C(2,2) − 1 = 0）。K0318 正本の
   curve_packing_fixed_width.py を実行して U_{3,4} = 69 = min(A,B) を確認
   （整数最適化解 [x=18, y=30]）。閉包掃引の目標幅は 69。
4. **小盤完全分類 (m = 4..8)**: 第三の独立系（枝刈り全列挙）が全極大安全配置を決定。
   m=4,5,6 では全極大が欠損（満容量極大は 0 個）、満容量 (3,3,3) 極大は m=7 で
   初出（64 個）し m=8 で 976 個。最小欠損極大は全幅 5 石。
   kissat の SAT 判定（欠損極大の存在）と全幅で一致。

## 観察（予想として記録・未証明）

- m ≥ 6 の witness が一様に 8 石・(3,3,2) 型であることから、欠損極大は「不足行の
  空点すべてを、残る2行の ≤ 6 石によって張られる円（3行板上 ≤ 6 点・各行 ≤ 2 点）で
  被覆する」パターンに帰着していると観察される。かつて「m=23 が被覆破綻の候補幅」
  という予想を記録していたが、**m=23 witness の発見により反証された**: 被覆パターン
  は幅 23 でも成立する。witness band の終端（のあるなら）は 24 ≤ M ≤ 69 のどこかで、
  外側行欠損系と中央行欠損系で異なる可能性がある（後者は m=23 まで SAT 確認・
  前者は m=22 まで）。
- 証明候補は K0077 型の「円の局所形分類 + 一般計数」（3行板上の 4 点以上円は
  3行への切り方で有限分類可能）あるいは K1177 観察と同型のブロッキング計数。
  q=4 は r=3 の境界形状で K0318 型の被覆計数の項が全て退化するため、
  固定幅 q=4 は packing 定理の力が最も弱い領域である。

## 解釈規約

- 各幅の SAT は実在 witness（2系統検証済み）による存在証明。INDET の 24,25 には
  いかなる存在/非存在主張もしない。M_{3,4} ∈ [24,69] は K0024 上界の引用と
  witness band のみによる区間であって、M の確定値の主張ではない。
- 決定インスタンスの conflicts は pinned kissat の決定論的再現対象。
  INDET の cap 下 conflicts は環境依存の参考値。
- 標準 11×11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま（固定幅 w=3 レーンは標準盤と無関係）。
