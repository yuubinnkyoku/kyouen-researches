# (4,23,5) class-split 掃引 — 行欠損極大非存在の完全被覆 (2026-11-21 高速レーン・宣言 d92c8f51)

## 位置づけ

K1197（(4,22,5) class-split 完結）が「frontier moves to 4x23」と明示した次幅。
現在の値は **M_{4,5} = 21 または ≥ 24**（witness band m=5..20 は K0833・
witness-free 幅 {21,22} は K0857+K1197・上界 U_{4,5}=140 は K0318・
監査規約は K0821）。本掃引は (4,23,5) を absence-capable に完全分解する。

- 全 129+ instance 群が UNSAT で完結 → witness-free 幅集合 {21,22,23}・
  **M_{4,5} = 21 または ≥ 25**（M=22,23,24 は不可能・上界 140 不変）。
- witness 発見（SAT）→ witness を復号・2 系統検証して増分 witness として出版し、
  **M_{4,5} ∈ [24,140]** に鋭く更新する。
- cap 下 INDET が残る bucket は honest negative として記録し、決着済み空間のみ
  主張する（未決着は次回実行へ繰り越す）。

## 器材（m22 lane 出版物の byte pin・宣言ノート d92c8f51 記載のとおり）

- scripts/sat.js md5 `0cc6021a4e523a0d7f4d5ea0f5f5d40c`（K0810 census。
  m22 レーン dir には同封されていなかったため、m21-surgery lane から byte pin
  で取得して同封した。frontier/q4-lane と同一 file・全 w で汎用）
- scripts/sat2.js md5 `282ae832efa0080127c6c153e65e1c3c`
- scripts/sat3.js md5 `d03f908ea99ba819caee2a6fbb471c1b`
- scripts/sat4.js md5 `df472efc76685963b2f36c3651e75aaf`
- scripts/verify_witness.py md5 `0530d166572987988a01ec40dee12d4c`
- solver: kissat 4.0.4 linux-amd64（公式 zip・md5 `3a5eba830aaf6008e604f…`）
- driver: sweep23.sh（m22 lane sweep22.sh の m=23 定数版）・
  sweepp0x2gen23.sh（sweepp0x2gen.sh の m=23 定数版・B 範囲は下記）
- 実行環境: cgroup cpu.max 100000/100000 = 実効 1.0 CPU・逐次 single kissat。

## 被覆の完全性（4×21/4×22 lane と同一構造・幅だけ違う）

- 正準欠損クラス 9 個（行ミラー V: 0↔3, 1↔2）:
  {0},{1},{0,1},{0,2},{0,3},{1,2},{0,1,2},{0,1,3},{0,1,2,3}。
- 単一クラスは k∈{0,1,2,3}（正確石数）× minpos p∈0..11 で分解
  （sound H-split: min(x1, 22−x_k) ≤ floor(22/2) = 11。minpos と lex の
  併用は unsound のため全インスタンス lex なし）。
- multi クラス 7 個は直接。
- c0k3p0/p1/p2 は m=22 実績（600s cap で 3,852,260 / 6,854,166 / 6,939,580
  conflicts すべて INDET・その後 x2 分割 57 sub-bucket 57/57 UNSAT で決着）から、
  m=23 では direct 試行を skip して x2 完全分割のみで決める（設計判断。
  sat4.js の事例解析〔2番目石の列 B で disjoint 完全分割〕は単独で
  bucket の完全被覆として sound）。
- x2 の B 範囲: k=3 は B∈p+1..21（m−2）・k=2 は B∈p+1..22（m−1・k-aware 上界）。
  c0k3p0: b1..21（21 bucket）・c0k3p1: b2..21（20）・c0k3p2: b3..21（19）。
- 計: 陽性対照 1 + multi 7 + c1k3 12 + c0k3 direct 9（p3..p11）+ k2 24 + k1 24
  + k0 2 = 79 direct・x2 60（direct INDET が他に出れば追加）。

## 陽性対照（較正記録）

(4,20,5) class {0} --krow=0:3 --minpos=1 — CNF md5 `362034b210d89ed3a25d34072995f3a6`
（m21 lane/m22 lane と同一 CNF）・**SAT rc=10・conflicts 375,415 bit-exact**
（本環境 19.9s・m21 lane 20.0s・m22 lane 39.3s と秒数は CPU 配分差のみ）。
decode 15 石 rows [3,4,4,4]・sat3.js verifyConfig ok・verify_witness.py ok。
本対照をもって pinned 器材・環境の較正とする。

## 運用

- records.jsonl は append-only・機械出力（per-instance CNF md5 ledger・conflicts・
  sec・cap）。resumable: per-key skip（同等 cap 既存なら再実行しない）。
- driver は nohup 単一 background で逐次実行、records 増分を定期的に出版して
  環境リセットに対処する。
- cap は direct/x2 とも 900s（m22 takeover 規約）。

## 結果

IN FLIGHT — 掃引実行中（開始 2026-11-21T09:37Z）。決着後に本 README を更新し
K 項目へ昇格する。
