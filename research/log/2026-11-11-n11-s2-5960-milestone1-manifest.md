# 2026-11-11 S2 {59,60} milestone-1 S6 worklist manifest（長期レーン）

- 開始時 main = 00a460eb（全6ペアクラス完了のコミット、並走分取り込み済み）。
- 目的: K0729 greedy順序の先頭2証明書（certA={5,115}・certB={27,93}・blocker 4個）について、
  S5 orbit代表からS6 orbit worklistを厳密に確定し、外部solver（generate_five_terminal_loss7系・
  df-pn系）が直接消費できるbatch manifestを整える。
- 幾何機械: 禁止マスク生成をBareiss 121回det4から整数外接円公式（(D·z−U)^2 == R^2 の整数比較、
  直線の場合は外積）に差し替え。verify_conditional_s6_cover_46.py のreconstruct不変量を全て再現
  （94 / 7,890 / 7,813 / 3,868 / {2:3791,3:77}、priority S4鍵 0x...3800800000000000 = bits {47,59,60,61}）。
  第三系統の独立検証となる。
- 結果: certA 54 S5 orbit（raw義務4,795）→ S6 orbit 2,191、certB 54（4,698）→ 2,150、
  S5共通2・S6共通79・**union 4,262**（K0725のcensus 2,191/2,150/79/4,262と完全一致）。
- 新規測定: 各S6 orbit repの合法手数（cost）分布 min 52 / median 77 / max 93 / mean 76.78 /
  sum 327,221 raw S7辺。≤60が50件存在し、solverはcost昇順消化で早期exitのWIN7当たりが
  期待できる（s6sweepの平均~7.7試行と同じ構造）。
- 出力: scripts/milestone1_worklist.ts（自己完結再現・単独実行でfull manifestを返す）・
  output/milestone1_manifest.json（S5 106 rep×義務数 + S6 4,262鍵cost順フルリスト + protocol）。
- protocol: WIN_for_mover証明書=認定済みWIN7子鍵1個、LOSS=全合法子認定、同一canonical鍵の
  verdict不一致はWIN/LOSS conflictとして即停止・監査、D4不変性で1 orbit 1 repのみ認定。
  既存cache（s6sweep 3,868・frontier 2,401）は中央系（51を含む位置）に偏在し、milestone-1の
  S6/S7鍵（51を含まない）との一致は原理的にほぼないため、当座のcache再利用は期待できない。
- 負の観測（実験事実）: 7石飽和（maximal-safe）による1レベルWIN7判定を試験したところ、
  94 universe由来のS6 3,854 WINのうち飽和S7子で解けるものは1件もなかった
  （K0675のWIN7認定は全て深い戦略証明書に由来）。この観測により「飽和shortcutで安く閉じる」
  道は閉ざされ、milestone-1のS6 orbitは全件が深探索であることが確定した。
- 11×11空盤・二石root {49,60} は **UNKNOWN**。
- 次回: 外部計算資源でmilestone-1のS6 orbit消化（cost昇順・resume形式）、
  またはmanifestのcert拡張（greedy 3位 {71} 以降のS5/S6 orbit列挙）。
- なお generated再生成（uv/Python）は本環境では未実施（CI差分検出あり・保留中の既知課題）。

- 訂正（同一コミット時間帯の並走とK番号衝突）: 並走セッションが先に
  K0745（5×19満容量witness）をmain反映していたため、本項目は **K0746** に再採番した
  （旧K0745-s2-5960-milestone1-s6-manifest.mdは削除・内容不変）。
