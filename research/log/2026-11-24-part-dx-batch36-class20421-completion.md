# Part DX completion: batch-36 (closure class 20421) clean 45-key probe - drive complete 45/45

Part: DX (single-owner lane). 2026-11-24T23:35:48Z 宣言 → 2026-11-25T00:14Z 完了。
本logは [declaration](2026-11-24-part-dx-batch36-class20421-declaration.md) (commit
bd5a0b2656af158c4e705bf27be191ba8d99fd4e, log sha 695619bb…) の完走記録。

**11x11 空盤は UNKNOWN のまま。19 central-reply root も全て UNKNOWN。
本batchは verdict 不消費 (consumed 0)。nodes は bookkeeping であり
win/loss/distance の主張ではない。**

## 実行チェーン (全 commit は main へ直接 push ・全出版ファイル fetch-back byte 照合済み)

1. 宣言 bd5a0b2656af158c4e705bf27be191ba8d99fd4e (racing guard 0 件・solver は宣言後初実行)
2. kit 1/5 scripts f84ecc02224a91c014f9522f1234b42640c844b6 (jsreplay 84585617 + runbatch f591f8c2, byte-clone)
3. kit 2/5 sources 342f0e329e36f533ffa5a04deccf971b264f6517 (batch-3 packet pins ad05073a/7877f4a0, closure b7241eb0, refresh-summary 5fe3e5ab, quarantine 81d23160, worklist extract 2e6102be)
4. kit 3/5 canonical cache 1a033ddcae9567e89295e2245b8731238e89a5de (23d40e36, 6,573 rows = BASE)
5. kit 4/5 input 6ab84ef4fef48fb74332741899d84eacd0a541ef (45 csv + batch-keys-b36.json d5918203, maker make_batch36_keys.py c71a4877: gates G1-G6, 4回 byte-identical, tamper battery 9/9 fail-closed)
6. kit 5/5 val-gate cf8e07f0606b450dfdedd2dcd05dd4d46c1ad72a (4 molecules x input/baseline byte-clone)
7. val-gate outputs ffde117b44dc079ae8a4d0391284cab3acfc8de3 (dx-host fresh 4/4 node-exact: at2m x2 2000000,0,2000000 / first-15m 15000000,2,3651923 / second-15m 15000000,2,5040200)
8. inc1-6 raw 90 (45x2 pass): fdb3ceba → 98887893 → 46e02d0e → ad3b3bc2 → fe8c94a8 → d79a83fe (+ status.log)
9. final c0a4f60e34b0beabd76485886fb31574ca3e63b6: README + MANIFEST-sha256.txt (160 entries) + batch-audit.json 8974d3ed

## 結果 (2-pass fresh-cold @15M 逐次, 23:40:23Z(d005) → 00:13:41Z(d049))

- 45/45 完走 (全行 `# replay_done`, TRUNCATED 0)
- **40 LOSS** (採用は後続 adoption Part で実施)
- **5 WIN (不消費)**: d008 15000000,1,5273778 / d009 15000000,1,4997146 / d021 15000000,1,5266012 / d026 15000000,1,6877739 / d029 15000000,1,2007513 (scrutiny owner C++ gate 9193f5b6 pending)
- EXHAUSTED 0 / MISMATCH 0 (rc42 hard-stop 未発動)
- nodes/pass: all-45 183,921,575 / loss-40 159,499,387

## class 20421 会計

49 子 = batch-3 既probe 4 (d001/d003/d004 LOSS 2-pass, d002 WIN, いずれも canonical chain 未採用) + 本batch 45。全45キーは canonical cache 23d40e36 に 1行も存在せず (G4), quarantine 0 (G5)。adoption が 40 + (別incrementの) batch-3 3 LOSS 行を消費すれば残 unknown は WIN 6 行となる見込み (closure reaudit の機械導出待ち。主張ではない)。

## 次step (adoption Part)

40 exact LOSS 行 (必要なら batch-3 の 3 LOSS を別 increment) を canonical chain 6,573 行 (BASE 23d40e36) に pinned merger s5_union_merge.py (sha 90711961, byte-clone) で採用 → merge-audit x3 同一 sha → merged cache 出版 (40行採用なら 6,613 行) → refresh fork (Part DW 4aaabcd5 型) で closure/coverage/per-root 3 出力 reaudit → deltas → 完了log。並走 Part DY (batch-37, class 16371) 採用が先着した場合は BASE を相手 merged cache に切替。WIN 6 行は一切不消費。
