# K1136/K1137/K1139 WIN8-D10証明書抽出の外部再実行第二検証（2026-11-20）

## 位置づけ

残余29行レーンの3証明書抽出
（K1136: root `00000000000000043800000008180010`・K1137: root
`00000000000200003800200008180000`・K1139: root
`0000000800000000380000000810000a`・各8石WIN8-D10）に対する
**外部第二検証**である。出版社レーンの3実験dir
（`n11-residual29-win8-cert-extract-root438000000818-20261120/`・
`n11-residual29-win8-cert-extract-root00000000000200003800200008180000-20261120/`・
`n11-residual29-win8-cert-extract-root0810000a-20261120/`）の全61ファイルを
git blob SHAでbyte pinし、pin byteだけからprobe・抽出・検証器・監査機械を
**新規に再実行**して、出版正本（証明書・BigInt検証・Bareiss検証・19 gate監査正本）
と照合した。単一オーナー宣言は
[宣言ノート](../../log/2026-11-20-n11-k1136-k1137-k1139-cert-extract-ext-second-verification-single-owner-note.md)
（commit `c9d5b415a8`・2026-11-20T19:43:48Z）のとおり、受入条件7項目はすべて達成した。

本dirはself-containedである。harness `verify_cert_extract_ext_second_20261120.py`
（SHA-256 `ca662e57053f504684c8dcc44f66c182d338978a3b9b70369a40754d9c59b276`・
30,141 bytes・stdlibのみ・fail-closed・時刻を持たない決定論的監査JSON 1点を出力）と、
pin取得器 `fetch_master.py`（SHA-256 `c3c4c9ff…`）と
pin表 `pin-manifest.json`（SHA-256 `949868e2…`・61ファイル分のgit blob SHA正本）が
出版byte取得・再実行・照合の全工程を行う。出版社実装の流用はpin照合のための
実行のみに限られ、検証ロジックは本レーンのharnessが独立に持つ。

## 受入条件と達成結果

宣言ノートの受入条件に対する結果（監査正本 `output/harness-audit.json`・
SHA-256 `cf6a26abf0a459bcfb42bbb2d649ace5d3d1f1a5aee63a01af1de8b79d6a145f`・
15,549 bytes・gate 43・status PASS・3回のbattery全実行でbyte一致）:

1. **出版byte pin（達成）**: pin commit `28d223a2dd254b8a85cc342dff3f4bd801d1b31f`
   （2026-11-20T19:39:00Z時点のmain HEAD）から3実験dir全61ファイルを取得し
   git blob SHA-1照合61/61（runner v17固定コピー git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59` 3点・
   証明書3点 SHA-256 `dbcb0bae…`/`7bd64a47…`/`089e175d…` 込み）。
2. **probe再現（達成）**: 各rootで両AND順序×2回=4 probe＋pilot_d6制御の
   計8レコードをpinned runner v17でfresh実行し、出版
   probe-repro-both-orderings.jsonlの決定論的字段（nodes・loss・terminal石数・capped）と
   値完全一致（K1136 ac1/ac0 nodes 882,327/1,054,873・K1137 261,294/288,448・
   K1139 1,226,804/1,416,679）。
3. **抽出再現 A1/A2/B（達成）**: A1（初手毎新規プロセス・並列度2）を2回と
   Run B（単一プロセス一括）を新規実行し、per-moveの
   nodes/nRows/fbt_drops/fatalが出版ext-summaryと完全一致。
   A1 nodes総計はK1136 3,539,166・K1137 1,399,389・K1139 3,515,506、
   BはK1136 2,564,865・K1137 1,057,553・K1139 2,808,991。
   A1==A2はper-move byte一致（rows byteも一致）。A1の証明書組立
   （header行+root行+sorted-unique strategy行）が出版証明書と**byte-identical**
   （SHA-256 3点再一致・K1136 34,845行/K1137 19,527行/K1139 48,020行）で、
   Bの行集合も一致。
4. **検証器再実行（達成）**: BigInt独立検証（`verify_win8_certificate_bigint_independent.mjs`）の
   出力が出版 `bigint-verification.json` と3根ともbyte-identical、
   Bareiss検証（`verify_win8_cert_bareiss.ts` root-check＋subroots全走査）の
   出力も3根ともbyte-identical。
5. **監査機械再実行（達成）**: 出版監査機（`assemble_win8_audit_root*.py`）を
   取得byteそのままのpristine複写で各rootにつき3回
   （同一cwd 2回＋隔離EXPERIMENT_ROOT cwd 1回）再実行し、
   出版監査正本 SHA-256 `d0653834…`〔K1136〕・`dafa177b…`〔K1137〕・
   `e706ca6f…`〔K1139〕 と**byte-identical**（19/19 gate PASS）。
   さらに本レーンがfresh生成したsummary/probe記録を差し替えての監査機実行も
   19/19 PASS・byte-identical（監査正本はms非依存データしか埋め込まないため成り立つ）。
6. **tamper 3件（達成・fail-closed）**: 出版社が試験していないoffsetでの改変が
   いずれもreturncode 1・監査未書込・gate failで捕捉された。
   (t1) 証明書本文offset 300007のXOR 0x01 → gate g16（第三手法全木走査）・
   g17（三手法集計一致）がfail。副次的な観察として、この改変はstrategy行由来であり
   `bareiss --root-check`（root行由来データのみ検査）はreturncode 0を返す。
   root-checkを唯一の防御としない**防衛の深さ**の実測記録である。
   (t2) 監査pin入力 `.input-k1086.json` offset 1111 → g01 pin fail。
   (t3) 本レーンfreshのext-summary-a1 move-1 nodes 2757→2758 → g11 fail。
7. **出版とguard（本dirがpart1に該当）**: 行を1つも閉じない。

## 行順序に関する実験事実（出版transport細部の確定）

出版ext-summary-a1/a2の行順序は、K1136/K1137はxargs挙動由来の数値順、
**K1139は辞書順**（`01` < `02` … < `58`ではなく `1` < `10` < … 型）であった。
本レーンの再実装はすべて数値昇順で行を書く。したがって行順序は
**publisher transport detailであり再現対象ではない**。比較は
 per-move値の照合（order非依存）と行集合一致で行い、per-move値は完全一致した。
監査正本の`line_order_note`にこの規約を機械可読で記録した。

## `ms`の扱い

ext-summary・probe記録の`ms`（wall-clock）は時刻依存のため再現対象外
（K1160の`wall_s`学知見と同型）。監査JSONは`ms`/経過時間を一切含まないため
battery全体がbyte決定的であり、3回のbattery全実行で監査正本SHAが一致した。

## 再現手順

```
python3 fetch_master.py        # pin commit 28d223a2d から61ファイル取得+git blob検証 → master/
python3 verify_cert_extract_ext_second_20261120.py --stage pin
python3 verify_cert_extract_ext_second_20261120.py --stage root --root k1136   # 約3分
python3 verify_cert_extract_ext_second_20261120.py --stage root --root k1137   # 約2分
python3 verify_cert_extract_ext_second_20261120.py --stage root --root k1139   # 約2分
python3 verify_cert_extract_ext_second_20261120.py --stage tampers
python3 verify_cert_extract_ext_second_20261120.py --stage finalize
sha256sum run/harness-audit.json   # → cf6a26abf0a459bcfb42bbb2d649ace5d3d1f1a5aee63a01af1de8b79d6a145f
```

各stageは300秒のコマンド上限内に収まる設計。実行環境はnode v22.20.0
（`--experimental-strip-types`）・python3.12・2コアで、抽出は並列度2（レーン方針どおり
控えめ）。battery 1巡は約8分（tamper込み）。`output/` 下のfresh生成記録
（probe・summary・bigint・bareiss・監査3回分・fresh-data差し替え分）は
seq3（3巡目）の成果物である。実行中にsandbox環境リセットが1回発生したが、
出版済み分には無影響で、当局pin表からmasterを再取得して再開した
（中断・リセットも実験事実として記録）。

## 同梱物

- `verify_cert_extract_ext_second_20261120.py`: harness本体（stage分割・43 gate・監査JSON出力）
- `fetch_master.py` / `pin-manifest.json`: 出版61ファイルの取得器とgit blob pin正本
- `output/harness-audit.json`: 監査正本（gate 43・status PASS・決定論的）
- `output/fresh/{k1136,k1137,k1139}/`: 本レーンfresh実行記録
  （`probe-fresh.jsonl`・`ext-summary-a1/a2/b.jsonl`・`bigint-fresh.json`・
  `bareiss-rc-fresh.json`・`bareiss-stats-fresh.txt`・`audit-r1/r2/r3.json`・
  `audit-freshdata.json`・`rows-a1/a2-bytes.txt`）

## 限界

本検証は「検証の検証」であり、**行を1行も閉じない**。残余行数・pool P^parallel
120,416根は不変。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4は
すべてUNKNOWNのまま。**
