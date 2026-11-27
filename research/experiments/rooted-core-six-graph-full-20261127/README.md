# 6頂点グラフ核全型（純二点辺clutter全体）の全長周期認証

実験日: 2026-11-27。レーン: 高速レーン（K0684系列）。
単一オーナー: 本 session。official run は出版後に確定した post-hoc 実行であることを開示する
（出版前対抗probe・宣言の形式を取らず、本READMEとlogに実行順を正直に記録する。
研究内容的には新規の計測であり、既存のどの出版監査とも重複しない族を対象とする）。

## 命題（有限・完全）

6頂点 {0..5} 上の純二点辺clutter（= 根0付き単純グラフ）の**全体**について、
2^15 = 32768 raw 入力は根付き同型でちょうど **544型** であり
（Burnside軌道数計算・orbit-stabilizer被覆の二重導出で確認）、
どの型 C に長さ L の二点禁止道を付けても

```
f_C(L+34) = f_C(L)   for all L >= 500
```

が成立する。共同開始 500（最悪状態の最終周期破綻は L=499）・必要値 1069・
`jointly_certified=true`。K0682の有限窓定理（N=max(500,最終破綻+1), T=34,
必要値 2N+69, 窓 N..2N+35）による全長認証であり、全544型・全閉包663状態が
窓条件を満たす。最小最終周期は**全544型でちょうど34**（1・2・17への短縮は
どの型でも成立しない、窓500..1069上の機械検査）。

## 族の意味と新規性

- K0682は≤5点の全clutter（二点辺・三点辺の混在を含む）を全長証明済み。
- 6点では純三点辺の全型（10688型・共同開始637）まで証明済みであったが、
  **二点辺を含む6点核の完全族は初めて**。7点純三点辺≤5本の閉包に現れた
  1379個の二点辺混在状態は着手による三点辺の退化で生じた副産物であり、
  完全族ではなかった。本実験は初の「二点辺を含む核の完全族」の全長認証である。
- 辺数のヒストグラムは対称単峰 (1,2,5,13,29,52,76,94,94,76,52,29,13,5,2,1)
  であり、**15辺（完全グラフK6）まで稠密な核を含む**。既存の完全族
  （純三点辺、辺数上限あり）と異なり、辺数に上限がない稠密核の族として
  34周期予想への新しい証拠を与える。
- prefix上のGrundy最大は **22**（一意の達成状態 (6,[3,5,6,10,12,18,20,34])・
  L=159）。純三点辺6点全型の29・7点≤5本族の33を下回る。二点辺のみの稠密核は
  予想に反してGrundy値を押し上げない（観測であり全称主張ではない）。
- 最悪開始は (6,[3,5,6,9,17,24,34,40]) と (6,[3,5,6,9,10,17,20,34,36]) の
  2状態（最終周期破綻499）。開始分布は71個の異なる値（最小46・最頻値50）。

## 実装・依存

- `solve_graph.py`: 公式 solver。pinned engine
  `rooted-core-tail-periodicity-20261107/engine.py`（出版済み・byte-clone利用）と
  K0682認証済み≤5点表（500以降34周期ブロック拡張）を再利用し、
  `rooted-core-seven-pure-triple-five-edges-20261125/solve_core.py` の構造適応。
  閉包663状態のうち新規544状態（初期型そのもの）・既知119状態。
  決定性: 同一host 3走（うち1走は PYTHONHASHSEED=random）すべて byte 一致。

## 検証電池

- `verify_independent.py`（独立第二実装）: engine不使用・K0682表不使用の
  fresh 再帰で全閉包663状態を 0..1069 で全再計算し、公式544レコードと
  全値一致（records_checked=544, errors=0, PASS）。2走 byte 一致。
  窓500..1035の周期34一致も独立に確認。
  正直開示: 初版は path list を [0] で初期化したまま per-length 追加した
  index shift bug があり、自身の record 比較で FAIL（fail-closed）して
  修正した。公式 audit は影響なし（公式 solver は検証済み solve_core の
  path 構成の clone で index==length）。
- `verify_direct.py`（原始第三実装）: 層化無作為標本76状態 × L=0..8 の
  684比較を、canonical/remap/path表/再帰式を一切使わないラベル付き局面の
  直接ゲーム木再帰（K0682 proof の原始着手規則のみ）で全一致。
- `verify_enum.py`: E1 fresh canonical 列挙 544型 = E2 Burnside 軌道数 544 =
  audit `distinct_initial_types`、E3 orbit-stabilizer 被覆 Σ120/|Aut| = 32768。
- `verify_tamper.py`: fail-closed 電池。control=PASS、T1値改変/T2 phantom
  レコード/T3 certified flag反転/T4窓主張改変、すべて FAIL (rc≠0)。
- `output/crosscheck_seven_point.json`: 出版済み7点純三点辺≤5本監査
  （2604新規状態）のうち純二点辺状態103個のうち本族と重なる102状態が、
  全 prefix 0..1069 で本公式 audit と完全一致（既出版との交差照合・外部錨）。

## 限界

- 6点グラフ核の**完全族**の有限定理であり、7点以上のグラフ核・三点辺混在の
  6点核の全体・無界核の全称証明ではない。K0684は予想のまま。
- 開始500は本族の共同上界であり、核によらない一様上界の主張ではない
  （K0682の513型と同じ値だが、これは族をまたぐ一様性の証拠・観測にとどまる）。
- Grundy値22・周期34・開始分布の観察は有限観測であり法則ではない。
- verdict は通常プレイの抽象残余ゲームに対するもので、標準11×11空盤の
  いかなるroot/classの判定も消費しない。

## 再現

```sh
python3 solve_graph.py              # ~40s, writes output/audit.json
python3 verify_independent.py        # ~140s, full independent recompute
python3 verify_direct.py            # <1s, primitive sample check
python3 verify_enum.py              # ~20s, Burnside + coverage
python3 verify_tamper.py <case>     # control | T1..T4, one case per run
```

依存: `research/experiments/rooted-core-tail-periodicity-20261107/`
（engine.py・output/audit.json = K0682認証済み513型表）。標準ライブラリのみ。
