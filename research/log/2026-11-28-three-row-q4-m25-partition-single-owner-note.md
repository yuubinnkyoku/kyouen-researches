# 2026-11-28 3行 q=4 m=25 分割掃引: 単一オーナー宣言 (publish-then-execute)

- HEAD pin: `07937d7415cccc12f04f6c74691838e97cc4abb2` (K1353 artifacts 直後)。
- レーン: 固定幅 3×m・q=4 の行欠損極大 witness の m=25 判定、および実行時間が許す限り m=26 以降の増分掃引。
  K1183 (M_{3,4} ∈ [24,69]) のレジューム第1項・第2項 (m=24 と同一の63分割手法・増分出版) の直接実行。
  m=25 全63 triple UNSAT ⟹ P(25) の有限機械証明で witness-free 帯 {24,25}・境界 [24,68]。
  SAT ⟹ witness band が m=25 で再開し M_{3,4} ≥ 26。
- 器材 pin (全て本宣言時点の main から sha 検証取得済み):
  sat.js md5 `0cc6021a4e523a0d7f4d5ea0f5f5d40c`・sat2.js md5 `282ae832efa0080127c6c153e65e1c3c`
  (four-row-q6-q7-frontier-20261121 正本)・sat3.js md5 `f1c0d1cd00883b6adbeb835aac4dab88`・
  sat4.js md5 `96a84063f77bb45463ba470f05a06d58`・verify34.py md5 `7b97ef1ac727b0741847a81d4dea9bc8`・
  extract_witness.js md5 `3e0b5fccc2bbc24fac99c7146d78ffcc`・partition_closure.py md5 `ef7c9ac0c998dacd96fb83f3e2540f4a`
  (three-row-q4-frontier-20261121 正本)・kissat 4.0.4 公式 linux-amd64
  md5 `3a5eba830aa6008a604fcc9bbe99a325` / sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1`。
- 較正 (宣言前に実施・開示): 陽性対照 (3,23,4) --rowY=1 --lex=H が **SAT 471,357 conflicts で
  出版値と bit-exact 再現** (CNF vars 57,742 / clauses 191,141・md5 `782b6104c8aa3e399a278cfc77a65be1`)。
  witness 8石 rows [3,2,3] は sat.js verifyConfig (ok=true) + verify34.py (safe=1・maximal=1・deficient=1) の
  2系統検証 PASS。エンコーダ決定性統制も CNF メタ値が全て出版値と一致。
- 分割規約 (m=24 と同一・partition_closure.py の意味論): 欠損空間は行和 triple (r0,r1,r2) ∈ {0..3}^3 ∖ {(3,3,3)} の63通り。
  (i) row-k piece: sat3 --rowY=Y --kex=K (K∈{0,1})・行2は行0のV鏡像・4件で r∈{0,1} の全 triple を被覆。
  (ii) row-sum piece: sat4 --rspec・残る {2,3}^3∖{(3,3,3)} の15 triple は12件 (V鏡像で (3,2,3)/(3,2,1)/(3,2,0) は
  (3,2,3)→V image など既約) で被覆 (m=24 では12件)。全 piece の SAT は witness 2系統検証・UNSAT は
  conflicts を台帳に記録し closure を機械検査 (pending 0 / uncovered 0 で閉包)。
- INDET の取り扱い: cap 下 INDET は honest negative として records に残し、cap を段階的に吊り上げて再実行する。
  決定インスタンスの conflicts は pinned kissat 再現対象。
- 同一性・不参入: 6x26 四レーン (a9dde1d3 / f9a982d2 / e61acf82 / 9e703319)・6x23 six-row q7 sweep
  (16:48Z 宣言)・seven-row q4 幅69/70 系・n11 コスト系レーンには全て不参入 (本レーンは w=3 固定幅で
  標準盤と無関係)。three-row lane の前回宣言 72fdd106 (2026-11-21) は終息済みで、本宣言が後継。
- publish-then-execute: 本宣言以降に CNF 生成・kissat 実行・witness 検証を行う。結果は
  research/experiments/three-row-q4-m25-partition-20261128/ に出版し、records は増分。
  verdict NOT consumed・標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・
  全 closure class は全時点 UNKNOWN (本レーンは w=3 で標準盤に無関係)。
