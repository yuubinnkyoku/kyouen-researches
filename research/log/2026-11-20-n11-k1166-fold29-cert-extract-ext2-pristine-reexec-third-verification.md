# K1166（fold29証明書抽出外部第二検証）のpristine再実行第三検証（2026-11-20）

## 経緯と位置づけ

n11検証ラティスの未着手枠として残っていた「K1166第三検証」（K1136/K1137/K1139
WIN8-D10証明書抽出の外部再実行第二検証を第三環境で再現する工程）を本次実行で取得した。
着手前に最新main（`1c42dcf25c…`・2026-11-20T22:42Z）を再取得し、次の並走状況を確認した:

- K1168第三検証（fold21 ext2の第三検証）は並走レーン完了（commits `3e7447021b`〜`8eaa5edb7f`・
  K1168 itemへの記録と実験dir出版）。
- fold18 ext2（`c2e8eb09f7`）・fold19 ext2（`9606203aec`）は他レーン宣言済み着手禁止。
- K1166の第三検証を対象とする宣言・実験・logはmain上に存在しない（直近200 commit確認）。
- 出版社自身のpost-publication reproduction run（`7c1e765d88`）は出版社レーンの自家記録であり、
  第三環境によるpristine再実行の出版ではない。

単一オーナー宣言ノートを先行出版（commit `ec24b235f806822086680fee4075820679c78acf`・
宣言時HEAD `1c42dcf25c…`・受入条件5項目・fetch-back byte一致）。

## 実施内容

1. **出版byte pin**: main固定commit `1c42dcf25c…` からK1166実験dirのbyte 5点を取得し
   SHA-256照合（README `6605abff…`・fetch_master `c3c4c9ff…`・pin表 `949868e2…`・
   harness `ca662e57…`〔30,141 bytes〕・監査正本 `cf6a26ab…`〔15,549 bytes・gate 43・PASS〕）。
2. **master再構成×2**: pin commit `28d223a2d…` から61ファイルを`fetch_master.py`（改変なし）で
   2回再構成し、git blob SHA照合 61/61を両回確認（`all_blob_pins_ok: true`）。
3. **battery 1巡（素環境）**: stage分割（pin → root k1136 → k1137 → k1139 → tampers →
   finalize）でharnessをbyteそのまま実行。実測 wall time: fetch 13.9 s・pin 0.17 s・
   k1136 91.1 s・k1137 52.1 s・k1139 111.8 s・tampers 9.3 s。43 gate PASS・
   監査JSONが出版正本とbyte-identical。
4. **battery 2巡（隔離環境）**: /dev/shm隔離cwd・隔離HOME・全stage `PYTHONHASHSEED=random` でもう1巡
   完走。実測: fetch 11.4 s・k1136 89.3 s・k1137 51.7 s・k1139 111.3 s・tampers 8.9 s。
   43 gate PASS・監査JSONがbattery 1とbyte一致・出版正本ともbyte一致。
   **per-stage parts 5点（pin/k1136/k1137/k1139/tampers）も両battery間で全byte一致**。
5. **tamper fail-closed確認**: harness内蔵3件（証明書本文offset 300007・pin入力offset 1111・
   fresh nodes 2757→2758）が両batteryともreturncode 1・監査未書込で捕捉。t1での
   `bareiss --root-check` returncode 0・監査機g16捕捉の防衛の深さも再実測。
6. **第三検証record**: `assemble_third_record.py`（新規・stdlibのみ・fail-closed・sorted keys・
   時刻/絶対path排除）がbyte 5点pin・両battery全gate・監査byte同一性・battery間同一性を再検査して
   `third-verification.json`（gate 20・PASS・`a6a3e048…`・4,363 bytes）を生成。
   3実行（既定seed 2回＋`PYTHONHASHSEED=random` 1回）でbyte一致。
7. **負の制御（本レーン独自offset）**: 出版監査正本offset 8888の1 byte XOR 0x01で
   assemblerがreturncode 1・record未書込（fail-closed）・復旧後にrecord SHA完全復元を確認。

## 実験事実・知見

1. **重いbatteryの第三検証はstage分割300秒制限内で完走可能**: 総括約8分の重計算battery
   （3根×probe/extraction/監査機複数回）は、出版byteのpin取得からfinalizeまで
   6 stageに分割することで、300秒コマンド上限の第三環境で中断なしに完走した。
   実測stage時間は出版時・postpub時（13.0/90.0/52.8/112.2 s）と環境差の範囲で一致。
2. **battery間byte一致はparts単位まで及ぶ**: 出版社の主張は「3回のbattery全実行で監査正本SHAが一致」
   （finalize出力の一致）だった。本検証では両batteryの監査JSONに加えてper-stage parts 5点が
   すべてbyte一致することを確認し、battery全体の再現性を段階単位で直接立証した。
3. **file_system.read_fileの1ファイル直読みpush**: K1166第二検証レーンの「push_filesのcontentは
   read_fileでローカル原稿を直接読んで渡す」方式を1ファイルずつの直読みに拡張し、
   part1 12ファイル（125 KB）がpush 1回でfetch-back 12/12 byte一致。read_fileの
   文字数ベース長さとbyte数の確認（ASCII fileは一致・日本語混在fileは3バイト文字差）も
   恣意的な転写を行わない構成で成立した。
4. 第三検証record組立機は「監査JSONのSHA比較」型とは異なり、fail-closedの再検査を
   20 gate独立に持つ（byte 5点pin・両battery各5 partの全gate再検査・監査同一性・battery間
   同一性・サイズ確認）。K1165/K1170系列の「第三検証harness」と位置づけは同じで、
   対象がfold receiptではなく証明書抽出の第二検証batteryである点が新しい。

## 結果の意味

- K1136/K1137/K1139のWIN8-D10証明書抽出（per-root nodes総計 A1 3,539,166/1,399,389/3,515,506・
  B 2,564,865/1,057,553/2,808,991・証明書byte `dbcb0bae…`/`7bd64a47…`/`089e175d…`）は、
  出版社・第二検証者・第三検証者（本レーン・別sandbox・別環境変数）の3環境で
  監査含め全gateが再現した。
- K1166の出版主張はすべて第三環境で再現: master 61 pin・probe両AND順序・抽出A1/A2/B・
  証明書byte同一・BigInt/Bareiss byte同一・出版監査機19/19（3回+fresh差し替え・3根）・
  harness監査43 gate byte-identical・tamper 3件fail-closed。

## 出版

- 宣言: commit `ec24b235f806822086680fee4075820679c78acf`（fetch-back byte一致・SHA-256 `5777a519…`）。
- part1: commit `4eb2205e7fcb30e34fcbb8bdd658ad82c27c513e`（実験dir
  `research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/`
  12ファイル・fetch-back 12/12 byte一致）。
- part2: knowledge item K1172＋本log。
- part3: knowledge README末尾bullet。

## 解釈規約

本検証は「検証の検証の検証」であり、行を1行も閉じない。残余行数・pool P⁗ 120,416根は不変。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
