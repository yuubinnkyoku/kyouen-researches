# n11-fold16-external-second-verification-root8890020-20261121

標準11×11空盤レーン（head-1410系）の fold16 receipt fold（第23 receipt・
6番目WIN8 receipt fold・WIN8-D10 root `00000000010000889002000080100000`・
K1113証明書・出版実験 `research/experiments/n11-residual55-win8-receipt-fold-root8890020-20261120/`）
に対する**外部第二検証（単体ext2）**の成果物一式。
単一オーナー宣言:
`research/log/2026-11-21-n11-fold16-external-second-verification-single-owner-note.md`
（commit `c6a55000`・以降の並走fold16系コミットなしをlist_commitsで確認済み。
宣言時点のHEADは第一宣言受入後も `c6a55000` から非破壊）。

## 主結果（2026-11-21時点）

- **全1061 gate PASS**（P 12 / I 75 / C 932 / X 26 / T 16）。監査正本
  `output/external-audit.json`（108,139 bytes・
  sha256 `09f80902d8c2159b26db971504a582d43acb77879021e684c56bbbdcbe7cf19d`）は
  同一cwd 2回＋隔離cwd/HOME+`env -i`+`PYTHONHASHSEED=random` の3実行で
  byte-identical。検証機1実行約210秒（fold16機単体pristine runは約46秒）。
- W入力37 pin（12 Git blob SHA-1 + 25 SHA-256）を出版repo byteのみから
  静的URLで再取得・全件fail-closed照合
  （fold14/fold15レーンで確立した静的URL再構成機設計の直接適用）。
  fold11出版機（`9b3e06c8…`）・fold12出版機（`706bfa7a…`）・
  fold13出版機（`5c27f1ae…`）・fold14出版機（`7b88a565…`）・
  fold15出版機（`03000c14…`）をW16に配置し、5機の入力pin表がfold16機pin表
  （12 blob + 25 SHA-256）の部分集合であることを機械確認
  （fold11機pin(10)⊂fold12機pin(13)⊂fold13機pin(16)⊂fold14機pin(19)⊂
  fold15機pin(22)⊂fold16機pin(25)の鎖・本検証機のI段で全段再照合）。
- fold16出版機のpristine再実行4回（同一W 2回・隔離copytree/cwd/HOME・
  隔離+`PYTHONHASHSEED=random`）すべてreceipt出力が出版正本
  `edd55258…` とbyte-identical。各回の機内fold11 rerun receipt
  （`d7bf2cd5…`）も出版正本とbyte-identical。加えてfold15出版機を隔離W複写上
  で独立実行し `bae2b3c1…` byte一致・機内fold11 rerun `d7bf2cd5…` byte一致
  （宣言受入条件の外側確認・検証機V vr15段に再実装）。
- チェーン全段の独立再構成: base worklist 6,438行（cost 509,109）→
  fold15適用後 frontier 6,173/488,954・solved 1,675・incidence 11,753・
  needed 4,481/355,402・残余55行・五親target 57/112
  （fold4/fold56(5-6)/fold7/fold8/fold9(9-12)/fs13(13-16)/fold10/fold11/
  fold12/fold13/fold14/fold15の12出版記録を段ごとに再計算しpublished値と照合）。
- fold16 receipt主張の第三実装による値単位再導出: coverage 5行
  （K1113 g07主張4行＋余剰1行 `00000000000000801222000100000000`・
  28 canonical行は2方法〔224 D4像2石除去操作とC(8,6)=28部分集合〕で再導出し
  一致・closed edge cost 379）・影響4親（全c2: 20→18/21→19/42→39/60→57・
  完全閉鎖0・合計10 row-closings）・
  frontier_after 6,168/488,575・solved 1,680・incidence 11,743・
  needed 4,476/355,023・五親target 57→61・残余55→51行
  （51行hex全列挙照合）・win16候補16根のうち6根retire
  （fold11 4行+fold12 3行+fold13 3行+fold14 4行+fold15 3行+fold16主張4行=
  21行retire・残10根28行はfold16閉鎖行と不交差）・残余23行掃引計画との不交差。
  K1113 19 gate主要値（probes nodes 575,570/409,407・extraction nodes
  4,424,758/4,424,758・証明書 775,317 bytes 21,446行 sorted unique・
  third_method terminal 7,653/visited 48,855/winner 31,320/loser 9,882/
  応手辺 43,837/range [14,18]/subroot mobility 50）とroot合法手50の
  survival規約再実装による独立再導出、K1097 27 gate・win16 footprint
  49行exactly-once partition・root/D4正準/quadruple-freeを再照合。
- **closed-before-this-receipt 1行を含む2例目のWIN8 root**: fold16 rootの
  28 canonical行分類はopen-frontier 5/not-in-worklist 22/
  closed-before-this-receipt 1（`00000000000000003800000008003000`・
  fold13 receipt閉鎖済み。fold14 rootに次ぐ2例目。二重閉鎖は分類と
  coverage再導出から構造的に除外され、`closed_history` 全履歴と
  worklist・residual55の三方で機械確認）。
- tamper検査: worklist offset 300,111・K1113証明書 offset 740,321の
  1 byte XOR（fold14レーン 200,222/888,222・fold15レーン 208,888/919,191と
  独立の未試験offset）がともにfail-closed（rc≠0・fold16/fold11 rerun出力と
  も未書込・WT内のpinned fold15 recordは無改変）。
- **IV.source_record clean patternの維持**: 出版fold16 receiptの
  `independent_verification.source_record` はK1113証明書抽出実験
  （`n11-residual58-win8-cert-extract-root8890020-20261120`）を正しく指す
  （fold12 receipt〔K1175監査〕・fold15 receipt〔K1179監査〕のstale参照
  erratumと対照的に、fold16 receiptは自実験dirを記載。
  `certificate_source`・`verdict_join_summary`・`schema`/`experiment`各欄も
  正しい。receipt byteは不変）。

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
  reconstruct_fold16_inputs.py        # W16/pub16f再構成機（静的URL・全pin fail-closed）
                                      # sha256 c70cbc453a1f712fa51d66123790cd053d7198edd4bdcf53aa6ec055b78594d4
  verify_fold16_external_20261121.py  # 別実装検証機（第三実装・1061 gate・stdlibのみ）
                                      # sha256 3291794504d98f2c7d7204f623325c92d2d898ea6e246ede476e6e736ac51627
output/
  external-audit.json                 # 監査正本（3実行byte一致）
                                      # sha256 09f80902d8c2159b26db971504a582d43acb77879021e684c56bbbdcbe7cf19d
  reproduction.log                    # 実行記録
```

## 実行方法

```sh
python3 scripts/reconstruct_fold16_inputs.py <W_root> <pub_root> [<pinned_commit>]
# pinned_commit 既定: c6a55000（宣言ノート出版HEAD）
python3 scripts/verify_fold16_external_20261121.py <W_root> <pub_root> <out_json>
```

W再構成はapi.github.comを使わない（全入力をraw.githubusercontent.comの
固定commit URLから取得し、blob SHA-1 / SHA-256を計算照合する）。
