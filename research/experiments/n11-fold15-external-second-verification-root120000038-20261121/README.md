# n11-fold15-external-second-verification-root120000038-20261121

標準11×11空盤レーン（head-1410系）の fold15 receipt fold（第22 receipt・
5番目WIN8 receipt fold・WIN8-D10 root `00000000012000003800080009000000`・
K1114証明書・出版実験 `research/experiments/n11-residual58-win8-receipt-fold-root120000038-20261120/`）
に対する**外部第二検証（単体ext2）**の成果物一式。
単一オーナー宣言:
`research/log/2026-11-21-n11-fold15-external-second-verification-single-owner-note.md`
（commit `0a1a52d4`・以降の並走コミットなしをlist_commitsで確認済み）。

## 主結果（2026-11-21時点）

- **全981 gate PASS**（P 12 / I 64 / C 863 / X 26 / T 16）。監査正本
  `output/external-audit.json`（101,443 bytes・
  sha256 `6800759ea5e899b84866079ac36fae2316d78a85620e1b32187abc26a0fed717`）は
  同一cwd 2回＋隔離cwd/HOME+`PYTHONHASHSEED=random` の3実行でbyte-identical。
  検証機1実行約105秒（fold15機単体pristine runは約23秒）。
- W入力34 pin（12 Git blob SHA-1 + 22 SHA-256）を出版repo byteのみから
  静的URLで再取得・全件fail-closed照合
  （K1175/K1176/fold14レーンで確立した静的URL再構成機設計の直接適用）。
  fold11出版機（`9b3e06c8…`）・fold12出版機（`706bfa7a…`）・
  fold13出版機（`5c27f1ae…`）・fold14出版機（`7b88a565…`）をWに配置し、
  4機の入力pin表がfold15機pin表（12 blob + 22 SHA-256）の部分集合であることを
  機械確認（fold11機pin⊂fold12機pin⊂fold13機pin⊂fold14機pin⊂fold15機pinの鎖）。
- fold15出版機のpristine再実行4回（同一W 2回・隔離copytree/cwd/HOME・
  隔離+`PYTHONHASHSEED=random`）すべてreceipt出力が出版正本
  `bae2b3c1…` とbyte-identical。各回の機内fold11 rerun receipt（`d7bf2cd5…`）も
  出版正本とbyte-identical。加えてfold14出版機を隔離W複写上で独立実行し
  `ed3159fd…` byte一致・機内fold11 rerun `d7bf2cd5…` byte一致
  （宣言受入条件の外側確認・検証機V vr14段に再実装）。
- チェーン全段の独立再構成: base worklist 6,438行（cost 509,109）→
  fold14適用後 frontier 6,179/489,440・solved 1,669・incidence 11,765・
  残余58行・五親target 54/112（fold4/56/7/8/9-12/fs13(13-16)/fold10/fold11/
  fold12/fold13/fold14の11出版記録を段ごとに再計算しpublished値と照合）。
- fold15 receipt主張の第三実装による値単位再導出: coverage 6行
  （K1114 g07主張3行＋余剰3行・28 canonical行は2方法〔224 D4像2石除去操作と
  C(8,6)=28部分集合〕で再導出し一致・closed edge cost 486）・
  影響4親（全c2: 13→10/62→59/54→51/40→37・完全閉鎖0・合計12 row-closings）・
  frontier_after 6,173/488,954・solved 1,675・incidence 11,753・
  needed 4,481/355,402・五親target 54→57・残余58→55行（55行hex全列挙照合）・
  win16候補 12→11根（主張行 retire: fold11 4行+fold12 3行+fold13 3行+
  fold14 4行+fold15 3行=17行・残32行はfold15閉鎖行と不交差）・残余23行不交差。
  K1114 19 gate主要値（probes nodes 825,127/657,152・extraction nodes
  2,723,200/2,141,807・証明書 1,171,958 bytes 32,470行 sorted unique・
  third_method terminal 11,338/visited 69,115/winner 44,580/loser 13,197/
  応手辺 61,058/range [14,18]/subroot mobility 53）とroot合法手53の
  survival規約再実装による独立再導出、K1097 27 gate・win16 footprint
  49行exactly-once partitionを再照合。
- **53-mobility root初のreceipt fold**: fold15 root（K1086 addtwo-greedy23
  sweep起点）は合法手53であり、このレーンで初めて50超のmobility rootの
  receipt foldを検証した。fold15 rootの28 canonical行分類は
  open-frontier 6行/not-in-worklist 22行/closed-before-this-receipt 0行
  （fold14 subgeometryの1行と違い閉鎖済み行を含まない。
  receiptは6行全てをこの fold で閉じ、うち3行は五親target行・
  3行はworklist内のtarget外余剰行〔複数余剰行の初事例〕）。
- tamper検査: worklist offset 208,888・K1114証明書 offset 919,191の
  1 byte XOR（fold14レーン 200,222/888,222と独立の未試験offset）がともに
  fail-closed（rc≠0・fold15/fold11 rerun出力とも未書込・WT内のpinned
  fold14 recordは無改変）。
- **source_record stale参照erratum（fold12型の再発）**: 出版fold15 receiptの
  `independent_verification.source_record` はfold14証明書抽出実験
  （`n11-residual65-win8-cert-extract-root9090022-20261120`）を指しており、
  K1114実験dir（`n11-residual58-win8-cert-extract-root120000038-20261120`）の
  stale参照となっている（fold13/fold14 receiptは正しく記載していた。
  receipt byteは変更せず、監査JSON observationsにerratumとして記録し
  K1114フォローアップに回す）。`certificate_source`・`verdict_join_summary`・
  `experiment`各欄はK1114を正しく指している。

## 位置づけ

- 本検証は検証の検証（簿記・決定性・入力pin・fail-closed防衛の再検査）であり、
  行は1行も閉じない。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
  REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を
  勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**

## レイアウト

```
scripts/
  reconstruct_fold15_inputs.py        # W15/pub15f再構成機（静的URL・全pin fail-closed）
                                      # sha256 7757cb5130942e8891697fcf0903f37d9c8d27f3ed6a8ca1b85a5fc07fd582be
  verify_fold15_external_20261121.py # 別実装検証機（第三実装・981 gate・stdlibのみ）
                                      # sha256 ade19de29fa34bb8f0f7913ece230daa428797792c9db59279e8489d872eac99
output/
  external-audit.json                 # 監査正本（3実行byte一致）
                                      # sha256 6800759ea5e899b84866079ac36fae2316d78a85620e1b32187abc26a0fed717
  reproduction.log                    # 実行記録
```

## 実行方法

```sh
python3 scripts/reconstruct_fold15_inputs.py <W_root> <pub_root> [<pinned_commit>]
# pinned_commit 既定: 0a1a52d4（宣言ノート出版HEAD）
python3 scripts/verify_fold15_external_20261121.py <W_root> <pub_root> <out_json>
```

W再構成はapi.github.comを使わない（全入力をraw.githubusercontent.comの
固定commit URLから取得し、blob SHA-1 / SHA-256を計算照合する）。
