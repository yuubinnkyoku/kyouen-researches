# fold16（root 8890020）単体の外部第二検証 — 実行記録（2026-11-21）

study log: 宣言から出版まで。対象は fold16 receipt fold
（第23 receipt・6番目WIN8 receipt fold・root `00000000010000889002000080100000`・
K1113証明書・出版実験 `research/experiments/n11-residual55-win8-receipt-fold-root8890020-20261120/`）
の外部第二検証（単体ext2）。

## 1. 宣言と着手時状況

- 単一オーナー宣言: `research/log/2026-11-21-n11-fold16-external-second-verification-single-owner-note.md`
  （commit `c6a55000`・2026-11-21T01:55:00Z想定）。着手時点でmain HEADの
  直近がfold15宣言ノート（`0a1a52d4`）と並走のK1177 band extension・
  K1178系partコミットであることをlist_commitsで確認し、fold16単体ext2の
  先行宣言なしを確認済みで着手（fold15単体ext2は`0a1a52d4`で宣言済みのため
  着手禁止・本レーンはfold16のみ）。
- 検証機はfold14外部第二検証の出版済み検証機
  （commit `23de00dc`・sha256 `d966dad5…`）を土台に
  fold16固有の外科手術と定数差替で構成（builder `build_verify16.py` は
  exact-match rep・出現回数assert 33置換でfail-closed・SRC SHA照合つき）。

## 2. W16ローカル破損と完全復旧（実験事実として記録）

- battery初回PASS後のcleanup作業中に、誤って広すぎるglob
  （`-path "*output*"`の`*.json`一括削除）がW16のpinned record群
  （fold11-15 receipt・K系監査・証明書等、I段のsha256 pin対象約20ファイル）を
  削除した。出版repo側の正本は無事。
- 再構成機（scripts/reconstruct_fold16_inputs.py・HEAD pin `c6a55000`）の
  再実行が出版repo byteのみからW16入力tree 43ファイルを完全復旧
  （12 blob + 25 SHA-256全pin照合・pin表部分集合鎖
  F11(10)⊂F12(13)⊂F13(16)⊂F14(19)⊂F15(22)⊂F16(25)の再確認つき）し、
  fold16機pristine run（46秒・rc 0）のreceipt byte一致まで復旧した。
- またbattery run2の1回目は実行環境のinfraエラー（Koyeb remote command
  失敗）で出力書込前に中断した。scratch treeを除去して清掃状態から
  batteryをやり直し、3実行byte一致を正規に完了した
  （中断時点で成果扱いはしていない）。
- 中間状態をローカルaloneに残さない設計の実地検証
  （K1179の実行環境リセットpanic-recoveryと同種の効果・本件は
  オペレーションミス由来）。

## 3. 検証バッテリ（正規実行）

1. **W16/pub16f再構成**（reconstruct_fold16_inputs.py）: 37 pin全照合・
   5機pin部分集合鎖の機械確認。fold16機pristine run・rc 0・46秒・
   receipt byte-identical（`edd55258…`）。
2. **検証機run1**（通常cwd・デフォルト環境）: **1061 gate全PASS**
   （P 12 / I 75 / C 932 / X 26 / T 16）・210秒・監査sha256 `09f80902…`。
3. **run2**（同一cwd・反復）: 1061 gate PASS・監査sha同一 byte一致。
4. **run3**（隔離cwd・HOME差替・`env -i`・`PYTHONHASHSEED=random`）:
   1061 gate PASS・監査sha同一 byte一致（env -i下ではPATHに
   `/usr/local/bin`の明示が必要な点に注意）。
5. fetch-back: 出版commit固定raw URLで5ファイルsha256照合（5/5一致）。

## 4. 主な観察（監査JSON observations該当）

- **IV.source_record清潔記載の維持**: 出版fold16 receiptの
  `independent_verification.source_record` はK1113実験
  （`n11-residual58-win8-cert-extract-root8890020-20261120`）を正しく指す。
  fold12（K1175）・fold15（K1179）のstale参照erratumの直後であるが、
  fold16は自実験dirを記載している。byte-true gateで照合し、erratum対照として
  記録するのみでreceipt byteは変更しない。
- **closed-before-this-receipt 1行を含むWIN8 rootとして2例目**
  （fold14 rootが初例）: 28 canonical行のうち
  `00000000000000003800000008003000` はfold13 receipt閉鎖済みで、
  coverage 5行には含まれない。二重閉鎖の構造的除外をclosed_history全履歴・
  worklist・residual55の三方照合で確認。
- **1061 gateへの増分**: fold15検証機（981 gate）との差分として
  I段が5機pin鎖（fold15機表の追加とfold16機表25 sha化）で75 gateに、
  C段がfold15 join・K1113 19 gate・fold16 coverage/parent/target/
  win16 retire構成の再導出で932 gateになった。検証機1実行は約210秒
  （X batteryにfold16機4回＋fold15機1回の純実行を含む）。

## 5. 受入条件対照（宣言ノート）

- 宣言受入条件はK1173系列と同一の定型（出版byte pin・W再構成・機械pristine
  4回・上流機独立実行・chain再構成・値単位再導出・tamper 2件・監査3実行
  byte一致・解釈ガード）。全条件を検証機がgateとして実装し、3実行すべてで
  PASSした。

## 6. 出版

- part1（本実験dir）: 5ファイル（README・再構成機・検証機・監査正本・
  reproduction.log）を単一push。push直前HEAD `563cf9b6`（fold15単体ext2の
  K1179 part1-3・宣言ノート2件・K1177系を確認し、fold16系への競合なしを
  確認）。出版commit `056b8470`・fetch-back sha256照合 5/5一致。
- part2: knowledge item K1180（K1113系列・依存K1116/K1113/K1097）＋本log。
  K番号は3点確認（items dir探索・knowledge README・code searchすべてK1180
  未使用）の上でK1180を取得（README最大既存はK1179）。並走との衝突時は
  先着優先・本レーンは必要に応じて再採番する。
- part3: knowledge README K1180 bullet追記。
- バッテリ3実行・諸SHA・コピー検証の内容差異に時刻依存・乱数依存なし
  （監査JSONは決定的）。

## 7. 位置づけ

- 本検証は検証の検証であり、行は1行も閉じない。WIN8-D10証明書は当該8石rootの
  ゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数・
  coverage数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**

