# (4,24,5) multi-class krow-pinned decomposition 宣言 (2026-11-27 高速レーン)

- 宣言時点: kit `research/experiments/four-row-q5-m24-class-split-20261127/`
  (宣言 `37afeb4c`・checkpoint 1 `96dc2b08` の続き)。直前の kit path 最新 commit は
  `96dc2b08` (自 session・並走衝突なし・宣言時 HEAD `21f8f487`)。
- 状況: 直接掃引で k2/k1/k0 全バケット (50) UNSAT・multi c012/c013/c0123 直接
  UNSAT (1.48M/1.37M/0.59M conflicts)・multi c01/c02/c03/c12 直接は CAP=220s で
  INDET (1.66M〜2.69M conflicts・honest negative)。k3 直接バケットは c0k3p0/p1
  が 220s INDET (m23 では同型に 382〜486s を要したため本環境では直接決着困難)。
- 本宣言: 上記 INDET multi 4 クラスを m21 規約どおり krow ピン分解で決着する。
  - 器材: `multigen24.sh` (sat3.js `d03f908e…` byte・kissat 4.0.4 md5
    `3a5eba83…` 出版 pin・records24.jsonl 同一 schema・append-only・resumable)。
  - 分解: multi クラス D={a,b} を両欠損行の石数 (k0,k1)∈{0..3}² の 16 個の
    厳密数ピースに分解 (互いに素・網羅)。k0≥1 の抵抗ピースは第 1 欠損行の
    minpos p=0..11 (sound H-split: min(x1,23−x_k0)≤11・単一クラス bucket と
    同一規約) で追分解。k0=0 ピースは直接のみ。
  - 監査: `coverage_check24.py` を v2 化 — multi は「直接 UNSAT」または
    「16 ピース全 UNSAT (k0≥1 は minpos 副分割可)」で決着。k2/k3 bucket の
    直接 INDET は完全 x2 副分割 (sat4.js・k=3: B∈p+1..22, k=2: B∈p+1..23)
    でも決着可能に一般化 (c0k3p0/p1/p2 の設計どおり x2 専任と同じ規則の拡張)。
  - 較正: 陽性対照 (4,20,5) c0k3p1 CNF md5 `362034b2…` byte-exact・SAT 375,415
    conflicts bit-exact は本 host で再現済み。分解ピースの予備較正として
    c01 (2,2) minpos=0 UNSAT 587,021 conflicts / 49s および
    c01 (3,3) minpos=0 UNSAT 2,050,757 conflicts (265s cap 内完走) を事前測定
    (出版後の本格掃引で同名ピースを再実行して records に反映する)。
- 判定 (不変): 全 piece UNSAT なら witness-free {21,22,23,24}・
  **M_{4,5} = 21 または ≥ 26**。SAT なら witness 復号 + 3 系統検証。
- Not claimed: 個別 INDET は不在主張でない。(4,q≠5)・w 行族・Grundy・11×11 は
  一切不消費 (全時点 UNKNOWN)。verdict 不消費。
