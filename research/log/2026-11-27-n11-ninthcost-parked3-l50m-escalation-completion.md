# n11 ninth-cost ladder L50M parked-3 escalation completion (2026-11-27)

長期レーン (11x11 弱解決) の ninth-cost (第9コスト) ラダー完了の記録。
本 log は wave A 宣言 `59db0d52` (publish-then-execute) と wave B raw 出版
`41b331d1` を受けての完走報告である。

## 実行内容

- 対象: parked-3 (k02/k04/k07)。BASE は head of record 0935c94c
  (class 1297036692683751424:134217728、6,875行 WIN203/LOSS6672)。
- jsreplay pin `84585617...` (Node v22.20.0)。入力3点 byte検証済み
  (k02 `8c2a0438...` / k04 `dc3bfeb4...` / k07 `928a1b98...`)。
- 各鍵 cold pair (run1/run2)、cap 50,000,000。全6走完走、すべて node-exact
  で pair identical。

## 確定値 (nodes は bookkeeping、verdict 不消費)

| key | verdict | nodes | 備考 |
|-----|---------|-------|------|
| k02 | WIN(1)  | 18,123,017 | wall 104/98 s |
| k04 | LOSS(2) | 24,309,957 | wall 133/133 s、raw byte 完全同一 |
| k07 | WIN(1)  | 27,621,128 | wall 153/148 s |

これにより ninth-cost ladder は完全閉鎖: 12解決行 (9 LOSS + 3 WIN:
k12/k02/k07)、33鍵は2M抑制のまま、parked 0。

## 開示事項

- 環境reset 1回発生 (300s超過のfetchループ)。reset前の k02 pair は完走済みで
  値を記録しており、公式 pair は reset 後に再実行して node-exact 一致
  (cross-reset determinism の副次的確認)。
- T3 tamper 初回は sed が無音 no-op (rc=0) となりハーネス缺陷を検出。
  byte差分検証つき python flip でやり直した。
- 手再構成した MANIFEST (サイズ不一致) は破棄し、実ファイル取得から
  機械生成した (手転写不使用)。

## fetch-back と pre-audit

- wave B 出版 (raw 6点 + batch-summary-l50m.json sha `e0b27ffd...` +
  MANIFEST-raw-sha256.txt 122行) は fetch-back 8/8 byte一致を確認済み。
- 独立検証ハーネス `audit_ninth_ladder.py` (fresh 実装、527 gates) を
  `research/experiments/n11-ninthcost-ladder-preaudit-20261127/` に出版。
  clean 3走とも rc=0 PASS・JSON byte同一 (sha `a3ff228d...`)。
  tamper 5/5 fail-closed。詳細は同キットの README を参照。

## レジューム (adoption 前提)

- 3新解決行 (k02/k07 WIN, k04 LOSS) は単一実装の成果であり、adoption には
  C++ gate 宣言と第三実装 corroboration (third_impl.js pin 08ea958f,
  cap 400M, 2 cold passes; k12 先例) が必要。
- k02/k07 WIN 行は adoption 時に flip-census 審査が必須。
- 11x11 空盤・19 central-reply roots・二石root {60,27}・第三手 {100,108}・
  全 closure class は全時点 UNKNOWN。
