# 単一オーナー宣言: 残余72行 replace9 whole-record第二検証（K1151）pristine再実行による第三検証

- 宣言時刻: 2026-11-20T15:06:08.710Z
- オーナー: 本レーン（n11 replace9 whole-record 再実行第三検証）。同一成果物の並走レーンが存在する場合は先着出版を優先し、後着は撤退して記録する（AGENTS.md 規則）。

## 対象

K1151（残余23行 代替9根 depth-10掃引〔K1146〕whole-record 独立第二検証、出版 commit `f7aa541f342d67b33f34fee2df5e31c262cb0691`・2026-11-20T14:41:19Z 出版・本レーンが同日出版）の実験一式（検証機・10入力snapshot・監査正本）の、出版後のpristine再実行第三検証。

出版 pin（上記 commit の raw CDN から取得し、本宣言前に照合済み）:

- 実験dir: `research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/`（13ファイル）
- 検証機 `scripts/verify_replace9_whole_record_20261120.py`: SHA-256 `e92fb7556a6f12c6e3cee06477e5387ddb6214cb58875e4ee3385010f9043e8a`
- 監査正本 `output/replace9-whole-record-second-verification-20261120.json`: SHA-256 `5888afb3e1c07f8555fbafc73fc0b9d1006b0a31c88bbdd55a0d8975c0cabcb4`（115,002 bytes）
- 10入力snapshot `output/.input-*.json(l)`: K1085 `5fdd342d…`・K1086 `3045e152…`・K1089 `808fbda1…`・K1091 `edd7ac84…`・K1095 `335eca5e…`・K1097 `2896deb0…`・cover-decision `c5aaf83e…`・probe-records `bdacf0e7…`・replace9 `e8f5d674…`・K1147外部監査 `17dbd6ab…`（検証機内部のfail-closed pinが全入力を照合する）

## 範囲

byte 同一の 13 ファイルに対して:

1. 検証機 pin（e92fb755…）・監査正本 pin（5888afb3…）の確認
2. 同一cwd 2回のpristine再実行、隔離tree複写+隔離cwd+隔離HOME 1回、隔離+PYTHONHASHSEED=random 1回の計4回。各実行の出力が出版監査とbyte一致（334 gate・0.2秒未満/回）
3. tamper test（10入力の1つを1 byte変更し、検証機のfail-closed pinが捕捉することの確認）
4. 検証harness自身の決定性（同一cwd 2回＋隔離cwd 1回の監査byte一致）

DFPNエンジンの再実行、残余行の閉鎖、K1149（全probe再実行第二検証）・K1147・K1148・K1153等の他成果の変更は行わない。また、出版社が本レーン自身であるため、本検証の意味は「出版byteをGitHubから再取得しただけで第三環境・第四〜第七環境相当で再現できること」（輸送・転写・記憶媒体を介さない独立検証可能性）の確定にある。

なお本宣言前に実施した事前 probe として 1 回の pristine 再実行（0.16秒・334 gate all_pass=True・出力 SHA-256 出版監査と一致）を兵站的事実として記録する。

## item 採番

本検証の item は K1155 を取得する（現 main の次の空き番号。K1150〜K1154 が取得済みであることを本宣言時に確認）。

## 解釈規約

本検証は行を1行も閉じない。WIN8-D10 candidate は証明書ではない。REFUTED-D10 は LOSS 証明ではない。node数・solved数を勝敗として読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
