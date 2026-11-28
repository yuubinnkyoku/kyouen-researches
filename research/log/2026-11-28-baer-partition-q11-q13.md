# 完了 log: Baer partition (Bruck) 検証の q=11・q=13 拡張

- 高速レーン・自実行・GitHub API 出版のみ (ユーザーPC到達不可)。
- 出版鎖: 宣言 `709c8515` (HEAD pin 60c712c0・publish-then-execute・単一オーナー)
  → 実行 (q=11 57s・q=13 161s・両方バッテリ全 PASS) →
  kit + K1374 addendum + 本 log (単一 commit)。
- 実験 dir: research/experiments/baer-partition-q11-q13-20261128/

## 結果

1. **q=11 (PG(2,121))**: Bruck 分割を全数機械検証 — 111 軌道 × 133 点・
   per-orbit プロファイル {1:14630, 12:133}・design 検査 PASS
   (N=14763・直線サイズ 122・点次数 122・2直線交差 1 点 (2,000 サンプル))・
   Singer 商位数検証 PASS。軌道対 union 266 点 witness
   (全直線交差 >=2・プロファイル {2:14497, 13:266}) →
   **PG(2,121) t=2 min <= 266 < 363 = 3q^2**。
2. **q=13 (PG(2,169))**: 157 軌道 × 183 点・プロファイル {1:28548, 14:183}・
   design 検査 PASS (N=28731・直線サイズ 170)。witness 366 点
   (プロファイル {2:28365, 15:366}) → **PG(2,169) t=2 min <= 366 < 507 = 3q^2**。
3. K1374 の有限検証範囲は q = 2,3,4,5,7,8,9,11,13 に拡大 (impl1)。
   q=11,13 は単一実装 (impl2 は gamma 探索のスケール外・宣言で事前開示)。
   design・Baer・位数の多重 fail-closed 検査は q=11,13 でも全数実施。

## 開示

- 実装1 スクリプトは前段 kit 版から2点のみ変更:
  (a) factor_pp の 11/13 サポート、(b) O(ordE) 位数ループのゲート
  (ordE > 600,000 で skip・factor test は位数完全検証として十分)。
  q=2..9 はループありのまま検証済みで、前段の数値は不変。
- 有限機械検査のみ。下界は主張しない。標準 11x11 空盤・19 central-reply
  roots・二石 root {60,27}・第三手 {100,108}・S2・全 closure class は
  全時点 UNKNOWN・verdict 不消費。

## レジューム

- さらに大きい q (16, 17, 19, ...) は build_lines が O(N·(q^2+1)) で
  増える (q=16: N=65793・直線サイズ 257・推定 ~10 分強)。impl1 のみ。
- PG(2,16) disjoint 対全数 census・PG(2,9) k=25 SAT は長期レーン向け。
