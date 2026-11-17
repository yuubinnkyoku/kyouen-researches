# 2026-11-18 n11 class2-lane: cost78c claim structure audit

## 対象と固定入力

作業開始時に最新 main と `AGENTS.md`、`research/knowledge/README.md`、K0023・K0863・K0865・K0868・K0907・K0909、cost78c claim、head-1473 census v11、cost64d/cost70b の転送元記録を再取得した。branch / PR は作成しない。

- 作業開始時 main の最新 commit search 結果: `9bf3866cd4a2b71cdf5d11cb313ffc7173abf1b2`
- cost78c claim blob: `7c38b88e33d1c176bdedf582bea7138cfa6a067a`
- census v11 blob: `1e2b6a2b688db1a93098edea62b5793b54efaaba`
- K0868 blob: `b097210d0b49d7cf014cc6a554298b1e49e83384`
- cost64d claim blob: `e3cf7378a08b156c5c0299c52e4ccbcd59de9236`
- cost70b sweep blob: `d0eb4d23f674d218b23065ca72d4b63b58a9eeea`
- cost70b raw batch 5 blob: `67ded8a966b1880604985fd817fbe4195f29f47d`

## 結果

K0868のdet4規約を独立に実装し、6石 child `00000000000000403800000008000008` の20個の3点組を全て調べた。

- 石bit: [3, 27, 59, 60, 61, 70]。child hexとの一致を確認。
- 空セル115個を、合法78・禁止37へ完全分割。
- 禁止37セルすべてにdet4=0となる具体的な3石 witness を付与。
- 独立再導出した合法bit集合はclaimの78候補と完全一致。
- open 66 bit と confirmation 12 bit は互いに素で、和集合は合法78候補と完全一致。
- 12 confirmation rootすべてについて、childにbitを追加した局面のD4正準形がclaimのroot_canonと一致。
- 12件の転送元を全て照合。10件はcensus v11の既存verdict mapにあるREFUTED-D10 bitとD4正準形が一致、cost64d bit3はtarget bit13とraw-identical、cost70b bit48はraw batch 5の `loss=false,capped=false` とD4正準形一致。
- census v11の選択対象、edge cost 78、demand {c1:0,c2:1,c4:0} もclaimと一致。

監査器はPython標準ライブラリのみで、入力Git blob SHAを固定して再計算する。実験出力JSONには37個の禁止セルとそのwitness、12転送の照合結果を保存する。

## 解釈境界

これは探索前の構造・転送元監査であり、depth-10探索を実行していない。新しいWIN/LOSS verdict、証明書、receipt foldは発生していない。12件のREFUTED-D10は個別7石rootの深さ10以内先手勝ち不成立であり、LOSS証明ではない。cost78cの66 open bitは未探索のまま。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はすべて UNKNOWN。
