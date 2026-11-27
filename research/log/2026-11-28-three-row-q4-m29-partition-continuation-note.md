# Three-row q=4, m=29 SAT row-sum partition — single-owner continuation note (wave A)

継続単一オーナー宣言。commit `02307f675f4c3c0d2700ca470b173b4c2310fd54`
(2026-11-27T17:58Z・publish-then-execute・「実行時間が許す限り m=26 以降の増分掃引」条項) の
m=29 増分。本宣言時 main HEAD: `50d3a210fd49e1d5e3ccc055a3afb8ccc34f095b`。
m=28 は本レーンが完了済み（kit `871b2297`・完了 log・K1183 追記3）。
repo 検索で m=29 を掃引する既存 lane・宣言は存在しないことを確認済み
（m=27 lane は m=27 完了 `ddbe1392` のみで m≥28 不着手を宣言）。

## 目的と主張範囲

- 3×29・q=4 の行欠損極大 witness の非存在を m=24..28 と同一の
  行和 63-triple 分割 (row-k piece 4件 + row-sum piece 12件・
  うち重い (3,2,3)/(2,3,3) は leftmost-column 29分割) で掃引する。
- **P(29) 自体は列挙閉包 (three-row-q4-enumeration-20261121・ext28plus・K1183) で
  既に確定済み**。本実行の新規性は **P(29) の 2方法化** のみ。
  SAT piece が1つでも SAT になった場合は列挙閉包との矛盾として
  即座に全停止・報告する (その場合 witness を sat.js verifyConfig +
  verify34.py で検証する)。
- **m≥30 の新幅主張はしない。**

## 器材 pin (m25/m26/m28 kit と同一)

- sat.js md5 `0cc6021a4e523a0d7f4d5ea0f5f5d40c`・sat2.js md5 `282ae832efa0080127c6c153e65e1c3c`・
  sat3.js md5 `f1c0d1cd00883b6adbeb835aac4dab88`・sat4.js md5 `96a84063f77bb45463ba470f05a06d58`・
  verify34.py md5 `7b97ef1ac727b0741847a81d4dea9bc8`
- split_piece.py = m25 kit 版・partition_closure_3row.py = m26/m28 kit 版
- kissat 4.0.4 linux-amd64 sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`

## 宣言前較正 (開示・m28 実行と同一環境の継続)

- m=26 全16 CNF md5 16/16 一致 + m=26 代表4片 conflicts 4/4 bit-exact
  （m28 kit README・完了 log に同じ）に加え、**本環境で m=28 の全70片が
  決着済み**（全 UNSAT・決定性代表2件 bit-exact）。同一環境・同一器材の増分適用。

## 実行規律

- 分割片実行は bash 呼び出し cap のため 1呼び出しで予算内の数片を逐次実行
  (INDET が出たら台帳に INDET と記録し不在主張としない)。
- 決定性: 代表片 2件の再実行で conflicts bit-exact 一致を確認する。
- 閉包: partition_closure_3row.py で decided 63 / pending 0 / uncovered 0 / SAT 0 を機械検査。
- verdict NOT consumed。**標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・
  第三手 {100,108}・S2・全 closure class は全時点 UNKNOWN。**
