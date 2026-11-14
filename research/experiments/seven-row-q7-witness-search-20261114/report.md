# 7×m q=7 行欠損witness探索 — 新ファミリー (7,7)（q=w 対角）のwitness 7×7..7×25 と M_{7,7} ≥ 26

日付: 2026-11-14（高速レーン第9回・第2バッチ）

## 主張

1. **(7,7)（7×m・q=7・q点共円/共線禁止・q=w の対角ファミリー）**: 行欠損の極大安全配置
   （満容量 42 = 7·(q−1) 石に対しある行 ≤ 5 石）が **m=7..25 の全幅で存在する**。
   本ファミリーは CSV・knowledge のいずれにも未記載で、これが最初の結果である。
   - m=7..14 は深欠損（30, 32, 34, 37, 38, 39, 40, 41 石・deficiency 12..1）。
     m=10..14 は上位6行が6石・最下段のみ 1..5 石という構造的な系列。
   - m=15..25 はすべて単一欠損の **41石**（行パターンは 5 が1行のみ・6が6行）。
   - すべて census 不使用 sat.js verifyConfig と Python Fraction 独立実装の
     **2系統検証で safe+maximal+行欠損 PASS**。
   - よって witness 幅集合は {7..25} を含み、**M_{7,7} ≥ 26**
     （上界は K0318 曲線パッキング代入 U_{7,7}=708・`seven-row-inband-families-20261114/output/w7_upper_bounds.json`・
     M ∈ [26, 708]）。
2. **m=25 の解法（方法論の再確認）**: def 単一節（OR）符号化は 240s cap で INDET
   （conflicts 2,478,476）だったが、**rowY 行固定分解**（V 対称で 4 クラス
   y=0..3）の **rowY=3（中央行）で SAT**（756,785 conflicts・200s cap 内）。
   他 3 クラスは 200s cap で INDET（961,944 / 970,708 / 1,130,645 conflicts・
   正直な負記録・不在の主張ではない）。
   (7,8) m=24 と同様、**行固定分解が OR 実例の壁を突破する**ことが q=7 でも成立。
3. **witness 探索の前線は 7×26**。m=25 の witness は 41 石 rows 6,6,6,5,6,6,6
   （rowY=3 分解で発見）。

## 結果一覧（def-search）

| m | 石数 | 行パターン | kissat conflicts | 判定 |
|---|------|-----------|-----------------|------|
| 7 | 30 | 6/6/6/3/5/3/1 | 0 | SAT |
| 8 | 32 | 6/6/6/4/5/4/1 | 0 | SAT |
| 9 | 34 | 6/6/6/5/6/5/0 | 0 | SAT |
| 10 | 37 | 6/6/6/6/6/6/1 | 0 | SAT |
| 11 | 38 | 6/6/6/6/6/6/2 | 0 | SAT |
| 12 | 39 | 6/6/6/6/6/6/3 | 0 | SAT |
| 13 | 40 | 6/6/6/6/6/6/4 | 0 | SAT |
| 14 | 41 | 6/6/6/6/6/6/5 | 0 | SAT |
| 15..24 | 41 | 単一欠損（5が1行） | 62 .. 2,105,329 | SAT |
| 25 | — | — | 2,478,476（240s cap） | INDET |

m=25 は `../output/row-split/` の行固定分解で SAT（rowY=3・756,785 conflicts・
41石 witness rows 6,6,6,5,6,6,6）。

## 手法と検証

- 符号化: `seven-row-inband-families-20261114/scripts/sat2.js`（K0810 census +
  sequential counter + 極大性）を verbatim。q=7 = w のため genfast.js
  （半整数中心census・q ≥ w+1 が適用条件）は**不適用**であり、sat2.js の
  全三つ組census（n = 7m ≤ 175 で実用）をそのまま使用。
  def 単一節 ∨¬rowGe[y] は「総石数 < 42 ⟺ ある行 ≤ 5」の完全符号化
  （全行 ≤ 6 は列方向の共線禁止とは独立に census の行曲線カウンタで強制される）。
- ソルバ: kissat 4.0.4 公式 linux-amd64 バイナリ（変更なし・240s cap、
  行固定分解は 200s cap）。
- 検証: 全 witness は decode_verify.js（census 不使用 sat.js verifyConfig）と
  verify_witness.py（Python Fraction・整数厳密・独立実装）の **2系統検証**で
  safe + maximal + 行欠損 PASS。
- **決定性較正**: m=24 def OR 実例の再実行で conflicts **2,105,329 が bit-exact 再現**
  （`output/w7q7-determinism-check/` は未push・レコードのみ本 report に記載）。
  sat2.js/q=7 の CNF は前回実験（seven-row-q8-witness-search-20261114）で
  cross-reset bit-exact 検証済みの同一コードから生成。
- 機械的な整合: m=7..14 の witness は行6石が上位6行に現れる構造で、
  行方向の容量上限 6（q−1）と整合。census の行曲線カウンタは
  m ≥ q = 7 を要求し、実際に m=7 が最小探索幅である。

## 正直な負記録

- m=25 def OR: 240s cap INDET（2,478,476 conflicts）。
- m=25 rowY=0/1/2: 200s cap INDET（961,944 / 970,708 / 1,130,645 conflicts）。
  witness が見つかったのは rowY=3 クラスのみで、他クラスの不在は主張しない。
- m=26 以降は未走査。sat2.js の全三つ組censusは n=7m について O(n³) で
  m=26..28 までが実用範囲の目安。

## 範囲と限界

有限機械検証（census 完全性とソルバ正確性まで）。数論的証明ではない。
M_{7,7} の確定には 7×26 以降の評価と上界 708 の改善（K0342 型 tail 評価）が残る。
q=w の対角ファミリーで単一欠損witness帯が m=15..25 で続く観測は
(7,8)（m=13..24）と同型であり、行固定分解の有効性とも合わせて
7行族の一般傾向として記録する。

## 備考

K番号は作業時点での仮番号（AGENTS.md の再採番規則による）。
実行環境は 2026-11-14 高速レーン第9回と同一（kissat 4.0.4 公式バイナリ）。

---

## 第3バッチ（並走レーン・m=26 witness）

日付: 2026-11-14（高速レーン・並走独立run）

同一実験ディレクトリで並走した独立runによる追加バッチ。符号化・ソルバ・
検証プロトコルは第1・2バッチと同一（sat2.js verbatim・kissat 4.0.4 公式
linux-amd64 バイナリ・2系統検証）。

1. **m=26 行欠損witness**: rowY=3（中央行）固定分解で **SAT
   （1,951,966 conflicts・約233s）**。41石 witness rows 6,6,6,5,6,6,6・
   2系統検証 PASS（`output/w7q7_7x26q7_rowY3.witness.json`・
   raw log `output/w7q7_7x26q7_rowY3.kissat.txt`・レコードは
   `output/results.jsonl` の m=26 エントリ）。
   → witness 幅集合は {7..26} を含み **M_{7,7} ≥ 27**（M ∈ [27, 708]）・
   **witness 探索の前線は 7×27**。
2. **並走独立再現（決定性の追証）**: 本runは共有実例で第2バッチと
   conflicts が bit-exact 一致（m=24 def OR: 2,105,329・
   m=25 rowY=3: 756,785）。別runによる再現であり、決定性較正の
   「単一run内再実行」を補う独立再現の傍証となる。
3. **正直な負記録**: m=27 rowY=3 は 262s cap で INDET
   （2,242,940 conflicts・不在の主張ではない）。

