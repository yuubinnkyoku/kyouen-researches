---
id: K1283
title: "z1 面の確定: H2 の全称証明による T-B1 無条件昇格と z1-δ2 行完全分類・δ3 非零 / クラスE 下界パッケージ（落下子は常に arm-1・C手子 1 XOR T-H1 = 0 の L-Z1F エンジン・宣言ノートに証明全文収録・33,691 点公式監査 bad 0・4 走 byte-identical）"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "unconditional package closing the z1 plane (notation: m=min(X), mixed = |X|>=2 and max>m, arm-1/arm-2, class E = mixed with mult(m)>=2 and not arm-2). T-H2 (THE main theorem, proved universally, no hypothesis remains): for every m>=1 and every mixed X with min(X)=m: H(2m+2;X;1)=min(sumX,2m+2)%2, i.e. value 1 exactly for X=(m,m+1), else 0. Keys: (1) the min-fall child of any row-m move is ALWAYS an arm-1 mixed shape at row m-1, and its C-child is 1 XOR H(2j+2;Y;0) = 1 XOR T-H1(j) = 0 (K1282), giving lemma L-Z1F: H(2j+3;Y;1)>=1 unconditionally for every arm-1 mixed Y (every j>=1) — unlike the z0 side where T-H1's proof needed the precise high-gap structure of the fall child, the z1 side only needs nonzero via the C-move probing the z0 plane directly; (2) the special shape (m,m+1) has fall child (m-1,m+1) = the (j,j+2) shape, and lemma L-S gives H>=2 there via opts {0 (C-child), 1 (stair child (j,j+1) = T-H2(j) special)}; (3) the row-1 base H2(1) closes by direct case analysis on F4/F3 plus the NEW floors G3z2 (budget-3 z2: multi -> 2 iff X=(1,1), else 1; single v(x,2,3): x=2 ->2, x>=3 ->1) and B2z3 (budget-2 z3: (1,) -> 1, else 0) — it does NOT depend on the open row-1 budget-4 z0 family F14b."
  - "pack proved alongside (all full proofs in the single-owner declaration note §2): T-E1: for every m>=1, a>=2: H(2m+2;(m^a);1)=0 — this completes the full classification of the z1 delta-2 row (mixed via T-H2, allm via T-E1, single via the published closed form v). Note the fall child of (m^a) at budget 2m+1 sits at z1-delta-3 of row m-1 (2(m-1)+3=2m+1) and is arm-1 mixed, so L-Z1F gives >=1; the C-child is 1 XOR T-Q-allm(m) = 1 (K1282); 0 is in no option. (This corrects the K1281 exploration memo's budget arithmetic that placed the fall child at the z1 frontier of row m-1; recorded honestly in the note §2.3.) L-Z1F: for every j>=1, arm-1 mixed Y: H(2j+3;Y;1)>=1 (C-child 1 XOR T-H1(j)=0 in opts). L-S: for every j>=1: H(2j+3;(j,j+2);1)>=2 (value in {2,3}). T-N0z1: for every m>=1, mixed X: H(2m+3;X;1)<>0 — universalizes K1281 observation (c); classes: arm-1 -> C=0; arm-2 (m>=2) -> C = 1 XOR T-LC(arm-2)=0; mult>=2 non-arm-2 -> stair/compress child is T-H2(m)-generic (=0) or T-E1(m) allm (=0); row 1 with mult(1)>=2 -> A-child 0 via T-H2(1)/T-E1(1). T-IIz1: for every m>=2, class E at z1 delta-3: H>=2 (C-child 1 XOR T-E(m)=1 AND a 0-witness child — the exact value 2 is conjecture C-IIz1-2, OPEN, 790-point census all 2)."
  - "corollary T-B1' (THE upgrade): K1281 T-B1 becomes an UNCONDITIONAL theorem: for every m>=2 the z1 band R in [m+2,2m] plus diagonal collapse H(R;X;1)=v(sumX,1,R) for all mixed/allm X with min=m, and the z1 frontier R=2m+1 classification (mixed -> 2, (m,m) -> 0, allm a>=3 -> 2). Proof: the K1281 II-1'/II-2'/II-3' skeletons are reused verbatim with H2 replaced by T-H2 and T-B0(i) by the unconditional T-B0' (K1282); the only H2 consumption of II-3' is at row m-1 (T-H2(m-1) is already proved), so no cycle — the in-row order is P1-band -> P1-diag -> Q1 -> T-H2 -> T-E1. Together with K1282 T-B0', the low-z band z in {0,1} is now an unconditional theorem over the full budget range (band all windows w, diagonal, frontier, delta-2; delta-3 partially on the z1 side). Floors G3z2/B2z3 and the v-identities v(1,2,2)=1, v(x,2,2)=0, v(1,2,3)=1, v(2,2,3)=2, v(x,2,3)=1 (x>=3) are proved in full in the note §2.1."
  - "declarations and PROVENANCE (publish-then-execute, strongest form): single-owner declaration note published FIRST at c075b512 (observed HEAD 5855e3f8, K1283 free, no competing declaration), machine kit frozen at 536921ff with a manifest path-prefix fix at 52939752 (sha256 of verify_k1283.py = ca515df5887948bd880928fde4576877e23b4addb613566d6b252a20d5deaeb3, fetch-back verified byte-identical against all 12 files; engine block pin bd5f22e4... sha-gated in-kit every run; header byte-reused from the published K1282 machine). Official runs executed AFTER publication from the FETCHED-BACK kit: 4 runs rc=0, stdout byte-identical sha256 cf182f24df6af7dc622f181011024e0447c5493291d63c8fa1b3f8666240df69 = declared expectation exactly (same cwd x2 PYTHONHASHSEED 1/random + isolated trees /tmp with env -i x2 PYTHONHASHSEED 99/7). Declared totals matching measured EXACTLY: 33,691 comparisons / bad 0, counts=[6,947; 64; 2,976; 3,388; 4,278; 21; 650; 790; 8,757; 5,820] = [D1 H2 census (row-1 wide + m=2..7 mixed + tall giants), h2_ones=7 exactly the (m,m+1) corners; D2 T-E1 allm m,a=1..8; D3 frontier classification m=2..7; D4 band+diagonal collapse sum>=R regime; D5 L-Z1F + T-H1 C-anchors; D6 L-S + stair/anchors + v(2,2,3); D7 T-N0z1 + n0_hist {1:454,2:196}; D8 T-IIz1 + ii_hist {2:790}; D9 G3z2 + B2z3 + v identities; D10 published anchors both planes + singles-v both engines x<=15,z<=7,R<=19]. Mutation battery 10/10 fail-closed exactly as pre-declared: --tamper-engine -> rc=2 (mutated sha 0ea47a80... != pin), h2/e1/q1/band/lzf/ls/n0/ii/g3 -> rc=1 bad=6,947/56/2,940/3,388/4,278/14/650/790/4,355. Audit outputs published at the same kit dir at 44215dad (audit_run1-4.json, run1-4.info, detcheck.json, tamper records x10, MANIFEST-sha256 30 files). honest records: dryrun1 D7 comparison-operator draft bug detected against declared values (fail-closed debugging), the pre-declaration exploration E9 caught the (1,1)@3z2=2 exception missing from the first G3z2 draft, and tamper_n0.out is byte-identical to dryrun1.json (both implement the same wrong (h==0) predicate — a consistent by-product recorded in the C commit)."
relations:
- type: resolves
  target: K1281
  note: "K1281 残課題1(b)（H2 の全称証明）を完了。T-H2 が仮説 H2 を無条件定理化し、T-B1′ により K1281 T-B1 の結論（z1 帯全域+対角崩壊・前線分類）が無条件定理に昇格（II-1′/II-2′/II-3′ の証明骨格をそのまま再利用し H2 を T-H2 で置換）。K1281 観測 (c) も T-N0z1 として全称化。これで K1281 の仮説 H1/H2 は両方とも全称証明済みになり、低 z (z∈{0,1}) 帯は全域無条件定理で完成。"
- type: depends_on
  target: K1282
  note: "T-H1（L-Z1F の C手子値 1 XOR 0 の供給源）・T-Q/T-Q-allm（T-H2/T-E1 の C手子 z0 前線値 2/0）・T-LC（T-N0z1 arm-2 経路）・T-E（T-IIz1 の C手子 1 XOR 0）・床分類 F0–F5 ・行1基底 J1/F3/F4・T-B0′（系 T-B1′ の z0 帯+対角供給）・機体 header（verify_k1282.py の ENGINE_BLOCK+PIN 行 byte 流用）。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R) と A0/A1 補助計算（崩壊値表示・single 側・v 系恒等の全基盤・D9/D10 で両 engine 照合）。"
- type: depends_on
  target: K1270
  note: "z1 窓+1 行 H(m+2;X;1)=v(Σ,1,m+2)（全 m>=2）が z1 帯帰納の底部 w=1（D10 アンカー再照合）・底部 P1(2)/P1(3) と K1270-z1。"
- type: extends
  target: K1278
  note: "T_B（z1 窓+2 行）が z1 帯帰納の底部 w=2 スライスとして包含（m=3 の R=5）。witness (2,3)@5z1=2 は D10 アンカーで再照合。"
- type: related
  target: K1269
  note: "min=1 z1 窓+1 分離 T2 の実値を D10 アンカーで再照合。行1の z1 側は本項で δ2 (H2(1)/T-E1(1)) と δ3 非零（T-N0z1 行1類別）が確定し、窓側（K1269）と床（G3z2/B2z3）で接続。"
- type: related
  target: K1267
  note: "min=1 z0 窓+1 分離 T1 の実値を D10 アンカーで再照合。本項 z1 行1基底は z0 側 J1–J5（K1282）と対称に、F14b に依存しない A/B/C 手の場合分けで閉じた点が構造的差分。"
- type: related
  target: K1265
  note: "{1,1} 全 R 崩壊の D10 アンカー再照合。床 G3z2 の (1,1)@3z2->2 例外は K1265 側の min=1 座標 (budget-3 z2) に位置する新事実。"
- type: related
  target: K1268
  note: "統合 sharpness census の予想 C1（低 z 崩壊帯）の z1 側が予算全域の無条件定理として完成（これで C1 の z∈{0,1} 帯が全域で定理化）。z>=2 側は open 継続。"
- type: related
  target: K1254
  note: "z>=2 面・FR-X との接続面。本項確定の z1 構造（δ2 完全分類・δ3 非零/クラスE 下界・L-Z1F/L-S ラダー片）が z>=2 面ラダーの z1 側境界を与える。"
- type: related
  target: K1279
  note: "z10 ストリップとは非接触（本項は z<=1・band 中心）。ただし本項の「C手子が直前 z 面の同一形状値を 1 XOR で消費する」構造はストリップ梯子の C手子依存（B10/A10）と同型で、z 連続性の観測対象として記録。"
artifacts:
- path: research/log/2026-11-24-z1-front-h2-proof-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート（出版 c075b512・観測 HEAD 5855e3f8・対抗宣言なし・K1283 仮採番時に items 空き確認）。定理 T-H2/T-E1/系 T-B1′/T-N0z1/T-IIz1・補題 L-Z1F/L-S・床分類 G3z2/B2z3/v 系・行1基底 H2(1)/T-E1(1) の証明全文・依存グラフ・主張区分（C-IIz1-2/C-LS2 は open 明記）・protocol D1–D10・honest 記録を収録。証明の正本。
- path: research/experiments/z1-front-h2-proof-20261124/
  role: machine
  note: 実験キット一式（出版 536921ff・MANIFEST パス訂正 52939752）: README・verify_k1283.py (sha256 ca515dfe...)・engine_block.py (pin bd5f22e4...)・exploration {explore1.py, explore1.out: E9 G3z2 (1,1)→2 例外捕捉を含む honest 記録}・dryrun 4 本 (dryrun1 = D7 演算子誤りの fail-closed 検出・dryrun2-4 全green)+ 公式監査成果物（出版 44215dad: audit_run1-4.json・run1-4.info・detcheck.json・tamper 記録 10 ファイル・MANIFEST-sha256 30 files）。fetch-back byte/sha 照合済み。
- path: research/log/2026-11-24-z1-front-h2-proof.md
  role: report
  note: 実行 log（宣言→機体→fetch-back 公式監査→出版の全記録・受入判定・次課題）。
---

## 概要

z1 面（z=1・残り R 軸）が確定した。K1281 が仮説として残した H2 を
全称証明し、低 z (z∈{0,1}) の R 帯を全域無条件定理で完成させた:

- **T-H2**: ∀m≥1・mixed で H(2m+2;X;1)=min(Σ,2m+2)%2
  （H=1 ⟺ X=(m,m+1)）。**T-E1**: allm a≥2 → 0。z1-δ2 行はこれで
  完全分類。
- 鍵は (1) 落下子が常に arm-1 mixed で **C手子 = 1 XOR T-H1 = 0**
  が無条件に非零 0-options を供給（L-Z1F）すること、
  (2) 特別形 (m,m+1) の落下子 (m−1,m+1) が L-S（≥2）で処理できる
  こと、(3) 行1基底が新規床 G3z2/B2z3 の直接場合分けで閉じ
  （F14b 非依存）、の 3 点。
- **系 T-B1′**: K1281 T-B1（z1 帯+対角崩壊・前線分類）が無条件昇格。
  T-N0z1（δ3 mixed ≠0）・T-IIz1（δ3 クラスE ≥2）が加わり、
  z1 部分木の min≥2 帯/前線/δ2/δ3-mixed が O(1) 判定可能に。

## 主張の区分（過大主張の防止）

- 定理（全称証明）: T-H2・T-E1・T-B1′(i)(ii)・T-N0z1・T-IIz1（≥2
  まで精確）・L-Z1F・L-S（≥2・値域 {2,3} まで）・G3z2・B2z3・
  v 系・行1基底 H2(1)/T-E1(1)。
- 予想（open）: **C-IIz1-2**（クラスE の値 =2・census 790 点全て
  2・fall 子は z1-δ4(m−1) 領域で ≠2 の確認が残る）・**C-LS2**
  （(j,j+2) の値 =2・j=1 の fall は確定値 1）・(α) クラスの generic
  値（census では 1/2 混在 {1:454, 2:196}・法則未確定）・
  z1-δ3 allm・z1-δ4+・z≥2 面・純カウントラダー・F14b。
- census は証明ではない: D1–D10 の 33,691 点は定理の実機照合
  （bad 0）であり、定理の全称性は証明によって成立する。

## 公式監査（publish-then-execute・fetch-back 機体から走行）

- 宣言 c075b512 → 機体 536921ff（+MANIFEST 訂正 52939752）→
  fetch-back 12 ファイル byte 照合 → 公式 4 走（同一 cwd×2
  PYTHONHASHSEED=1・random + 隔離 tree/env -i×2 PYTHONHASHSEED=99・7）
  すべて rc=0・stdout byte-identical
  （sha256 cf182f24…= 宣言想定）。~18.5s/走。
- counts=[6,947; 64; 2,976; 3,388; 4,278; 21; 650; 790; 8,757; 5,820]
  ・総計 33,691 点・bad 0・h2_ones 7〔=(m,m+1) コーナー 7 点〕・
  n0_hist {1:454, 2:196}・ii_hist {2:790}。
- 変異電池 10/10 検出（engine rc2〔mutated sha 0ea47a80…≠pin〕・
  h2 6,947 / e1 56 / q1 2,940 / band 3,388 / lzf 4,278 / ls 14 /
  n0 650 / ii 790 / g3 4,355・すべて宣言どおり）。監査成果物は
  同一実験 dir に出版（commit 44215dad・detcheck.json・
  MANIFEST-sha256 30 files）。
- honest 記録: dryrun1 の D7 比較演算子誤実装を宣言値突合で検出
  修正・宣言前探査 E9 が G3z2 草稿の (1,1)@3z2→2 例外を捕捉
  （床分類修正後に bad 0・(1,2) special の B 子 (2,)@3z2 =
  v(2,2,3) = 2 と整合）・K1281 走査メモの T-E1 落下子の予算
  誤り（z1 前線(m−1) → 正しくは z1-δ3(m−1)）を §2.3 で訂正記録。

## 11×11・規約への接続

- verdict 不消費・11×11 空盤・二石 root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4 はすべて UNKNOWN 維持。
- z1 面の枝刈り: T-B1′/T-H2/T-E1/L-Z1F/T-N0z1/T-IIz1 により
  z1 サブツリーの min≥2 帯/前線/δ2/δ3-mixed ノード評価が
  O(1) 閉形式・非零下界に置換できる。別レーン（giant）への
  構造補題として接続記録のみ（採用判断は giant レーンオーナー）。

## 次課題（単一オーナー候補）

1. C-IIz1-2 / C-LS2 の精密化: fall 子（z1-δ4(m−1) 領域）の
   値 ≠2 確認。z1-δ4 の開拓が本格的な次段。
2. (α) クラス（z1-δ3 arm-1 一般形）の値の構造化
   （census {1:454, 2:196} の 1/2 分岐則）。
3. z1-δ3 allm・z≥2 面（z=2 帯端シフトの一般形）・純カウント
   ラダー・F14b。
