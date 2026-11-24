# K1310 実行 log — 遷移窓非合同行 collapse（publish-then-execute・単一 chain）

主張・手証明・機体宣言の正本は
[単一オーナー宣言ノート](2026-11-24-ncw-window-single-owner-note.md)
（出版 7b992b5f）。本 log は機械実行・公式監査・出版 chain の記録。

## 出版 chain

1. **宣言 7b992b5f**（着手時 HEAD ffde117b・push 時観測 HEAD fdb3ceba・
   K1310 採番空きを commit 検索で確認（search 0 hits）・Part DX batch-36並走
   レーンは直交・対抗宣言なし）。証明全文（§2.0–§2.6 区域 mex 代数・
   パリティ不変量 P1–P5・C-descent 非合同性保存・K1309 packet との差分）+
   機体宣言（12 電池 counts・総計 51,439）+ 変異表 13 種を事前宣言。
   ※ 前実行からの続き: 宣言 push の呼び出し結果が未受領だったため、本実行は
   list_commits による push 成功確認から開始した。
2. 宣言ノート fetch-back byte 検証: raw 取得 200・sha256 は宣言 pin
   `3c2eb517…`（stdout）と対になる本文 26,623B を API/raw 両面で照合。
3. **キット e6ea44fb**（13 ファイル・`ncw-window-20261124`）:
   README.md・verify_k1310.py（22,098B・sha `58fd5e46…`・engine pin
   `bd5f22e4…` startup ゲート内蔵）・engine_block.py（`582c93c1…`・
   K1282..K1309 chain と同一 bytes）・explore_ncw.py/.out（宣言前探索
   X1..X8 + L2 補題 108,000 凍結）・predry/dryrun1-4 (+.info・4 走
   byte-identical `3c2eb517…`）。push 時に最新 main を再取得（HEAD 7b992b5f
   のまま・競合なし）。K1309 キット README（3,879B）を形式テンプレートとして
   踏襲（想定 3,879B→K1310 版は 4,632B・ファイル sha 表・電池表・変異表・
   監査プロトコル・規約の全節を維持）。
4. **fetch-back 9/9 byte 一致**: verify_k1310.py・engine_block.py・
   explore_ncw.py/.out・dryrun1-4.out 全ファイルが宣言 pin sha256 と
   byte 一致（初回 raw 取得で全ファイル 200・CDN 404 retry 不要）。
   dryrun1-4.out は 4 走とも sha `3c2eb51742c568536b0bf67738be3c2f7b59bf87ae8a1eba42e28ead11168949`。
5. **公式 4 走**（fetch-back bytes から）: 同一 cwd×2〔PYTHONHASHSEED
   =random/1〕+ 隔離 tree/env -i×2〔99/7〕。全走 rc=0・stdout byte-identical
   sha256 `3c2eb517…`（= 宣言 = predry・約 2.5 秒/走・python 3.12）。
   counts `[12096, 5760, 4320, 2058, 9016, 1512, 3870, 4960, 372, 1295, 4680, 1500]`
   総計 **51,439 bad 0**・engine_gate PASS。
6. **変異電池 13/13 fail-closed**（事前宣言どおり・全て初走で一致）:
   `--tamper-engine` rc=2（変異 sha `0ea47a80…` ≠ pin・stdout は mismatch
   報告のみ）・np1〔D1〕12,096・np2〔D2〕5,760・np3〔D3〕4,320・bd〔D4〕
   2,058・ty〔申立関数 P/Bm flip〕40,690（D1+D2+D3+D4+D5+D10 主張部分
   1,260+D11+D12・D6–D9=0 は申立関数を参照しない engine 照合電池故の
   honest 値）・be〔D6〕1,512・cp〔D7〕3,870・ps〔D8〕4,960・xg〔D9〕372・
   rw〔D10: 申立 1,260+凍結表 '3,2' 行改変 1〕1,261・ex〔D11〕4,680・
   bs〔D12〕1,500・すべて rc=1。
7. **成果物 73aa36d6**（23 ファイル）: output/audit_run1-4.out+.info（info は
   run 名・rc 追記の K1309 形式）・tamper レコード 13 ファイル・
   detcheck.json（verdict **OFFICIAL-PASS**・公式 4 走・変異 13 種の申立/実測
   per-battery 一致表・engine pin・fetch-back 記録収録）・MANIFEST-sha256
   （34 entries・README/MANIFEST 自己除外の K1309 規約）。
   detcheck 生成スクリプトは clean counts・battery 名・engine sha・4 走 sha・
   変異表 bad 配列をすべて assertion で検査してから書き出し。
8. **fetch-back 照合**: 成果物 push 後に MANIFEST 全行の raw fetch 照合で
   bytes 不変を確認（後述のとおり publish 後実施）。
9. K item・README bullet（本 commit）。

## 受入判定

- 4 走 byte-identical（同一 cwd 2 走 + 隔離 tree/env -i 2 走で sha 一致）。
- 電池 13/13 が事前宣言の正確な bad 数・rc で fail-closed（検出器が単に壊れて
  いないことの双方確認・per-battery bad 配列も宣言どおり）。
- fetch-back 全ファイル byte 一致（宣言→機体→成果物の出版 chain で bytes 不変）。
- **verdict OFFICIAL-PASS**（detcheck.json）。

## 規約の再明記

- 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  全時点 UNKNOWN・verdict 不消費。
- census 51,439 点は定理の実機照合であって証明の代替ではない
  （全称性は宣言ノート §2 の手証明による）。
- D10 OBS-NCW 凍結表サブサンプションは観測→定理実例の昇格確認であり
  新規法則主張ではない。O-G2（3 山以上の窓面）と F1（C-SUM 3 トークン）は
  open のまま。
- 宣言ノート §6 honest 記録: L2（B-exit 一様則）の初版手分析は g=z 分岐を
  σ=2 と誤予測したが、出版前の機械追試 108,000 点（z2..60・NCW 全 k・
  g≤120・bad 0）で (g+1)%2 一様に修正（mex 閉包への影響なし）・predry 初回
  rc=127（シェル起動の一次的な失敗・再実行で解消）・D3 note 欄・`None or`
  構文の是正、をすべて宣言段階で記録済み。

## 次課題

- **O-G2**: 内面 k≥1・3 山以上の窓面（multi-c web）。2 山 packet が単一 R
  強帰納で閉じた点を typed 化の足がかりにできるか。
- **F1**: C-SUM 3 トークン typed 化（K1308/K1309 から不変）。
- **L2 の一般化**: B-exit 一様則の m>1・r 人版。
- **F2**: 11×11 巨大レーンオーナーへの枝刈り格子拡大の記録のみ
  （採用判断はオーナー側）。
