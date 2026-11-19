# 第17 WIN7-D10 証明書本体の出版と独立レーン byte-exact 再現（2026-11-20）

## この実行の経緯

- 前回（K1069出版レーン）の再開として、K1069が発見した
  WIN7-D10 root `00004000000000821082000000000100`（child `00004000000000821082000000000000` + bit 8）
  の第17証明書抽出・三重独立検証に着手した。
- 着手からまもなく、並走 n11 レーンが commit `0c1264b228`（2026-11-19T20:51:01Z）で
  同じ成果を丸ごと出版済みであることを検出した
  （`n11-residual78-seventeenth-win7-cert-extract-20261120/`・38 gate 全PASS・triple verified）。
  両レーンの着手は互いに不可視であった
  （K1067/K1068 二重出版事故と同じ同時着手パターン）。
- 本レーンは実験一式の再出版を行わず（重複出版回避）、以下の照合と補完だけを行った。

## 独立抽出の一致確認（duplicate agreement）

本レーンの抽出は windfall4 実験(commit pin `d2e918055a`)の検証スクリプト一式
（extractor blob SHA-1 `c267f260d1d6fcc49ed5367509e854c81822497e` 照合済み）から行い、
次の結果を得た:

- 抽出: 60 loser first-move（`legal_candidates.py` 独立列挙と一致）・
  sum 4,250,297 nodes・49,591 行・fbt_drops 0・fatal なし・perMove 全 ok/uncapped・
  terminalRange ⊆ [13,17]。2 回実行で証明書 byte-identical。
- 三重検証: TS Bareiss sub-root 分解 60/60 PASS・consumed union==rows（missing 0 / extra 0）、
  純 python exact Bareiss 60/60 PASS・visited_winner_states 150,963、
  BigInt 3x3 余因子 60/60 PASS。root-check 7 石・mobility 60。

これらの数値はすべて、並走の検証正本
`output/seventeenth-cert-triple-verification-20261120.json` の記録と完全一致した。
証明書 SHA-256 は同一の
`21dd2f0e9f0b8ec22e917fce5a732835098baf37570a227bebacacb4c13807c8`
（1,791,541 bytes・49,593 行）。すなわち第17証明書は
「並走レーン 2 実行 + 本レーン 2 実行」の計 4 回の独立抽出すべてで byte-exact 同一であり、
engine・extractor の決定論がレーン横断で追加確定した
（K1069 掃引のノート内再実行一致に続く、完全独立プロセス間での初の証明書単位の一致例）。

## 証明書本体の出版（ギャップ補完）

- 並走の検証正本は `certs/win7-root-00004000000000821082000000000100-20261120.n11`
  を正本として pin しているが、commit `0c1264b228` のファイル一覧に certs/ はなく、
  証明書本体が repo に存在しない状態だった
  （windfall4 の4枚は本体が出版されているため不整合。証明の可搬性・独立検証可能性を損なう）。
- 本レーンが保持する byte-exact 同一の証明書本体を
  commit `b7a6db5fb0`（2026-11-19T20:56:22Z）で
  `research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/certs/win7-root-00004000000000821082000000000100-20261120.n11`
  として出版し、pin を充足した。
- 着地検証: commit-SHA pin 付き raw 取得で SHA-256 `21dd2f0e…7c8`・
  1,791,541 bytes・ヘッダ2行・末尾行 `…0100 13` + 改行保持を確認済み。

## 解釈と次回への引継ぎ

- 本 log は証明書の「発見・検証」の再主張ではなく、(a) 独立レーン間の byte-exact 合意、
  (b) 証明書本体の repo 補完、の二つの事実の記録である。判定の正本は並走実験dirの
  38 gate 正本のままである。
- **本項はどの残余行も閉じない。** fold10（第17 receipt fold・残余 74→72 行の見通し）は
  実験dir README の「次の一手」に並走レーンが宣言済みのため、本レーンでは
  二重事故防止のため着手していない。次回実行は単一オーナー宣言ノートで合意を
  確認してから fold10 に着手すること。
- REFUTED-D10 は LOSS 証明ではない。pn/dn・solved 数を勝敗として読まない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。**
