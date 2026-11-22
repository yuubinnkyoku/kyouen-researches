# K1226/K1224 出版カタログの TS 第三系統再監査(2026-11-22)

## 位置づけ

K1226(7x7 k=8 bounded census 331 leader・7x7/8x8 witness)と K1224(7x7 k=7 カタログ
16配置・2軌道)の出版成果を、既存の2系統(Node/Python 実機材)から独立な
**第三系統**で再検証した。新規の数学的主張は一つもない(再検証実験)。

この再監査は、実行環境の node/python・bash が失効した期間に、純TS計算と
github_app 入力だけで完結する作業として設計・実行した
(n7 k>=8 full-census レーンのセッションログ research/log/2026-11-22-n7-rows-k8plus-dfs-session-log-1.md 参照)。

## 方法

- 禁止四点組: det[[x^2+y^2,x,y,1]x4]=0(共円・三点同一視)を Leibniz 展開・整数演算で
  全 C(n^2,4) 組を直接判定。出版 Fraction 行列式と同規約の独立実装
  (n<=8 では全中間値が 2^53 未満のため Number 演算で厳密)。
- SAFE: k石の全 C(k,4) サブセットが禁止組を含まない。
- MAXIMAL: 全空点が blocked(空点 c + 既存3点の禁止quadが存在)。uncovered は非blocked空点数。
- 軌道: 反射・90度回転を生成子とする位数8の D4 閉包を機械生成し、
  osize/stab/indicator(0<1 辞書式)lex-min を計算。
- trips = 三点共線3組数、dirs = その方向数(gcd正規化・向き忘却)。
- 入力は8ファイルすべて git blob SHA でピン(output/reaudit_summary.json の inputPins 参照)。
  取得時 main HEAD: 95a119851acf6d649bdbde1574ea73d698c164ef。

## 結果(全照合一致・verdict ALL-MATCH)

1. **F アンカー**: F_3..F_8 = 14/194/826/2491/6364/14564。
   F_5..F_7 は既存出版アンカー、F_8=14564 は n8k9 determinism.json の
   encoding.F に一致(F_8はdeterminism出版と同じ値のため新規性なし)、F_3/F_4 は出版較正値と一致。
2. **census 331 leader**: 331/331 SAFE+MAXIMAL・331/331 indicator-lex-min・
   軌道重複0・閉包総数2644。osize {8:330,4:1}・stab {1:330,2:1}・
   trips {0:2,1:34,2:119,3:131,4:36,5:8,6:1}・dirs {0:2,1:40,2:126,3:123,4:36,5:3,6:1}
   はいずれも出版 verify_census8_partial.json と一致。
   **per_leader 331件の {safe,maximal,nViol,nUnc,lexmin,dup,osize,stab,trips,dirs}
   全項目で不一致0件**(summary一致のみでなく全leader照合)。
   trips=0 の2軌道 [10,12,15,20,25,27,42,45]/[10,12,14,23,39,40,45,46] と
   stab=2 の [3,6,14,19,29,34,42,45] も出版 K1226 記述と一致。
3. **n7 witness + tamper**: [17,19,22,26,27,28,30,31] SAFE+MAXIMAL。
   1石除去8通りは全て SAFE かつ NOT-MAXIMAL、uncovered [5,9,13,7,9,3,10,10] は
   出版 tamper_k8_summary.json と完全一致(たまたま一致ではなく全要素一致)。
4. **n8 witness + tamper**: shot1/shot2 とも SAFE+MAXIMAL・互いに非合同。
   trips/dirs は shot1 (3,2)・shot2 (5,4) で determinism.json 出版値と一致。
   shot1 tamper uncovered [4,8,15,10,10,12,10,18,10] は出版 tamper_n8k9_summary.json と
   完全一致。shot2 tamper uncovered [4,7,6,4,7,10,9,6,4] は出版対照なし
   (determinism は shot1 のみ記載)のため**本実験の新規データ**として記録
   (出版主張「全 SAFE かつ NOT-MAXIMAL」と整合)。
5. **K1224 カタログ**: 16配置全 SAFE+MAXIMAL・trips {2:8,3:8}・dirs {2:8,3:8}・
   D4閉包はちょうど2軌道(全16配置を被覆)で出版 orbit_details の
   members と完全一致。石リスト辞書式代表 [1,9,22,23,27,44,45]/[3,10,22,23,30,32,38]
   および SAT規約代表 [10,13,14,17,19,21,45]/[18,21,22,26,31,32,38] も一致。

## 判別力(陰性対照)

- コンパクション前の実行で、n8 用反射 (x,7-y) を n7 に誤適用したビルドが
  軌道ゲート不合格(像の盤外化・closure退化)となり、出版値との不一致で検出された。
  誤結果は不採用・修正再実行で合格。本実験では同型の誤写像を意図的に適用して
  盤外像(49..55)と退化closure(2集合)で必ず不合格になることを再確認した。
- F アンカー一致(6盤面)と per_leader 331件照合は既知値照合による陽性対照。

## 決定性・trust boundary

- 純TS・乱数不使用・時刻非依存の決定的アルゴリズム。コア監査は本セッションで
  3回独立実行(コンパクション前2回・後1回)ですべて同一結果。
- run_typescript sandbox は Node ではなくファイルI/O・時計を持たない
  (入力は github_app.get_file_contents)。実行3本を統合した正本:
  scripts/reaudit_k1226_k1224.ts。

## 非主張

- census 完全性は不主張のまま(7x7 8石行の軌道数は >=331 のみ。完全性は
  n7 k>=8 full-census レーンの仕事)。M_7/M_8 の上界は扱わない。
  8x8 k=9 census も未実施のまま。
- 本実験は有限再検証であり形式証明ではない。K1224/K1226 の本文変更も行わない。
