# 単一オーナー宣言: 4行 q=5 class-split レーン m=23 掃引（(4,23,5) 行欠損極大非存在）

- 宣言日時: 2026-11-21T09:36Z
- 宣言時 HEAD: `49ad0dbc0a13b77995913584d48986fc14163ae4`（main）
- レーン: `(4,23,5)` 行欠損極大安全配置の非存在。K1197（(4,22,5) class-split 完結・
  witness-free 幅集合 {21,22}）が「frontier moves to 4x23」と明示した次幅。
  基礎は K0857（(4,21,5) 非存在）・K0833（witness band m=5..20）・
  K0318（上界 U_{4,5}=140）・K0821（witness-free 幅集合と M の監査規約）。
- 先行宣言の不在確認: 宣言時点の main（HEAD 49ad0dbc）に (4,23,5) を掃引した
  出版・宣言なし。2026-11-21 のアクティブ宣言は knowledge integrity repair
  （ed5427f2・完走済み）・three-row q4 m>=28 extension（e9c3cd86）・
  s11 decision lane（a45a626d）・n11 K1181 census 第三検証（9f44f618）・
  vertical-fiber z17-y4 第三検証（d6858a93）であり、いずれも本レーンに非接触。
  m22 レーン（f0b1fbad 引継ぎ）は K1197 出版で完走・file 非接触。
- 新規実験 dir: `research/experiments/four-row-q5-m23-class-split-20261121/` のみ新規出版する。
  m22 レーン dir `four-row-q5-m22-class-split-20261115/` は凍結・出力・records 一切変更しない。
  frontier レーン（SAT・records.jsonl）・m22 / s11 / n11 / 3行q4 各レーンのファイルに接触しない。

## 器材（全て m22 lane 出版物の byte pin）

- scripts/sat2.js md5 `282ae832efa0080127c6c153e65e1c3c`
- scripts/sat3.js md5 `d03f908ea99ba819caee2a6fbb471c1b`
- scripts/sat4.js md5 `df472efc76685963b2f36c3651e75aaf`
- scripts/verify_witness.py md5 `0530d166572987988a01ec40dee12d4c`
- solver: kissat 4.0.4 linux-amd64（公式 zip・md5 `3a5eba83…`）
- driver: sweep23.sh（sweep22.sh の m=23 定数版。変更は幅依存定数のみ:
  minpos 範囲 0..11〔min(x1, 22−x_k) ≤ floor(22/2) = 11〕・k3 x2 上界 B ≤ m−2 = 21・
  k2 x2 上界 B ≤ m−1 = 22・run の m=23 代入）と sweepp0x2gen23.sh（同様の m=23 定数版）。

## 完全被覆の構造（4×21/4×22 lane と同一構造・幅だけ違い）

- 正準欠損クラス 9 個（行ミラー V: 0↔3, 1↔2）:
  {0},{1},{0,1},{0,2},{0,3},{1,2},{0,1,2},{0,1,3},{0,1,2,3}。
- 単一クラスは正確石数 k∈{0,1,2,3} と minpos p∈0..11 で分解
  （sound H-split: min(x1, 22−x_k) ≤ 11。H は行を保存。minpos と lex の併用は
  unsound のため全インスタンス lex なし）。
- multi クラス 7 個は直接。INDET が出たら krow 分解→x2 分割（m22 lane 規約）。
- c0k3p0/p1/p2 は m22 実績（600s cap で 3,852,260 / 6,854,166 / 6,939,580
  conflicts すべて INDET・sweepp0x2 57 sub-bucket で決着）から、m=23 では
  direct 試行を skip して x2 完全分割（B ∈ 1..21 / 2..21 / 3..21 の disjoint 被覆）
  で決める。これは設計判断として本ノートと README に明記する（x2 の alone
  被覆は sat4.js の comment 記載どおり完全・disjointな事例解析で sound）。
- 計: 陽性対照 1 + multi 7 + c1k3 12 + c0k3 direct 9（p3..p11）+ k2 24 + k1 24 + k0 2
  = 79 direct と x2 60（c0k3p0 21 + p1 20 + p2 19。direct INDET が他に出た分は追加）。

## 陽性対照（必須較正）

(4,20,5) class {0} --krow=0:3 --minpos=1: m=20 witness の V 像。
4×21 lane（SAT 20.0s）・4×22 lane（SAT 39.3s）ともに conflicts 375,415 が
bit-exact。本レーンでも同一 CNF（md5 `362034b210d89ed3a25d34072995f3a6d`）で
SAT 375,415 conflicts を再現することを開始条件とする。

## 受入条件

1. **器材は pin のまま**: 上記 4 script が byte 一致のまま実行する。
   実験の出力は新規 dir 配下のみ。records.jsonl は append-only・機械出力のまま
   （per-instance CNF md5 ledger・conflicts・sec・cap）。
2. **主張の正確な言葉遣い**:
   - 全 129+ instance 群が UNSAT で完結した場合のみ「(4,23,5) に行欠損極大安全配置は
     存在しない」を主張し、witness-free 幅集合 {21,22,23}・監査規約形
     **M_{4,5} = 21 または ≥ 25**（M=22,23,24 は不可能・上界 140 不変）と記述する。
   - witness が発見された場合（SAT）は js decode + python verify の 2 系統検証の上
     増分 witness として出版し、**M_{4,5} ∈ [24,140]** に鋭い形で更新する。
   - cap 下 INDET が残る bucket は honest negative として記録し、決着済み空間のみ
     を主張する（未決着は次回実行へ繰り越す・無理に押し進めない）。
3. **検証チェーン**: 陽性対照 の bit-exact 再現・m22 lane の pinned scripts 同一 byte
   再利用・CNF 生成の決定性（再生成 md5 一致）・SAT 時の 2 系統 witness 検証。
4. **K 項目**: 決着時に新規 K 項目を出版する（採番は push 直前 3 点確認:
   items/404・README grep・直近 items コミット）。
5. **並走への配慮**: 他レーン（three-row q4 m>=28・s11・n11・vertical-fiber・
   knowledge integrity）のファイルに触れない。push 競合・HEAD 不一致・取得失敗時は
   残 part を次回実行へ繰り越す。driver は resumable で、records.jsonl 増分を
   定期的に出版して環境リセットに対処する。

以上の条件で本レーンの (4,23,5) 掃引を開始する。
