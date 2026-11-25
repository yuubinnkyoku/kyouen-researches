# K1309 実行 log — 遷移窓合同行 collapse（publish-then-execute・単一 chain）

主張・手証明・機体宣言の正本は
[単一オーナー宣言ノート](2026-11-24-window-congruent-single-owner-note.md)
（出版 7041fd07）。本 log は機械実行・公式監査・出版 chain の記録。

## 出版 chain

1. **宣言 7041fd07**（着手時 HEAD 42cb2abc・K1309 空き確認後に push・
   証明全文+機体宣言+変異表 12 種を事前宣言）。
2. 宣言ノート fetch-back byte 検証: 直前実行でツール応答失敗により未確認
   だったものを、本 continuation 冒頭に curl で再取得して完了。
   `cmp` byte 一致・sha256 `c18b9f9c83d1f42b3a529b8333e55b187b80bc60c454fe4d293e0249cd7a8b57`。
3. **キット 3c11a737**（12 ファイル・`window-congruent-20261124`）:
   README.md（3,879B）・verify_k1309.py（21,367B・sha `cd1328e3…`・
   engine pin `bd5f22e4…` startup ゲート内蔵）・engine_block.py（`582c93c1…`・
   K1282..K1308 chain と同一 bytes）・explore_wc.py/.out（宣言前探索 X1..X8 凍結）・
   predry/dryrun1-4 (+.info・4 走 byte-identical `3b5aa0b1…`)。
   push 直前に最新 main を再取得（HEAD 7041fd07 のまま・競合なし・
   kit ディレクトリ空き 404 確認）。
4. **fetch-back 12/12 byte 一致**: verify/engine_block/explore_wc/predry 8
   ファイルは即時照合成立。README.md のみ初回 404
   （API contents では存在・size 3,879 確認）→ raw CDN 遅延と診断し
   retry 1 回で 200・sha `3be4982b…` 一致。「404 = 未出版」と誤診しないための
   API 側存在確認を先に行った点を honest 記録。
5. **公式 4 走**（fetch-back bytes から）: 同一 cwd×2〔PYTHONHASHSEED
  =random/1〕+ 隔離 tree/env -i×2〔99/7〕。全走 rc=0・stdout byte-identical
   sha256 `3b5aa0b153569026d1e3312d5e1a1a6ffb46a6046417e388fdd5f0c0049cc8dd`
   （= 宣言 = predry・約 1.2–1.3 秒/走・python 3.12）。
   counts `[10752, 3456, 3840, 888, 8736, 1344, 3740, 2600, 341, 35, 4680]`
   総計 **40,412 bad 0**・engine_gate PASS。
6. **変異電池 12/12 fail-closed**（事前宣言どおり・全て初走で一致）:
   `--tamper-engine` rc=2（変異 sha `0ea47a80…` ≠ pin・stdout は mismatch
   報告のみ）・wc1〔D1=10,752+D5=672〕11,424・wc2〔D2+D5〕4,128・
   wc3〔D3+D5〕4,512・bw〔D4〕888・ty〔D5〕8,736・be〔D6〕1,344・
   cp〔D7〕3,740・ps〔D8〕2,600・xg〔D9〕341・rw〔D10 凍結表 1 行〕1・
   ex〔D11〕4,680・すべて rc=1。
7. **成果物 7c0d311f**（22 ファイル）: output/audit_run1-4.out+.info・
   tamper レコード 12 ファイル・detcheck.json（verdict OFFICIAL-PASS・公式 4 走・
   電池 12 種の申立/実測一致表・engine pin・fetch-back 記録を収録）・
   MANIFEST-sha256（33 entries・README/MANIFEST 自己除外）。
   push 前に最新 main 再取得（HEAD 3c11a737 のまま・競合なし）。
8. **fetch-back 33/33 sha 一致**: MANIFEST 全行を raw fetch して照合。
   宣言ノート・キット・成果物を通じて bytes 不変。
9. K item・README bullet（本 commit）。

## 受入判定

- 4 走 byte-identical（同一 cwd 2 走 + 隔離 tree/env -i 2 走で sha 一致）。
- 電池 12/12 が事前宣言の正確な bad 数で fail-closed（検出器が単に壊れて
  いないことの双方確認）。
- fetch-back 全ファイル byte 一致（宣言→機体→成果物の出版 chain で bytes 不変）。
- **verdict OFFICIAL-PASS**（detcheck.json）。

## 規約の再明記

- 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  全時点 UNKNOWN・verdict 不消費。
- census 40,412 点は定理の実機照合であって証明の代替ではない
  （全称性は宣言ノート §2 の手証明による）。
- D10 非合同行凍結表は観測の再現性照合であり法則主張ではない。
- 宣言ノート §6 honest 記録: 機体初回構築で engine sha gate が block 誤りを
  即時検出（修正後に `cd1328e3…` として宣言）・§2.4 D1 表の初回誤算は
  D5 typed 検査との矛盾で宣言前に是正。

## 次課題

- **O1′**（非合同窓行の真の法則）: D10 凍結表が入力。非合同行の C 子が
  非合同行に落ちる自己参照 blocker の解除が本体。
- **O2**（床非合同行・OBS-BW 含む）: 同一 blocker。
- **F1**（K1308 から不変）: C-SUM 3 トークン typed 化。
- **F2**: 11×11 巨大レーンオーナーへの枝刈り格子拡大の記録のみ
  （採用判断はオーナー側）。
