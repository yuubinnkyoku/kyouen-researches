# n11-residual78-cache-join-resolve6-20261120

K1059 が宣言した「次の一手 = resolve6」の実行: 39 dead root 除外後、
K0863 の 8,964-root 全体 verdict cache を D4 正準形 root 単位で再構築し、
post-cache sweep 記録・published WIN receipt と結合して残余 78 行の
add-one-stone 候補を再照合した。branch/PR は作らず main に直接出版。

## 何をしたか

- **cache 再構築**: K0863 の出版 scan スクリプト
  (`n11-class2-lane-sterile-unclosability-20261116/theorem_applicability_scan_20261116.py`)
  をそのまま import し、corpus 1,279 ファイルから engine map を再構築。
  manifest sha256 検証 1,272/1,279 一致（差 7 ファイルは post-scan 修復系
  inflight/cost69h raw で、現 main 上に無く既知の差分。133 target child の
  verdict 分布は出版 scan と完全一致）。engine bits 8,960（出版 8,964 との
  差 4 bit は非 target 系 corpus 修復由来）、WIN/REFUTED 同一 root 衝突 0。
- **結合**: engine cache ∪ 115 published transfers ∪ post-K0863 掃引
  (sweep48/sweep28/k1039_sweep28/k1040_sweep3/sweep35/sweep43/sweep39_dead)
  ∪ sweep6 両順序 probe ∪ published WIN receipt fold roots
  （global・second/third・fourth・fifth/sixth・seventh・eighth・ninth-twelfth
  の全入力 chain を fold 正本から再構築）。
- **resolve5 正本との整合**: universe 再構築 7,969 == resolve5 出版値
  （gate PASS・SHA-256 5a2f4815… の正本を pin）。39 dead root は全て
  judged REFUTED に含まれることを gate で確認。
- **再照合**: 78 残余行への coverage・最大 matching・greedy set cover・
  singleton を再計算し、既知 WIN (receipt) の余行被覆も照合。

## 結果（output/post-saturation-full-cache-join-resolve6-20261120.json が正本）

- universe 7,969 内: judged REFUTED **446** / judged WIN **4** /
  fresh 7,519 / fresh-safe **4,417** / fresh-unsafe 3,102
  （resolve5 の fresh-safe 4,728 − 39 dead + join 判明分。
  決して pn/dn や solved 数ではない）。
- pair 辺 667（resolve5 時点 706 から join 判明分が減）・78 行すべてに
  singleton 候補あり・**最大 matching 39・stranded 0**
  （新規 39 本の live witness 計画が残余 78 行を 1 回被覆で完全に覆う）。
- source 別判断 root 数: cache-engine 279 REF / transfer 5 REF /
  sweep48 42 / sweep43 39 / sweep39_dead 39 / sweep35 26 / sweep28+k1039 25+25 /
  k1040 3（root-source 重複帰属あり）。
- **windfall**: cache 由来の WIN7-D10 verdict 4 root が残余行を被覆
  （class2-lane-cost65h child `00000000000000803202000000001000` の
  bit 40/43/99/118。root `…83202010000001000` ほか 4 本は正本参照）。
  全て 7 石・D4 正準形・unsafe 0。raw batch 行（batch3/4/7/8）は
  loss=true・uncapped・terminalStoneRange [13,17]・andclose=true、
  pilot_d6 (3,402 nodes, loss=false) 合格、bit 43 は別プロセス node-exact
  再現（3,269,824）。**単一順の depth-10 verdict であり receipt 化には
  証明書抽出（child=root−最小セットビット）と BigInt 3x3 / Bareiss 4x4
  による独立二重検証が必須。それまではこれら 4 行を閉鎖扱いにしない**（出力
  JSON の `win_cover_detail` に出典・bit 行・pilot 行・lane context を
  証拠として記録済み）。
- 全 12 gate 合格（pin-resolve5・pin-sweep39・corpus-manifest・
  k0863-harvest・k0863-target-children-exact・k0863-transfers・sweep6・
  receipt-roots・join-conflict-free・universe-size・dead39-excluded・
  win-coverage-of-residual）。WIN/REFUTED conflict 0 で fail-closed。

## 決定論性・再現

- stdlib のみ・repo ルートから
  `python3 research/experiments/n11-residual78-cache-join-resolve6-20261120/resolve6.py`
  で約 25 秒。**2 回実行で byte-identical**
  （出力 SHA-256 `e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a`）。
  sort_keys JSON・wall time は記録外。

## 解釈規約（他の n11 項目と同一）

- REFUTED-D10 は LOSS 証明ではない。fold・被覆は行の簿記であり
  ゲーム理論的値には一切言及しない。witness root は条件付き depth-10
  掃引計画であり証明書ではない。stranded 0 は本 scope の候補集合に
  限る数学でない観察であり、scope 外の閉鎖機構を否定しない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4
  はすべて UNKNOWN のまま。** 本項は 78 行の勝敗を 1 行も確定しない。

## 次の一手

1. windfall 4 WIN root の証明書抽出（extractor v16 + 二重検証）→
   receipt fold 候補。抽出規約は child=root−最小セットビット・生整数 hex。
2. 39 live witness の depth-10 両順序掃引（K1059 と同一 driver/runner v17
   規約・pilot_d6 制御）。
3. 並走 candidate-supply-scope-audit の「full 8,964 cache join は未実施」
   記述は本実験で解消（同 audit の正本と数値整合: 4,689→join 後 fresh-safe
   4,417・706→pair 辺 667・78 singleton は不使用のまま）。
