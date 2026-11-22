# K1238: 偶数y (10..16) two-token 統一テンプレート機械検証

- **kind**: proposition（機械検証＋補題 L1 は証明つき）
- **status**: observed（機械検証された同一性の主張。閉形式自体の正しさは含まない）
- **系**: two-token vertical-fiber 族（K1141/K1152/K1233/K1234/K1237 の後方検証）

## 主張

cand14 fit コード本体（`vertical-fiber-two-token-y14-parametric-allz-fit-20261122/cand14.py`、
module docstring 〜 `def main()`）は `Y = 14` の 1 行を除き y 依存リテラルを含まない。
これの Y 代入（名前は in_T14→in_TY 等の機械置換のみ）で得られる単一テンプレート uni(Y) は、

- **uni(10) = 出版 cand10（fit 版・全称 verifier 組込み proved 版の両方）**,
- **uni(12) = 出版 cand12（fit 版・全称 proved 版の両方）**,
- **uni(14) = 全称 proved cand14**,
- **uni(16) = 出版 cand16（fit 版）**

と一致する（grid 401,814 点 bad 0、行 census 640 行 bad 0、merge 領域本文一致、
実行 0.6 秒・audit に入力 SHA-256 pin）。偶数 y の 4 全族は単一の Y パラメトリック
コードで再生される。奇数 y = 13, 15 の全称証明済み表とは**一致しない**（陰性対照:
T 差分行 2、P 差分行 54/62、小 box 不一致 2,649/1,660 点、最初の不一致 (2,13,28)/(4,15,32)
で proved が 0・テンプレートが 1）。テンプレートは偶数 y 特化。

## 構造（一致の根拠・行分類で全能动的に確定)

- **Lemma L1（証明つき）**: 任意の k ≥ 0 で b_{k+1} ∪ I[2k+2) = b_k ∪ I[2k+1)
 （b_k = 奇数 offset 1..2k−1、I[t) = offset ≥ t）。両辺とも [1,∞) から偶数
 {2,4,…,2k} を除いた集合。
- **y=10 出版明示表（43 行）**: 26 行は (k,th) 定数同一、15 行（z-even I 行 10 行 +
  z-odd 対角・pin 行 5 行）は alias（pub (k+1,2k+2) vs テンプレート (k,2k+1)）で
  L1により全 offset 集合同一、2 行は定型（z-even 対角 False、z-odd sweep = b_Y）。
- **y=12**: formula 形式そのままで定数が数値同一（(d+38)//4 = (d+3Y+2)//4 等、
  d = −12..12 で assert）。
- **y=14**: テンプレートの由来（fit = main = proved 組込み）。
- **y=16**: コード本体の正規化差分（コメント除去・名前正規化後）完全一致
 （残差はローカル変数名 b14/b16 のみ）。Y+2 翻訳の純正性。
- よって4族の同一性は全パラメータで成立（grid の有限性は本質的制約でない）。

## 限界と帰属

- 本項は「出版表が単一コードで再生できる」ことの検証であり、4 閉形式自体の
  正しさの証明ではない。y=10/12/14 全称は各レーンの成果、y=16 は observed
 （K1237・probe 899 行 74,741 点一致のみ）。
- L1 は自明な集合恒等式だが、y=10 表の機械再生に実際に必要な構成要素である。
- 横断法則の一般補題化（K1235 part 2 系）は本結果を前提データとして使用できる。

## 成果物

- 実験: [check report](../experiments/even-y-two-token-unified-template-check-20261122/report.md)・
  [検証器](../experiments/even-y-two-token-unified-template-check-20261122/scripts/check_even_y_unified.py)・
  [実行記録](../experiments/even-y-two-token-unified-template-check-20261122/output/check-run.txt)・
  [audit](../experiments/even-y-two-token-unified-template-check-20261122/output/audit.json)
- log: [作業log](../log/2026-11-22-even-y-unified-template-check.md)・
  [宣言ノート（単一オーナー・先行出版）](../log/2026-11-22-even-y-unified-template-single-owner-note.md)
- 関係: K1141（y=10 全称）・K1152（y=12）・K1233/K1234（y=14 fit/全称）・
  K1237（y=16 fit）・K1231/K1235（y=13/y=15 全称・陰性対照側）

（2026-11-22・fast lane）
