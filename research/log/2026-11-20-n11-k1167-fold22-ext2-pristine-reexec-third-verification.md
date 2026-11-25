# K1167（fold22外部第二検証）pristine再実行第三検証 2026-11-20

## 実行の位置づけ

前回の長期レーン実行でfold22 receipt fold の外部第二検証レーン（K1167）が
part1〜3を出版したことを受け、本実行はその第三検証を単一オーナーとして実施した。
対象と手続きは fold24/K1164第三検証（K1165）と同一の
「出版byte→W再構成→pristine再実行→tamper探針→harness監査」である。

## 単一オーナー宣言

- ノート: `research/log/2026-11-20-n11-k1167-fold22-ext2-pristine-reexec-third-single-owner-note.md`
- commit `53501d73`（宣言時点でfold22 ext2 pristine-reexec laneは不在。
  fold21 ext2 lane（`98c90cb510`/`d323e780f9`）が別系統として稼働中であることに留意）。
- 受入条件6項目: (1) K1167出版5ファイルのpinned commit再取得とSHA-256照合、
  (2) 同梱再構成機の固定ref 2回独立実行とW tree byte一致、
  (3) 出版検証機のpristine再実行4回と監査byte一致、
  (4) 本レーン独自offsetのtamper 3件fail-closed、
  (5) harness監査の決定性（3実行byte一致）、(6) stage分割設計。

## 実施内容（harness `verify_k1167_fold22ext2_third_20261120.py`・SHA-256 `2f6290bf…`）

stage分割: pin | reconstruct-w1 | reconstruct-w2 | wcmp | rerun-r1..r4 | tampers | finalize。
stdlibのみ・fail-closed（不一致でstage record未書込・exit 1・失敗時も記録保存の例外を明示）。

1. **pin**（6 gate）: K1167出版5ファイルをpinned commit `4eb6cbf05` から再取得し
   SHA-256照合。5/5一致（README `6b32ce99…`・reconstruct `dfa50996…`・
   verifier `ca11cbbc…`・監査 `b4b082f8…`・log `5059c458…`）。
2. **reconstruct ×2**: 固定ref `34c29854c64286bbb1792ff28dc1973aef341e20` で2回。
   **実験事実**: 試行1回目はapi.github.comの403 rate limit（quota 0・21:45:19Zリセット・
   並走レーンとの共有IP無認証枠の共喰い）でfail-closed中断・記録保存し、
   リセット後の再試行で2回とも成功（workaround不使用）。pub 4・blob 12・sha256 48行
   （43 PIN256 pin + 5 chain機・fold21機はfold22機55 pinの部分集合として配置）。
3. **wcmp**（10 gate）: 2本のW treeが60ファイル・14,673,721 bytesで全ファイルbyte一致。
   manifestのpath欄は対象外・ref/pin数/機械リスト一致。fold22出版byte 4点は
   両pub copyでSHA-256照合かつ相互byte一致。
4. **rerun r1..r4**: r1/r2同一cwd・同一W1（in-place反復・出版検証機自身のx1/x2方式と同じ）、
   r3は独自再構成W2 + 隔離cwd/HOME、r4はW2のfresh copytree + 隔離cwd/HOME +
   `PYTHONHASHSEED=random`。全4回returncode 0・stderr空・stdout
   `ALL 1463 GATES PASS` + UNKNOWNガード行・出力監査SHA-256 `b4b082f8…` が出版正本と
   byte一致。r1実測35.0秒（user 28.7秒・fold22機6回起動込み・出版時実測約34.4秒と整合）。
5. **tampers**（3探針・本レーン独自offsetでfold22出版社・K1167レーン双方が未試験）:
   t1 copytree Wの `inputs/worklist.csv` byte offset 1234 XOR 0x01 →
   `W blob pin inputs/worklist.csv`・rc=1・監査未書込。
   t2 copytree Wの `k1125/certs/win8-root-00000000000000801202000000840500-20261120.n11`
   byte offset 17522 XOR 0x01 → `W sha256 pin …`・rc=1・監査未書込。
   t3 K1167実験dir写しの出版監査 byte offset 4096 XOR 0x01 →
   本harnessの実験dir pin gateが `pin mismatch output/external-audit.json` で捕捉。
   機械内T-gate（出版社offset）・検証機I-section gate（W pin）・harness pin gateの
   三層防衛が互いに独立なoffsetで実測作動。本番W・pubは無改変。
6. **finalize ×3**: harness監査正本 `output/harness-audit.json`
   （4,853 bytes・SHA-256 `fdb72c40…`・finalize 9 gate・時刻フィールドなし）が
   同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random`の3実行でbyte一致。
7. **post-battery再照合**: W1/W2/W4ともfold22機の入力55 pin（12 Git-blob + 43 SHA-256）
   がbattery後にすべて無改変（fold22/output receipt の追記のみ・61ファイル）。

## 出版とfetch-back検証

- part1（実験dir `research/experiments/n11-fold22-ext2-pristine-reexec-third-verification-root840500-20261120/`・
  README.md・scripts/verify_k1167_fold22ext2_third_20261120.py・output/reproduction.log・
  output/harness-audit.json の4ファイル）: 初回commit `41053a7d`。
  **実験事実（転写タイポ）**: 初回pushのREADMEに転写1文字の打鍵タイポ（1 byte）があり、
  fetch-back byte検証が即捕捉。訂正push `bf54c57f`（修正と同時に別位置に新タイポ発生を
  再びfetch-backが捕捉）→ `0ac8dc31`（String.rawがエスケープbyteを保持する問題で
  backslash混入・fetch-back捕捉）→ `b40f4668` で最終的に4/4 byte一致を確認。
  README最終SHA-256 `6f6ceb0a…`（8,232 bytes）。
  最終版fetch-backはpinned commit `b40f4668` のraw URLで4ファイルともcmp一致。
- part2（本ファイルとknowledge item `K1170-n11-fold22-ext2-pristine-reexec-third-verification.md`）:
  K番号はpush直前に三点確認（items README grepでK1170不在・候補item 404・README末尾参照なし。
  K1168=fold21外部第二検証・K1169=n8-ge16 partition fresh complete search は並走レーン取得済み）。
- part3: knowledge README末尾bullet追記（HEAD pin取得→末尾確認→push直前HEAD移動チェック→
  fetch-back byte一致確認）。

## 限界（解釈規約）

本実験はK1167監査の決定性・入力pin・fail-closed防衛の再検査であり、
S6行・五親target行を1行も閉じない。fold22 receipt自体の6行閉鎖（残余35→32行）は
Publisherの成果簿記であり、K1167はその外部第二検証、本実験はその第三検証である。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4は
すべてUNKNOWNのままである。**
