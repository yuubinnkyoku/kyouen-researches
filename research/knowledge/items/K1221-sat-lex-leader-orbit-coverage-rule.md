---
id: K1221
title: SAT対称性破り（lex-leader鎖）は「受理言語の全列挙照合」と「全軌道被覆100%」の双機械検査を出版前に必須とする規約 — D4鎖初版の軌道完全遮断瑕疵（n=4で8,548軌道中3,195遮断・UNSAT2ショット取り下げ）を自家検査で発見し、完全二方向Tseitin鎖で修正・P1〜P5検査で確認した実例
kind: method
status: active
topics: [search-methods, verification, maximal-safe]
aliases: ["lex-leader orbit coverage check", "symmetry breaking soundness gate"]
relations:
- type: related
  target: K1206
  note: "ごとりの3系統検証思想の符号化側拡張: model（SAT側）は幾何検証で救済できるが、UNSAT側は符号化の健全性に完全依存するため機械検査を挟むまで出版しない"
- type: related
  target: K0031
  note: "修正版v2.1によるs_7=7の再導出が本規約下最初の較正実績（K1220）"
- type: related
  target: K1204
  note: "censusアンカー照合と同じfail-closed思想をlex-leader鎖に適用"
artifacts:
- path: research/experiments/s12-s13-sat-stabilization-20261122/README.md
  role: source
  note: "§2〜§3: 符号化の正確な意味論と、瑕疵のフォレンジクス（棄却ベクトル数・遮断軌道数・取り下げ範囲）"
- path: research/experiments/s12-s13-sat-stabilization-20261122/scripts/lexchain_orbit_check.mjs
  role: verifier
  note: "規約の実装: P1 デサイダvs d鎖全列挙照合 / P2〜P3 draft遮断の定量化 / P4 受理言語==A<=lex g(A) の全列挙両方向照合 / P5 軌道被覆。全検査PASS"
- path: research/experiments/s12-s13-sat-stabilization-20261122/output/lexchain_orbit_check.json
  role: certificate
  note: "検査結果の機械可読正本（n=3,4全列挙・n=5..13サンプリング）"
- path: research/experiments/s12-s13-sat-stabilization-20261122/scripts/enc_sat2.mjs
  role: verifier
  note: "修正版v2.1: 標準Crawford型 d_c <=> d_{c-1} and (A_c=B_c) 完全二方向Tseitin鎖+ブロッキング句"
- path: research/experiments/s12-s13-sat-stabilization-20261122/scripts/enc_sat2_draft_chain.mjs
  role: data
  note: "瑕疵鎖のアーカイブ（バイト完全再現: cnf2/n7k6のsha256と一致）。再発防止の負の対照"
- path: research/experiments/s12-s13-sat-stabilization-20261122/scripts/cnf-sha256.txt
  role: manifest
  note: "draft（cnf2）とv2.1（cnf3）のCNFハッシュの区別記録"
---

# lex-leader鎖の機械検査規約と瑕疵の実例

## 規約（以後のSATレーンすべてに適用する）

対称性破り节を含むCNF符号化でUNSAT結果を知識に昇格する前に、次を機械検査する:

1. **受理言語の全列挙照合**: 鎖のデサイダを、定義通りの条件（A <=lex g(A)、固定点は受理）と
   小盤面（実例ではn=2,3,4の全列挙・n=5..13の決定的サンプリング）で両方向照合する。
   d鎖変数を介する場合、鎖の充足を独立に列挙してデサイダと照合する（P1・P4）。
2. **軌道被覆**: 全対称軌道（D4×平行移動の商）に受理代表元が残ることを全列挙で確認する（P5）。
   1個でも完全遮断軌道があれば、UNSATは「対称性のせい」の可能性があり無効。
3. SAT側のmodelは鎖の正否に依らず幾何独立検証で救済できるが、元を正すまでUNSATは出版しない。

## 実例: D4 draft鎖の瑕疵と取り下げ

- 初版の鎖は「strict減少時のみ鎖を強制する」向きの3句構成で、等ビットで鎖が閉じ、以降の位置の
  制約が消える。その結果 A<=lex g(A) を満たすベクトルを棄却（n=3で274、n=4で36,808 member/gate対）し、
  **軌道を完全遮断する**（n=3: 102中30、n=4: 8,548中3,195。lex-min代表が遮断される軌道も3,783）。
- 完全遮断軌道が存在する時点で、draft鎖下のUNSAT（n7k6 default/sh42 他）は述語の不在と
  遮断のどちらでも起こり得るため、**すべて取り下げた**（実験README §3・ラン表の「無効」行）。
- これは自家の機械検査（出版前のP1〜P3）で捕捉され、外部指摘ではない。検査を挟んでいなければ
  「s_7>=7のSAT再証明」として知識に昇格していた内容の誤りであった。
- 修正: d_c <=> d_{c-1} and (A_c=B_c)（d_{-1}=top）の完全二方向Tseitin鎖+ブロッキング句
  （-d_{c-1} -A_c B_c、c=0は無条件）。修正過程で3件のミス（E1のsubsumption・forward句の否定向き・
  符号）を検査がそれぞれはね、最終版でP1〜P5全PASS。
- 修正版の実コスト: 同一述語（n7k6）のUNSAT探索が70.23秒/832,104 conflicts から13.56秒/174,155
  conflicts へ（条件付き伝播が強い鎖はむしろ速い）。正しさと速さが両立した。

## 限界

- P4/P5の全列挙はn=3,4（とn<=2）までで、n>=5はサンプリング照合である。ただし受理言語の等しさの
  証明は鎖の構造（各句の意味論）から手証明されており、検査は実装ミスの網羅的な捕捉装置。
- 規約はCNF対称性破り一般（Crawford Shenoy Joslin refs型）にそのまま適用できる。UNSATの別の
  誤り源（under-constrained predicate・solver欠陥）はここでは扱わず、第2符号化一致と別規約（K0009系）に任せる。
