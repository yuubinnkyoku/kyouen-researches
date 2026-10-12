# 11×11 最有力S4の未解決境界と `{60,27}` LOSS（2026-10-12）

## 結果

統合時の最新 `origin/main` `2f023e6ee7a314c791f42010bb3111b736d93efe` 上で確認した。対象S4 `(1297036692683752448,0)` の106 canonical S5子は独立整数幾何から再生成した。直前状態はLOSS40 / WIN0 / UNKNOWN66、第三手被覆117/119だった。raw history、cache、15M UNKNOWN、保存S6、競合中solverを確認してから、最初の8局面を共有4・単独4、合法手数帯を散らして固定した。

66件のcold direct S5 exact探索は、各15,000,000 node上限、`--exact-order=count`、1 root 1 processで、65 LOSS / 0 WIN / 1 UNKNOWN、合計403,074,801 nodes・1,129.4秒だった。15M UNKNOWNを同じ条件で再探索せず、未解決は `(1152921504607899649,536870912)` の1件となった。先行2M probeを省いたこの標本では多数が決着したが、より安価になる一般則とはしない。比較対象の直近20 S5 LOSS（81,806,285 nodes）とも対象・選定が異なり、平均費用を単純比較しない。

この最後のS5の完全canonical S6境界は98子。raw historyで検証した保存済みexact S6 WIN 2件を再利用し、残る96子を法的手数の分位に散らして、cold 1M first passを実行した。

- 1M pass: 77 WIN / 0 LOSS / 19 UNKNOWN、40,892,814 nodes・121.96秒。
- K0374方式に沿う15M escalation: 1M UNKNOWNのうち12件を異なる予算で一度ずつ処理。11 WIN / 1 LOSS、33,862,288 nodes・95.64秒。最初のS6 LOSSで停止し、残る7件はUNKNOWNのまま。
- S6 LOSS witness: `(1152921504675009536,536870912)`、合法手87、15M上限中5,859,060 nodes。

固定元先手視点では5石S5はANDなので、この一つのexact S6 LOSSからS5 LOSSが成立する。独立監査後、このS5をexact-only worker cacheへ出し、安全化済みatomic mergeを通した。最終exact S5 cacheは5,851行（WIN159 / LOSS5,692）、SHA-256 `c469eff06559c57b7f4b679c80c1e576c7bddb6f69ea03da0b8b64d0ef4aa198`。追加行のcache `nodes` 欄は導出値のため0であり、S6 rawの5,859,060 nodesとは区別する。

独立`Board`で全3,384 S4子境界を再生成した結果、対象S4は全106 S5子LOSSでS4 LOSSとなった。全3,384 classはLOSS32 / WIN274 / UNKNOWN3,078。第三手被覆は119/119、未被覆0。追加で必要なUNKNOWN S4 classの整数最小値は0、有理LP双対も0で一致した。

`{60,27}` rootの119合法手を個別に再生成し、各手の三石AND局面に少なくとも一つの四石LOSS応手を割り当てた。旧残余100・108の両方には今回の対象S4を割り当てた。従って二石rootは偶数ORでLOSS。以前の115対象classも再分類し、LOSS1 / WIN54 / UNKNOWN60だった。全第三手が既に覆われたため、この順位表は今後の作業キューではなく事後的な分類と費用proxyである。

## 信頼範囲

新規S5/S6のexact葉はsolver-trusted exactで、solver raw・合法手数・canonicality・固定先手極性・保存証拠・cache衝突/隔離・SHA-256を監査した。全119 root手、S4応手、S5境界は独立整数幾何で再生成し、AND/ORを独立伝播した。既存31 LOSS classやそのcache一次出力に残るK0372記載の信頼依存は消えていない。この結果は**terminal-onlyの独立minimax DAG証明ではない**。11×11空盤面の勝敗も分類しない。

solver binary SHA-256: `8d0781ce89ad11a7cd8011cf351d627793b5b76351b7639e433875a43f627cb2`。solver source SHA-256: `48e51bb56288e090f51996eb4d9a208ca0458d11f73ba61bf5f08dade25db446`。S6 boundary source `independent.py` SHA-256: `954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f`。各raw、run manifest、audit receipt、worker cache、merge receipt、全frontier、root proof、候補順位には個別SHA-256を記録した。profile-off binaryの`--log`出力は全行0 byte（空ファイルSHA-256もreceiptに記録）で、rawとrun manifestをsolver結果の一次データとしている。

## 保存物と再現

- `input/`: 凍結したS5/S6選定・1行入力、baseline cache、solver build/source SHA。
- `output/raw/`: 66 S5とS6全試行の1行solver rawに加え、再利用した保存S6 raw 2件。後者は `input/saved-s6-raw-relocations.json` のSHA-256で固定し、tracked rawへbyte-identicalに移した。各選定・費用・SHAは対応する`*-run.json`に保存。
- `output/`: 事前監査、全batch audit receipt、S6全98子の統合集計、exact-only merge receipt、3,384 class frontier、119手被覆、整数/LP双対、115候補再分類、root LOSS proof、raw inventory audit。
- `scripts/`: 独立幾何選定、cold solver runner、S5/S6 raw監査、安全なmerge、frontier・被覆・root再構成。

`output/raw-sha256-audit.json` は23個の監査receiptが参照する202 raw記録を再読し、176個のユニークrawについて内容SHA、replay行、局面key、石数、合法手数、予算、nodes、判定を照合する。未追跡 `.local` rawへの依存は0件。S6保存rawのうち1件は旧history上の `.local` パスに由来するが、Git管理された同一SHAのrawを収録し、移動manifestが旧history SHAとraw SHAを記録する。

cacheはexact-only worker出力を独立監査した後、atomic mergeした。merge receiptはUNKNOWN drop 0、quarantine conflict 0、final cache SHA-256を記録する。独立root監査はこのcacheをsolver出力と区別し、solver-trusted葉を終局まで閉じた証明とは扱わない。

1M first passをrawから再監査し、S6境界を集約する:

```powershell
python research/experiments/n11-s4-boundary-direct-20261012/scripts/summarize_s6_split.py `
  --audit research/experiments/n11-s4-boundary-direct-20261012/output/s6-first-batch-audit.json `
  --audit research/experiments/n11-s4-boundary-direct-20261012/output/s6-second-batch-audit.json `
  --audit research/experiments/n11-s4-boundary-direct-20261012/output/s6-third-batch-audit.json `
  --audit research/experiments/n11-s4-boundary-direct-20261012/output/s6-fourth-batch-audit.json `
  --audit research/experiments/n11-s4-boundary-direct-20261012/output/s6-fifth-batch-audit.json `
  --audit research/experiments/n11-s4-boundary-direct-20261012/output/s6-sixth-batch-audit.json `
  --audit research/experiments/n11-s4-boundary-direct-20261012/output/s6-seventh-batch-audit.json `
  --audit research/experiments/n11-s4-boundary-direct-20261012/output/s6-eighth-batch-audit.json `
  --audit research/experiments/n11-s4-boundary-direct-20261012/output/s6-ninth-batch-audit.json `
  --audit research/experiments/n11-s4-boundary-direct-20261012/output/s6-tenth-batch-audit.json `
  --audit research/experiments/n11-s4-boundary-direct-20261012/output/s6-eleventh-batch-audit.json `
  --audit research/experiments/n11-s4-boundary-direct-20261012/output/s6-twelfth-batch-audit.json `
  --output research/experiments/n11-s4-boundary-direct-20261012/output/s6-first-pass-summary.json
```

15M escalation and S5→S4→root proof can be rechecked without launching exploration:

```powershell
python research/experiments/n11-s4-boundary-direct-20261012/scripts/audit_s6_split.py `
  --selection research/experiments/n11-s4-boundary-direct-20261012/input/s6-fourteenth-batch-selection.json `
  --run-manifest research/experiments/n11-s4-boundary-direct-20261012/output/s6-fourteenth-batch-run.json `
  --worker-cache research/experiments/n11-s4-boundary-direct-20261012/output/s6-fourteenth-derived-s5-worker.cache
python research/experiments/n11-s4-boundary-direct-20261012/scripts/audit_frontier.py `
  --output research/experiments/n11-s4-boundary-direct-20261012/output/frontier-after-s6-parent-loss.json
python research/experiments/n11-s4-boundary-direct-20261012/scripts/audit_root_loss.py `
  --output research/experiments/n11-s4-boundary-direct-20261012/output/root-60-27-loss-proof.json
python research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py `
  --s5-cache research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache `
  --out research/experiments/n11-s4-boundary-direct-20261012/output/cardinality-after-s6-parent-loss.json
python research/experiments/n11-s4-boundary-direct-20261012/scripts/reclassify_115_candidates.py
```

safe mergeの実行記録は`output/s5-s6-derived-cache-merge-receipt.json`。merge regressionはUbuntu/WSLで26件PASS。長時間solver探索は手動runnerからだけ実行し、同一root・同一予算UNKNOWNは再実行しない。
