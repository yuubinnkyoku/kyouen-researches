# n11-centralreply-closure-class20421-batch36-20261124 (Part DX)

Part DX (2026-11-24/25): closure class 20421 (S4 graph rank 9 in the
post-b35loss26 reaudit, mask [1155173304420536320, 131072]) の clean
(honest-label-free) 45 cost children d005..d049 を pinned runner/replica で
2-pass fresh-cold @15M で全 45 キー honest label した probe batch。

**11x11 空盤は UNKNOWN。19 central-reply root も全て UNKNOWN。
本dirのどの行も root verdict を主張しない。nodes は bookkeeping。**

## 結果 (45/45 two-pass node-exact・MISMATCH 0・EXHAUSTED 0)

- **40 LOSS** (採用は後続の別 Part で実施・本 batch は verdict 不消費)
- **5 WIN (不消費)**: d008 `15000000,1,5273778` / d009
  `15000000,1,4997146` / d021 `15000000,1,5266012` / d026
  `15000000,1,6877739` / d029 `15000000,1,2007513`
  (scrutiny owner C++ 第二実装 gate pin `9193f5b6…` 通過後のみ採用可)
- nodes/pass: all-45 183,921,575・採用候補40 159,499,387
- drive 23:40:23Z (d005) → 00:13:41Z (d049)・逐次 1 solver/row/process

## class 20421 の会計 (adoption 後に closure reaudit が機械導出する値)

49 子 = batch-3 既 probe 4 (d001/d003/d004 LOSS 2-pass・d002 WIN・いずれも
canonical chain 未採用) + 本 batch 45 (40 LOSS + 5 WIN)。全 45 キーは
canonical cache `23d40e36…` に 1 行も存在せず (G4)・quarantine 0 (G5)。
adoption Part が 40 (+ 別途のbatch-3 3) exact LOSS 行を消費した場合の
残 unknown は 6 (WIN 6 行) となる見込み (主張ではなく closure reaudit
による機械導出待ち)。

## kit (publish-then-execute・全出版物 fetch-back byte 照合済み)

- scripts: jsreplay.js `84585617…` (byte-clone) / runbatch.sh `f591f8c2…`
  (byte-clone) / make_batch36_keys.py `c71a4877…` (新規 maker・G1-G6)
- sources: batch-3 packet (batch-keys `ad05073a…` / status `7877f4a0…`) /
  closure-classes `b7241eb0…` / refresh-summary `5fe3e5ab…` / canonical
  cache `23d40e36…` / quarantine `81d23160…` / worklist extract
  `2e6102be…` (probe-worklist regen `86767be9…` からの class 20421 49行・
  regen は本セッションで byte 再現確認)
- input: 45 csv + batch-keys-b36.json `d5918203…` (probe_order 81..125)
- val-gate: 4 molecule input/baseline byte-clone + dx-host fresh 4/4
  node-exact (at2m ×2 `2000000,0,2000000`・first-15m
  `15000000,2,3651923`・second-15m `15000000,2,5040200`)
- output: raw 90 (45×2 pass・全行 `# replay_done` 完走) / status.log /
  batch-audit.json `8974d3ed…`
- 宣言: research/log/2026-11-24-part-dx-batch36-class20421-declaration.md
  (`695619bb…`・racing guard 0 件・solver は宣言後に初実行)
