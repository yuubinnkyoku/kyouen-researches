# 2026-11-27 3枝REMO cap16 境界 単一オーナー宣言 (publish-then-execute)

- 着手時 HEAD: `b4cefa42179a0e8427f36ce7e6cb89105ebf1467` (2026-11-27T14:31:44Z)
- 作業: K0886 (cap≤15) が限界節で登録した次の検証課題「枝サイズ≥16 は未走査。16≡1 (mod 3) で、これまで未観察の剰余での新キー族の出現は次の検証課題」への着手。
  3枝REMO・r=3・枝サイズ≤16 の正準プロファイル完全列挙 (Burnside 予測 orbits) と決定的 mask エンジン sweep、
  キー (sorted sizes, γ) センサス (一様決定 / 一様非決定 / mixed) の測定・出版。
- 機材系譜: K0883/K0886 kit の `mask_engine_fast.js` byte-clone (改変なし)・列挙は K0883 検証器の
  `constrained_vectors` / `direct_constrained` / `burnside_fix_counts` / `branch_perms` / `orbit_representative` verbatim。
- 事前較正 (宣言前実施・開示): cap7 orbits=2,048 (K0862 と一致)・cap14 orbits=123,272 (K0883 と一致・
  Burnside fix(id),fix(trans),fix(cyc)=(692102,15638,308))・cap15 orbits=189,864 (K0886 と一致)・
  K0883 出版 packed part1of2/part2of2 sha256 再取得一致 (f627814d…/7848e20c…)・
  cap15 先頭 2,000 プロファイル sweep スモーク 6.2s。cap16 の測定値は未取得 (prof 列挙のみ実施)。
- 受入条件: (1) sweep 2 走 byte-identical (r=3)。 (2) K0886 出版 r=3 cap15 packed レコードを D_15 部分列位置で全件再現・
  K0883 cap14 レコードを D_14 部分列位置で全件再現 (順序保存部分列性 D_14⊂D_15⊂D_16 の機械検証込み)。
  (3) cap15 キー数 3,060・非坍縮 110 キーの再現。 (4) fail-closed 検証器 + tamper 電池 fail-closed。
  (5) 主張は有限完全列挙の事実のみ (全称昇格しない)・順位決定性は扱わない・r≥4 は触及しない。
- 暫定 K番号: K1346 (main 採番確認: K1346..K1350 の commit 検索 0 件・K1345 は既存。衝突時は AGENTS.md に従い再採番)。
- 標準 11×11 空盤・二石 root {60,27}・第三手 {100,108}・S2・全 closure class は全時点 UNKNOWN・verdict 不消費。
  本作業は multiplayer REMO 有限センサスであり標準盤には一切触れない。
