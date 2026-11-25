# 2026-11-18 n11 class2-lane: cost78c raw batches 1–3 audit

## 入力と範囲

最新 main を再確認し、`AGENTS.md`、knowledge README、K0023・K0863・K0865・K0868・K0907・K0909、cost78c claim v1、head-1473 census v11、先行した独立幾何監査、cost78c raw batch 1–3を取得した。作業開始時 main は `500f8c86e53b0a49695fe5db9d31dcd9e6b9401d`。raw batchの出典commitは `c368cbe8bfa72462d480bc2e9dc7c7152907c339`。

## 監査結果

3 batch（各9候補+pilot 1件）を独立に読み直した。

- 対象はopen bitの先頭27個と完全一致。重複・欠落なし。
- pilot_d6は3件すべて3402 nodes、loss=false、capped=false。
- 27候補すべて `andclose=true`、cappedなし、終端石数範囲[13,17]。
- 候補探索節点合計 **98,469,708**（pilot 10,206を含む全記録98,479,914）。
- raw v17結果は **5 WIN7-D10**（bits 1,4,9,30,49）、**22 REFUTED-D10**、0 capped。
- 27個の7石rootのD4正準形は全て相異なる。5つのWIN正準形も互いに相異なり、12 confirmation rootの既知REFUTED正準形との一致なし。
- 5つのWIN rootはすべて7石、terminal range [13,17]。bit1は7,264,656 nodes。

batch別候補節点は 36,696,776 / 30,741,077 / 31,031,855。commit subjectはbit1の最初のWINとその節点数を強調しているが、raw batch 1–3全体にはbit4/9/30/49も `loss=true` として記録されている。集計はcommit subjectではなく、pinしたper-bit JSONLから行った。

## claimとの不整合と未完了作業

cost78c claim v1は取得時点でもstatus文字列が `batches_run 0` のままで、raw batch 1–3の公開内容と同期していない。この監査では並走レーンとの競合を避け、claim本体は変更していない。次のclaim更新時にbatch数・5 WIN/22 REFUTED・98,469,708 nodesを反映する必要がある。

v15 cross-engine照合、5 WIN候補の証明書抽出、証明書の独立検証、receipt foldは未実施。したがって今回の5件は、固定pinされたv17 raw結果に基づくWIN7-D10候補であり、まだ独立クロスエンジン検証済み証明書ではない。22 REFUTED-D10もLOSS証明ではない。

## 再現物

- `scripts/audit_cost78c_raw_batches_1_3_20261118.py`
- `output/class2-lane-cost78c-raw-batches-1-3-audit-20261118.json`

監査値の実計算は独立JavaScript整数実装で行い、Python標準ライブラリ版は固定入力pin付きの再現器として公開した。このrunではPython版そのものは起動していない。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4は引き続き UNKNOWN。
