# 2026-11-22 偶数y統一テンプレート機械検証（fast lane 作業 log）

## 経緯

y=16 fit 出版（K1237、本日 21:29Z）の後、cand16 = cand14 の Y+2 機械翻訳という
主張を偶数 y 全系列に一般化して検証した: cand14 fit コード本体は Y 定数 1 行以外に
y 依存リテラルを含まないため、「Y 代入のみで偶数 y = 10, 12, 16 の全出版表を再生
できるか」が自然な次の問いだった。宣言ノート（単一オーナー・先行出版、
commit e083ac28）の後に実験 dir（commit d0100259）を出版した。

## 使用入力（全て repo 内・audit に SHA-256 pin）

- cand10/cand12/cand14/cand16 fit、verify_y10/y12/y13/y14/y15_universal.py

## 結果（全て PASS、検証器 1 実行 0.6 秒）

1. **grids 6 掃引 401,814 点 bad 0**
   - uni(10) vs cand10 fit 80,600 / proved 143,664
   - uni(12) vs cand12 fit 76,539 / proved 41,184
   - uni(14) vs cand14 proved 29,877
   - uni(16) vs cand16 fit 30,150
2. **行 census 12 本 640 行 bad 0**（off ≤ 160、[120,160] 尻尾定数性も検証）
3. **y=10 出版明示表の表現分類**: 43 行中 26 行 (k,th) 定数同一、15 行 alias
 （z-even I 行 10 行 + z-odd 対角 d=-10 と pin d=-6,-2,2,6）、2 行定型。
   alias は Lemma L1（b_{k+1} ∪ I[2k+2) = b_k ∪ I[2k+1)、証明つき）で
   全 offset 集合同一 → y=10 の同一性は全パラメータで成立。
4. **y=12**: 定数の数値同一（(d+38)//4 = (d+3·12+2)//4 等）。
5. **y=16**: 正規化差分完全一致（残差はローカル変数名 b14/b16 のみ）。
   → 偶数 y 4 族は単一コード系に固定。
6. **奇数 y 陰性対照**: y=13/y=15 の全称証明済み表とは不一致
 （T 差分行 2 行ずつ・P 差分行 54/62 行・box 不一致 2,649/1,660 点・
 最初の不一致 (2,13,28)/(4,15,32) で proved 0 vs テンプレート 1）。
   テンプレートは偶数 y 特化。odd-y 表は K1231/K1235 レーンの証明のまま。

## 誠実記録

- 検証のローカル実行が宣言ノート出版に先行した（宣言ノートに明記）。
- fit 版と proved 版（verify_y10 組込み）の差はコメント 1 件のみで コード行は意味同一（unified diff で確認）。
- 本検証は一致の検証であり、閉形式自体の正しさ（特に y=16 observed）を証明しない。

## 次候補（後続 run へ）

- y=16 全称 verify_y16_universal.py（統一テンプレート実装で記述可能・別宣言必須）。
  A子/B子/C子・clip 窓 2y+2=34・census z=0..79 は K1237・y16 fit log に記載済み。
- 横断法則の一般補題化（K1235 part 2 系）は本結果を前提データとして使用できる。

## 成果物

- [実験 report](../experiments/even-y-two-token-unified-template-check-20261122/report.md)・
  [検証器](../experiments/even-y-two-token-unified-template-check-20261122/scripts/check_even_y_unified.py)・
  [audit.json](../experiments/even-y-two-token-unified-template-check-20261122/output/audit.json)・
  [check-run.txt](../experiments/even-y-two-token-unified-template-check-20261122/output/check-run.txt)・
  [宣言ノート](2026-11-22-even-y-unified-template-single-owner-note.md)・
  K item: [K1238](../knowledge/items/K1238-two-token-even-y-unified-template-check.md)
