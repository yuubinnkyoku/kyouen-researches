# K1166（fold29証明書抽出外部第二検証）のpristine再実行第三検証（2026-11-20）

## 位置づけ

K1166（K1136/K1137/K1139 WIN8-D10証明書抽出の外部再実行第二検証・出版実験dir
`n11-fold29-win8-cert-extract-ext-second-verification-20261120/`）に対する
**pristine再実行第三検証**である。単一オーナー宣言は
[宣言ノート](../../log/2026-11-20-n11-k1166-fold29-cert-extract-ext2-pristine-reexec-third-single-owner-note.md)
（commit `ec24b235f806822086680fee4075820679c78acf`・宣言時HEAD `1c42dcf25c…`）のとおり。
宣言の受入条件5項目はすべて達成した（受入条件と達成結果の詳細は
`output/reproduction.log`）。

第三の実行環境で、K1166の出版byte（harness
`verify_cert_extract_ext_second_20261120.py` SHA-256 `ca662e57…`・30,141 bytes・
取得器 `fetch_master.py` `c3c4c9ff…`・pin表 `pin-manifest.json` `949868e2…`・
出版監査正本 `cf6a26ab…`）を**1 byteも改変せず**に取得し、出版社の第二検証
battery全体を2巡実行した。

## 手法と結果

1. **出版byte pin（達成）**: main固定commit `1c42dcf25c…` からbyte 5点を取得し
   SHA-256照合（README `6605abff…`・fetch_master `c3c4c9ff…`・pin表 `949868e2…`・
   harness `ca662e57…`・監査正本 `cf6a26ab…`〔15,549 bytes・gate 43・PASS〕）。
2. **master再構成（達成）**: 改変なしの `fetch_master.py` でpin commit
   `28d223a2dd254b8a85cc342dff3f4bd801d1b31f` から出版社3実験dir全61ファイルを
   再構成し、git blob SHA照合 61/61（両batteryとも `all_blob_pins_ok: true`）。
3. **battery 1巡目（達成）**: stage分割（pin → root k1136 → k1137 → k1139 → tampers →
   finalize・各stage 1コマンド300秒上限内・実測 91.1/52.1/111.8/9.3 s）で
   harnessを改変なく実行し、**43 gate PASS・監査JSONが出版正本
   `cf6a26ab…` とbyte-identical**（cmp一致）。per-rootのprobe・抽出A1/A2/B・
   証明書組立（byte-identical）・BigInt・Bareiss・出版監査機pristine 3回＋fresh記録
   差し替えの各gateも両回とも全PASS。
4. **battery 2巡目（達成・環境独立性検査込み）**: 隔離cwd・隔離HOME・
   `PYTHONHASHSEED=random` でもう1巡完走し、**監査JSONがbattery 1巡目と
   byte-identical（parts 5点も全byte一致）**かつ出版正本ともbyte一致。
   K1166実験の「battery全体がbyte決定的」という主張を第三環境で確定。
5. **tamper 3件（達成）**: harness内蔵の改変試験3件（証明書本文offset 300007・
   pin入力offset 1111・fresh nodes 2757→2758）が両batteryともreturncode 1・
   監査未書込でfail-closed捕捉。
6. **第三検証record（達成）**: `scripts/assemble_third_record.py`（stdlibのみ・
   sorted keys・時刻/絶対path排除・fail-closed）がbyte 5点pin・両battery全gate・
   監査byte同一性・battery間byte同一性を再検査して
   `output/third-verification.json` を生成。**3実行（既定seed 2回＋`PYTHONHASHSEED=random`
   1回）でbyte一致**（SHA-256 `a6a3e048…`・4,363 bytes・gate 20・PASS）。
7. **負の制御（達成）**: 本レーン独自の出版社未試験offset（出版正本offset 8888の
   XOR 0x01）でassemblerがreturncode 1・record未書込でfail-closed捕捉することを
   実測。復旧後にrecord SHAが完全復元することも確認。

## 同梱物

- `scripts/assemble_third_record.py`: byte決定的record組立機（gate 20・fail-closed）
- `scripts/verify_part_gate_completeness.py`: 5 partの43 gateがpin済みauditを完全再構成するかを検査する補助器
- `tests/test_part_gate_completeness.py`: 8種類の合成改変試験（欠落・余分・重複・値改変・battery差・JSON重複key・audit順序）
- `scripts/reproduce.sh`: 詳細な再現手順（byte 5点取得・master再構成・両battery・record）
- `output/third-verification.json`: 第三検証record正本（`a6a3e048…`・gate 20・PASS）
- `output/reproduction.log`: 両batteryの実行記録・受入条件対照・負の制御
- `output/battery1/harness-audit.json` / `output/battery2/harness-audit.json`:
  本レーン2巡のharness監査（両者byte一致・出版正本ともbyte一致 `cf6a26ab…`）
- `published/`: 本検証で取得した出版byte 5点（SHA-256で機械照合に使用）

## 追補: part gate完全性のfail-closed検査（2026-11-21）

元の `assemble_third_record.py` はpartごとのgate辞書が非空で、存在するentryがすべてpassなら合格としていた。finalize後に同じgateが両batteryのpartから欠落しても、最終auditのSHA pinとpart間byte一致だけではpartの完全性を直接確認できない。

補助検証器 `scripts/verify_part_gate_completeness.py` は、pin済みaudit（43 gate・15,549 bytes・SHA-256 `cf6a26ab…`）を各batteryで再確認し、5 partのgateを次の完全分割として検査する。

| part | prefix | 期待数 |
|---|---|---:|
| pin.json | `g_pin_` | 1 |
| k1136.json | `k1136_` | 13 |
| k1137.json | `k1137_` | 13 |
| k1139.json | `k1139_` | 13 |
| tampers.json | `tamper` | 3 |
| **合計** | | **43** |

結合したgate辞書がauditの `gates` と値まで完全一致すること、part間重複がないこと、JSON objectの重複keyがないこと、2 battery間のpart bytesが一致することをfail-closedで確認する。成功時だけ `output/part-gate-completeness.json` を出力する。

`tests/test_part_gate_completeness.py` に8種類の合成改変試験を追加し、`reproduce.sh` は今後のbattery実行後に試験と補助検証器を呼ぶ。判定ロジックは合成43 gate fixtureで、正常分割PASS・欠落（両battery同時）/余分/重複/値改変の拒否を確認した。

**制約**: 元の2 batteryの `parts/` はGit管理されていないため、この補助検証を歴史的実行へ遡及適用したとは主張しない。元の第三検証record（20 gate・SHA-256 `a6a3e048…`）は不変。新しい検査は今後の再現実行で実partへ適用する。ゲームのverdict・receipt・S6行は変更しない。

## 限界

本検証は「検証の検証の検証」であり、**行を1行も閉じない**。残余行数・pool
P^parallel 120,416根は不変。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
すべてUNKNOWNのまま。**
