# 2026-11-22 七行・八行家族 高速レーン session log (w65-01 発見, M_{7,4} ≥ 66)

単一オーナー宣言: `66e7033b6e` (`research/log/2026-11-22-seven-eight-row-translation-census-single-owner-note.md`,
宣言時 HEAD `646e9d3fdc`)。本 log はその宣言に続く実行の発見順・事故・判断の記録。

## 発見史 (時系列)

1. **(リセット前・前パートのsession内成果, 中央違いipa食用)** 宣言後、同一セッション内で
   純並進census (7家族×20 seed, 全family target−1 ちょうどで停止, anchor (6,4) m46 で
   K1211 出版 placements 340/340 一致, 2回実行 byte一致) → targeted surgery エンジン構築 →
   正の対照 PC1–PC3 (winA→winC on 7×35, m30→m31 on 7×31, base53→pair0/pair1 on 7×57,
   いずれも既知 witness の石集合レベル再現) → 陰性対照 NC74/NC75 (出版 negative 再現:
   (7,4) w60 pair1 両軌道 2R2A = 0, (7,5) winC id@0 = 0) を通过。
2. **maximalUnder バグ**: 防御用 fullVerify が手術中の全 hit を誤検出 → 原因特定:
   `maximalUnder` が除去石の vacated cell を走査していなかった。修正後、全 hit は真正。
3. **幅60の26 witness surgery hit** (JS エンジン, seed は published pair0/band53 系):
   pair0 id@13 の 1石再配置 (18,1)→(52,1) を含む計26個の相互に異なる 7×60 witness。
   連鎖censusで そのうち R=64 達成配置 (bboxw47, id@10, U=(64,6)/(64,0)) により
   幅60..64 の連続 witness ⇒ M_{7,4} ≥ 65 (下界 60→65)。
4. **幅65 第二弾 (クラス(ii) 2R2A, 60秒/問題 cap)**: w60-05/08/10 の id/H 像 +10 シフト
   6問題。5問題 0 hit、**w60-10 id@10 で 2R2A hit 1件** (N=5,434,000, 33.0s, pruned 27,960):
   remove [[21,5],[50,1]] add [[33,1],[63,5]] → **w65-01** ふし (fullVerify safe+maximal+def,
   tamper drop (13,4) → (1,4) unblocked で reject)。⇒ **M_{7,4} ≥ 66**。
5. **ここでハードインフラ障害**: 成果は work tree (/home/user/work/lane78/) にのみ存在し
   push 前に Koyeb 503 → 環境リセットで全滅。消えたもの: JS エンジン 3本, 26 witness
   の stones, census/stage 記録一式, stage_y65 の完全 JSON。残ったもの: 対話ログに
   印字済みだった w65-01 の stones/removed/added/tamperCheck と stage_y65 の 6問題の
   N/hits 計数 (上記の通り session-only 記録として保持)。
6. **(本パート, リセット後再構築)** w65-01 を対話ログから正当復元し Knowledge kit
   (`_78-row-frontier-kit-20261122/`) に即時退避。その後:
   - `verify_int.py` を clean-room 新規実装 (整数円 3×3行列式, isqrt 2次方程式, 浮動小数点なし)。
   - **v1 バグ**: 判別式0の接円で同一格子点を二重計上 → 曲線石数水増し (偽4点・5点曲線10本)
     と偽 unblocked。**陰性対照 (tamper drop/relocate) がこのバグを顕在化させた**。
     修正後 w65-01 は safe+maximal+def 完全一致, tamper 2対照は JS エンジンの記録
     (drop (13,4) → (1,4) first unblocked) と cell 単位で一致。
   - **翻訳スイープ (幅54..75, D4像 × 全シフト, 全配置を新検証器で直接検証)**:
     w65-01 単一家族は **幅54..65 の 12連続幅すべてに witness** (幅あたり4..8配置),
     **幅66..75 では 0配置**。7行 (6,4) W1 family の10連続幅 (K1211) を超える
     単一石集合の最多タイ記録となる12連続幅。R(family) = 65。
   - **幅66 クラス(i) targeted surgery (完全列挙)**: base = w65-01 id@11 (7×66 で
     unblocked は左端 T=(0,6) のみ)。T を通る base石ちょうど2個の曲線 190本, add候補
     93 セル。**1R1A 1,860候補・2R1A 17,670候補 (93×190, addcells∩base=∅ 機械確認),
     いずれも完全走査で 0 hit** (2R1A は bash 300秒 cap で3分割+per-a1 progress resume
     で完走: progress 93/93)。クラス(ii) 2R2A (≈13.8M final states, ナイーブPython実装
     で≈90h) とクラス(iii) c0=0 (3石追加で def-mode 必ず破綻: rows 0..5 は既に q−1) は
     今回未走査・open。scoped local negative, 不在主張ではない。

## 主張のスコープ

- **下界 (存在主張)**: M_{7,4} ≥ 66 (w65-01, 2系統検証)。
- 12連続幅 (54..65) witness は純並進 D4 像の機械検証事実 (この seed 限定的)。
- 幅66 の 1R1A/2R1A クラスは対象 base 配置 (T=(0,6) 単一不足) に対する完備走査で
  0 hit (k=20/19 に限る, c0=2 に限る)。他クラス・他 base 配置は未走査。
  7×66 の成否は UNDETERMINED。
- 上界 T_7 = 1929 不変。CSV の bounds は 66..1929 に更新。
- 標準 11×11 空盤・二石 root・class 1/2/4 は非接触で UNKNOWN のまま。
  候補数を勝敗として読まない。
- 前パートの26 witness (幅60) の stones はリセットで喪失。**今回の出版物は
  それに依存しない**。pair1 軌道などの陰性計数は session-only 記録。
  再構築 (published seeds から stage 再実行) は次バッチに持ち越し。

## 次バッチ (着手前に必ず最新main再取得・hourly並走に注意)

1. 幅66 クラス(ii) 2R2A: 増分計数エンジン (曲線辞書差分) で ≈13.8M final states を
   実行可能化 (JS 再構築でもよい)。hit なら M_{7,4} ≥ 67。
2. 幅66 クラス(ii) の別 base (H像/V像, s=17 H配置など) と c0=1 曲線の直接列挙設計。
3. 喪失26 witness の再構築: pair0/band53 seeds (出版済み CSV note の 2-for-2 near
   幅60) から 1R1A/2R1A/2R2A stage を再実行して stones を再取得・保存。
4. (7,5)/(7,6)/(7,7)/(7,8)/(8,9)/(8,10) 各 frontier への同型 c0=2 手術の移植。

## 器材

- Knowledge kit: `kyouen-research/_78-row-frontier-kit-20261122/` (リセット耐性镜像,
  repo側が正式)。
