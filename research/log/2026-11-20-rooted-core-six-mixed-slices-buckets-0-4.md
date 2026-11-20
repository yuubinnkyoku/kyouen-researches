# 2026-11-20 rooted-core 6点mixedスライス: j=0..4 全長認証と環境障害からの再構成

[K0684](../knowledge/items/K0684-fixed-core-path-period-thirty-four-conjecture.md) の
mixedレーン（[単一オーナー宣言](2026-11-20-rooted-core-six-mixed-slices-single-owner-note.md)参照）。

## 経緯

1. 宣言後に bucket機械（35ビット列挙・Burnside軌道型・単状態正確再帰・有限窓認証・
   生subset照合）を構築し、j=0..5を認証、j=6を拡張パスまで実行した。
2. 13:20Z頃、実行環境がリセットされ、未出版の機械・進捗・証明書がすべて失われた
   （同時刻帯に他レーンm22も「execution-environment outage」として同種の
   障害を記録している: HEAD 13:12Z の「log execution-environment outage」コミットbb869188）。
   出版済みだったのは宣言ノートのみ。
3. `rooted-core-tail-periodicity-20261107` から `engine.py`・`proof.md`・`verify.py`・
   `output/audit.json`（513型基礎表）をbyte-exactに再取得し、機械をスクラッチ再構築した。
4. 再構築実装が失われた実行の認証済み数値をすべて再現したことを確認してから出版した:
   - j=0: 544型・joint 500・max 22
   - j=1: 81,900ラベル/1,018型・joint 500・max 24
   - j=2: 143,170/1,663型・joint 500・max 33
   - j=3: 213,900/2,336型・joint 500・max 30
   - j=4: 286,755/3,045型・joint 571・max 33・証人 `(6,[3,13,22,28,49])`
   - （j=5の実行中資産も失われたが再実行して別途出版する）
   再現は「独立に書かれた2実装が同じ完全族で同じ値を返す」交叉検証として機能している。
5. j=0は隔離cwd再実行でrecords byte-identicalを確認（SHA-256 `c207ce11…`）。

## 成果

- **j=0（6点・純二点辺＝全グラフ544型）で6点純二点辺核は全て証明済み**
  （開始500・Grundy最大22・最小末尾周期全型ちょうど34）。6点の両極端（純二点辺・
  純三点辺10,688型）の両方が認証済みになった。
- j=1..4により「三点辺ちょうど1..4本＋非空両立二点辺」の完全族も全長認証。
  現時点で、6点核のうち未認証は「三点辺5本以上かつ二点辺1本以上」だけ。
- j=4で初めてjoint開始が500を破り571。先行の純三点辺≤6本族732型の開始571と
  同一上限が出現（mixedで開始が大きくなる構造のヒント）。

## 記録形状

証明書は各bucketの `output/bucket_j{J}_head.json`（認証ヘッダ）と
`output/bucket_j{J}_witnesses.json`（結合状態とworst証人の全0..必要値prefix）。
全型records（j=0..4で計31MB）は実行経路上のサイズ制約でrepo未格納とし、
SHA-256 pinと決定的再現（`run_bucket.py`の隔離cwd再実行・j=0でbyte-identical実測）で担保する。
j=5..20は続きとして宣言の下で次回実行が再開する。
