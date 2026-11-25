# n11-fold12-external-second-verification-root8005021-20261121

標準11×11空盤レーン（head-1410系）の fold12 receipt fold（第19 receipt・
WIN8-D10 root `00000000000000003800000008005021`・出版実験
`research/experiments/n11-residual68-win8-receipt-fold-root8005021-20261120/`）
に対する**外部第二検証（単体ext2）**の成果物一式。
単一オーナー宣言:
`research/log/2026-11-21-n11-fold12-external-second-verification-single-owner-note.md`
（commit `de32ca573ba179985579ae9608c3851810c078c8`）。

## 主結果（2026-11-21時点）

- **全655 gate PASS**（P 12 / I 34 / C 571 / X 24 / T 14）。監査正本
  `output/external-audit.json`（70,149 bytes・
  sha256 `c309d69337461518390b7a5cb466e49da6c5c98b7fbcd0a4fd187bf03b52eb07`）は
  同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random` の3実行でbyte-identical。
- W入力25 pin（12 Git blob SHA-1 + 13 SHA-256）を出版repo byteのみから
  静的URLで再取得・全件fail-closed照合（api.github.com依頼なしの
  raw.githubusercontent.com固定commit URL+blob/SHA照合。未解決だった
  worklist/ledger/auditの3 blobは検証中に静的パスを特定してbyte照合解決）。
  fold11出版機（`9b3e06c8…`）をWに配置し、fold11機の入力pin表が
  fold12機pin表の部分集合であることを機械確認。
- fold12出版機のpristine再実行4回（同一W 2回・隔離copytree/cwd/HOME・
  隔離+`PYTHONHASHSEED=random`）すべてreceipt出力が出版正本
  `0f73795c…` とbyte-identical。各回の機内fold11 rerun receiptも
  出版正本 `d7bf2cd5…` とbyte-identical。加えてfold11出版機を
  隔離W複写上で独立実行し `d7bf2cd5…` byte一致（宣言受入条件3の外側確認）。
- チェーン全段の独立再構成: base worklist 6,438行（cost 509,109）→
  fold11適用後 frontier 6,201/491,110・solved 1,647・incidence 11,803・
  残余68行・五親target 44/112（fold4/56/7/8/9-12/fs13(13-16)/fold10/fold11の
  8出版記録を段ごとに再計算しpublished値と照合）。
- fold12 receipt主張の第三実装による値単位再導出: coverage 8行
  （K1106 g07主張3行＋余剰5行・28 canonical行は2方法〔224 D4像2石除去操作と
  C(8,6)=28部分集合〕で再導出し一致・closed edge cost 584）・
  影響5親（c1 3: 58→56/65→63/75→72・c2 2: 44→41/25→22・完全閉鎖0）・
  frontier_after 6,193/490,526・solved 1,655・incidence 11,790・
  needed 4,501/356,974・五親target 44→47・残余68→65行（65行hex全列挙照合）・
  win16候補 15→14根（主張45→42行）・残余23行不交差。
  K1106 19 gate主要値（probes 619,138/751,581・nodes 3,272,039/2,876,091・
  証明書 945,298 bytes 26,083行 sorted unique・third_method
  terminal 10,191/visited 59,594/winner 38,442/loser 10,961/応手辺 53,352/
  range [14,18]）とroot合法手41のsurvival規約再実装による独立再導出、
  K1097 27 gate・win16 footprint 49行exactly-once partitionを再照合。
- tamper検査: worklist offset 96,300・K1106証明書 offset 456,789の
  1 byte XOR（出版社未試験offset）がともにfail-closed
  （rc≠0・fold12/fold11出力とも未書込）。
- **erratum記録（文書フィールドのみ・byte pin対象外）**: 出版receiptの
  `independent_verification.source_record` がfold11証明書抽出実験
  （root 8003180）を指しており、K1106（root 8005021）を指していない。
  文字列はfold12機sourceの固定値。`certificate_source` ブロックと全sha pinは
  正しい。監査JSONのobservations欄に記録した。

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
  reconstruct_fold12_inputs.py        # W12/pub12再構成機（静的URL・全pin fail-closed）
                                      # sha256 caa30f346ede97324f0cc268c2b3adf74ae8ce26a8691be4dadbaf66f3da6710
  verify_fold12_external_20261121.py  # 別実装検証機（第三実装・655 gate・stdlibのみ）
                                      # sha256 43afc1cd31d5d731858388532d5b07266ac60b2e7265f2490fc6574d5a6578f9
output/
  external-audit.json                 # 監査正本（3実行byte一致）
                                      # sha256 c309d69337461518390b7a5cb466e49da6c5c98b7fbcd0a4fd187bf03b52eb07
  reproduction.log                   # 実行記録
```

## 実行方法

```sh
python3 reconstruct_fold12_inputs.py <W_root> <pub_root> [<pinned_commit>]
# pinned_commit 既定: de32ca573ba179985579ae9608c3851810c078c8
python3 scripts/verify_fold12_external_20261121.py <W_root> <pub_root> <out_json>
```

W再構成はapi.github.comを使わない（全入力をraw.githubusercontent.comの
固定commit URLから取得し、blob SHA-1 / SHA-256を計算照合する）。
