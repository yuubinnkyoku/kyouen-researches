# K1311 実行 log — 境界帯全多重度 collapse（publish-then-execute・継続 chain）

主張・手証明・機体宣言の正本は
[単一オーナー宣言ノート](2026-11-25-boundary-band-single-owner-note.md)
（出版 7653a639）。本 log は機械実行・公式監査・出版 chain の記録。

## 出版 chain

1. **宣言 7653a639**（着手時 HEAD 6247d6a5〔前実行 tarball〕・宣言 push 時観測
   HEAD 04c132fd〔Part EA kit・長期レーン・直交。着手以降の 10 commit はすべて
   Part DZ/EA の 11×11 canonical cache 採用系列で items/log への knowledge 変更
   なし〕・K1311 採番空きを commit 検索で確認（search 0 hits）・対抗宣言なし）。
   証明全文（§2.1 L-SDB 3 枝スライス・§2.2 二重帰納 typed mex・子型
   (A-a)/(A-b)/(B)/(C)・存在補題・区域代数 R-I..R-V）+ 機体宣言（12 電池
   counts・総計 12,409）+ 変異表 13 種を事前宣言。
   ※ 前実行からの続き: 宣言 push と kit push（e92542fd・13 ファイル）まで出版済み。
   本実行は「宣言ノート+kit の fetch-back byte 照合」のツール呼び出し結果が
   未受領だったため、fetch-back から再開した。
2. **fetch-back 14/14 byte 一致**（宣言ノート = sha256 9ccea925…・kit 13 ファイル）:
   get_file_contents で全ファイルを取得しローカル保存→sha256sum で宣言 pin と照合。
   verify_k1311.py = 4b5b81de…（19,093 B）・engine_block.py = 582c93c1…・
   explore_db.py = 5747cb9a…・explore_db.out = 6b48b840…・dryrun1-4.out は 4 走とも
   811d7ae3…・dryrun1-4.info はローカル predry 正本と同一・README.md はローカル
   正本と同一（README は MANIFEST 自己除外対象・pin 宣言外）。全ファイル一致。
3. **公式 4 走**（fetch-back bytes から）: 同一 cwd×2〔PYTHONHASHSEED=random/1〕+
   隔離 tree/env -i×2〔99/7〕。全走 rc=0・stdout byte-identical sha256
   `811d7ae3390ef43c94cc24f3ae5d77c32de179bc9336d468be49201997d44bdb`
   （= 宣言 = predry・約 2.2 秒/走・python 3.12）。
   counts `[240, 1628, 1353, 2303, 1659, 861, 1390, 1200, 747, 521, 7, 500]`
   総計 **12,409 bad 0**・engine_gate PASS。
4. **変異電池 13/13 fail-closed**（事前宣言どおり・全て初走で一致）:
   `--tamper-engine` rc=2（変異 sha `0ea47a80…` ≠ pin・stdout は mismatch 報告
   のみ）・np1〔D1〕228・np2〔D2〕1,540・np3〔D3〕1,297・np4〔D4〕2,295・
   ty〔D5 申立 flip〕1,659・ce〔D6〕838・tl〔D7〕1,390・fs〔D8〕1,199・
   kb〔D9〕747・ao〔D10〕512・ob〔D11〕7・rs〔D12〕490・すべて rc=1
   （per-battery bad 配列も宣言どおり対象電池のみ非ゼロ）。
5. **成果物 5cf2c639**（23 ファイル）: output/audit_run1-4.out+.info・
   tamper レコード 13 ファイル・detcheck.json（verdict **OFFICIAL-PASS**・
   公式 4 走・変異 13 種の申立/実測 per-battery 一致表・engine pin・
   published chain 収録）・MANIFEST-sha256（34 entries・README/MANIFEST
   自己除外の K1309 規約）。detcheck 生成スクリプトは clean counts・battery 名・
   engine sha・4 走 sha・変異 bad 配列をすべて assertion で検査してから書き出し。
   push 直前に最新 main を再取得（HEAD e92542fd のまま・競合なし）。
6. **fetch-back MANIFEST 全 34 行照合**: 成果物 push 後に MANIFEST-sha256 および
   新規 22 ファイルを取得し、全 34 行が fetch-back bytes と sha256 一致
   （kit root/predry は最初の fetch-back と同一 blob・重複パスなし）。
7. K item・run log・README bullet（本 commit）。

## 受入判定

- 4 走 byte-identical（同一 cwd 2 走 + 隔離 tree/env -i 2 走で sha 一致）。
- 電池 13/13 が事前宣言の正確な bad 数・rc で fail-closed
  （per-battery bad 配列も宣言どおり単一電池のみ非ゼロ）。
- fetch-back 全ファイル byte 一致（宣言→機体→成果物の出版 chain で bytes 不変
  ・MANIFEST 34 行全照合）。
- **verdict OFFICIAL-PASS**（detcheck.json・f3a33c08…）。

## 規約の再明記

- 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  全時点 UNKNOWN・verdict 不消費。
- census 12,409 点は定理の実機照合であって証明の代替ではない
  （全称性は宣言ノート §2 の手証明による）。
- tail 行 D7 は公刊 K0832 Lemma P 系の転写照合（接続記録のみ・再主張しない）。
  D11 OBS-BBL 凍結表は観測登録であり新規法則主張ではない。
- 下帯 k≤z+n−3（n≥3）は open（O-BBL）。K0832 予想 A（j=0）・C（j=1）は
  open のまま（予想 B のみ E=z+2 部分族として回収）。
- 宣言ノート §6 honest 記録: 初期探索スクリプトの昇順タプル E 誤計測
  （n=4..7 に偽の不一致 11+1）と typed options の tied-top 誤検出は
  宣言前に修正し凍結正本に反映済み。

## 次課題

- **O-BBL**: n≥3 の下帯 k≤z+n−3 の真の法則。OBS-BBL 凍結表
  （triples k=z 行・z=1..7・(80,80,68)→(80,0,0) の naive 不一致計数）が証人
  データ。予想 A/C の生息地。
- **O-DB2**: 区域 mex の内側 2 行（E=k−1, k の (C) 値遷移 3=1^2）の逆読みで
  下帯の typed 化が可能か（B 手 n−1 子が境界行 z+1 に落ちる構造）。
- **一般化**: r 人対戦版・d 次元版の境界行 collapse。
- **F2**: 11×11 giant レーンオーナーへの接続は記録のみ（採用判断はオーナー側）。
