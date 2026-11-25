# n11-fold14-external-second-verification-root9090022-20261121

標準11×11空盤レーン（head-1410系）の fold14 receipt fold（第21 receipt・
4番目WIN8 receipt fold・WIN8-D10 root `00000000000000909002200080100000`・
出版実験 `research/experiments/n11-residual62-win8-receipt-fold-root9090022-20261120/`）
に対する**外部第二検証（単体ext2）**の成果物一式。
単一オーナー宣言:
`research/log/2026-11-21-n11-fold14-external-second-verification-single-owner-note.md`
（commit `2a6f14de95`・先行宣言なしを直近コミット列で確認済み）。

## 主結果（2026-11-21時点）

- **全880 gate PASS**（P 12 / I 54 / C 772 / X 26 / T 16）。監査正本
  `output/external-audit.json`（91,543 bytes・
  sha256 `fe6370f7e9cd30eaca7cc0ce3a61d39e9a6dd1eb47c8ba4f300e680f5d55b102`）は
  同一cwd 2回＋隔離cwd/HOME＋`env -i`+`PYTHONHASHSEED=random` の3実行でbyte-identical。
  検証機1実行約53秒（fold14機単体pristine runは約11.4秒）。
- W入力31 pin（12 Git blob SHA-1 + 19 SHA-256）を出版repo byteのみから
  静的URLで再取得・全件fail-closed照合（api.github.com非依存の
  raw.githubusercontent.com固定commit URL+blob/SHA照合。
  K1175/K1176レーンで確立した静的URL再構成機設計の直接適用）。
  fold11出版機（`9b3e06c8…`）・fold12出版機（`706bfa7a…`）・
  fold13出版機（`5c27f1ae…`）をWに配置し、fold11機・fold12機・fold13機の
  入力pin表がfold14機pin表（12 blob + 19 SHA-256）の部分集合であることを
  機械確認（fold11機pin⊂fold12機pin⊂fold13機pin⊂fold14機pinの鎖）。
- fold14出版機のpristine再実行4回（同一W 2回・隔離copytree/cwd/HOME・
  隔離+`PYTHONHASHSEED=random`）すべてreceipt出力が出版正本
  `ed3159fd…` とbyte-identical。各回の機内fold11 rerun receipt（`d7bf2cd5…`）も
  出版正本とbyte-identical（機内fold12/fold13 rerun gateは隔離W複写上で実行され
  returncode 0で通過）。加えてfold13出版機を隔離W複写上で独立実行し
  `c2bf8051…` byte一致・機内fold11 rerun `d7bf2cd5…` byte一致
  （宣言受入条件3の外側確認・検証機V vr13段に再実装）。
- チェーン全段の独立再構成: base worklist 6,438行（cost 509,109）→
  fold13適用後 frontier 6,184/489,813・solved 1,664・incidence 11,775・
  残余62行・五親target 50/112（fold4/56/7/8/9-12/fs13(13-16)/fold10/fold11/
  fold12/fold13の10出版記録を段ごとに再計算しpublished値と照合）。
- fold14 receipt主張の第三実装による値単位再導出: coverage 5行
  （K1109 g07主張4行＋余剰1行 `00000000000000889002400000000000`・
  28 canonical行は2方法〔224 D4像2石除去操作とC(8,6)=28部分集合〕で再導出し一致・
  closed edge cost 373）・影響4親（全c2: 22→20/23→21/67→64/63→60・
  完全閉鎖0・合計10 row-closings）・
  frontier_after 6,179/489,440・solved 1,669・incidence 11,765・
  needed 4,487/355,888・五親target 50→54・残余62→58行（58行hex全列挙照合）・
  win16候補 13→12根（主張39→35行・fold11 4行+fold12 3行+fold13 3行+fold14 4行の
  4 retire合計に照合）・残余23行不交差。
  **fold14は主張4行のWIN8候補として初のfold**（K1109 receiptの主張行数4の直接確認）。
- **closed-before-this-receipt行の初出**: fold14 rootの28 canonical行分類は
  open-frontier 5行/not-in-worklist 22行/closed-before-this-receipt 1行
  （`00000000000000003800000008003000`・fold13 receiptが閉じた行）で、
  WIN8 receipt foldとして初めて閉鎖済み行を含む。二重閉鎖の回避
  （同を行をこのreceiptのcoverageに含めない）を分類・coverage双方で機械確認。
  K1109 19 gate主要値（probes nodes 512,590/614,246・extraction nodes
  6,102,650/6,102,650・証明書 1,082,873 bytes 29,942行 sorted unique・
  third_method terminal 10,239/visited 65,134/winner 42,115/loser 12,780/
  応手辺 58,084/range [14,18]/subroot mobility 50）とroot合法手50の
  survival規約再実装による独立再導出、K1097 27 gate・win16 footprint
  49行exactly-once partitionを再照合。
- tamper検査: worklist offset 200,222・K1109証明書 offset 888,222の
  1 byte XOR（出版社未試験offset）がともにfail-closed
  （rc≠0・fold14/fold11 rerun出力とも未書込・WT内のpinned fold13 recordは無改変）。
- **source_record清潔パターンの継続確認**: 出版fold14 receiptの
  `independent_verification.source_record` はK1109証明書抽出実験
  （`n11-residual65-win8-cert-extract-root9090022-20261120`・root 9090022）を
  正しく指しており、fold12 receipt（K1175監査でerratum記録）のような
  上流実験へのstale参照はない。監査JSONのobservations欄に記録した。

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
  reconstruct_fold14_inputs.py        # W14/pub14再構成機（静的URL・全pin fail-closed）
                                      # sha256 62a72b36eb70a74c3b9fcc85c10c59a7bab73550807e957382645d38866d5d59
  verify_fold14_external_20261121.py  # 別実装検証機（第三実装・880 gate・stdlibのみ）
                                      # sha256 d966dad55d54b6c1608f5f046469b2fd9a95b3b38c4f12a69f516e83fb708b0c
output/
  external-audit.json                 # 監査正本（3実行byte一致）
                                      # sha256 fe6370f7e9cd30eaca7cc0ce3a61d39e9a6dd1eb47c8ba4f300e680f5d55b102
  reproduction.log                    # 実行記録
```

## 実行方法

```sh
python3 scripts/reconstruct_fold14_inputs.py <W_root> <pub_root> [<pinned_commit>]
# pinned_commit 既定: 2a6f14de95（宣言ノート出版HEAD）
python3 scripts/verify_fold14_external_20261121.py <W_root> <pub_root> <out_json>
```

W再構成はapi.github.comを使わない（全入力をraw.githubusercontent.comの
固定commit URLから取得し、blob SHA-1 / SHA-256を計算照合する）。
