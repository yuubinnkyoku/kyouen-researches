# fold15（root 120000038）単体の外部第二検証 — 実行記録（2026-11-21）

study log: 宣言から出版まで。対象は fold15 receipt fold
（第22 receipt・5番目WIN8 receipt fold・root `00000000012000003800080009000000`・
K1114証明書・出版実験 `research/experiments/n11-residual58-win8-receipt-fold-root120000038-20261120/`）
の外部第二検証（単体ext2）。

## 1. 宣言と着手時状況

- 単一オーナー宣言: `research/log/2026-11-21-n11-fold15-external-second-verification-single-owner-note.md`
  （commit `0a1a52d4`・2026-11-21T01:26:36Z）。着手時点でmain HEADが宣言コミット
  であることをlist_commitsで確認し、先行宣言なしを確認済みで着手。
- 検証機はfold14外部第二検証の出版済み検証機
  （commit `23de00dc`・sha256 `d966dad5…`）を土台に
  fold15固有の外科手術と定数差替で構成（builderはexact-match rep・
  出現回数assertでfail-closed）。

## 2. 環境リセットとpanic-recovery（実験事実として記録）

- 検証機初バッテリrun1の直後（981 gate PASS・約105秒を一度確認した段階で）
  沙緒実行環境がリセットされ、ローカル作業ファイル（W15 tree・検証機・
  監査JSON・builder等）を全喪失した。出版repo側の正本は無事。
- この時点で出版済みだったのは宣言ノートのみ。しかし再構成機
  （scripts/reconstruct_fold15_inputs.py・HEAD pin `0a1a52d4`）が設計通り機能し、
  W15入力tree（12 blob + 22 SHA-256全pin照合）と出版byte（receipt
  `bae2b3c1…`・machine `03000c14…`・README `c1cd6768…`）を約8.6秒で完全再構築し、
  fold15機pristine run（23.1秒）のreceipt byte一致まで復旧した。
- 検証機はrepoから再取得したfold14検証機（byte照合 `d966dad5…`）からbuilderを
  再投入して再構築（62,390 bytes・sha256 `ade19de2…`）し、バッテリ全体を
  最初からやり直した。重要な中間状態をローカルaloneに残さない設計の実地検証
  （単一撤退可能点: builderそのもの。builderは積み上げた全修正を1ファイルに
  焼き込む形で再投入した）。

## 3. 検証バッテリ（再構築後の正規実行）

1. **W15/pub15f再構成**（reconstruct_fold15_inputs.py）: 34 pin全照合・
   fold11⊂fold12⊂fold13⊂fold14⊂fold15 pin部分集合鎖の機械確認（8.6秒）。
   fold15機pristine run・rc 0・23.1秒・receipt byte-identical。
2. **検証機run1**（通常cwd・デフォルト環境）: **981 gate全PASS**
   （P 12 / I 64 / C 863 / X 26 / T 16）・105.6秒・監査sha256 `6800759e…`。
3. **run2**（同一cwd・反復）: 981 gate PASS・105.1秒・監査sha同一 byte一致。
4. **run3**（隔離cwd・HOME差替・`PYTHONHASHSEED=random`）: 981 gate PASS・
   監査sha同一 byte一致。
5. fetch-back: 出版commit固定raw URLで5ファイルsha256照合（5/5一致）。

## 4. 主な観察（監査JSON observations該当）

- **source_record stale参照erratum（fold12型の再発）**: 出版fold15 receiptの
  `independent_verification.source_record` がfold14証明書抽出実験
  （`n11-residual65-win8-cert-extract-root9090022-20261120`）を指している。
  fold13/fold14 receiptは実験dirを正しく記載した直後の再発で、
  receipt生成テンプレートの陳腐化が示唆される。当該欄はbyte-trueでgateし、
  erratumとして記録するのみでreceipt byteは変更しない。
- **53-mobility root初のreceipt fold**: root合法手53をsurvival規約再実装で
  独立再導出（K1114 extraction 2,723,200/2,141,807 nodes・third_method
  11,338終端の再照合を含む）。
- **6行全閉鎖・余剰3行の初事例**: 28 canonical行分類は
  closed-before-this-receipt 0行（fold14の1行とは対照的に閉鎖済み行を含まず）、
  receiptは6行すべてをこのfoldで閉じる。うち3行は五親target行・3行は
  target外worklist行（1 receiptで複数のtarget外余剰行を閉じた初事例）。

## 5. 受入条件対照（宣言ノート）

- 宣言受入条件はK1173系列と同一の定型（出版byte pin・W再構成・機械pristine
  4回・上流機独立実行・chain再構成・値単位再導出・tamper 2件・監査3実行
  byte一致・解釈ガード）。全条件を検証機がgateとして実装し、3実行すべてで
  PASSした。

## 6. 出版

- part1（本実験dir）: 5ファイル（README・再構成機・検証機・監査正本・
  reproduction.log）を単一push。push直前HEAD `c6a55000`（並走fold16宣言ノート
  ・K1177 band extension・fold14系列partコミットを確認し、fold15系への
  競合なしを確認）。出版commit `2e1bc1ea`・fetch-back sha256照合 5/5一致。
- part2: knowledge item K1179（K1114系列・依存K1115/K1114/K1097）＋本log。
  K番号はREADME上の最大既存K1178を確認の上K1179を仮定
  （remo lane（commit `644182655f`）がK1178を仮定していたが既にfold14系列が
  使用済みのため再採番規則に従う。並走との衝突時は先着優先・本レーンは
  必要に応じて再採番する）。
- part3: knowledge README K1179 bullet追記。

## 7. 位置づけ

- 本検証は検証の検証であり、行は1行も閉じない。WIN8-D10証明書は当該8石rootの
  ゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数・
  coverage数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**
