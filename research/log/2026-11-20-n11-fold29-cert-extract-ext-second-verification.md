# K1136/K1137/K1139 WIN8-D10証明書抽出の外部再実行第二検証: 実行記録（2026-11-20）

## 経緯

- **宣言（2026-11-20T19:43:48Z・commit `c9d5b415a8`）**:
  単一オーナー宣言ノート
  [宣言ノート](2026-11-20-n11-k1136-k1137-k1139-cert-extract-ext-second-verification-single-owner-note.md)
  を先行出版した。受入条件は7項目（出版byte pin・probe再現・抽出A1/A2/B再現・
  検証器再実行・監査機械再実行・tamper 3件fail-closed・出版とguard）。
  fold/fold23/fold25/fold26外部第二検証・round-5 refsolve・WIN8-D10 root
  `00000000010000809002000040002001` 証明書抽出・WIN8証明書行共有監査は
  他レーン宣言済みであり着手していない。
- **pin基準**: 宣言ノートどおり pin commit `28d223a2dd254b8a85cc342dff3f4bd801d1b31f`
  （2026-11-20T19:39:00Z時点のmain HEAD）。出版社の3実験dir
  （`n11-residual29-win8-cert-extract-root438000000818-20261120/`・
  `n11-residual29-win8-cert-extract-root00000000000200003800200008180000-20261120/`・
  `n11-residual29-win8-cert-extract-root0810000a-20261120/`）の全61ファイルを
  GitHub raw（pinned commit）から取得し、git blob SHA照合で正本固定した。
  runner v17固定コピーはgit blob `c132cc6425eee3feaeef1d697dd74f968cfedb59` 3点。
- **環境**: node v22.20.0型run（`--experimental-strip-types`）・python3・共有sandbox 2コア。
  抽出は並列度2でレーン方針どおり控えめ。実行中にsandbox環境リセットが1回発生し
  ローカル作業器材が一度消滅したが、出版済み分には無影響で、
  当局のpin表（`pin-manifest.json`）から `fetch_master.py` でmasterを再取得・
  git blob再照合してbatteryを再開した（失敗・中断も実験事実として記録）。
- **harness設計**: 300秒のコマンド上限内に各工程を収めるためstage分割
  （`--stage pin|root --root k1136|k1137|k1139|tampers|finalize`）。
  監査JSONから`ms`/経過時間を完全に排除してbyte決定性を確保し、
  `ms`等時刻依存字段は再現対象外と規約化（宣言ノート受入条件2・3どおり。
  K1160の`wall_s`学知見と同型）。
- **battery（3巡）**: pin 61/61 → 各rootでprobe fresh再実行（両AND順序×2＋
  pilot制御・計8レコード/根）→ 抽出A1/A2/B再実行 → 証明書組立照合 →
  BigInt/Bareiss再実行照合 → 出版監査機pristine再実行（同一cwd 2回＋
  隔離EXPERIMENT_ROOT 1回）＋fresh-data差し替え実行 → tamper 3件。
  3巡すべてgate 43 PASS・監査正本
  `cf6a26abf0a459bcfb42bbb2d649ace5d3d1f1a5aee63a01af1de8b79d6a145f`
  byte-identical（慣行最小限界の3実行一致）。1巡約8分。
- **probe再現**: 出版probe-repro-both-orderings.jsonlの決定論的字段と
  全レコード値完全一致（K1136 ac1/ac0 nodes 882,327/1,054,873・
  K1137 261,294/288,448・K1139 1,226,804/1,416,679・pilot 3,402）。
- **抽出再現**: A1（初手毎新規プロセス）を2回（A1・A2）とRun B（単一プロセス一括）
  を実行し、per-moveのnodes/nRows/fbt_drops/fatalが出版と完全一致。
  A1 nodes総計 3,539,166/1,399,389/3,515,506・B 2,564,865/1,057,553/2,808,991。
  A1==A2はper-move byte一致。証明書組立（header+root+sort -u）は3根とも
  出版証明書と**byte-identical**（`dbcb0bae…` 34,845行・`7bd64a47…` 19,527行・
  `089e175d…` 48,020行）、B行集合も一致。
- **検証器再実行**: BigInt独立検証・Bareiss root-check/subroots全走査の
  出力が出版byteと3根ともbyte-identical。
- **監査機械再実行**: pristine再実行3回（r1/r2同一cwd・r3隔離）のすべてで
  19/19 gate PASS・監査正本が出版正本
  `d0653834…`〔K1136〕・`dafa177b…`〔K1137〕・`e706ca6f…`〔K1139〕とbyte-identical。
  本レーンfresh生成記録を差し替えた監査機実行も19/19 PASS・byte-identical
  （監査正本はms非依存データしか埋め込まないため成り立つ）。
- **行順序の実験事実**: 出版ext-summary-a1/a2の行順序はK1136/K1137は
  xargs挙動由来の数値順、**K1139は辞書順**であった。本レーン再実装は数値昇順で、
  行順序は**publisher transport detail（再現対象ではない）**と規約化し、
  per-move値照合（order非依存）と行集合一致で判定した（監査正本
  `line_order_note`に機械可読で記録）。
- **tamper 3件（出版社未試験offset・fail-closed）**:
  (t1) K1137証明書本文offset 300007のXOR 0x01 → 監査gate g16（第三手法全木走査）・
  g17（三手法集計一致）fail・returncode 1。副次的観察として、この改変は
  strategy行由来のため `bareiss --root-check`（root行由来データのみ検査）は
  returncode 0を返し、root-checkを唯一の防御とできないことが実測された
  （防衛の深さの記録）。
  (t2) 監査pin入力 `.input-k1086.json` offset 1111のXOR 0x01 → g01 pin fail。
  (t3) 本レーンfresh ext-summary-a1 move-1 nodes 2757→2758 → g11 fail。

## 結果

harness `verify_cert_extract_ext_second_20261120.py`（SHA-256
`ca662e57053f504684c8dcc44f66c182d338978a3b9b70369a40754d9c59b276`・
30,141 bytes・stdlibのみ・fail-closed）は、出版byte pinのみから
3根のprobe・抽出・証明書・検証器・監査機械の再実行を行い、
全43 gate PASS（3巡byte一致）でK1136/K1137/K1139の外部第二検証を成立させた。
監査正本 `output/harness-audit.json`（15,549 bytes・gate 43・status PASS・
時刻なし・SHA-256 `cf6a26ab…`）。残余20行・pool P⁗ 120,416根に変更を与えない。

## 出版

3部構成でmainに直接出版（AGENTS.mdに従いbranch/PRは作らない）。K番号はpush直前に
3点確認（item 404・README bullet grep・items pathへの新規commit確認）で
**K1166**を取得した（宣言ノートはK番号を確定しない設計で先行出版済み）。

- part1: 実験dir 44ファイル
  `research/experiments/n11-fold29-win8-cert-extract-ext-second-verification-20261120/`
  （commit `80ce56914d`・2026-11-20T20:21:25Z・fetch-back curl + cmp 44/44 byte-identical・
  pinned SHA URL）。self-contained構成: harness・取得器・pin表・監査正本・
  3根のfresh実行記録（probe・summary・bigint・bareiss・監査×3・fresh-data差し替え分）。
- part2: K1166 item＋本log（このcommit）。
- part3: knowledge README末尾へのK1166 bullet追記。

## 解釈上の制限

本検証で行を1行も閉じない。残余20行・pool P⁗ 120,416根は不変。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
