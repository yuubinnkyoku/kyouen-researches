# Three-row q=4, m=28 SAT row-sum partition — single-owner continuation note (wave A)

継続単一オーナー宣言。commit `02307f675f4c3c0d2700ca470b173b4c2310fd54`
(2026-11-27T17:58Z・宣言時 HEAD `07937d7415`・publish-then-execute・
「実行時間が許す限り m=26 以降の増分掃引」条項) の m=28 増分。
本宣言時 main HEAD: `548695e70c8544d8637fb26221c959a149092da9` (2026-11-27T19:31Z)。
並走レーンの m=27 宣言 (`65e225583992c529dda764704ddfa8f69899b114`・
2026-11-28-three-row-q4-m27-partition-continuation-note) とは掃引幅で完全に分離
(本レーンは m=27 には着手しない・あちらは m≥28 に着手しないと宣言済み)。
repo 検索で m=28 を掃引する既存 lane・宣言は存在しないことを確認済み。

## 目的と主張範囲

- 3×28・q=4 の行欠損極大 witness の非存在を、m=24..27 と同一の
  行和 63-triple 分割 (row-k piece 4件 + row-sum piece 12件・
  うち重い (3,2,3)/(2,3,3) は leftmost-column m分割) で掃引する。
- **P(28) 自体は列挙閉包 (three-row-q4-enumeration-20261121・ext28plus・K1183) で
  既に確定済み**。本実行の新規性は **P(28) の 2方法化** のみ。
  SAT piece が1つでも SAT になった場合は列挙閉包との矛盾として
  即座に全停止・報告する (その場合 witness を sat.js verifyConfig +
  verify34.py で検証する)。
- **m≥29 の新幅主張はしない。**

## 器材 pin (m25/m26 kit と同一)

- sat.js md5 `0cc6021a4e523a0d7f4d5ea0f5f5d40c`
- sat2.js md5 `282ae832efa0080127c6c153e65e1c3c`
- sat3.js md5 `f1c0d1cd00883b6adbeb835aac4dab88`
- sat4.js md5 `96a84063f77bb45463ba470f05a06d58`
- verify34.py md5 `7b97ef1ac727b0741847a81d4dea9bc8`
- split_piece.py = m25 kit 版 (leftmost-column 完備健全 case-split)
- kissat 4.0.4 linux-amd64 sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`
  (release zip `kissat-4.0.4-linux-amd64.zip` sha256 `63282e5168ca040a2018edfba0726bf893a7a6bcdb1db87feb67857e2da697a7`)

## 宣言前較正 (開示)

- m=26 の全16 CNF (k_r0_0/k_r0_1/k_r1_0/k_r1_1・s_* 12件) を本環境で
  再生成し、m26 kit 出版 `cnf_manifest_m26.txt` の md5 と
  **16/16 byte-exact 一致** を確認済み (rowY=1 は --lex=H,V)。
- さらに pinned kissat で m=26 の代表4片 (s_0-2-0 / k_r0_0 / s_2-2-2 / s_3-2-2) を
  実行し、出版 `records_m26.jsonl` の conflicts (1 / 611 / 18,195 / 202,989) と
  **4/4 bit-exact 一致** を確認済み (全 UNSAT)。
  したがって m=28 CNF 生成は同一 pin 器材の増分適用。

## 実行規律

- 分割片実行は bash 呼び出し cap のため 1呼び出しで少数片を逐次実行
  (タイムアウトは片当たり cap 内・INDET が出たら台帳に INDET と記録し
  不在主張としない)。
- 決定性: 代表片 2件の再実行で conflicts bit-exact 一致を確認する。
- 閉包: 汎用 `partition_closure_3row.py` (m26 kit 版) で
  decided 63 / pending 0 / uncovered 0 / SAT 0 を機械検査する。
- verdict NOT consumed。本レーンは w=3 固定幅で標準 11×11 盤に無関係。
  **標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・
  第三手 {100,108}・S2・全 closure class は全時点 UNKNOWN。**
