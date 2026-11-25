# n11-fold13-external-second-verification-root9840004-20261121

標準11×11空盤レーン（head-1410系）の fold13 receipt fold（第20 receipt・
WIN8-D10 root `00000000000000003800000009840004`・出版実験
`research/experiments/n11-residual65-win8-receipt-fold-root9840004-20261120/`）
に対する**外部第二検証（単体ext2）**の成果物一式。
単一オーナー宣言:
`research/log/2026-11-21-n11-fold13-external-second-verification-single-owner-note.md`
（commit `5a9e8142942786ffe1b2afa2be228caea3d3d18f`・宣言 2026-11-21T01:00:00Z・
先行宣言なしを直近30コミットで確認済み）。

## 主結果（2026-11-21時点）

- **全774 gate PASS**（P 12 / I 44 / C 673 / X 29 / T 16）。監査正本
  `output/external-audit.json`（81,632 bytes・
  sha256 `4fe40fa254b4d2658bb0fadbc47dadb43c3d85214be8a9517b525693b416be81`）は
  同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random` の3実行でbyte-identical。
  検証機1実行約29秒。
- W入力28 pin（12 Git blob SHA-1 + 16 SHA-256）を出版repo byteのみから
  静的URLで再取得・全件fail-closed照合（api.github.com非依存の
  raw.githubusercontent.com固定commit URL+blob/SHA照合。
  K1175レーンで確立した静的URL再構成機設計の直接適用）。
  fold11出版機（`9b3e06c8…`）・fold12出版機（`706bfa7a…`）をWに配置し、
  fold11機・fold12機の入力pin表がfold13機pin表（12 blob + 16 SHA-256）の
  部分集合であることを機械確認（fold11機pinはfold12機pinの部分集合でもある）。
- fold13出版機のpristine再実行4回（同一W 2回・隔離copytree/cwd/HOME・
  隔離+`PYTHONHASHSEED=random`）すべてreceipt出力が出版正本
  `c2bf8051…` とbyte-identical。各回の機内fold11 rerun receipt（`d7bf2cd5…`）と
  機内fold12 rerun receipt（`0f73795c…`・隔離W複写上）も出版正本とbyte-identical。
  加えてfold11・fold12出版機を隔離W複写上で独立実行し `d7bf2cd5…`/
  `0f73795c…` byte一致（宣言受入条件3の外側確認・検証機vr11/vr12段にも再実装）。
- チェーン全段の独立再構成: base worklist 6,438行（cost 509,109）→
  fold12適用後 frontier 6,193/490,526・solved 1,655・incidence 11,790・
  残余65行・五親target 47/112（fold4/56/7/8/9-12/fs13(13-16)/fold10/fold11/fold12の
  9出版記録を段ごとに再計算しpublished値と照合）。
- fold13 receipt主張の第三実装による値単位再導出: coverage 9行
  （K1108 g07主張3行＋余剰6行・余剰6行は単一WIN8 receiptとして最多・
  28 canonical行は2方法〔224 D4像2石除去操作とC(8,6)=28部分集合〕で再導出し一致・
  closed edge cost 713）・影響5親（c4 3: 87→84/90→87/75→72・
  c2 2: 61→58/16→13・完全閉鎖0・合計15 row-closings）・
  frontier_after 6,184/489,813・solved 1,664・incidence 11,775・
  needed 4,492/356,261・五親target 47→50・残余65→62行（62行hex全列挙照合）・
  win16候補 14→13根（主張42→39行・fold11 4行+fold12 3行+fold13 3行の
  3 retire合計に照合）・残余23行不交差。
  K1108 19 gate主要値（probes nodes 1,143,198/1,528,656・extraction nodes
  4,109,768/3,075,922・証明書 1,640,220 bytes 45,286行 sorted unique・
  third_method terminal 17,333/visited 103,531/winner 66,627/loser 19,571/
  応手辺 91,337/range [14,18]）とroot合法手57のsurvival規約再実装による
  独立再導出、K1097 27 gate・win16 footprint 49行exactly-once partitionを再照合。
- tamper検査: worklist offset 117,777・K1108証明書 offset 777,777の
  1 byte XOR（出版社未試験offset）がともにfail-closed
  （rc≠0・fold13/fold11出力とも未書込・WT内のpinned fold12 recordは無改変）。
- **fold12レーンのerratumパターンの解消確認**: 出版fold13 receiptの
  `independent_verification.source_record` はK1108証明書抽出実験
  （`n11-residual65-win8-cert-extract-root9840004-20261120`・root 9840004）を
  正しく指しており、fold12 receipt（K1175監査でerratum記録）のような
  上流実験へのstale参照はない。監査JSONのobservations欄に対照記録した。

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
  reconstruct_fold13_inputs.py        # W13/pub13再構成機（静的URL・全pin fail-closed）
                                      # sha256 1b54624fe1ccbbb91d390895aa4669fc1aa1c411ac884b750bc7e694389114e9
  verify_fold13_external_20261121.py  # 別実装検証機（第三実装・774 gate・stdlibのみ）
                                      # sha256 aeda41e1df244cf331a9435260d8ed83652971af8e29bfa289648cf981abf6bc
output/
  external-audit.json                 # 監査正本（3実行byte一致）
                                      # sha256 4fe40fa254b4d2658bb0fadbc47dadb43c3d85214be8a9517b525693b416be81
  reproduction.log                    # 実行記録
```

## 実行方法

```sh
python3 scripts/reconstruct_fold13_inputs.py <W_root> <pub_root> [<pinned_commit>]
# pinned_commit 既定: 5a9e8142942786ffe1b2afa2be228caea3d3d18f
python3 scripts/verify_fold13_external_20261121.py <W_root> <pub_root> <out_json>
```

W再構成はapi.github.comを使わない（全入力をraw.githubusercontent.comの
固定commit URLから取得し、blob SHA-1 / SHA-256を計算照合する）。
