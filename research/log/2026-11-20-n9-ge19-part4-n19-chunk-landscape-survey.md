# n9-ge19 lane part4: n9-19 (9×9・19石) チャンク landscape 調査 — L1 全63 chunk 被覆・L2 probe・外挿 (2026-11-20)

単一オーナー宣言: `research/log/2026-11-20-n9-ge19-k9-upper-decision-single-owner-note.md`
(commit `21f8610464d2711f768b5764d23b21a40295dee5`) の手法 (a) に基づく。
part1 (`0afda0e6`/`9a1c7a98`)・part2 (`906b893f`)・part3 (`5d65700715`/`40531eb48d`) に続く。
**判定対象 n9-ge19 は依然 INDET のままで、本 part は K_9 への一切の主張をしない。**
本 part は (i) 実験環境・スクリプト正本性の fresh 再現、(ii) min(S) 場合分割チャンクの
L1 全数被覆と L2 probe による landscape の計測、(iii) 前回からの再開規約 (marathon resume
protocol) の確定、の 3 点からなる survey / bookkeeping 出版である。

## 1. 環境・正本性の fresh 再現 (本セッション、2026-11-20 22:08Z〜22:36Z)

- 7 スクリプト (ksearch.js / ksearchp.js / chunker.js / naive.js / fastsat.js /
  gen_strong_cnf.js / eval_strong.js) を raw pinned 取得し、git blob SHA-1 を本体側
  listing と照合して 7/7 一致を確認 (ksearchp `66938de2…`・chunker `addab282…` 他)。
- 既出版 state への audit 再実行: n7t15 `complete=true / all_unsat=true /
  nodes_total=11,880,562`、n8t16 `complete=true / all_unsat=true /
  nodes_total=604,101,900` — part2/part3 出版値と完全一致。
- gen_strong_cnf.js fresh 再生成: n7_ge15_strong 22117 vars / 68510 clauses /
  FNV-1a-64 `0f3ee7fe14af06d4` — part1 出版値と完全一致。

## 2. n9-19 チャンク landscape (fresh 計測、2026-11-20)

`--n=9 --target=19` (NCELL=81、L1 chunk は min(S)=c 固定で c=0..62 の 63 本)。
記録: `results/n9t19-partition-records.jsonl` (出版時点 79 records・bytes 15120・
SHA-256 `221fc6daaa361a066ddbabfcb8d9a9c1b9408271c32dc474cb54df91ebd8c2e0`)。

### L1 全 63 chunk (全数被覆)

- **42 chunk が uncapped UNSAT で完了** (計 62,010,510 nodes)。重い順の代表値:
  [24] 10.0M、[26] 9.5M、[23] 9.1M、[22] 7.4M、[21] 7.0M、[25] 10.3M (59.2s で完了)、
  [27] 2.8M、[28] 1.2M、[29] 0.63M、c=30..44 は 0.03M..0.8M、c>=45 は概ね自明
  ([62] 3 nodes)。
- **21 chunk ([0]..[20]) が capped** (12s cap で 3.4M..5.5M 到達の時点で未完)。
- c>=26 で急激に軽くなる cliff があるが、単調ではなく cell 幾何に依存する
  (例: [17] 5.5M@12s は [16] 3.9M@12s より重い)。

### L2 probe (16 prefix に sample 探索 + 3 prefix 追加完走)

- 重い L2 子: [0,1] 5.2M@12s未完・[0,2] 5.8M@12s未完・[0,5]/[0,10]/[0,20] 4.5-4.7M@12s未完・
  [5,6]/[5,8]/[5,12]/[5,20]/[10,11]/[10,15]/[10,20]/[15,16]/[15,20] 3.4-4.5M@12s未完。
- 軽い側: [0,40] 0.03M 完了・[20,21] 0.68M 完了。
- **追加完走 (大きめ cap)**: [25] 10,334,296 nodes / 59.2s で UNSAT 完了・
  [0,20] 10,283,525 nodes / 61.2s で UNSAT 完了 (12s cap で 4.46M 未完だった chunk が
  約 2.3 倍の計算で閉じた例)・[15,16] は 60s cap でも 8.9M 到達で未完 (重い例)。

### audit snapshot (出版時点)

`complete=false / all_unsat=false / settled_leaves=45 / capped_internal=34 /
open_leaves=1783 / sat_records=0 / bad=[] / nodes_total=73,003,436`
(nodes_total は settled leaf のみ計上、capped の部分進捗は除外 — chunker の規約)。
sat_records=0 だが、これは open_leaves≠0 の未完 state であり何らの判定でもない。

## 3. marathon 進行に関する規約 (resume protocol・次回以降の執行)

1. state 正本は本出版 `results/n9t19-partition-records.jsonl`。次回実行は
   これを取得後に `chunker.js --mode=run --n=9 --target=19` (cap は 6..110s 程度の
   小刻み driver 呼出、wall<=280s/bash 呼出) で続きから走らせる。
   既 settled chunk は skip され、capped 内部 node は子展開される。
2. capped record は常に「未完了の作業」であり、capped verdict は簿記に採用しない
   (part2/part3 と同一規約)。sat レコードが出た場合のみ即 stop し、19石 witness の
   独立検証 (det4 全 4 点組 + census 交差) に入る (宣言受入条件 1)。
3. 判定は `--mode=audit` が `complete=true` かつ `sat_records=[]` になった時点でのみ
   「ksearch 系 n9-19 完全閉鎖 UNSAT」として扱う。それまでは INDET を維持する。
   fastsat 系の較正ゲート (n7_ge15_strong / n8_ge16_strong) は別途必要 (受入条件 2)。
4. 本レーン内の record 重複の取扱い: 本 part では fastsat 較正バックグラウンド実行と
   の CPU 競合下で 12s cap の暫定 record を書いた後に大きい cap で書き直した prefix が
   13 本あり、出版時に「同一 prefix は last-wins」で破棄した。audit の全 field は
   破棄前後で同一 (settled_leaves / nodes_total 変化なし、capped 内部 partial 値は
   last-wins で反映)。ksearchp の DFS は決定的で node 数は内容で決まり、CPU 競合は
   cap 到達の速さにのみ影響する (cap は挙動上「完了しなかった」ことの主張のみ)。

## 4. 読み方の注意 (他レーン・README 整合)

- 本 part の 42+3 個の UNSAT chunk はいずれも **19石安全配置がその chunk 内に
  1 つも存在しない** ことの有限完全列挙としては妥当な個別判定だが、open_leaves 1783 が
  残る全体としては何の判定でもない。**K_9 >= 19 も K_9 <= 18 も一切支持しない。**
- 規模の外挿は survey JSON (`results/n9t19-landscape-survey-20261120.json`) の
  heuristic_extrapolation に「数学的主張ではない・capped 部分データ由来」の明示付きで
  記録する (総 node 数オーダー 4e9..40e9・純 CPU 換算 4..40時間 → 複数セッションの
  marathon として現実的な範囲、という工学的見積りにすぎない)。

## 5. 実行の実録 (honest bookkeeping)

- 実行環境: 1.0 CPU / 約1GiB / Node、bash cap 300s 前後 (各呼出は 300 秒未満で停止)。
- 22:08Z-22:36Z: 正本性再現 (audit 再現 2 件・FNV 再生成 1 件) → chunker run 1 件
  (21 chunk capped) → ksearchp 直接 probe 3 バッチ (L1 残り全数・L2 probe・完走 3 件)。
- 競合する計算: n7_ge15_strong の fastsat 較正長時間実行 (受入条件 2 の fastsat 系
  ゲートの試み、別記) を同一マシンで並行中のため、ksearchp の実行は定常的に CPU の
  ~半分で走った
  (各呼出の wall は ksearchp の cap 到達が主であり、node 数自体は内容決定的)。
- 環境リセット: この part では発生せず (すべての bash 呼出は cap 内に完了)。

2026-11-20 高速レーン
