---
id: K1282
title: "z0 面の確定: H1 の全称証明による T-B0 無条件昇格と LAW-C/δ3-high-gap/δ4-C4/クラスII/クラスE 定理パッケージ（行帰納は行1基底事実のみで閉じる・宣言ノートに証明全文収録・42,725 点公式監査 bad 0・4 走 byte-identical）"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "unconditional package closing the z0 plane (notation: m=min(X), mixed = |X|>=2 and max>m, arm-1/arm-2 = mult(m)=1 / (max<=m+1 and mult(m+1)=1)). T-H1 (THE main theorem, proved universally, no hypothesis remains): for every m>=1 and every mixed X with min(X)=m and mult(X,m)=1: H(2m+2;X;0)=1. Proof by row induction on m whose induction step consumes ONLY row-1 base facts: the fall child (m-1,U) of the row-m delta-2 arm-1 position always keeps a token of value m... i.e. at row m-1 the value m=(m-1)+1 is absent-from-gap... precisely: the fall child has min m-1 and NO (m)-token adjacency required — the j remaining arm tokens U satisfy max(U)>=m+2>m, so the child is a high-gap arm-1 shape at row m-1, whose value 0 is supplied by T-L3(m-1) as the 0-witness (truncation (2(m-1)+2, x->2m) makes every row-(m-1) option a witness option), plus the compress child (frontier (m-1) mixed -> 2 by T-Q) and the stair child (row-(m-1) class II -> >=2 by T-II) complete mex{0,2,...}=1. The cycle closes because T-L3/T-Q/T-II/T-E/T-LC at row m-1 are themselves proved from row-(m-2) instances and row-1 bases J1-J5 (H1(1): H(4;{1}us>=2;0)=1, L3(1): H(5;{1}ss>=3;0)=0, B46: H(6;{1}t>=4;0)<>0, F14: H(4;{1^t>=2,2^u,s>=3};0)=0, II(1)), with the budget<=4 floor classification F0-F6 as the base layer."
  - "unconditional theorems proved alongside (all full proofs in the single-owner declaration note §2): T-Q: for every m>=2: z0 frontier R=2m+1 classified (mixed -> 2, allm (m^a) a>=2 -> 0) — extends K1281 T-B0(ii) from m>=3 to m>=2 and no longer needs H1 (mex{1,0}; T = 1 by band, min-drop child -> 0 by T-H1(m-1) or T-L3(m-1)). T-LC (LAW-C theoremized): for every m>=2, R=2m+2, z0 mixed X: mult(m)=1 -> 1; arm-2 -> 1; otherwise -> 0 (m>=1 in the census layer; proof: arm-1 is T-H1; arm-2 falls to (m,m+1)-core by C-child exclusion; mult>=2 non-arm-2 is T-E). T-L3: for every m>=1, z0 delta-3 R=2m+3 high-gap arm-1 (min=m, mult(m)=1, no (m+1)-token, max>=m+2): H=0. T-C4: delta-4 R=2m+4, arm-1 with a >=(m+3)-token (gap>=3, and gap=2 with a >=(m+3)-token also covered): H<>0. T-II: class II (arm-1 at delta-3 with an (m+1)-token AND a >=(m+2)-token): H>=2 (proved precisely to >=2; the value ==2 is the conjecture C-II2, OPEN, 916-point census all value 2). T-E: z0 delta-2 mult(m)>=2 mixed non-arm-2: H=0."
  - "corollary T-B0' (THE upgrade): K1281 T-B0 conclusion becomes an UNCONDITIONAL theorem: for every m>=2: z0 band R in [m+1,2m] full collapse H(R;X;0)=v(sumX,0,R) for all mixed/allm X with min=m (ALL windows w in [1,m] plus the diagonal w=m), and for every m>=2: z0 frontier R=2m+1 classification (mixed -> 2, allm a>=2 -> 0). Proof: K1281 II-1/II-2 (band interior, diagonal) and II-3 (frontier m>=3) are reused verbatim with every H1 occurrence replaced by T-H1; the m=2 frontier case is T-Q. This subsumes K1270 (w=1), K1278 T_A/T_A3 (w=2,3), and the K1278 claim-free 225/225 window-4 z0 observation (w=4 slice), now as unconditional theorem instances. The z1 plane (K1281 T-B1) remains CONDITIONAL on H2 (open)."
  - "declarations and PROVENANCE (publish-then-execute protocol, same as K1281): single-owner declaration note published FIRST at 89a8b438 (observed HEAD 4db1ffcb, K1282 free, no competing declaration), machine kit frozen at 2ca77ca6 (sha256 of verify_k1282.py = 7b70993aea68e80ef27dd4f059727427ea048c0e40015bd240f3841abc44354f, fetch-back verified byte-identical; engine block 2,508B pin bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92 sha-gated in-kit every run), official runs executed AFTER publication from the FETCHED-BACK kit (strongest protocol): 4 runs rc=0, stdout byte-identical sha256 b2600e453a2a78e0a92e47f7591d79379dd074a3f5c19a86538d6afc9a8f85c8 = declared expectation exactly (same cwd x2 PYTHONHASHSEED random/1 + isolated tree + env -i x2 RANDOM/99). Declared totals matching measured EXACTLY: 42,725 comparisons / bad 0, counts=[6,348; 2,976; 7,686; 4,256; 1,599; 916; 2,916; 1,134; 12,293; 2,601] = [D1 H1 census (m row-1 wide + arm-1 m=2..7 + tall giants); D2 frontier classification m=2..7; D3 LAW-C mixed census; D4 L3 high-gap census; D5 C4 census; D6 class-II census + ii_hist {2:916}; D7 class-E census; D8 row-1 base lemmas wide (F14, B46); D9 budget<=4 floor classification (fb1/b2/b3/b4 + singles vs closed form both engines); D10 published anchors + band/diagonal closure (K1278 witnesses, K1265, K1267, K1269, K1270 z0/z1, band sum>=R regime, diagonal mixed@2m -> 0)]. Mutation battery 8/8 fail-closed exactly as pre-declared: --tamper-engine -> rc=2 (embedded sha gate), --tamper=h1 -> rc=1 bad[0]=6,348, --tamper=q -> rc=1 bad[1]=2,940, --tamper=lawc -> rc=1 bad[2]=4,746, --tamper=lawc-arm2 -> rc=1 bad[2]=2,940, --tamper=l3 -> rc=1 bad[3]=4,256, --tamper=e -> rc=1 bad[6]=2,916, --tamper=ii -> rc=1 bad[5]=916. Audit outputs published at the same kit dir (audit_run1-4.json, run1-4.info, detcheck.txt, tamper records, MANIFEST-sha256)."
relations:
- type: resolves
  target: K1281
  note: "K1281 残課題1の前半（H1 の全称証明）を完了。T-H1 は仮説 H1 を無条件定理化し、T-B0′ により K1281 T-B0 の結論（z0 帯全域+対角崩壊・前線分類）が無条件定理に昇格（II-1/II-2/II-3 の証明骨格をそのまま再利用し H1 を T-H1 で置換・前線 m=2 は T-Q）。z1 側（H2/T-B1）は条件付きのまま open。"
- type: extends
  target: K1278
  note: "窓+2/窓+3 行の全称崩壊 T_A/T_A3/T_B が z0 帯全域の無条件定理の w=2,3 スライスとして包含され、claim-free のまま残した窓+4 z0 225/225 点観測（m=4..12）も w=4 スライスとして無条件定理化（K1281 では仮説 H1 条件付きだったものを本項で外す）。"
- type: depends_on
  target: K1270
  note: "窓+1 行 H(m+1;X;0)=v(Σ,0,m+1)（全 m>=2）が z0 帯帰納の底部 w=1（D10 アンカーで再照合）。min 落下子が行 m−1 の帯下端・前線・δ2 に当たる全箇所で T-B0′/T-Q/T-H1(m−1) と接続。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R) が崩壊値表示・選択肢集合一致判定・帯値 v(Σ,0,R) の全基盤（D9 singles 電池が両 engine で全照合）。"
- type: related
  target: K1281
  note: "（参照方向の追補）本項の T-LC は K1281 が finite-census observed として記録した LAW-C 全文の定理化。T-Q は同 D3 前線分類の m>=3 からの m>=2 拡張。z1 面の条件付き T-B1 と z>=2 面（K1279/K1280 ストリップ・z=2 帯端シフト観測）は open のまま残し、H2 が次の単一オーナー対象。"
- type: related
  target: K1267
  note: "min=1 z0 窓+1 分離 T1 の実値を D10 アンカーで再照合。行1基底 J1–J5（H1(1)/L3(1)/B46/F14/II(1)）は min=1 行の予算>=4 側を新規に確定する層で、K1267 の min=1 窓側分類と床分類 F0–F6 で接続。"
- type: related
  target: K1269
  note: "min=1 z1 窓+1 分離 T2 の実値を D10 アンカーで再照合（(1,1)→0・t>=3→2・t∈{1,2} v-collapse）。本項の z0 行1基底と対称な z1 行1基底は open（H2 側）として区別。"
- type: related
  target: K1265
  note: "{1,1} 全 R 崩壊の D10 アンカー再照合。床分類 F0–F6（予算<=4・多トークン）が本項の帰納の最下層を成し、(1,1)→0（β2 z0）など K1265 側の min=1 座標と連続する。"
- type: related
  target: K1268
  note: "統合 sharpness census の予想 C1（低 z 崩壊帯）の z0 側が予算全域の無条件定理として完成（w∈[1,m]+対角+前線+δ2）。z>=2 側・z1 側は open 継続。"
- type: related
  target: K1254
  note: "大型 z 側 merge 領域・FR-X との接続面。本項確定の z0 構造（δ ラダーの δ=2..4 と high-gap/II/E クラス分割）が z>=2 面ラダーの z0 側境界を与える。"
artifacts:
- path: research/log/2026-11-24-z0-front-h1-proof-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート（出版 89a8b438・観測 HEAD 4db1ffbc 側最新 main・対抗宣言なし）。定理 T-H1/T-Q/T-LC/T-L3/T-C4/T-II/T-E/T-B0′ と行1基底 J1–J5・床分類 F0–F6 の証明全文・主張区分（census≠証明・C-II2 open 明記）・protocol・honest 記録を収録。証明の正本。
- path: research/experiments/z0-front-h1-proof-20261124/
  role: machine
  note: 実験キット一式（出版 2ca77ca6・11 ファイル: README・verify_k1282.py (sha256 7b70993a...)・engine_block.py (pin bd5f22e4...)・exploration {census1, explore_ladder}・dryrun 3 本+dry0 事故記録）+ 公式監査成果物（同一 dir に出版: audit_run1-4.json・run1-4.info・detcheck.txt・tamper 記録 16 ファイル・MANIFEST-sha256・監査出版 commit 79163e48）。
- path: research/log/2026-11-24-z0-front-h1-proof.md
  role: report
  note: 実行 log（宣言→機体→fetch-back 公式監査→出版の全記録・受入判定・次課題）。
---

## 概要

z0 面（z=0・残り R 軸）が行帰納で全確定した。帰納の段消費が行1の基底
事実のみで閉じることを発見した点が本項の核心:

- **T-H1**: ∀m≥1・z0-δ2 arm-1 mixed（mult(m)=1）⟹ H(2m+2;X;0)=1。
  落下子は行 m−1 の high-gap arm-1 になり、その値 0 を T-L3(m−1)
  が 0-witness として供給する。圧縮子は行 m−1 前線 mixed→2（T-Q）、
  階段子は行 m−1 クラスII→≥2（T-II）。mex{0,2,…}=1。
- **T-L3/T-Q/T-II/T-E/T-LC** は互いに行 m−1 インスタンスと行1基底
  （J1–J5・床分類 F0–F6）から帰納法で確定し、サイクルが閉じる。
- **系 T-B0′**: K1281 T-B0（帯全域+対角崩壊・前線分類）が
  無条件定理に昇格。z0 面はこれで予算全域確定。

## 主張の区分（過大主張の防止）

- 定理（全称証明）: T-H1・T-Q・T-LC・T-L3・T-C4（≠0 まで）・
  T-II（≥2 まで精確）・T-E・T-B0′・J1–J5・F0–F6。
- 予想（open）: **C-II2**（クラスII の値 =2・916 点 census で全観測
  されるも証明は「mex に 0 が入らない」（≥2）まで・単一オーナー対象）、
  allm-δk（k≥2）の一般則、純カウント・ラダー（宣言ノート §2.5:
  (2,3)@k3=1・(2,3,3)@k3=0・(2,4)@k4=0・(2,4,4)@k4=1 などの根拠
  観測つき）、H2/z1 側・F14b。
- census は証明ではない: D1–D10 の 42,725 点は定理の実機照合
  （bad 0）であり、定理の全称性は証明によって成立する。

## 公式監査（publish-then-execute・fetch-back 機体から走行）

- 宣言 89a8b438 → 機体 2ca77ca6（凍結・fetch-back sha 一致）→
  公式 4 走（同一 cwd×2・隔離 tree/env -i×2）すべて rc=0・stdout
  byte-identical（sha256 b2600e45…= 宣言想定）。~8.3-8.5s/走。
- counts=[6,348; 2,976; 7,686; 4,256; 1,599; 916; 2,916; 1,134;
  12,293; 2,601]・総計 42,725 点・bad 0・ii_hist {2:916}。
- 変異電池 8/8 検出（engine rc2・h1/q/lawc/lawc-arm2/l3/e/ii rc1・
  bad 数はすべて宣言どおり）。監査成果物は同一実験 dir に出版
  （commit 79163e48・detcheck.txt・MANIFEST-sha256 参照）。

## 11×11・規約への接続

- verdict 不消費・11×11 空盤・19 central-reply roots・二石 root・
  S2 {59,60} は UNKNOWN 維持。
- z0 面の枝刈り: T-B0′/T-LC/T-E により z0 側の多くの子局面値が
  O(1) 判定になり、11×11 giant の z0 サブツリー評価の高速化に
  直結しうる（別レーンへの構造補題として記録・接続済み）。
