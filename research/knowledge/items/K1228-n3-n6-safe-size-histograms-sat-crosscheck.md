---
id: K1228
title: 3×3〜6×6の安全局面サイズ分布の三系統再導出とSATによるK_n行の独立確定
kind: verification
status: verified
topics: [maximum-safe, verification]
aliases:
- safe subset size histograms n3-n6
- Z coefficient rederivation n3-n6
relations:
- type: verifies
  target: K0004
  note: 安全集合総数298/5,811/151,394/5,081,289と最大石数での自然終了をサイズ別再導出で検査
- type: verifies
  target: K0029
  note: K_3..K_6=5/7/9/11をexactly-k SAT（K_n行の充足全列挙とK_n+1行のUNSAT）でDFSと独立に検査
- type: extends
  target: K1225
  note: 極大行全77行に対する安全側の補完（safe対maximalの行比較・n3を含む全367,440配置の幾何検査・K1225検証のn3非収録分）
- type: related
  target: K0226
  note: 本文引用の5×5サイズ別安全状態数1,25,300,2300,11824,37272,59192,35208,5172,100との一致
- type: depends_on
  target: K0057
  note: 禁止四点組カタログのアンカー（F_3=14を新規記録・F_4/F_5/F_6は既刊sha一致）
- type: depends_on
  target: K1224
  note: 列挙・SAT機材（enum_catalog/enc_sat2/sat_enum系）のbyte同一再利用
artifacts:
- path: research/experiments/n3-n6-safe-histograms-sat-crosscheck-20261122/README.md
  role: source
  note: 主張・方法・検証行列・trust boundary・刊行/非刊行の区切りの正本
- path: research/experiments/n3-n6-safe-histograms-sat-crosscheck-20261122/output/safehist_n3_n6.jsonl
  role: data
  note: 3系統一致の安全集合サイズ別ヒストグラム（Z_n係数）
- path: research/experiments/n3-n6-safe-histograms-sat-crosscheck-20261122/output/safe_count_n6_k12.json
  role: verification
  note: 6×6安全12石集合の非存在（exactly-k SAT・UNSAT）
- path: research/experiments/n3-n6-safe-histograms-sat-crosscheck-20261122/output/spectrum_summary.json
  role: verification
  note: master collation（全77行2走行決定性・全367,440配置幾何検証・軌道センサス・SATゲートの統合）
- path: research/experiments/n3-n6-safe-histograms-sat-crosscheck-20261122/MANIFEST-sha256.txt
  role: manifest
  note: 刊行物sha256・外部機材指紋・非刊行raw指紋の正本
---

# 3×3〜6×6の安全局面サイズ分布の三系統再導出とSATによるK_n行の独立確定

標準共円盤（q=4）の3×3〜6×6について、安全集合（禁止四点組を1つも含まない石集合、極大でない
ものも含む）のサイズ別個数（Z_n係数）を、相互に独立な3系統の実装（pinned Node DFSの2走行・
独立Python DFS・2^N全走査）で再導出し、exactly-k SAT（Sinz双方向カウンタ＋公式kissat 4.0.4）
で行の値とtailの消滅を独立確定した。いずれも既刊値の検査であり、新しい数値の主張ではない。

## 検査対象と結果

1. **Z_n係数の一致**: n3..n6の全33係数が
   (a) 3実装系統の完全一致、(b) archived監査コーパス（original-claims round4_b228d の
   Z_n(lam)係数）との全桁一致、(c) K0004の安全集合総数（298/5,811/151,394/5,081,289）との
   総数一致、(d) K0226本文の5×5引用値との一致。
2. **K_nのSAT単独確定**: exactly-k SATの全列挙がk=K_n行で56/64/100/464（K0030・K1225の
   極大行と一致）、k=K_n+1（3×3の6・4×4の8・5×5の10・6×6の12）でUNSAT。
   併せてK_3..K_6=5/7/9/11がDFSに依存せずSATのみから確定し、K0029の既刊値と一致。
   SAT符号化の健全性は3×3 k=1..7・4×4 k=4..8を2^N全走査ヒストグラムに対して較正済み。
3. **最大サイズ行の自動極大性（補題の機械確認）**: 最大サイズの安全集合は包含極大である
   （真拡大が安全ならば最大性に矛盾する自明な補題）。k=K_n行でSATのsafe全列挙個数が
   極大行の個数と一致する機械確認として現れる。中間行ではsafe個数がmaximal個数を上回る
   （例: 6×6 k=10はsafe 35,316対maximal 30,492）。
4. **s_5/s_6下側の再導出**: pinned enc_sat2 v2.1（安全+極大+lex-leader）で5×5 at-most-4・
   6×6 at-most-5がUNSATであり、s_5≥5・s_6≥6の下側をDFSと独立に再導出（値更新なし）。
5. **極大側の補完検査**: K0030全cell・全77行の2走行決定性、全367,440配置
   （K1225の幾何検証範囲外だった3×3の56配置を含む）のLeibniz幾何検証、D4軌道センサス
   （軌道数・安定化群、K1225出版値と完全一致）。

## 限界

- 有限計算であり形式証明ではない。実装を言うtrustを含む（K1224/K1225と同水準）。
- Z_n係数はarchived corpus既出データの再検査であり、本項は検査結果の記録。F_3=14
  （3×3禁止四点組数）のみが新規記録値。
- K0030/K0004/K0029/K0026の値は一切更新しない。n=2のZ係数の再検査・n7 k≥8・n8の安全行
  サイズ別分布・n≥9盤面は未着手。2n+1という形の一致（n=2..6）は観察として記録し外挿しない。
- 標準11×11空盤・二石root・S2・closure classは非接触（UNKNOWN）。
