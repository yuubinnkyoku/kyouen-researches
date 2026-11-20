---
id: K1169
title: "n8-ge16（8×8・16石安全配置の非存在）の chunk 分割完全探索による fresh 再検証"
kind: verification
status: verified
topics: [maximum-safe, search-methods, verification]
aliases:
  - "n9-ge19 lane 宣言較正条件 3 の n8 段（ksearch 系ラダー K_8=15 の fresh 再現）"
  - "n8-16 完全分割閉鎖 604,101,900 nodes・275 葉 chunk 全 UNSAT・audit complete"
  - "ksearch v3d generalized-prefix chunking と chunker audit による再検証"
scope: 有限盤面 8×8・q=4 完全指摘・安全配置（4点同一円・同一直線の禁止）のみ。n≠8 へ外挿しない。
relations:
  - type: verifies
    target: K0029
    note: 既知値表の 8×8 エントリ K_8=15 の上界側（16石の非存在）を、宣言 n9-ge19 lane の手法 (a)（min(S) prefix chunk 分割・append-only 記録・capped chunk の子展開・audit 完了ゲート）で fresh な完全探索として再検証した。下界側（15石 witness）は part1 の naive fresh witness が別途検証済み。
artifacts:
  - path: research/experiments/n9-ge19-k9-upper-decision-20261120/scripts/ksearchp.js
    role: solver
    note: ksearch v3d（v3c と同一エンジン＋ --prefix=p1,...,pm 汎用 chunk 化）。--min=c は --prefix=c と全フィールド一致を V1 制御で検証済み。
  - path: research/experiments/n9-ge19-k9-upper-decision-20261120/scripts/chunker.js
    role: verifier
    note: chunk 分割 driver（run・audit 両 mode）。audit は全 feasible 葉が uncapped UNSAT レコードを持つこと・SAT レコード不在を機械検証する完了ゲートで、レコード打ち切り改竄を fail-closed 捕捉（V6・truncation 制御）。
  - path: research/experiments/n9-ge19-k9-upper-decision-20261120/results/n8t16-partition-records.jsonl
    role: data
    note: n8-16 分割閉鎖の append-only 記録 280 件（275 葉全 UNSAT・capped 5 件は子展開、cap verdict は不採用）。
  - path: research/experiments/n9-ge19-k9-upper-decision-20261120/results/n8-partition-closure-20261120.json
    role: data
    note: 完了 audit 出力（complete・all_unsat・nodes_total 604,101,900）と再検査コントロール（audit 決定性・[0,1]/[8] fresh 再実行の全フィールド一致・tamper 捕捉）をまとめた results JSON。
  - path: research/experiments/n9-ge19-k9-upper-decision-20261120/results/chunk-resume-controls-20261120.json
    role: verifier
    note: 基盤制御群 V1..V6（prefix/min 恒等性・n7-15 whole 再現・SAT chunk witness 第三系検証・n7-15 完全分割閉鎖 audit・tamper ネガティブ制御）すべて PASS。
  - path: research/log/2026-11-20-n9-ge19-part3-n8-16-partition-closure.md
    role: log
    note: 実装・実行の実録（環境リセット 1 回を含む honest bookkeeping・次段の INDET 継続方針）。
  - path: research/log/2026-11-20-n9-ge19-k9-upper-decision-single-owner-note.md
    role: source
    note: 単一オーナー宣言（21f8610464…）。受入条件 3（n=7/8 既知値再現）のうち n8 段として本検証を実施。
---

## 命題（検証対象）

8×8 盤の安全配置（どの 4 点も同一円上・同一直線上にない配置、安全条件は
det[x^2+y^2, x, y, 1]≠0）に 16 石を含むものは存在しない（n8-ge16 = UNSAT）。
これは既知値 K_8=15（CYCLE5 完全最大探索による K0029 表の 8×8 エントリ）の上界側の
独立な fresh 再検証である。新数学主張ではなく、n9-ge19 lane（K_9 上界の SAT 決着実験）
の宣言が較正必須とする既知値の lane 内 fresh 再現（受入条件 3 の n8 段）を完了させる検証。

## 手法と根拠

- ksearch v3d（`ksearchp.js`）: v3c と同一の包含/除外 DFS（曲線 census・per-dangerous-curve
  at-most-3 伝播・aliveFuture bound・cnt==2 曲線の greedy partition bound）に、探索空間を
  「m 個の最小選択セルがちょうど p1..pm」である prefix chunk へ制限する `--prefix` を追加。
  chunk 全体の族は同長 m で空間の完全・素な分割をなす。`--min=c` は 1 要素 prefix と
  全フィールド一致（V1 制御: nodes 10,000,001 の node-cap で sat/capped/boundChecks/boundPrunes
  全一致）。非 chunk 部分は v3c の published 制御値と完全一致（V2 制御: n7-15 whole
  nodes 11,880,598）。
- chunker driver: chunk ごとに honest cap（タイムアウトでは verdict を一切採用しない）で
  実行し、capped chunk は子（p_{m+1}=d の全区間、計数上界 d ≤ NCELL+m−target で完全）へ
  展開。記録は append-only JSONL でプロセス・ホストをまたいで resume。
- audit: 記録から chunk 木を走査し、全 feasible 葉が uncapped かつ sat=false のレコードを
  持つこと・SAT レコード不在・capped 内部ノードが子で完全被覆されることを機械検証。

## 結果

- 280 records・275 葉すべて uncapped UNSAT・SAT レコード 0。capped は [0]/[1]/[2]/[5]/[5,7]
  の 5 件で、いずれも子展開で処理（cap verdict の不採用）。
- audit: complete=true / all_unsat=true / open_leaves=0 / **nodes_total=604,101,900**。
  audit 2 回の ts を除く全フィールド一致（決定性）。
- 再実行検査: 葉 [0,1]（22,365,212 nodes）と chunk [8]（18,012,396 nodes）の fresh 再実行が
  記録と全フィールド一致。レコード打ち切り＋capped 化の改竄 state で audit は
  complete=false / open_leaves=269 を検出（fail-closed 実証）。
- 下界側: W8（15石 witness）は part1 で naive fresh 採取・n8_ge15_strong 全節充足・
  独立 det4 再検査 forbidden 0（第三系）。合わせて K_8=15 が lane 内 fresh で上下両側再現。

## 限界

- 有限盤 8×8 の q=4 安全配置問題に限る。misère 版・他盤面サイズ・s_n・多人数版には一切言及しない。
- K_8=15 の値自体は既知（先行する CYCLE5 完全最大探索）であり、本項目は独立性の高い
  fresh 再検証としての位置づけ。検証の信頼は ksearch/ksearchp/chunker の決定性と制御群、
  および audit gate の fail-closed 挙動に基づく。
- 判定対象 n9-ge19（9×9・19石）は本検証では一切決着しておらず、n9-ge19 lane 全体の
  verdict は INDET のまま。K_9 への主張はない。
