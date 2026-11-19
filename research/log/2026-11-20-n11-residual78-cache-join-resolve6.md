# 2026-11-20 n11 長期レーン: resolve6の実行（K0863全体cache結合・39 dead root除外後の残余78行再照合）

## 経緯

- K1059 の追記が宣言した「次の一手: resolve6（39 dead root 除外後、
  K0863 8,964-root 全体 cache との root 単位結合・再照合）」を本実験で実行した。
- 前回の candidate-supply-scope-audit（n11-residual78-witness39-
  candidate-supply-scope-audit-20261120）の予測値（sweep39 外 fresh-safe
  4,689 本・未選択 pair 667 辺・78 singleton 候補未使用）を入力として使用。

## 何をしたか

- K0863 の出版 scan スクリプトをそのまま import し、corpus（研究実験
  n11-s2-5960-ms5-s7-reuse-20261113/output の 1,279 ファイル）から
  engine map を再構築。manifest sha256 は 1,272/1,279 一致、差 7 ファイルは
  post-scan 修復系（inflight/cost69h raw、現 main 上に無い。K0863 README の
  既知 gap 記述と整合）。engine bits 8,960（出版 8,964 と差 4 bit は
  非 target 系 corpus 修復由来）、133 target child は全て出版scan分布と
  完全一致、115 published transfers を取得。
- post-K0863 掃引 7 系統（sweep48・sweep28・k1039_sweep28・k1040_sweep3・
  sweep35・sweep43・sweep39_dead）・sweep6 両順序 probe・published WIN
  receipt fold 正本一式（global tarball を含む全 fold から root chain を
  再構築）を D4 正準形 root 単位で結合。WIN/REFUTED 同一 root 衝突 0
  （fail-closed）。
- resolve5 正本の SHA pin 照合・universe 再構築 7,969 gate・
  39 dead root 全て judged REFUTED gate。

## 結果（output/post-saturation-full-cache-join-resolve6-20261120.json が正本）

- universe 7,969 内: judged REFUTED **446** / judged WIN **4** /
  fresh 7,519 / fresh-safe **4,417** / fresh-unsafe 3,102。
  sweep39 外 fresh-safe 4,689 本のうち 272 本（268 REFUTED + 4 WIN）が
  cache join で既に判定済みだったことが判明（scope-audit の
  「未判定とは主張しない」記述の数値確定）。
- pair 辺は 706 → **667**、singleton 候補は 78 行すべてに残存、
  **最大 matching 39・stranded 0・witness 39 本**（live 計画。
  78 行を 1 回被覆で完全に覆う）。
- **windfall**: cache 由来 WIN7-D10 が 4 根、残余 4 行を被覆
  （cost65h child の bit 40/43/99/118。root は
  `00000000000000803202010000001000`・`00000000000000803202080000001000`・
  `00000008000000803202000000001000`・`00400000000000803202000000001000`。
  7石・D4正準形・unsafe 0）。raw batch 行（3/4/7/8: loss=true・uncapped・
  terminalStoneRange [13,17]・andclose=true）と pilot_d6 対照行
  （3,402 nodes・loss=false）を出典として JSON に記録。bit 43 は別プロセス
  node-exact 再現（3,269,824 nodes・determinism_rerun）。engine は
  repo-verbatim v16 runner・depth 10・andclose=1・cap 1e9。
- **単一順 verdict のため windfall 4 根は pending receipt 候補**。
  receipt fold による行閉鎖計上には証明書抽出（child=root−最小セットビット・
  生整数 hex）と BigInt 3x3 / Bareiss 4x4 による独立二重検証が必須。
  39 live witness 計画が 78 行を独立に完全被覆するため、被覆簿記は
  windfall を閉鎖扱いにしなくても成立する。

## 決定論性・運用

- stdlib のみ・repo ルートから 1 コマンド・約 25 秒。
  **2 回実行で byte-identical**
  （SHA-256 e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a）。
  全 12 gate PASS（pin-resolve5・pin-sweep39・corpus-manifest・
  k0863-harvest・k0863-target-children-exact・k0863-transfers・sweep6・
  receipt-roots・join-conflict-free・universe-size・dead39-excluded・
  win-coverage-of-residual）。
- corpus 差 7 ファイルの「missing on main」は K0863 出版時の scan 実行後に
  修復された corpus（cost-69h raw batch2/3 は並走レーンが復元済み）のうち
  現 main に無い inflight 系であり、target child 分布の完全一致から
  verdict 結合への影響なし（記録用の観察）。

## 解釈規約（不変）

- REFUTED-D10 は LOSS 証明ではない。windfall の WIN-D10 も receipt 化される
  までは行閉鎖ではない。fold・被覆も行の簿記でありゲーム理論的値に
  一切言及しない。witness root は条件付き depth-10 掃引計画である。
  stranded 0 は本 scope の候補集合に関する観察で、scope 外の閉鎖機構を
  否定しない。78 行は 1 行も閉じていない（frontier 6,213/492,021・
  solved S6 1,635・5親target 34/112 不変）。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4
  はすべて UNKNOWN のまま。**

## 次の一手

1. windfall 4 根の証明書抽出（extractor v16 repo-verbatim + BigInt 3x3 /
   Bareiss 4x4 二重検証）→ receipt fold 候補（fold 機械の入力 chain
   再構築を含む）。
2. 39 live witness の depth-10 両順序掃引（K1059 同一 driver/runner v17
   規約・pilot_d6 制御・cap 30M）。
3. 抽出・掃引のどちらかが進めば残余 78 行の閉鎖カウント（簿記）が
   前進する。どちらも判定そのものでなく被覆簿記段階の話であることに注意。
