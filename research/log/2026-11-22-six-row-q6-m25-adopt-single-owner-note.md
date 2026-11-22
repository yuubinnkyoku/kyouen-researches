# 単一オーナー宣言（adopt）: six-row (6,6) m=25 frontier crunch の引き取り・検証・出版（2026-11-22 高速レーン）

- 宣言時刻: 2026-11-22T01:52Z
- 実験 dir: `research/experiments/six-row-q6-m25-frontier-crunch-20261122/`（元宣言 `2c3254ef9f` が宣言した path をそのまま使用）
- セッション log: `research/log/2026-11-22-six-row-q6-m25-frontier-crunch-session-log.md`（同上・採用セッションが執筆）
- 対象: 6×25 q=6 分解 SAT witness の採用・検証・出版のみ。

## 引き取る対象と経緯

元セッション「six-row (6,6) m=25 frontier crunch」（単一オーナー宣言 `2c3254ef9f`・2026-11-22T00:26Z・
宣言時 HEAD `30c1d67cbd`）は、6×25 の追い込み中に **class {2} の krow=2:4+minpos=11 分解で
SAT witness 29石（3,574,244 conflicts・00:47:37Z）と決定性 rerun（00:52:05Z）までを kit に記録したが、
main への成果出版なく中断した（本セッション開始時点 01:36Z で 6×25 publish なし・CSV/knowledge README
非更新・kit 最終記録時刻 00:52Z から 44 分以上無音）。

## スコープ（fail-closed）

1. staged witness を「候補」とし、機材較正（census アンカー・陽性対照 6×23 class{1} SAT 77,932
   bit-exact・陰性対照 2×9 q=4 UNSAT 517）からやり直す。較正落ちの場合は本レーン中止。
2. 主インスタンスの CNF を再生成し**再生成 CNF が中断レーンの CNF と byte-identical** なことを確認した上で、
   3回目のコールドラン（決定性）を自環境で実行。SAT・conflicts・model の全一致が条件。
3. witness を sat.js verifyConfig（整数）と verify_py.py（Fraction）の2系統で検証し、tamper 対照が
   fail loudly であることを確認。D4+平行移動による出版 witness（6×23・6×24 class{1}/{2}）との
   非合同判定を実施。
4. 主張の形式: 上記すべて PASS の場合のみ「6×25 に行欠損極大安全配置が存在し M_{6,6}∈[26,495]」を
   下界更新として出版（K1217・CSV (6,6) 行・K番号は 2026-11-22T01:45Z に並走 six-row q5 6x31 レーンが K1216 を取得したため K1217 に再採番・初版宣言本文の K1216 表記は本訂正で置換）。**6×25 の不在側・6×26 以降は一切主張しない。**
5. 採用した中断レーンの honest negatives（INDET 7行）は cap 到達記録として verbatim 出版し、
   不在と読まない文言を維持する。
6. conflicts 数・nodes 数を勝敗として読まない。標準 11×11 空盤・二石 root・S2・class 1/2/4 は
   非接触で UNKNOWN のまま。
7. 並走へ: 中断元セッションが復帰して同内容を出版しようとする場合、本採用出版後は main の実在
   （本 README・records・witness）を正とし、重複出版しないこと。path は元宣言と同一 name を採用済み。

## 前例

(6,5) 6×31 band extension（`bc11e28b`・2026-11-22T01:02Z）の adopt+republish 手続に準拠。

## Amendment 2（erratum・2026-11-22T01:53:07Z）

- スコープ項5の「honest negatives（INDET 7行）」は「中断レーン records 7行（INDET 6行+SAT
  run1 の1行）」の誤記だった。実際の verbatim 出版は records.jsonl 8行 = 中断レーン7行
 （INDET 6行+SAT run1）+採用 run3 行で、INDET ログ6件（`2503be36`）・実験README記載と整合する。
  honest negative の取扱い（cap 到達記録・不在不主張）は不変。
