# 2026-11-17 n11 class2-lane: cost73k hybrid seed union design

## 開始時点

最新 main は `2375b55d1a8e3353f774cbe3fc64b4f0a916d1c0`。作業前に `AGENTS.md`、`research/knowledge/README.md`、K0023、K0863、K0865、K0868、K0907、K0909、およびcost73kのworker分割・seed容量関連の最新logを確認した。branch / PRは作成しない。

## 観察した非閉包

境界保存4-worker測定（入力JSON blob `b97c9334f04f98f6ba7bb8a4c8b1de9689810d5e`）では、FINAL4と出版2-way seedの比較が次の値だった。

| 集合 | 件数 |
|---|---:|
| boundary FINAL4 | 4,975,265 |
| published 2-way seed | 4,291,899 |
| 共通 | 4,291,637 |
| FINAL4のみ | 683,628 |
| 2-wayのみ | 262 |
| **和集合** | **4,975,527** |

共有4,291,637キーの値はFINAL4側が同等以上で、value violationは0。したがって、FINAL4の値を共有キーに使い、2-wayにしかない262キーを追加すれば、両方のキー集合を含むseedを構成できる。これは既存測定からの集合算術であり、262キーの実データを今回再構築したわけではない。

## ハイブリッドseedの構成案

- FINAL4のKYOENWM2レコードを、既存の順序のまま先頭に置く。
- 2-way seedにのみ存在する262レコードを、重複なしで後ろに追加する。
- ヘッダーは1行だけにする。2個目のヘッダーはレコードとして誤読されるため付けない。
- seedMemoは入力行を順番に処理し、内部で並べ替えない（orchestrator blob `5ac1e3c0ec47ec3f9ae63ed709362feb5a1df213` のPATCH_BLOCKを確認）。

追加分をFINAL4の後ろに置く限り、既存FINAL4キーの挿入順・挿入成否は変わらない。追加262キーの失敗は最大262件。境界FINAL4のMS=1<<24実測失敗14,657件を基準にすると、同じMSでの総失敗上限は14,919件（0.29985%）で、0.1% gateには届かない。

一方、和集合4,975,527件をMS=1<<25に置いた初期負荷は **14.8282%**。K0909の容量設計値（初期負荷およそ15%以下）に収まる。よって実験候補はMS=1<<25。ただし、**この境界保存seedに対するMS=1<<25の挿入失敗数・band node数は未測定**である。

注意点として、K0909の「MS=1<<25で失敗28件」は、別のノード数均衡4-way seed（4,985,986 keys）の結果であり、今回の境界保存FINAL4（4,975,265 keys）へ転写していない。

## 機械検査

`derive_hybrid_seed_union_73k_20261117.py` は、公開JSONのblob pin、2集合の分割恒等式、共有値の単調性、seedMemoの逐次読込を確認し、上記の導出値をJSONへ出力する。今回の実行では以下を確認した。

- FINAL4 = shared + FINAL4-only
- 2-way = shared + 2-way-only
- union = FINAL4 + 262 = 2-way + FINAL4-only
- shared value violations = 0
- seedMemoは行順を保持し、並べ替えをしない

出力 `hybrid-seed-union-design-73k-20261117.json` は **DESIGN_DERIVED_NOT_MEASURED** と明記する。実キーの再構築、seed挿入、探索は行っていない。

## 次の実測

1. pinned 2-way / boundary-4way distinct表から262件のkey/valueを再構築し、個別SHAと件数を固定する。
2. FINAL4の後ろへ追加し、MS=1<<25でseed挿入する。
3. 4,975,527件のrecord identity、conflict 0、inserted/failedを検査する。
4. 22 rootを再実行し、証明書byte 22/22一致を必須gateにする。boundary4-onlyとnode-balanced4-wayのper-bit nodesも比較する。

## 解釈ガード

これはcache seedの構成設計であり、探索・証明書生成・receipt foldではない。新しいWIN/LOSS verdictなし、証明書bytes不変、manifest行の閉鎖なし。WIN7-D10は個別7石rootの深さ10以内の先手勝ちだけを示し、REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4は引き続きUNKNOWN。
