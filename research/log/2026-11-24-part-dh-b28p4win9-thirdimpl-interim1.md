# Part DH interim note: takeover実行 D1-D4 green・D5開始時に実行環境outage (honest中途記録・非PASS主張)

- 2026-11-24T09:5xZ (authoring time)。takeover宣言 `a4e00aa3` (observed HEAD `e56c8cce`
  ・earliest_takeover 09:37:31Z経過後出版・対抗takeover search 0・DH dir scaffoldのみ機械確認済み)
  の引き継ぎで実行開始した executor laneからの honest途中記録。
- takeover準備中に実行環境reset 1回 (09:0x-09:1xZ・takeover宣言ノートにhonest記載どおり
  published evidenceから再復元・74 file出版commit byte照合+37 pin照合で再構築済み)。

## 実行済み (D1-D4・host計算・出力はhost上に存在・出版は環境復旧後のB wave)

- D1 rules-gate PASS (rc=0): quads 95,670 一致・triples 195,044 mismatches 0
  (`output/rules-gate.txt`)。
- D2 val-gate fresh 4/4 node-exact (wall_s以外全字段一致): at2m×2 budget-exhausted
  (result 0・nodes 2,000,000) / first-15m result 2・nodes 3,651,923 / second-15m
  result 2・nodes 5,040,200 (baselinesと一致・`.dh-host.out` 4本)。
- D3 negatives PASS (期待fail-closed・rc=1): ng1 GATE_FAIL "legal count mismatch:
  derived=87 declared=88" / ng2 GATE_FAIL "stone count mismatch: bits=5 declared=6"。
- D4 anchors a/b det-pair PASS: k02a result 1・expansions 9,106,337 (a=b同一)・ttHits
  4,991,527 / l1a result 2・expansions 7,660,202 (a=b同一)・ttHits 3,951,175
  (published pinと完全一致)。

## インシデント (honest)

- D5 replica (aa011 p1 発行直前) に実行環境が一時利用不可となり (09:4xZ〜・filesystem
  同期ロールバック失敗のエラー)、D5以降の計算を開始できていない。D1-D4出力はhost上に
  あるが本note時点で出版未済。環境復旧後に B wave (outputs) を出版して D5 resume する。
  **本noteは非PASS主張**: D5-D8未実施・audit未実施・何も完結していない。
- push競合・同時takeover・原オーナー再開時は、上記D1-D4が済んでいる事実は残るが、
  継続実行権は規約 (単一オーナー・停滯3.5h・対抗なし) を満たす次のlaneが判断する。

## verdict不消費 (固有文言)

- 対象9行 (aa011/aa054/aa022/aa034/aa037/aa032/aa028/aa021/aa050) は unadopted honest
  WIN labels のまま。**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 5343 (全54キー) はすべてUNKNOWNのまま。** nodes数・expansions数・
  ttHits数を勝敗や距離として読まない。
