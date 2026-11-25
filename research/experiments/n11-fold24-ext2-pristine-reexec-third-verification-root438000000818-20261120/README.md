# fold24外部第二検証（K1164）のpristine再実行第三検証（2026-11-20）

## 位置づけ

K1164（fold24 receipt fold＝K1140の外部第二検証・出版コミット `12b49de902`/`309d140861`/`afd5046663`）は、
出版社レーンが第三実装検証機による全再導出（gate 800）まで出版済みである。
本実験は、出版後の第三者が**出版byteとGitHubの固定参照だけから**K1164の監査正本をbyte再生できること
（pristine再実行第三検証）を確定するものである。単一オーナー宣言は
[宣言ノート](../../log/2026-11-20-n11-k1164-fold24-ext2-pristine-reexec-third-single-owner-note.md)
（commit `3c88de5ce4`・2026-11-20T19:15:00Z）のとおり、受入条件はすべて達成した。

harness `scripts/verify_k1164_pristine_third_20261120.py`（SHA-256
`f45aa1ac1d022c6517dd49f5e9bf151c0834ea82545410349fccb41d1ccd6d31`・14,351 bytes）は
stdlibのみ・fail-closed・時刻を持たない決定論的監査JSON 1点を出力する。
K1164検証機・fold24出版機・同梱監査機のいずれの実装も流用していない。

## 固定pin

入力は `staged/` 下の出版byte 12点（SHA-256 pinはharness内蔵・全件fail-closed）と、
出版済み `reconstruct_inputs.py`（SHA-256 `f4e1fa8e…`）を固定Git参照
`b91e85a99f0480f084835bdff51533d0cf5feaa8` で実行して再構成したW入力treeである。

- staged/k1164/はK1164実験dirの4ファイル（README・検証機 `9bc24e38…`・監査正本 `c7e10332…`・実行記録 `16b7678e…`）。
- staged/k1140/はfold24（K1140）出版実験dirの8ファイル
  （receipt `c4ab76d3…`・出版機 `f462733d…`・同梱監査正本 `49f330c6…`・再現log `cb01749a…`・
  `reconstruct_inputs.py` `f4e1fa8e…`・同梱監査機 `e0dbebe4…`・build_fold24.py `3c1e07fb…`・README `77c4ee40…`）。
- Wは本レーンが**2回独立に**再構成し、2回の全入力（70ファイル・61 pinが検証機側で再照合される分を含む）が
  byte一致した。harness正準W manifest digestは `1426b676…`（pin gate内蔵）。

## 実施内容と結果

監査正本 `output/harness-audit.json`（3,184 bytes・SHA-256
`efffaab8ad5693afe432fe6f66abea30ffd1eb2b7a3e524af65718057bda327e`・gate 66・status PASS）の内容:

- 出版byte pin 12/12照合とdouble reconstructionのW byte一致。
- K1164検証機のpristine再実行4回（同一cwd 2回・隔離cwd/HOME・隔離+`PYTHONHASHSEED=random`）。
  全実行でreturncode 0、監査JSONが出版監査正本 `c7e10332…` と**byte-identical**、
  stdout（gate 800・machine_runs 4・tamper_cases 2の要約JSON）も4実行で同一。
  各実行はfold24機4回再実行（fold23隔離rerun chain込み）・同梱独立監査の再実行・検証機自身のtamper 2件を含む。
- 本レーン固有のtamper 3件（出版社T-gateのoffset 777/12345とは別位置・別surface）:
  W `inputs/worklist.csv` offset 404・W fold23 receipt記録 offset 3456・pub receipt offset 2024の
  1 byte XOR 0x01が、いずれもreturncode 1・監査未書込・GATE FAILEDでfail-closed捕捉。
- harness監査正本は同一cwd 2回＋隔離HOME/cwd＋`PYTHONHASHSEED=random` の3実行でbyte-identical。
- smoke実行（単体の検証機default環境実行）も出版監査とbyte一致（実測49.8秒・出版社環境の49.5秒と同等）。

実験事実として、harness初版のW manifest digest定数はshell側正準形（`./`接頭辞）で計算されており、
harness自身のfail-closed digest pin gateがbattery前に捕捉した（K1158・K1160・K1164出版時の
pin転写typo捕捉と同じ防御パターンが第三検証側でも有効）。修正後のharnessが本正本である。

## 再現手順

```
python3 staged/k1140/reconstruct_inputs.py <W_A>          # 固定Git参照から61 pinを再構成（2回はbyte一致確認）
python3 staged/k1140/reconstruct_inputs.py <W_B>
python3 scripts/verify_k1164_pristine_third_20261120.py staged <W_A> <W_B> <workdir> <out_json>
```

1 batteryは約3分18秒（4回の検証機再実行＝fold24機16回再実行＋tamper 3件を含む）。
`<out_json>` がSHA-256 `efffaab8…` と一致すれば再現成立である。

## 限界

本検証は「検証の検証」であり、S6行・五親target行を1行も閉じない。
fold24 receiptが3行を閉じたのは出版社の成果簿計、K1164が外部第二検証の成立、
本項目はその第三者再現性の確定である。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4は**すべてUNKNOWNのまま**。
