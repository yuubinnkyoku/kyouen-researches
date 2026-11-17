# 2026-11-18 n11 class2-lane: cost78c raw batches 1–6 audit

## 入力と範囲

最新 main を再確認し、`AGENTS.md`、knowledge README、K0023・K0863・K0865・K0868・K0907・K0909、cost78c claim v1、head-1473 census v11、先行した幾何監査、raw batch 1–6を取得した。作業開始時 main は `232dd35d9a4de98baca7a7c77e0357d9908408a6`。batch 1–3の出典commitは `c368cbe8bfa72462d480bc2e9dc7c7152907c339`、batch 4–6は `500f8c86e53b0a49695fe5db9d31dcd9e6b9401d`。

## 54/66 bitの独立集計

6 batch（各9候補+pilot 1件）を全てpin付きで再集計した。対象bitはcensus v11が選んだ66 open bitの先頭54個と完全一致し、重複・欠落はない。

- **9 WIN7-D10**: bits 1, 4, 9, 30, 49, 69, 75, 79, 100
- **45 REFUTED-D10**
- capped 0
- 候補探索節点 **164,783,764**（pilot 20,412を含む全記録164,804,176）
- 全54 rootのD4正準形は相異なる。9 WIN正準形も相異なり、既知12 confirmation rootとの一致なし。
- 全54候補で `andclose=true`、終端石数範囲[13,17]。pilot_d6は6/6が3402 nodes。

batch別候補節点は 36,696,776 / 30,741,077 / 31,031,855 / 22,541,283 / 20,110,810 / 23,651,757。

## claimの同期ずれ

raw batch 1–6がmainにある一方、cost78c claim v1は依然 `batches_run 0`・未実行というstatus文字列のまま。監査では競合する並走セッションのclaimを上書きせず、同期ずれを明示して残した。残りはopen bit 12個（66個中54個完了相当）。

v15 cross-engine照合、9候補の証明書抽出・独立検証、receipt foldは未実施。したがって9件は固定pinされたv17 raw結果上のWIN7-D10候補であり、独立クロスエンジン検証済み証明書ではない。45 REFUTED-D10もLOSS証明ではない。

## 再現物

- `scripts/audit_cost78c_raw_batches_1_6_20261118.py`
- `output/class2-lane-cost78c-raw-batches-1-6-audit-20261118.json`

監査値の実計算は独立JavaScript整数実装で行い、Python標準ライブラリ版は固定入力pin付きの再現器として公開した。このrunではPython版そのものは起動していない。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4は引き続き UNKNOWN。
