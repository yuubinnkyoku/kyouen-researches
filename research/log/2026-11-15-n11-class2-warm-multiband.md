# 2026-11-15 class2-lane warm multiband 35証明書バッチとchain head再計算

対象: 標準11×11の弱解決に向けたclass2-lane長期レーン。本セッションは
「巨大rootを回す」のではなく、coordinatorが選んだ検証可能な小証明の蓄積で
frontierを厳密に前進させた。

## 実施内容

1. **候補選定（coordinator計器）**
   - `scripts/rank_warm_candidates_20261115.py` を新規作成し、全公開sweep記録の
     未認証WIN7-D10候補（既存warm rebuild記録と公開証明書を持つrootを除く）の
     marginal_in_manifest を after-cost75b 基準（1,049/6,798/535,812/5,068/399,535）
     で再導出した。
   - 自レーンband（cost-61d/61e/61f/62a/63a/64b/65e/71b）から正利得35件、
     加えて cost-72 bit52（sweep所有者がwarm扱いを明示済み）を選択。
     並走band（cost-65h/67b/68c）は意図的に除外。
   - 出力: `output/class2-lane-warm-candidate-ranking-20261115.json`

2. **証明書抽出・独立検証（35件）**
   - `scripts/warm_rebuild_pipeline_20261115.py`: repo-verbatim抽出器
     （class4_child1_cert_extractor_exact.ts、blind kill-table空、FBS=1<<20、
     fbt_drops=0要請、行はLC_ALL=Cで整列・一意化）、4並列chunk実行。
   - 各証明書を `verify_win7_certificate_bigint_independent.mjs`
     （BigInt完全幾何、探索器・cache不使用）で検証: root 7石・安全、
     相手合法初手==legal_candidates.py独立列挙、全sub-root PASS
     （==mobility）、戦略/消費行和集合 0/0 双方向、終局石数13〜17、
     行は厳密増加・一意。
   - 計量: 戦略行合計 1,586,728 / 抽出節点合計 481,639,572。
   - キャリブレーション: 公開済みcost-71b bit-109証明書をbyte-exact再現
     （md5 513b87f7…）してから抽出を開始。
   - 公開: 27件は単一ファイル、8件（>1.75MB、push時の16MiB/約26op制約で
     単発不可）は `part1of2/part2of2` 分割（repo既存慣例）。全件の遠隔
     md5を照合し、分割8件は連結==全体md5を検査済み。

3. **root不在確認**
   - 全35 root hex について GitHub code search（quoted検索）を実施。
     ヒットは全てsweep/inflight/audit記録JSONとlog markdownのみで、
     先行する証明書ファイルは0件。`root_absence_check` として記録JSONに保存。

4. **記録JSON**
   - `scripts/rebuild_warm_records_20261115.py` で35件全ての検証を再実行
     （~1.4秒/件、全assert合格）し、`scripts/assemble_warm_multiband_record_20261115.py`
     で `output/class2-lane-warm-multiband-certificates-20261115.json`
     （35 record、band/child provenance、md5/sha256/bytes、storage layout、
     root_absence_check付き）を生成。

5. **chain headの取り込みと再現**
   - push前にmainを再取得したところ、並走レーンが cost-75c を完了し
     `class-frontier-cost75c-recompute-20261115.json`（第二class-2ターゲット
     S5 `00000000000000803202000000000000` を12 receiptで閉鎖、cost-72
     bit111 partial receiptもfold済み、1,062/6,785/534,768/5,055/398,491）
     がchain headになっていた。同recomputeの outstanding_not_folded は
     warm multiband証明書のfoldを「chain headへの正規merged recompute」
     として明示的に本バッチに委ねていた。
   - cost-75cスクリプト・sweep/raw batch/証明書記録を取得し、runpyで
     基準を再現: 出力は公開headと byte-identical（md5 ef7e332f…）。

6. **merged recompute**
   - `scripts/recompute_frontier_warm_multiband_20261115.py`: after-cost75c
     基準をassert（1,062/6,785/534,768/5,055/398,491）→ 35記録を公開順に
     fold（各marginalは拡大和集合から再導出、root==child|1<<bit・rows・
     sub-roots・union・md5・sha256を全件assert）。
   - 結果: **解消S6 1,109 / 残り 6,738 / 費用 531,295 /
     open需要 5,008 / 395,018**。
   - 35 receipt合計: marginal 166、manifest内 47。zero-mim 5件。
     - cost-71b bit14: cost-75c bit22（既fold）と同一root
       `00000000000000803202000000404000` の独立再抽出でWIN7一致。
       正の重複相互照合として記録（marginal 0は正しい）。
     - cost-64b bit102 / cost-61e bit102 / cost-61f bit102 / cost-61d bit119:
       manifest親は基準時点で既被覆。
   - best coverable class-2五石親 `00000000000000809102000000000000` は
     35軌道・2,525 → **17軌道・1,220**。
   - 2回実行でbyte-identical（frontier JSON・ranking CSV・top-candidates CSV）。

## 公開物

- 証明書: `output/class2-lane-cost{61d,61e,61f,62a,63a,64b,65e,71b,72}-certificates/`
  （27単一 + 8×2分割、全件remote md5照合済み）
- 記録: `output/class2-lane-warm-multiband-certificates-20261115.json`
- chain head: `output/class-frontier-warm-multiband-recompute-20261115.json`
  + ranking/top-candidates CSV（after-warm-multiband）
- スクリプト: `scripts/rank_warm_candidates_20261115.py`,
  `scripts/warm_rebuild_pipeline_20261115.py`,
  `scripts/rebuild_warm_records_20261115.py`,
  `scripts/assemble_warm_multiband_record_20261115.py`,
  `scripts/recompute_frontier_warm_multiband_20261115.py`

## 運用メモ

- pushは16MiB/約26-28opのrun_typescript制約下で1ブロック1ファイル。35ページ
  を超えるファイルはpush演算の実行前に制限へ到達するため、1.75MB超は分割必須。
  fast-forward競合（並走pushと同時）は同内容再pushで解決。raw CDNは404を
  負キャッシュするため、着地確認はコネクタのget_file_contentsでも行うこと。
- warm_records.jsonはchunk並列で互いに上書きされるため、全件再構築は
  `rebuild_warm_records_20261115.py`（検証再実行・~1.4秒/件）で行うこと。

## 未完・次回

- cost-71b残りWIN7 bits 1/74/94/117、cost-61d bit22（=cost-71b bit1 root）
  の証明書化。並走band（65h/67b/68c）は触らない方針を維持。
- cost-72 sweep完了記録はcost-72レーンが公開する（bit52は本バッチでreceipt
  としてfold済み）。
- 解消計数はmanifest被覆の前進であり、勝敗の確定ではない。

## 勝敗に関する明記

**標準11×11空盤、二石root {49,60}、S2 {59,60}、class 2、class 4 はすべて
UNKNOWNのままである。**本セッションのsolved数増加（1,062→1,109）は
manifest被覆の帳簿上の前進であり、空盤や二石rootの勝敗を意味しない。
