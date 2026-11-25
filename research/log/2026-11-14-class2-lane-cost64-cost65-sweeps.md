# 2026-11-14 長期レーン: class2-lane cost-64 + cost-65 sweep 完結（31 WIN7-D10・証明書31件・frontier 749→786・class-2 blocker 2 orbit / 143 まで低下・11×11はUNKNOWNのまま）

## 何をしたか

main f0a9819a（cost-64関連の並走pushなし・後に6084cbc6 docsコミットのみ確認）を確認してから、
cost-61(b)後の最安未sweep S6 childを2件連続でsweep・証明書化・frontier再計算まで完走した。

1. **cost-64 sweep**: S6 `00000000000000801a0a000000000000`（cost 64）の64非退化候補
 （=全合法7石目・repo runnerの--enum拡張で列挙・既存cost-61(a)(b)の61/61候補と
  完全一致で検証）をv15 engine verbatim・native Node v22・4並列worker・
  close-first AND（depth>=8）・cap 50M・depth 10単発で完走:
  **24 WIN7-D10（bits 0,4,10,14,22,24,33,35,40,43,52,53,54,78,79,88,90,99,105,106,
  109,113,114,119）+ 40 REFUTED-D10 + 0 capped・総 195,421,906 nodes**
 （単一orbitとして過去最大のWIN7収穫・従来の記録はcost-60の19）。
  pilot d6 制御 5,949 × 5回全PASS。最重量3候補（14/88/33）の独立再実行で
  **node-exact（10,225,960 / 6,360,916 / 5,622,261）**。terminal range 全候補 [13,17]。
2. **cost-64 WIN7証明書24件**: kill-tableなしblind抽出（各候補1プロセス）で
  **904,966行・抽出総 159,574,305 nodes・fatal 0**。repo verifier
 （Bareiss・engine不使用）で全24件 **root-check PASS（7石）・全合法sub-root PASS
 （41〜56手/件）・双方向union 0/0・terminal [13,17]**。
3. **cost-65 sweep**: S6 `00000000000000003802000008000010`（cost 65・上記frontier
  再計算で判明したblocker最安残orbit）の65候補を同一プロトコルで完走:
  **7 WIN7-D10（bits 0,12,52,72,73,84,90）+ 58 REFUTED-D10 + 0 capped・
  総 135,869,766 nodes**。pilot 5,949 × 4全PASS・最重量3候補（2/33/52）独立再実行
  node-exact（10,683,075 / 5,935,031 / 5,184,341）。
4. **cost-65 WIN7証明書7件**: blind抽出 **247,077行・37,218,114 nodes**。
  全件 root-check PASS・sub-root PASS（41〜55手）・union 0/0・terminal [13,17]。
5. **frontier再計算（recompute_frontier_cost64.py / _cost65.py）**:
  全段階制御が公表値と完全一致（baseline 638 → … → after_cost61 735 →
  **after_cost61b 749/7097/557548/5314/417555 をassert再現**）してから
  cost64 covers 141（marginal 126・manifest内30）→ **after cost64:
  solved 779・unique remaining 7067・sum 555,327・open 5284/415,334**、
  cost65 covers → **after cost65: solved 786・unique remaining 7060・
  sum 554,836・open 5277/414,843**。
6. **class-2 blocker S5 `00000000000000003802000008000000` の激減**:
  10 orbit / 688 → **4 orbit / 276（cost-64後）→ 2 orbit / 143（cost-65後）**。
  残りは cost-68 `00000000000000801a02000080000000` と
  cost-75 `00000000000000801a02040000000000` の2 orbitのみ。
  best class-4 は 24/1934 不変。

## 実装メモ

- runnerに `--enum` モードを追加（freshEngineのlegalMovesをそのまま使用）。
  cost-61(a)(b)の候補集合61/61を完全再現することで列挙の正しさを検証した。
- sweepの4並列workerは~500k nodes/s/worker・64候補で~5分。証明書抽出は
  blindでも1候補あたり1〜14M nodesで実用的（kill-table-firstは不要）。
- **cost-68 childは候補あたり2〜10倍重い**（bit1: 7.8M nodes / 128秒）。
  本セッションではforeground一括走査が300秒timeoutで環境ごとリセットされ、
  中断（bits 0/1/2のpilot観測のみ・verdictは未確定・記録対象外）。
  **バックグラウンド detach プロセスはコマンド境界でkillされる**場合があり、
  sweepは300秒以内のforegroundバッチに分割し、バッチ単位でJSONLを永続化する。

## 反映

1コミット1ファイルで cost64: sweep record・証明書record・証明書24件・
recompute script・recompute JSON・ranking CSV・top-candidates CSV、
cost65: 同構成7+4件、計38コミット。全証明書はpush後にraw md5一致を確認
（bit14他・MemoryLimitError後もコミット成立・着地はcommit listで実確認）。
反映前にmain再取得で並走確認（docs-only 6084cbc6 のみ・主題独立）。

## 解釈ガード

- WIN7証明書は「対応する7石rootから深さ10以内の勝ち」の証明のみ。
- REFUTED-D10 は「深さ10以内のWIN7の否定」のみ（より深い勝ちは排除しない）。
- frontier再計算は既知receiptsのbookkeepingであり新しい勝敗判定を含まない。
- **11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN。**

## レジューム

1. **cost-68 `00000000000000801a02000080000000` のsweep（最優先）**
 （blocker残orbit・68候補・1候補あたり1〜10M+ nodes・300秒foreground分割・
  バッチ単位JSONL永続化・WIN7証明書はbit0/3.4M級から）。
2. 続いて cost-75 `00000000000000801a02040000000000`。
  この2 orbitを閉じればclass-2 blocker S5が完全解消。
3. blocker解消後の次のclass-2 S5は `00000000000000809082000000000000`
 （c1=1・37 orbit/2507）と `00000000000000809102000000000000`（40/2850）。
