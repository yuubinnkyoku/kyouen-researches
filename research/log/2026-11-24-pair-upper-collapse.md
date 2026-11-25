# 上半畳み込み実行 log（fast lane・K1308）— 2026-11-24

単一オーナー宣言 `research/log/2026-11-24-pair-upper-collapse-single-owner-note.md`
に従う publish-then-execute の全記録。

## 実行順序

1. **着手・最新 main 確認**: 観測 HEAD `295b9505`（Part DW 完了 log 22:16:48Z・
   11×11 b35loss26 canonical adoption・規約どおり verdict 不消費）。
   AGENTS.md・knowledge README を再確認。items/log 系列から:
   K1303 公刊 (`4e132464`)・K1304/K1305（PG(2,9)）・K1306 宣言 (`53d2d335`・SLB/L/E
   typed ladder)・K1307仮宣言 (`4d2d506a`・REMO 3-branch r=3 sweep) を確認。
   本 package の領域（ペア上半 k ≥ z・床 k ≥ z・全 plane）は untouched
   （O-G4 として K1303 が残した开放置）→ **K1308 を採番**（衝突時再採番規約）。
2. **宣言前探索**（explore_upper.py・frozen）: E1 T-UH 3,600+far 2,592 bad 0・
   E2 T-DU′ 630+210 bad 0・E3 Z-DIAG 1,152+450 bad 0・E4 窓非合同行 29 反例
   （z3 clean・z≥4: 5/2/8/4/10）・E4b 合同行 1,296 点（z3..13）clean → OBS-WC・
   E5 L-SB 2,520 bad 0・E5b 境界読み 103 bad 0・E6 C-SUM 3 重 1,344 / 混合 840 /
   4 重 180 bad 0・E6b 混合の早期安定化 obs・E7 cross-engine 720 bad 0・
   E8 シャープネス（床 k=z−1: z1→1, z2→2, z3..6→0・対角 g=z+1 → 2）・
   E9 面 0/1/2 上半閉包 648 bad 0。
3. **機体構築** verify_k1308.py（K1303 wrapper 踏襲・engine block は chain から
   byte 流用（pin bd5f22e4…）・D1–D11）。電池設計瑕疵を宣言前に 2 件是正
   （honest 記録・宣言ノート §2.6）: (a) K1286 T-B0 の定義域 2m+j≥0 を欠いた
   b0 電池（2 域外 cell を除外し D6 count 1,941）・(b) tamper=ty で z=0 床
   10 cell が正当通過するため期待 bad は 1,502（全 1,512 中）。
4. **predry 4 走**: 同一 cwd×2（PYTHONHASHSEED=random/1）+ 隔離 tree/env -i×2
   （99/7）すべて rc=0・stdout byte-identical
   `d3e244f42f290db0cb0a28d15cd9dec482386e808fcc673db6e4995e16c88d25`・
   総計 20,588 点 bad 0。変異 9 種を事前検収（engine rc=2・uh 5760・du 972・
   zd 1260・ty 1502・sb 2623・ps 1941・cs 2364・rw 6 すべて rc=1）。
5. **宣言出版**: push 直前に K1308 空きを再確認（items 系列の最終公刊は K1305・
   対抗宣言なし）し `eabcb742` で宣言ノート出版（証明全文・機体宣言・変異表
   事前宣言込み）。
6. **キット出版**: `28959626`（README・verify_k1308.py 973c97a5…・engine_block.py
   582c93c1…・explore_upper.py/.out・output/dryrun1-4 (+.info)・13 ファイル）。
7. **fetch-back**: raw で 13/13 ファイルの sha256 byte 照合 + 宣言ノート全文照合
   （差分なし）。
8. **公式 4 走**（fetch-back bytes から・隔離 tree/env -i 含む）: 4/4 rc=0・
   stdout byte-identical・predry と同一 sha `d3e244f4…`。
9. **変異電池**（fetch-back bytes から）: 9/9 宣言どおり fail-closed
   （engine rc=2・8 claim tamper すべて rc=1・bad 数は宣言数と完全一致）。
10. **成果物出版**: `30bbcbb5`（audit_run1-4.out+.info・tamper レコード 9・
    detcheck.json OFFICIAL-PASS・MANIFEST-sha256 27 entries）。
11. **K item・README bullet 出版**: 本ログ併記。並行実行との競合は発生せず
    （push ごとに main 再取得・すべて fast-forward で反映）。

## 受入判定

- 20,588 点 bad 0・公式 4 走 byte-identical（宣言 sha と一致）・変異電池 9/9
  事前宣言どおり・fetch-back 13/13 byte 照合・detcheck OFFICIAL-PASS。
- 定理 4 本（T-UH・T-DU′・Z-DIAG・L-SB）は手証明全文つきで公刊済み。
- census 予想（C-SUM）・観測（OBS-WC・OBS-BW・E6b）は未証明として明示。
- 反例（窓非合同行交互予想・29 件）は honest 記録として obs 凍結。
- 11×11 UNKNOWN 不変・verdict 不消費・Part DV/DW・K1306/K1307仮レーンと非接触。

## 次課題

1. F1: 3 トークン以上の typed 上半解析（C-SUM の単一コピー 3 重から全称化）。
2. O1: 遷移窓（z ≥ 3）の真の法則（合同行 Z-DIAG 追従の全称化が本命）。
3. O2: 床窓行 k=z−1 の消滅則（z ≥ 3）。
