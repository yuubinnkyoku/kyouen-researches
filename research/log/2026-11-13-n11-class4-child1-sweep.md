# 2026-11-13 n11 class4-batch1: S6 child #1 7th-stone sweep（d10）と engine v14 修正

## 目的

類4最良候補 S5 `00000000020000003800000080000000` の S6 child #1
`00000000020000003800000080080000`（6石 {27,31,57,58,59,89}、loser to move）に対して
66個の非退化7石目候補を深さ制限探索（d=10 ply, terminal 13-17石）で走査し、
WIN7-within-depth-10 証明書の元となる勝ち候補を特定する。

## engine v14 の修正（本セッションで発見・修正、記録必須）

1. **memo mVal Uint8 オーバーフロー（致命的）**: packed 値 `w*32+l+1` は w=32（未証明勝ち）
   エントリで 1025+ となり 255 を超える。Uint8 切捨てにより LOSS@d=0 が「近い勝ち」と誤読される。
   → **Uint16Array で解決**。v12 以前の「d=6 で勝ち」は全て無効。
2. **FULL[3] = 0x01FFFFFF**: 0x07FFFFFF は盤外 cell 121/122 を着手可能にした。修正済み。
3. **候補合法マスクの chunk バグ**: 7石目の bit を chunk0 からのみ除去していたため
   bit>=32 の候補では自分の着手セルが合法手に残留し、同一局面への「着手」→ memo 衝突
   （bit=32/95 の偽 nodes=1 artifact）を生んだ。→ bit をその所属 chunk（<32:L0, <64:L1,
   <96:L2, else L3）から除去するよう修正。**本修正以前の bit>=32 候補の結果は全て無効**。
4. **ST[6] 未設定**: 候補 loop で ST[6] を設定せず solve すると newBannedInto が stale な
   7石目で禁止マスクを計算した。修正済み。

## engine 検証

pilot root `00000000000000003802000008000006`: d=6 fail 3,257 nodes, d=8 fail 108,869,
**d=10 WIN 622,788 nodes, maxStones=17** — 公表 terminal range [13,17] と一致。
pilot 証明書は公開済みのため再生成していない。

移動順序の測定: mobility ordering は closeScore ordering より 6倍悪い
（pilot d6: 20,121 vs 3,257 nodes）。closeScore を維持。

## child #1 sweep 結果（d=10、nodeCap 700,000/run、root mobility 昇順）

| bit | mob | 結果 | nodes |
|-----|-----|------|-------|
| 85 | 44 | d6/8/10 全fail | 40,965 / 102,274 / 132,921 |
| 95 | 44 | d6/8/10 全fail | 60,171 / 172,738 / 275,989 |
| 48 | 46 | d10 fail | 379,447 |
| 81 | 46 | d10 fail | 323,872 |
| 72 | 48 | d10 fail | 219,730 |
| 32 | 49 | **未完**（700k node 消費しても完了せず >1M 見込み） | — |
| 87 | 49 | **未完**（同上） | — |

- 候補の難度は mob 44-46 で 22万-38万 nodes、mob 49 で >70万 nodes と急増。
- 残り 59 候補（bit=91 以降、mob 49-63）は未走査。全候補目録は
  `class4-batch1-progress-audit.json` の candidate_order_mob 参照。
- 勝ち候補はまだ見つかっていない。**d=10 fail は「10 ply 以内の勝ちなし」であって
  候補の反証ではない**（より深い勝ちはあり得る）。

## 解釈上の注意

- 11x11 空盤・二石 root {49,60}・S2 {59,60} はいずれも **UNKNOWN**。
- 本エントリの fail は WIN7-within-depth-10 の否定のみを意味する。

## 次回

1. bit=91（mob 49）から sweep 継続（skipBits {85,95,48,81,72}）。
2. bit=32, 87 は専用 run（または d=8 先行）で再挑戦。
3. win 発見時: 証明書再構築 → verify mirror PASS → deflate+b64 →
   `class4-batch1-certificates/<rootHex>-win7.cert.gz` + verifier + verified JSON を push。

> ※後日の訂正: 冒頭の6石表記 {27,31,57,58,59,89} は audit JSON からの転写誤り。
> 正しくは hex key の bit-cell **[19,31,59,60,61,89]**（66候補・mob 全一致で確認、第2セッション参照）。

## 第2セッション（2026-11-13、長期レーン）: engine v15 再構築・commit・検証、child_cells 訂正

### 再現性ギャップの解消（本セッションの主成果）

engine v14 は前セッションの sandbox 内にのみ存在し repo に残っていなかった。
本セッションで規則定義（n11-central-19-cover-20261031/verify_five_terminal_loss7.py）から
**engine v15 として再構築し、scripts/class4_child1_sweep_engine.ts として commit した**
（commit 449d0941）。以後の sweep はこのスクリプトを正本とする。

### v15 の検証（全て PASS）

- child#1 の非退化7石目候補 66 個の集合と全 66 個の root mobility が
  candidate_order_mob と完全一致（規則実装の直接検証）。
- pilot root: lossAt(6)=false（5,949 nodes）・lossAt(8)=false（277,800 nodes）—
  公表 d6/d8 fail と判定一致。
- **WIN 検出の独立制御**: 公表 LOSS7 向き root 00000000000000a03808100000000000
  （winner=root mover・786 strategy states）で winAt(10)=true・
  terminal 石数範囲 [12,16] が公表 verifier 統計 (12,16) と完全一致。
- pilot d10 は v15 では sandbox deadline 内に完了せず（>700k nodes で capped）。
  公表 v14 d10 WIN（622,788 nodes・maxStones=17）がstanding evidence。
  **v15 の node 数は v14 と直接比較できない**（ordering 詳細が異なる）。
  判定と terminal 範囲のみが比較可能量。

### 再構築時に発見した実装バグ（v15 開発中、記録用）

1. **move 配列の共有エイリアシング**: legalMoves が単一配列を再利用すると
   再帰レベル間で内容が破壊され loop が静かに途切れる（per-depth 配列で解決）。
2. **着手セル自身の bit を child banned に OR し忘れる**と同一セルへの再着手が
   合法になり memo を汚染する（v14 の per-chunk bit bug と同族）。

### 訂正: audit JSON の child_cells

前セッションの child_cells [27,31,57,58,59,89] は転写誤り。
hex key の bit-cell は **[19,31,59,60,61,89]**（66 候補・mob 全一致で確認）。
audit JSON を訂正済み（commit 1664139c）。

### sweep 進捗（mob-50 帯は重い）

- bit=25: d10 で >950k nodes で capped（450k でも capped）。**未反証・未解決**。
- bit=40: 同様に >950k nodes で capped。**未反証・未解決**。
- heavy pending リスト: {7, 25, 32, 40, 87}（いずれも capped のみで判定なし）。
- 勝ち候補はまだ見つかっていない。

### 次回

1. mob-50 帯の残り 80, 83, 108 から継続（1実行1候補・nodeCap ~950k）。
2. heavy pending {25,40,7,32,87} は d=8 先行か実行間 memo 永続化（file_system 経由の
   状態 dump）で専用対応。
3. win 発見時: 証明書再構築 → repo verifier（verify_five_terminal_loss7.py 複製・
   winner_parity=1）で検証 → deflate+b64 → class4-batch1-certificates push。

### 解釈上の注意（変更なし）

- 11x11 空盤・二石 root {49,60}・S2 {59,60} はいずれも **UNKNOWN**。
- capped 実行はいずれの方向にも何も証明しない。

## 第3セッション（2026-11-13、長期レーン）: bit=80 capped、cross-run memo永続化の計測的否定的結論、安価プローブ戦略

### bit=80（mob 50）d10

950k nodes で capped（複数回）。**未反証・未解決**。heavy pending に追加。
このときの memo 状態（計測価値あり）:
- occupied 238,430 / 262,144（91%）、proven bounds 117,212 件
- **全 117,212 件が確定 win/lose bounds**（noWin/noLose bound >=5 は cap frontier に存在しない —
  frontier 部分木は一度も完成しない）
- win bound 分布: 1ply=31,813 / 3=57,585 / 5=7,573 / 7=205 / 9=1
- lose bound 分布: 2=13,077 / 4=6,745 / 6=212 / 8=1

### cross-run memo 永続化: 計測に基づき**不可**と結論

1. sandbox 16MiB 制限: base working set ~13-15MB、headroom <1MB。
   全 117k bounds の dump（~4.7MB）は in-run に保持不能（write_file 引数も run に保持される）。
2. 高価値のみ（win>=5/lose>=4、~15k行）の永続化は I/O 上可能だが、
   **resume 効果がない**: 落とした浅い facts（win<=3/lose<=2、~89k件）を毎回再証明して
   予算を消費する。loaded entries による root-level memo hit は 0 件、frontier は前進しない。
3. memo 表が91%占有率で memoEntry の probe 失敗が多発し、同一 key の重複エントリが
   発生（dump 4,766行 -> unique 1,796）。MS=1<<19 は 16MiB に収まらない。
4. file_system read_file は ~64KB/chunk で打ち切られる。offset/next_offset の
   loop が必須（最初の loader は 14,737行中 1,594行しか読めていなかった）。

**結論**: mob-50帯の完了には (a) 外部計算資源、(b) 証明書の decomposition
（universal 節点を child 単位の独立 fact に分割）、(c) 探索の根本改善のいずれかが必要。
sandbox内での単純な memo 永続化の再試行はしないこと。

### 安価プローブ戦略（150k/candidate triage）

残候補を 150k nodes/candidate で一斉スキャン（WIN 候補は遠か 950k で完了し得るため）。
結果: 83, 108, 6, 18, 77, 94 が各 150k で capped、103 は 50k で予算切れ。
**全候補 heavy、verdict 無し**。mob-51..52 帯も軽くない。
次回は 43, 75, 82, ... の残り 46 候補を継続プローブ。

### AND 節点 move ordering の負の結果

lossAt（AND 節点）の子を wscore 昇順（石から遠い手を先）にソートすると
pilot d8 で **1.8倍悪化**（>500k capped vs baseline 277,393 nodes 完了）。
bit 順（デフォルト）を維持。closeScore は winAt（OR 節点）専用のまま。

### log 復元（運用記録）

第2セッションの log 追記で push_files が**ファイル全体を置換**してしまい、
第1セッションの記録が一時失われた。git 履歴（1664139c 時点）から復元し、
訂正注記付きで再push（ceb8218）。以後 log 追記は必ず既存全文を読み戻して
結合してから push すること。

### 解釈上の注意（変更なし）

- 11x11 空盤・二石 root {49,60}・S2 {59,60} はいずれも **UNKNOWN**。
- capped 実行（950k 含む）はいずれの方向にも何も証明しない。

### プローブ継続（第3セッション後半）

150k probes をさらに15候補実施: 43, 75, 82, 11, 37, 70, 84(50k), 93, 113, 114, 118,
28, 42, 45, 78(149,998)。**全候補 capped、verdict 無し**。
計22候補がすべて 150k を超えたため、150k プローブはこれ以上情報を増やさない。
残り32候補（3, 34, 54, 88, ..., 2、mob 56-63帯）は各々フル ~950k run が必要。
audit JSON に全プローブ結果を反映済み（4b0e86ce）。

## 第4セッション（2026-11-13、長期レーン）: bit=3 capped、v15-vs-v14 コスト監査（インフレ 1.8-7.2倍）、順序/deepening 否定結果、close-first AND の -30%

### bit=3（mob 56、未走査帯の最初）d10

fresh memo・cap 950k で capped。**未反証・未解決**。heavy pending に追加。
pilot d6 制御（loss=false・5,949 nodes）は公表値と完全一致（実装健全性の再確認）。
run ceiling の再確認: pilot+950k×2 の混在 run と 1.4M node 尘用 run は両方
process safety deadline 超過（timeout 2件を実験事実として記録）。~950k-1M/run が上限。

### v15-vs-v14 コストインフレの定量監査（本セッションの主成果）

v14 の d10 反証 6 候補を v15 で安価に再確認しようとしたところ、**1件も再現しない**:
- pilot d6: v14 3,257 vs v15 5,949（1.83x）/ pilot d8: 108,869 vs 277,800（2.55x）
- bit85 d10: v14 132,921 vs v15 >950,000（≥7.15x）
- bit95 d10: v14 275,989 vs v15 >950,000（≥3.44x）
- bit48 d10: v14 379,447 vs v15 >500,000（≥1.32x、500k cap で打ち切り）

**解釈**: v14 の node 数は失われた実装の産物であり、committed engine（v15）では
再現不能。v14 の d10 反証 6 件は判定・terminal range の standing evidence として有効だが、
node 数は非比較対象。**第2-3セッションの「mob-50帯は一様に重い」結論は
このインフレで交絡している**（v15 の 950k cap には v14 が 133k-380k 自単位で
完了した候補が含まれる）。以後の予算計画は v15 単位で行うこと。

### v14 効率回復の試み（全て否定的・計測済み）

1. **OR/AND ソート方向グリッド**（close-desc/close-asc/bit × 3、9組合せ）pilot d6:
   5,917-14,179 nodes。v14 の 3,257 に近づく組合せなし（default が最良）。
2. **closeScore 半径/重みバリアント**（r1/r2/r3/r4/r3sq/r3flat）pilot d6:
   5,949-5,970 nodes。不感。
3. **細段階 deepening**（d2→d4→d6→d8、memo 共有・累積）pilot:
   34/683/6,637/284,462。v14（3,257/108,869）を再現しない。
4. **カウンタ定義仮説**: winAt 呼び出しのみ（694/92,769）・lossAt のみ（5,255/184,624）も
   v14 公表値と不一致。
5. **last-response ordering**（winAt 子を相手直前の石への chebyshev 距離でソート）bit85:
   d6 13,818 / d8 211,848 / d10 capped。d8 でむしろ悪化。
6. **bit85 deepening**（d6→d8→d10・累積）: 13,820 / 186,626 / >950,000。
   興味深い非対称: d6 段階は v14 の 40,965 より **3倍安い**のに d10 段階は爆発する。

### 唯一の肯定的結果: close-first AND ordering

lossAt（AND 節点）の子を wscore **降順**（近い手を先）にソートすると
pilot d8 が 277,800 → **193,556 nodes（-30%）**。ただし深さ依存（d6 では 7,646 と悪化）。
d10 での効果は未検証（bit95 close-AND >756k capped で有意差未確定）。
第3セッションの「昇順は1.8倍悪化」結果と対になう検証として記録。
（v16 候補: d8+ 段階に限定して採用する価値あり。）

### 次回

1. close-first AND variant を heavy-pending 1件（例: bit=25）に 950k で適用し、
   d8 の -30% が d10 に届くかを検証。
2. 届かない場合、sandboxでの候補消化は情報効率が乏しいと判断し、
   (a) 外部計算ランナー向け engine+driver の整備、または
   (b) certificate-chunked decomposition（universal 子ごとの独立 fact 分割）
   に移行する準備を優先。
3. mob-56 帯の継続は1実行1候補（34, 54, 88, 102, ...）で並行して継続可。
4. win 発見時: 証明書再構築 → repo verifier → deflate+b64 → class4-batch1-certificates push。

### 解釈上の注意（変更なし）

- 11x11 空盤・二石 root {49,60}・S2 {59,60} はいずれも **UNKNOWN**。
- capped 実行（950k 含む）はいずれの方向にも何も証明しない。
