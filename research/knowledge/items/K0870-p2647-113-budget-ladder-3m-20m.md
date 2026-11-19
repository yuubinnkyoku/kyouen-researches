---
id: K0870
title: p=2647 サイズ1322 形状クラス(1,1,3) の層別19 d は 3M/10M/20M ラダーで 8 件 UNSAT に到達し、11 件は 20M でも UNKNOWN である
kind: computation
status: computed
topics: [geometry, maximum-safe, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0712
  note: 固定原点・一完全対の三値還元（d 固定 CNF）の上での予算ラダー
- type: depends_on
  target: K0736
  note: d を引数化した一般 d 符号化（各段は再生成 CNF）
- type: supports
  target: K0768
  note: 100k 掃引の「決まる d の地図」に対する予算軸の拡張
artifacts:
- path: research/experiments/parabola-ternary-selection-20261109/output/ladder-d914-target1322-budget3000000/result.json
  role: data
  note: void 内部 d=914 の SOLVER_UNSAT、conflicts 628,202、92.507 秒
- path: research/experiments/parabola-ternary-selection-20261109/output/ladder-d820-target1322-budget20000000/result.json
  role: data
  note: 20M 段まで掛かった d=820 の SOLVER_UNSAT、conflicts 13,294,778、3,813.133 秒
- path: research/experiments/parabola-ternary-selection-20261109/output/ladder-d147-target1322-budget20000000/result.json
  role: data
  note: 全段 UNKNOWN で尽きた 11 d の代表（d=147、3段すべて UNKNOWN）
- path: research/log/2026-11-13-a2647-candidate-a-ladder-result-omp.md
  role: log
  note: 方法・45 件の判定表・留保（DRAT 未保存）
- path: research/log/2026-11-16-a2647-ladder-drat-receipts-omp.md
  role: log
  note: W28 による後続監査の記録（下記「限界」の追記参照）
- path: research/experiments/parabola-ternary-selection-20261109/output/ladder-drat-d622-budget3000000/audit-drat-trim.json
  role: data
  note: W28 の領収書の代表。d=622 の drat-trim VERIFIED（576.3 秒、証明 3,801,225 行）
- path: research/experiments/parabola-ternary-selection-20261109/output/ladder-drat-native-d820-budget20000000/audit-drat-trim.json
  role: data
  note: 8/8 完了を閉じた d=820 の drat-trim VERIFIED（8,204.7 秒、binary-drat 2,367,583,553 B）。pysat 宛先ディレクトリの init.json だけが pysat 由来で、領収書の正本はここ（pysat 宛先側の同一バイト複製は追跡しない）
- path: research/experiments/parabola-ternary-selection-20261109/output/ladder-drat-native-d820-budget20000000/init.json
  role: data
  note: d=820 のネイティブ領収書の来歴（CNF 一致判定と参照 pysat 領収書、solver 同定）
- path: research/log/2026-11-17-w34-knowledge-update-draft-omp.md
  role: log
  note: 8 件の監査表・W28 との照合・限界の整理
scope: p=2647、size=1322、形状クラス (x,c,e)=(1,1,3)。層別 19 d（147,188,194,488,602,622,703,717,820,914,977,1003,1040,1103,1166,1229,1258,1266,1292）を conflict 予算 3,000,000→10,000,000→20,000,000 で段階実行した有限計算（全 45 実行）。各 d は決着段で停止。
evidence: 45 件の result.json を実読集計。判定 SOLVER_UNSAT 8・UNKNOWN 37・SAT 0、solve_seconds 合計 127,328.3 秒を確認した。加えて決着 8 件は DRAT 領収書 8/8 VERIFIED（W34 ログ）。
---

## 結果

層別サンプル 19 d を単一の固定 d 三値 CNF（K0712）に対して conflict 予算
3M→10M→20M と段階的に上げ、全 45 実行を得た。判定は SOLVER_UNSAT 8・
UNKNOWN 37・SAT 0、solve_seconds 合計 127,328.3 秒。

決着した 8 d はすべて SOLVER_UNSAT で、段ごとに次のとおり
（d: 決着段 / conflicts）:

- 3M 段で決着（5 件）: 622 / 1,796,375、914 / 628,202、977 / 417,436、
  1040 / 447,601、1292 / 674。
- 10M 段で決着（2 件、3M は UNKNOWN）: 1258 / 4,176,372、1266 / 3,945,161。
- 20M 段で決着（1 件、3M・10M は UNKNOWN）: 820 / 13,294,778。

全段 UNKNOWN で尽きた 11 d: 147, 188, 194, 488, 602, 703, 717, 1003,
1103, 1166, 1229（3M / 10M / 20M のいずれも UNKNOWN）。

## 解釈

予算増は決着数に対して実際に効く。100k 予算の掃引（K0768）で UNKNOWN だった d のうち
8 件が 20M 以下で SOLVER_UNSAT に到達した。特に 914, 977, 1040 は、K0768 が
「中盤 d=852..1278 の 427 件はすべて UNKNOWN（UNSAT 0 件）」とした区間の内部に
ありながら 3M 段で速く決着した。

したがって中央区間 d=852..1278 の「UNSAT 0 件」は、
**「決着する d が存在しない区間」ではなく「100k 予算では届かない区間」**として
読み替えるのが適切である（この読み替えは本有限計算のみを根拠とし、
区間内の残り d が決着可能であることを含意しない）。

1292 は K0768 の尾部連続 UNSAT 帯（d=1279..1316）の近傍で、674 conflicts の
即時決着はその尾部パターンと整合する。

一方、11 d は 20M でも決着せず、この予算帯では予算ラダーを伸ばすだけでは
残り全 d の決着は見通せない。

## 限界

- **本ラダー自体の出力には proof が無い**（`ladder-d<D>-target1322-budget<B>/` は
  `init.json` / `input.cnf.gz` / `result.json` のみで、`scope` も unaudited と明記する）。
  ただし決着 8 件の SOLVER_UNSAT はすべて、同一入力・同一予算の再実行と drat-trim による
  独立検証で領収書化済みである（下記「追記（2026-11-17）」）。ラダーの生出力と領収書は
  別ディレクトリであり、前者は今も未監査のまま保持する。
- これは**クラス (1,1,3) の判定ではなく**、A(2647) の範囲 1296 ≤ A ≤ 1322 を動かさない。
  UNKNOWN 37 件は UNSAT でも SAT でもない。
- 各段は独立の再生成 CNF での実行であり、段間で学習節は共有されない
  （K0768 の単一インスタンス昇順掃引とは履歴の扱いが異なる）。
- 標本は層別 19 d に限る。「予算増が効く」はこの 19 d の範囲での観測であり、
  非標本の d への外挿は主張しない。

- 追記（2026-11-17、W34 統合）: 決着 **8 件すべて**が DRAT 証明付きで再解され、
  drat-trim で **VERIFIED（8/8）**となった。領収書は
  `output/ladder-drat-d<D>-budget<B>/` の `solver.json` / `audit-drat-trim.json` /
  `drat-trim.log`（証明本体 `proof.drat` / `proof.drat.gz` は 8 件とも未追跡。ASCII 7 件も
  d=820 の binary も同扱いで、検証は各 JSON の `proof_sha256` と入力 SHA で再現する）。
  d ごとの drat-trim 秒数:

  | d | 段 | 検証秒 | 証明形式 |
  |---|---|---|---|
  | 1292 | 3M | 0.24 | ASCII |
  | 977 | 3M | 144.59 | ASCII |
  | 1040 | 3M | 223.53 | ASCII |
  | 914 | 3M | 212.29 | ASCII |
  | 622 | 3M | 576.33 | ASCII |
  | 1258 | 10M | 1,564.20 | ASCII |
  | 1266 | 10M | 1,501.09 | ASCII |
  | 820 | 20M | 8,204.67 | binary（ネイティブ） |

  各再実行の `input.cnf.gz` はラダーの `init.json` の `encoded_cnf_sha256` と一致する
  （8/8 で実測照合）。したがって本ラダーの 8 件の SOLVER_UNSAT は、記録済みの
  入力同一性のもとで独立監査済みである。記録: W28
  `research/log/2026-11-16-a2647-ladder-drat-receipts-omp.md`（最初の 4 件と d=622）,
  W33 `research/log/2026-11-16-a2647-ladder-drat-native-omp.md`（ネイティブ経路の設計）,
  W34 `research/log/2026-11-17-w34-knowledge-update-draft-omp.md`（8/8 の集計）。
- 追記（2026-11-17）の限界 — **d=820 だけは pysat 方式ではない**。ネイティブ CaDiCaL 3.0.1
  （libcadical `c6073042`、証明をディスクへストリーム）で解き、binary DRAT
  （2,367,583,553 B、`proof_sha256` `0e92b79f…34d30`、added 19,610,968 / deleted 19,564,515）を
  drat-trim の binary モードで検証した。ASCII 版 7 件とは証明形式が異なり、conflicts も
  ラダー側の 13,294,778 ではなく 19,442,067（solve 4,820.64 秒）である。両者が共有するのは
  入力 CNF のバイト同一性と UNSAT 判定だけであり、conflicts の一致を領収書の根拠にしない。
  なお `output/ladder-drat-d820-budget20000000/` にある `init.json`（`solver: Cadical195`、
  749 B）は pysat ドライバが後から書いたもので、このディレクトリの追跡対象はこの 1 ファイル
  に限る（ネイティブ側 `init.json` は 1,622 B で `solver: cadical-native`、内容は別物）。
  `solver.json` / `audit-drat-trim.json` / `drat-trim.log` / `run.log` / `native-result.json`
  の正本はネイティブ実行の `output/ladder-drat-native-d820-budget20000000/` 側にあり、
  pysat 宛先ディレクトリの複製 3 件（md5 一致を実測）と `proof.drat.gz`
  （`proof_gz_sha256` 1e37e59c… が両者一致）は追跡も引用もしない。この 2 ディレクトリを
  pysat 方式の領収書として引用しない。
- 追記（2026-11-17）で**動かないもの**: UNKNOWN 37 件は依然 UNSAT でも SAT でもなく、
  クラス (1,1,3) の判定は未了、A(2647) の範囲 1296 ≤ A ≤ 1322 は不変である。
  8 件の領収書は「決着した d の UNSAT が入力同一性つきで監査された」ことだけを意味し、
  非標本 14 d や 20M 超の予算への外挿を含意しない。
