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
run ceiling の再確認: pilot+950k×2 の混在 run と 1.4M node 専用 run は両方
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
第3セッションの「昇順は1.8倍悪化」結果と対をなす検証として記録。
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

## 第5セッション（2026-11-13、長期レーン）: sandbox 飽和の確定（4候補全て capped）、close-first AND の d10 不達、外部ランナー整備・検証

### レジューム実行（第4セッション next 1-3）

全 run fresh memo・cap 950k・d10:

| bit | mob | ordering | 結果 |
|-----|-----|----------|------|
| 25 | 50 | close-first AND | capped 950k（未反証・未解決） |
| 34 | 56 | default | capped 950k（未反証・未解決） |
| 48 | 46 | close-first AND | capped 950k（未反証・未解決） |
| 81 | 46 | default | capped 950k（未反証・未解決） |

### 主結論: close-first AND の -30% は d10 に届かない + sandbox 飽和

- pilot d8 の -30%（277,800→193,556）は bit=25・bit=48 の d10 では 950k cap 内に
  完結させられず、有意な前進が無い。**d8 段階限定の改善としてのみ有効**。
- mob 44-56 に跨る4候補（うち2件は v14 が自単位 13-38万で反証済みの 48/81、
  1件は mob-56 帯初の full-budget 試行 34）が**全て v15 単位で 950k を超える**。
  第4セッションの判定基準により sandbox での候補消化は情報効率が乏しいと確定し、
  レーンを外部計算準備に移行する（certificate-chunked decomposition は次の代替）。

### 外部ランナーの整備・検証（本セッションの成果物）

`scripts/class4_child1_runner.ts`（commit 3b0603fa）:
- v15 と同一規則を **per-candidate freshEngine() factory** で完全リセット可能に包装
  （memo・fbt・wscore を候補間で共有しない — sandbox では実行毎に新規プロセスで
  等価実現していたが、外部では1プロセスで多数候補を回すため必須）。
- **pilot d6 制御内蔵**（loss=false・5,949 nodes 以外は abort）。
- close-first AND は depth>=8 に自動ゲート（d6 悪化の計測に基づく）。
- CLI: `node --experimental-strip-types class4_child1_runner.ts --bits 34,54 --depth 10 --cap 50000000 --out results.jsonl`
  （依存ゼロ・JSONL 出力・--andclose/--nocontrol/--child オプション）。
- **検証（sandbox 内でコミット対象コードをそのまま実行）**: pilot d6=5,949 ✓・
  pilot d8 default=277,393 ✓・pilot d8 close-AND=193,556 ✓（第4セッション計測と
  完全一致）・bit85 d6 fresh=13,820 ✓（第4セッション default 値と一致）。

### 外部での想定運用

- 1プロセス1候補・cap 5M-50M nodes（外部機には 16MiB/950k の制約なし）。
- 優先順: heavy-pending {7,25,32,40,80,87} → mob-56 帯（34 の再試行を含む
  54, 88, 102, ...）。JSONL を持ち帰り verdict を audit JSON に反映。
- node 数は引き続き v15 単位（v14 と非比較）。判定と terminal 範囲のみが比較可能量。

### 反映

- 3b0603fa: runner script（検証結果を header に記載）
- 8da0047a: audit JSON（session5_sandbox_saturation・pending_incomplete に 34/81 追加・
  not_yet_searched から 34 除去・bit25 に session5_close_and 注記）
- 本コミット: log 第5セッション
（全て push 後に repo から読み戻し検証。並走なし: 反映前に HEAD e2de0830 を再確認。）

### 次回

1. 外部計算資源で runner を実行し JSONL を回収・反映（資源が無い場合は
   certificate-chunked decomposition の設計に移行）。
2. sandbox 内での 950k 候補 grind は情報効率が乏しいことが確定したため
   原則再開しない（安価な制御・回帰は例外）。
3. win 発見時: 証明書再構築 → repo verifier（winner_parity=1）→ deflate+b64 →
   class4-batch1-certificates push。

### 解釈上の注意（変更なし）

- 11x11 空盤・二石 root {49,60}・S2 {59,60} はいずれも **UNKNOWN**。
- capped 実行（950k 含む）はいずれの方向にも何も証明しない。

## 第6セッション（2026-11-13、長期レーン）: certificate-chunked decomposition の設計・検証・実行 — bit85 の d10 反証を v15 単位で再現、bit7 が d10内 WIN7 候補（全50初手 kill）

### レジューム実行（第5セッション next 1-2）

外部計算資源が本セッションに無いため、次の代替である certificate-chunked decomposition
（第3セッションの結論 (b)、第5セッション next 2）を設計・実装・検証した。

### 手法: d10 判定の chunk 分解

- `lossAt(root,10)=false` ⟺ ∃ loser初手 m: ∀ winner応手 r: `lossAt(root+m+r,8)=false`（pass chunk）
- `lossAt(root,10)=true` ⟺ ∀ m: ∃ r: `lossAt(root+m+r,8)=true`（kill chunk）
- 深さ帳簿は 10−2=8（再帰的に 8→6→4 の梯子も可能）。
- **作業単位は chunk**（独立・未cap・depth-bounded engine証明）。実行予算で打ち切られても
  証明済み chunk は残り、記録済み chunk を skip して再開できる。capped chunk は pending
  のままで他を無効化しない。単一的 950k grind（第5セッションで情報効率乏しいと確定）
  の置き換え。
- 実装: `scripts/class4_child1_chunk_prover.ts`（engine v15 を verbatim 内蔵・依存ゼロ）。
  ledger: `output/class4-batch1-chunk-decomposition.json`。

### 制御（全て PASS）

1. bit85 d6 fresh = **13,820**（公表 v15 制御と完全一致）。
2. bit85 d8 fresh = **172,806**（新計測・default ordering）。
3. **制御A（同型性）**: bit85 の d8 分解（直接d8 witness m=0・40応手・chunk深さ6・
   1実行・memo共有）は総 **172,804** nodes で直接 d8 の 172,806 と差2（root節点分）しか
   違わず判定も一致 — 分解は1プロセス実行では直接探索と同型。
4. **制御B（決定論）**: chunk (m=2, r=66) の fresh 再解が 58,292 nodes・判定まで完全一致。

### bit85: d10 反証を v15 単位で再現（witness m=2）

- m=0（d8 witness）は d10 witness ではない: 応手 r=18 の chunk が loss=true（43,513 nodes）
  で m=0 は d10 で殺される。**witness 同定は深さ毎に行うこと**（新教訓）。
- m=2 は40応手全ての chunk が未cap・loss=false → **lossAt(root,10)=false、REFUTED**。
  総 1,701,951 nodes / 3実行（376,581 + 765,378 + 559,992）・capped chunk 0。
- 単体 v15 d10 は 950k で capped・判定なしであったのと対照的に、同一主張を
  再開可能な複数実行で閉じた。v14 の standing evidence（d10 反証）と判定一致。

### bit7: d10内 WIN7 候補の発見（本セッションの主成果）

- **全50個の loser 初手が kill された**: 各 m について winner 応手 r_k が存在し
  `lossAt(root+m+r_k, 8)=true`（未cap）。ゆえに `lossAt(root,10)=true`、
  すなわち **7石目 bit=7 は depth 10 以内の WIN（winner_parity=1）**。
- 総 4,156,721 nodes / 6実行（723,573 / 705,439 / 708,483 / 704,147 / 712,062 / 603,417）・
  capped chunk 0。kill 表（50件の m→r_k と node数）は ledger 参照。
- **検証**: 同一 run 内で pilot d6 制御 5,949 再現・kill chunk 3件の fresh 再解が
  node数完全一致（(0,114)=14,123・(120,28)=21,687・(110,8)=124,166）・
  root 50手の列挙が kill 表と完全一致。
- v14 は bit=7 を 506k で capped（判定なし）だった。chunk 分解で初めて判定が確定した。

### 解釈上の注意

- 本 verdict は v15 engine 規則（repo verifier 規則と公表制御で検証済み）での
  **depth-bounded な WIN7-within-10** である。証明書再構築と独立 verifier 実行は未実施
  （次回の最初の作業）。bit=7 の WIN7 候補という事実のみでは class 4・S2 {59,60}・
  二石 root {49,60}・11x11 空盤は閉じない。
- 11x11 空盤・二石 root {49,60}・S2 {59,60} はいずれも **UNKNOWN**。
- capped 実行はいずれの方向にも何も証明しない（本セッションの全 chunk は未cap 完了）。

### 反映

- e55d8225: chunk prover script（engine v15 verbatim 内蔵・検証記載）
- 674e1ec4: ledger JSON（bit85/bit7 の chunk 記録・kill 表・制御・解釈ガード）
- 0e011b6f: audit JSON session6_chunk_decomposition 追記
- 本コミット: log 第6セッション
（全て push 後に repo から読み戻し検証。並走: 高速レーン width67/68 キャンペーンと
主題独立・反映前に HEAD 5a1a19ef を再確認・競合なし。）

### 次回

1. **bit=7 証明書再構築**: chunk 毎に勝ち戦略木を抽出（深さ1,3,5,7,9のwinner着手）し
   `n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS` 形式
   （root 行・32hex board 行ソート済み）で証明書化 → repo verifier
   （verify_five_terminal_loss7.py 複製・winner_parity=1・EXPECTED に本件追加）で独立検証 →
   deflate+b64 → class4-batch1-certificates push。
2. heavy-pending {25,32,40,80,87,34} と未走査候補を chunk キャンペーンで消化
   （1候補複数実行・chunk毎に再開）。WIN 発見時は同じ証明書プロトコル。
3. d8 witness ≠ d10 witness の教訓を維持: より浅い witness の再利用は
   目標深さで chunk 集合を再検証してから。

## 第7セッション（2026-11-13、長期レーン）: bit7 WIN7 証明書の抽出・独立検証・反映（第6セッション next 1 完了）

### 証明書の抽出・構築

- root 00000000020000003800000080080080（S6 child + bit7・7石・loser to move）の
  勝ち戦略を n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS 形式で
  **30,947 行**（<32hex> <move> 昇順ソート済み・プレーンテキスト 1,121,870 bytes・
  md5 0f1fedfe06c658acdd02577f9d7da9d2）として確定。
- 抽出は extractW/extractL 再帰（winner手は closeScore 順で最初に lossAt=true となる手を
  記録、loserは全合法応手を展開）。**kill-first**（第6セッション kill 表 m→r_k を深さ1の
  優先手にする）で盲順の 10-40 倍削減（m=0 盲 597k → kill-first 数百k/実行）。
- 実行統計: b1(m10-44) 667,470 / b2(45-82) 634,317 / b3(83-92) 656,983 / b4(93-110) 643,407 /
  b5(112-120) 517,343 / r1fix(m0,8) 437,856 nodes・総 3,557,376。

### 独立検証（全て PASS）

- verify_five_terminal_loss7.py の TS 移植（厳密 Bareiss 4x4 行列式・number 演算で
  Hadamard bound 下厳密・BigInt リファレンス移植と 84 triple 完全一致・engine 不使用・
  cache 不使用）。単一 root 全文検証は 16MiB 制限で不可のため **50 部分木分解検証**
  （sub-root=root|m・8石・winner手番・局所 winner_parity=0、V1..V7 の 8実行単位バッチ）:
  全 50 sub-root PASS・terminal 石数範囲 [13,17]。
- **消費済み戦略行の和集合 = 30,947 行と完全一致**（comm 双方向 0・到達不能行/欠落行なし）。
- root 検査 PASS（7石・4点共円なし・loser mob=50）。
- **制御**: 公表 pilot root 00000000000000a03808100000000000（winner=root mover）での
  新規抽出 2,510 行が同一 verifier で PASS（terminal [14,16]。公表証明書786行とは
  別の有効戦略で、判定+terminal 範囲が比較可能量）。

### 運用事故 2 件（記録）

1. run 間の read-modify-write で read_file の ~64KB 切断により過去実験分 ~33k 行が欠落
   （第3セッションと同一過誤の再発）。**修正**: 実行ごとに独立ファイル + sort -u で bash merge。
2. run 1（m=0,8）末尾 24 行欠落を verifier の missing-row チェックが検出 →
   r1fix 再抽出で復元・証明書再構築。**verifier が実際の欠落を捕捉したことは
   検証プロトコルの有効性の実証**。

### 反映（全て push 後読み戻し確認）

- 761b6ea7: scripts/class4_child1_cert_extractor.ts（抽出器・engine v15 verbatim 内蔵）
- 31a52068: scripts/verify_bit7_win7_cert.ts（TS verifier 移植・sub-root 分解・root 検査）
- 8f38a849: output/class4-batch1-certificates/n11_s7_00000000020000003800000080080080.cert
  （1,121,870 bytes・md5 記録。deflate+b64 は sandbox に圧縮ツール無のため省略）
- 8defb938: output/class4-batch1-bit7-certificate.json（検証記録）
- a95a46f5: audit JSON session7_bit7_certificate 追記
- 本コミット: log 第7セッション

### 解釈上の注意（変更なし）

- bit=7 は「class4-batch1 内の深さ10以内 WIN7」として証明書+独立検証が完了したのみ。
  class 4・S2 {59,60}・二石 root {49,60}・**11x11 空盤はいずれも UNKNOWN**。
- 本証明書は 7石局面からの winner_parity=1 勝ちを深さ10以内で示すもので、
  空盤の勝敗を何ら断定しない。

### 次回

1. heavy-pending {25,32,40,80,87,34} と未走査候補を chunk キャンペーンで消化。
   WIN 発見時は同一証明書プロトコル（抽出 → 独立検証 → push）。
2. 外部計算資源が使える場合は scripts/class4_child1_runner.ts で cap 5M-50M を投入。
3. 証明書はプレーンテキスト運用（md5 記録）。読み戻し検証と union 等価チェックを
   プロトコルの標準部分とする。

## 第8セッション（2026-11-13、長期レーン）: bit25 chunkキャンペーン — 2件目のWIN7候補（全50初手 kill・6.77M nodes・10実行）

### レジューム実行（第7セッション next 1）

heavy-pending bit=25（mob 50。v15 単体 d10 は default/close-first AND とも 950k で
capped・判定なし）を chunk 分解で消化した。run 予算 ~620-700k・chunk cap 300k・
chunk 深さ 8・reply 順 wscore 降順（fail-fast）。予算打ち切りは kill 表を --dead、
解決済み pass reply を --done に渡して厳密に再開（再開欠落ゼロ）。

### 結果: bit25 は depth 10 以内の WIN7 候補（2件目）

- **全50個の loser 初手が kill された** → lossAt(root,10)=true。
  root hex 00000000020000003800000082080000（S6 child + bit25・7石・loser to move）。
- 総 **6,768,196 nodes / 10実行**（642,403 / 712,362 / 697,536 / 670,495 / 680,450 /
  689,548 / 692,524 / 670,967 / 696,745 / 615,166）・capped chunk 0。
  kill chunk 計 1,848,372 / pass chunk 計 4,919,824 nodes。
  kill 表（50件の m→r_k）と per-chunk node 数は ledger の bit25 エントリ参照。
- **検証（全て一致）**: pilot d6 制御 5,949（キャンペーン開始時）・
  kill chunk 4件の fresh 再解（(0,42)=219,816・(34,50)=12,317・(114,91)=8,041・
  (113,50)=34,181）と pass chunk 1件（(21,82)=92,425）が node 数まで完全一致・
  root 50手の列挙が kill 表と完全一致。terminal 石数範囲 [13,17]。

### 解釈上の注意（変更なし）

- bit=25 の WIN7 候補は class4-batch1 内部の深さ10以内判定にすぎず、
  class 4・S2 {59,60}・二石 root {49,60}・**11x11 空盤はいずれも UNKNOWN**。
- 証明書再構築・独立検証は未実施（次回の最初の作業。bit7 と同一プロトコル:
  kill-first 抽出 → 50部分木分解検証 → union 等価 → push）。

### 反映

- 65cb836a: ledger JSON（bit25 エントリ・kill 表・制御・解釈ガード）
- 続くコミット: audit JSON session7b_bit25_chunk_campaign・log 第8セッション
（push 後読み戻し確認。並走なし。）

### 次回

1. **bit=25 証明書再構築・独立検証・push**（第7セッションの bit7 プロトコル踏襲。
   verifier は --root 00000000020000003800000082080000 で再利用可）。
2. heavy-pending 残り {32,40,80,87,34} と未走査候補の chunk キャンペーン継続。
   WIN 発見時は同じ証明書プロトコル。
3. mob-50 帯で WIN7 が連続（bit7・bit25）— 帯全体の証明書化コストを考慮し、
   抽出器の kill-first 指定は ledger の kill 表から自動読み込みに拡張する価値あり。
## 第9セッション（2026-11-14、長期レーン）: bit25 WIN7 証明書の抽出・独立検証・反映（第8セッション next 1 完了）

### 証明書の抽出・構築

- root 00000000020000003800000082080000（S6 child + bit25・7石・loser to move）の
  勝ち戦略を n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS 形式で
  **37,854 行**（<32hex> <move> 昇順ソート済み・プレーンテキスト 1,363,951 bytes・
  md5 66c35945925c8c8286d58f745cc22507）として確定。
- 抽出は bit7 と同一の extractW/extractL 再帰 + kill-first（ledger bit25 kill 表を深さ1優先手）。
  実行統計: b1 357,373 / b2 496,080 / b3 555,389 / b4 480,926 / b5 457,485 / b6 563,911 /
  b7 719,805 / b8 348,057 / b9(m=0) 496,399 nodes・総 4,475,425 nodes（9実行）。
  m=0 は ok=true・capped=false・terminal range [13,17]（最終runで完走確認）。
- 生row 46,670 → sort -u で 37,854 unique。重複 hex は相互kill対（90<->72・37<->18・
  40<->70・50<->38・33<->45系）の共有部分木によるもので、同一局面に異なる勝ち手が
  競合する場合は sort -u の辞書式（最小move）規則で解決し、全文検証で閉包性を確認。

### 独立検証（全て PASS）

- repoの verify_bit7_win7_cert.ts を --root 00000000020000003800000082080000 で再利用
  （TS移植・厳密Bareiss 4x4行列式・engine不使用・cache不使用）。16MiB 制限のため
  証明書は read_file chunk 読み込み + 4語 open-addressing flat table で保持
 （Map<string> 全文保持は OOM）。
- **50 部分木分解検証**（V1..V7・8/8/8/8/8/8/2の7実行）: **全50 sub-root PASS**・
  terminal 石数範囲 [13,17]・terminals 計 13,161・opponent edges 計 72,848・
  seen states 計 81,162。
- **消費済み戦略行の和集合 = 37,854 行と完全一致**（comm 双方向 0・到達不能行/欠落行なし）。
- root 検査 PASS（7石・4点共円なし・loser mob=50）。
- **負制御（実効性の実証）**: 初回の verifier 実装は盤面 key の最上位語（bit64超）を
  Int32 に切捨てるバグがあり、missing-winning-player-move チェックが最初の sub-root
  （root|m=0）で即発火・中断 — 整合性チェックが表の破損を実際に捕捉。
  4語化修正後に全50 sub-root が PASS。

### 反映（全て push 後読み戻し確認・1コミット1ファイル）

- 0b835029: 証明書本体 output/class4-batch1-certificates/n11_s7_00000000020000003800000082080000.cert
  （1,363,951 bytes・md5 記録・git 37,856 additions = ローカル行数と一致）
- 5a9ec762: 検証記録 output/class4-batch1-bit25-certificate.json
- 6991c23f: ledger JSON（bit25 status 完了化・certificate オブジェクト追記・next item 1 済）
- 35f681b1: audit JSON session8_bit25_certificate 追記
- 本コミット: log 第9セッション

### 解釈上の注意（変更なし）

- bit=25 は「class4-batch1 内の深さ10以内 WIN7」として証明書+独立検証が完了したのみ
 （bit7 に次ぐ2件目）。class 4・S2 {59,60}・二石 root {49,60}・
  **11x11 空盤はいずれも UNKNOWN**。
- bit7 の 400 node 集計差（2026-11-14 監査の留保）は本証明書とは独立で未解決のまま。

### 次回

1. heavy-pending 残り {32,40,80,87,34} と未走査候補の chunk キャンペーン継続。
   WIN 発見時は同一証明書プロトコル（抽出 → 独立検証 → push）。
2. 外部計算資源が使える場合は scripts/class4_child1_runner.ts で cap 5M-50M を投入。
3. 共有部分木での move 競合は sort -u 最小move規則 + 全文検証で閉じられることを
   本セッションで実証済み — heavy帯の証明書コスト見積りに反映する価値あり。

## 第10セッション（2026-11-14、長期レーン）: bit32 chunkキャンペーン — heavy-pending初のREFUTED（witness m=44・15.88M nodes・23実行）・driver bug検出と完全再計算

### レジューム実行（第9セッション next 1）

heavy-pending bit=32（mob 49。v14 単体 d10 は 700k で capped・判定なし）を
chunk 分解で消化した。run 予算 ~700k・chunk cap 300k・chunk 深さ 8・
reply 順 wscore 降順（fail-fast）。予算打ち切りは state に chunk 進捗を記録して
厳密に再開（再開欠落ゼロ）。

### 結果: bit32 は depth 10 で REFUTED（heavy-pending 初の chunk 法による反証）

- **witness m=44**: winner 応手 48 個すべての chunk が未capで loss=false →
  lossAt(root,10)=false。root hex 00000000020000003800000180080000
 （S6 child + bit32・7石・loser to move）。
- 反証確定のため残り 8 初手 {76,104,105,106,116,117,118,120} は未走査のまま
  打ち切り（verdict に不要・記録済み）。
- 総 **15,884,259 nodes / 23実行**・capped chunk 0・単一chunk最大 275,350。
  kill 表（40初手の m→r_k）は campaign record 参照。全 kill の r≠m を確認済み。

### driver bug の検出と完全再計算（本セッションの重要修正）

- 初期2実行は winner 応手列挙を root 合法手リスト（初手 m 自身を含む）から行って
  おり、r===m の偽kill（1-node・石重複）が6件発生。レビューで検出し state から
  除去、影響初手は修正 driver（**replies = root合法手 − m**）で完全再計算した。
- **決定制御**: 再計算 chunk が独立実行間で node 数まで完全一致
 （(70,50)=23,416・(90,42)=136,346・(90,70)=56,072 が各2回）。
- 旧killのうち r≠m のもの（例: 初回run m=0 の r=10）は位置が合法のため有効。

### 解釈上の注意

- bit32 の REFUTED は「深さ10以内のWIN7の否定」のみ（より深い勝ちはあり得る）。
  class 4・S2 {59,60}・二石 root {49,60}・**11x11 空盤はいずれも UNKNOWN**。
- bit7 の 400 node 集計差の留保は未解決のまま。
- chunk 法は両方向を閉じられる（bit85/bit32 REFUTED、bit7/bit25 WIN7）ことが確定。

### 反映（全て push 後読み戻し確認・1コミット1ファイル）

- 77104f79: campaign record output/class4-batch1-bit32-campaign.json
 （verdict・witness・kill表40件・driver_bug_note・決定制御・解釈ガード・未走査8件）
- 58d0746c: ledger JSON（bit32 エントリ追記・next更新: item 2 IN PROGRESS）
- e850c5f3: audit JSON session9_bit32_chunk_campaign 追記
 （初回pushは31KBファイルでtimeout・読み戻し確認後に再pushで完了）
- 本コミット: log 第10セッション

### 次回

1. heavy-pending 残り {40,80,87,34} の chunk キャンペーン（同一プロトコル・
   修正driver: replies = root合法手 − m を必ず守る）。bit40/80 は mob50、
   bit87 は mob49、bit34 は mob56。
2. WIN7 発見時は bit7/bit25 と同一の証明書プロトコル
 （kill-first抽出 → 50部分木分解検証 → union等価 → 1コミット1ファイルpush）。
3. 外部計算資源が使える場合は scripts/class4_child1_runner.ts で cap 5M-50M を投入。

## 第11セッション（2026-11-14、長期レーン）: bit40 chunkキャンペーン — 2件目のREFUTED（witness m=8・3.10M nodes・5実行）・repo反映（audit timeout教訓の再現なし）

### レジューム実行（第10セッション next 1）

heavy-pending bit=40（mob 50。v15 単体 d10 は 950k で2回 capped・判定なし）を
chunk 分解で消化した。run 予算 ~650k・chunk cap 300k・chunk 深さ 8・
reply 順 wscore 降順（fail-fast）。予算打ち切りは候補ごとの state file
 （kill 表 + done replies）に逐次 flush して厳密に再開（再開欠落ゼロ）。
**winner 応手列挙は root+m の合法手リストから**（m は occupied ので
r===m は構造的に不可能 — 第10セッションの driver bug クラスの再発防止）。

### 結果: bit40 は depth 10 で REFUTED（2件目・最速の chunk 反証）

- **witness m=8**: winner 応手 44 個すべての chunk が未capで loss=false →
  lossAt(root,10)=false。root hex 00000000020000003800010080080000
 （S6 child + bit40・7石・loser to move）。
- 総 **3,101,124 nodes / 5実行**（656,192 / 650,950 / 660,051 / 650,062 / 483,869）・
  capped chunk 0・単一chunk最大 162,444・chunk計85（kill 5 / pass 80）。
  kill 表 {0:18, 2:90, 3:85, 6:84, 7:18}（全て r≠m）。
  残り44初手は未走査のまま打ち切り（verdict に不要・記録済み）。
- bit32（15.88M/23実行）と対照的に、witness が6番目の初手で見つかり
  chunk 法として最速で閉じた。**反証コストの分散は候補間で5倍以上**
 （bit85 1.70M / bit40 3.10M / bit32 15.88M）— 予算計画は per-candidate 見積り必須。

### 検証（全て PASS）

- pilot d6 制御 5,949（全5実行の冒頭で再現・5/5 PASS）。
- **witness 完全被覆**: root+8 の合法応手 44個と done 表が完全一致（欠落0）。
- **決定制御**: fresh 再解4件が node 数まで完全一致
 （pass (8,44)=79,103・(8,104)=68,443・kill (0,18)=28,157・(2,90)=97,107）。
- root mob 50 再確認・kill 表の r≠m 全確認。

### 解釈上の注意（変更なし）

- bit40 の REFUTED は「深さ10以内のWIN7の否定」のみ（より深い勝ちはあり得る）。
  class 4・S2 {59,60}・二石 root {49,60}・**11×11 空盤はいずれも UNKNOWN**。
- bit7 の 400 node 集計差の留保は未解決のまま。

### 反映（全て push 後読み戻し確認・1コミット1ファイル・並走なし）

- 6ddbbdbb: campaign record output/class4-batch1-bit40-campaign.json
- 7835203c: ledger JSON（bit40 エントリ追記・next更新: heavy-pending {80,87,34}）
- e6bedbb8: audit JSON session10_bit40_chunk_campaign 追記
 （34KB push・今回は timeout なし）
- 本コミット: log 第11セッション

### 次回

1. heavy-pending 残り {80,87,34} の chunk キャンペーン（同一プロトコル・
   応手列挙は root+m 合法手から）。bit80 は mob50、bit87 は mob49、bit34 は mob56。
   候補ごとに /home/user/bXX/state.json で再開。
2. WIN7 発見時は bit7/bit25 と同一の証明書プロトコル
 （kill-first抽出 → 50部分木分解検証 → union等価 → 1コミット1ファイルpush）。
3. 外部計算資源が使える場合は scripts/class4_child1_runner.ts で cap 5M-50M を投入。


## 第12セッション（2026-11-14、長期レーン）: bit80 chunkキャンペーン — 3件目のREFUTED（witness m=38・6.01M nodes・10実行）・repo反映

### レジューム実行（第11セッション next 1）

heavy-pending bit=80（mob 50。v15 単体 d10 は第3セッションから 950k で3回 capped・判定なし）を
chunk 分解で消化した。run 予算 ~600k・chunk cap 650k・chunk 深さ 8・
reply 順 wscore 降順（fail-fast）。予算打ち切りは候補ごとの state file
 （kill 表 + done replies・/home/user/b80/state.json）に逐次 flush して厳密に再開
（再開欠落ゼロ）。**winner 応手列挙は root+m の合法手リストから**
（m は occupied のので r===m は構造的に不可能）。

### 結果: bit80 は depth 10 で REFUTED（3件目の chunk 反証）

- **witness m=38**: winner 応手 44 個すべての chunk が未capで loss=false →
  lossAt(root,10)=false。root hex 00000000020100003800000080080000
 （S6 child + bit80・7石・loser to move。第3セッションの memo 構造計測と同一候補）。
- 総 **6,008,832 nodes / 10実行**（617,981 / 607,268 / 639,820 / 601,406 / 615,855 /
  607,250 / 644,349 / 646,137 / 609,691 / 419,075）・capped chunk 0・
  単一chunk最大 185,781・chunk計183（kill 15 / pass 168・witness 44応手計 1,513,491 nodes）。
  kill 表 {0:81, 2:90, 3:78, 4:103, 6:18, 7:28, 8:78, 15:32, 18:6, 28:50, 32:103,
  33:67, 34:28, 36:82, 37:45}（全て r≠m）。残り34初手は未走査のまま打ち切り
（verdict に不要・記録済み）。
- witness は16番目の初手で発見。**反証コストの分散は引き続き5倍以上**
 （bit85 1.70M / bit40 3.10M / bit80 6.01M / bit32 15.88M）— per-candidate 見積り必須。

### 検証（全て PASS）

- pilot d6 制御 5,949（キャンペーン開始時と事後制御実行の2回）。
- **witness 完全被覆**: root+38 の合法応手 44個と done 表が完全一致（欠落0）。
- **決定制御**: fresh 再解5件が node 数まで完全一致
 （kill (0,81)=60,593・(15,32)=63,944・(37,45)=88,230・
  pass (38,0)=61,268・(38,44)=57,513）。
- root mob 50 再確認・kill 表の r≠m 全確認。

### 解釈上の注意（変更なし）

- bit80 の REFUTED は「深さ10以内のWIN7の否定」のみ（より深い勝ちはあり得る）。
  class 4・S2 {59,60}・二石 root {49,60}・**11×11 空盤はいずれも UNKNOWN**。
- bit7 の 400 node 集計差の留保は未解決のまま。

### 反映（全て push 後読み戻し確認・1コミット1ファイル・並走なし）

- 8703c720: campaign record output/class4-batch1-bit80-campaign.json
- bdc2ad3d: ledger JSON（bit80 エントリ追記・next更新: heavy-pending {87,34}）
- f530b06c: audit JSON session11_bit80_chunk_campaign 追記（37KB push・timeoutなし）
- 本コミット: log 第12セッション

### 次回

1. heavy-pending 残り {87,34} の chunk キャンペーン（同一プロトコル・
   応手列挙は root+m 合法手から）。bit87 は mob49（bit32 と同帯で重い可能性）、
   bit34 は mob56。候補ごとに /home/user/bXX/state.json で再開。
   bit87 は本セッションで state file を初期化済み（root hex 00000000018000003800000080080000）。
2. WIN7 発見時は bit7/bit25 と同一の証明書プロトコル
 （kill-first抽出 → 50部分木分解検証 → union等価 → 1コミット1ファイルpush）。
3. 外部計算資源が使える場合は scripts/class4_child1_runner.ts で cap 5M-50M を投入。


## 第13セッション（2026-11-14、長期レーン）: bit87 chunkキャンペーン — 4件目のREFUTED（witness m=36・6.18M nodes・10実行）・repo反映

### レジューム実行（第12セッション next 1）

heavy-pending bit=87（mob 49。v14 単体 d10 は第1セッションから 700k で capped・判定なし）を
chunk 分解で消化した。run 予算 ~590k・chunk cap 300k・chunk 深さ 8・
reply 順 wscore 降順（fail-fast）。予算打ち切りは候補ごとの state file
 （kill 表 + done replies・/home/user/b87/state.json）に逐次 flush して厳密に再開
（再開欠落ゼロ）。winner 応手列挙は root+m の合法手リストから（r===m は構造的に不可能）。
bit87 の state 初期化は第12セッション log 記載後に実際に実施（root hex 00000000018000003800000080080000）。

### 結果: bit87 は depth 10 で REFUTED（4件目の chunk 反証）

- **witness m=36**: winner 応手 43 個すべての chunk が未capで loss=false →
  lossAt(root,10)=false。root hex 00000000018000003800000080080000。
- 総 **6,177,830 nodes / 10実行**（681,914 / 749,509 / 621,891 / 630,314 / 609,968 /
  686,697 / 648,812 / 605,978 / 603,920 / 338,827）・capped chunk 0・
  単一chunk最大 213,728・chunk計123（kill 12 / pass 111・log行数はバッチ順
  13/17/15/16/12/16/12/9/6/7）。
  kill 表 {0:40, 2:81, 4:28, 7:70, 8:83, 10:67, 11:43, 15:70, 25:37, 28:50, 33:25, 34:50}
 （全て r≠m）。残り36初手は未走査のまま打ち切り（verdict に不要・記録済み）。
- witness は13番目の検討初手で発見。**mob-49 帯内でも反証コストは2.6倍開く**
 （bit32 15.88M vs bit87 6.18M）— per-candidate 見積り必須（既知の教訓を再確認）。

### 検証（全て PASS）

- pilot d6 制御 5,949（キャンペーン冒頭）。
- **witness 完全被覆**: root+36 の合法応手 43個と done 表が完全一致（欠落0）。
- root mob 49 再確認（直接列挙）。
- **決定制御（2独立実行一致）**: kill 3件 (0,40)=80,233・(10,67)=52,102・(25,37)=29,291 と
  witness pass 2件 (36,70)=11,284・(36,116)=48,463 の fresh 再解を
  2つの独立実行で実施し node 数まで完全一致。
- **プロトコル上の相違（記録）**: 本キャンペーンでは per-chunk node log を
  state に永続化していなかったため、bit80 流の「記録値との照合」が不可。
  代替として2独立実行間一致で決定論を検証した。以後のキャンペーンは
  per-chunk log の永続化を必須とする（ledger next に反映済み）。

### 解釈上の注意（変更なし）

- bit87 の REFUTED は「深さ10以内のWIN7の否定」のみ（より深い勝ちはあり得る）。
  class 4・S2 {59,60}・二石 root {49,60}・**11×11 空盤はいずれも UNKNOWN**。
- bit7 の 400 node 集計差の留保は未解決のまま。

### 反映（全て push 後読み戻し確認・1コミット1ファイル・並走なし）

- 351ab120: campaign record output/class4-batch1-bit87-campaign.json
- d61ef077: ledger JSON（bit87 エントリ追記・next更新: heavy-pending {34}）
- b5daa30d: audit JSON session13_bit87_chunk_campaign 追記
- 本コミット: log 第13セッション

### 次回

1. heavy-pending 残り {34}（mob 56・mob-56 帯最初の候補）の chunk キャンペーン。
   同一プロトコル・応手列挙は root+m 合法手から・**per-chunk node log を state に永続化**。
   候補は /home/user/b34/state.json で再開（初期化はまだ未実施）。
2. WIN7 発見時は bit7/bit25 と同一の証明書プロトコル
 （kill-first抽出 → 50部分木分解検証 → union等価 → 1コミット1ファイルpush）。
3. 外部計算資源が使える場合は scripts/class4_child1_runner.ts で cap 5M-50M を投入。

## 第14セッション（2026-11-14、長期レーン）: bit34 chunkキャンペーン — 5件目のREFUTED（witness m=45・13.67M nodes・15実行）・heavy-pending全消化・repo反映

### レジューム実行（第13セッション next 1）

heavy-pending 最後の候補 bit=34（mob 56・mob-56帯最初。150kプローブ（第3セッション）と
v15単体d10 950k（第5セッション）でいずれもcapped・判定なし）をchunk分解で消化した。
chunk深さ8・応手列挙はroot+m合法手から（r===m構造的に不可能）・
**per-chunk node logをstate fileに永続化**（第13セッションのプロトコル改善を適用）。
実行はnative Node.js（sandbox 16MiB/60s制限なし・~530k nodes/s・実行毎fresh engine）。

### 結果: bit34 は depth 10 で REFUTED（5件目のchunk反証・heavy-pending全消化）

- **witness m=45**: winner 応手 42 個すべての chunk が未capで loss=false →
  lossAt(root,10)=false。root hex 00000000020000003800000088080000
 （S6 child + bit34・7石・loser to move）。witnessは22番目の検討初手で発見。
- 総 **13,672,100 nodes / 15実行**・capped chunk 0（記録上）・単一chunk最大 341,994・
  chunk計258（kill 21 / pass 237・witness 42応手計 1,946,019 nodes）。
  kill 表 21件 {0:40, 2:88, 3:40, 4:38, 6:81, 7:83, 8:50, 10:37, 11:3, 15:80, 18:25,
  21:32, 25:50, 28:80, 32:21, 33:7, 36:8, 37:32, 38:25, 40:84, 44:104}（全てr≠m）。
  残り34初手は未走査のまま打ち切り（verdictに不要・記録済み）。
- **heavy-pending は空になった**: {7→WIN7証明書, 25→WIN7証明書, 32/40/80/87/34→REFUTED}。
  S6 child #1 の7石目sweepはWIN7証明書2件・chunk反証6件・v14 standing反証5件で、
  残りは未走査候補（progress audit 参照）。
- **heavy帯コスト分布の更新**: bit85 1.70M / bit40 3.10M / bit80 6.01M / bit87 6.18M /
  bit34 13.67M / bit32 15.88M — mob-56帯の入口は13.67Mで、per-candidate見積り必須。

### 運用上の実験事実（記録）

chunk (36,8) は300k batch capで10連続のfresh batch実行すべてcap超過
 （各300,001 nodes・実行間memo非永続のため同一cap試行の純浪費 3,000,010 nodes）。
単体fresh実行（cap 20M）では **341,994 nodesで完走・loss=true（kill）** だった。
capを20Mに上げるだけで解決し深さ梯子の再帰は不要だった。
**教訓: batch cap retryはmemo永続がない限り純浪費。cap超過chunkは単体で大cap再実行する。**
(36,8) kill記録後にbatch chunk capを1Mに引き上げたが、以後300k超のchunkは発生していない。

### 検証（全て PASS）

- pilot d6 制御 5,949（公表v15制御と完全一致）。
- **witness完全被覆**: root+45 の合法応手42個と done 表が集合として完全一致
 （プログラム検証・欠落0・全loss=false・全未cap）。
- **決定制御**: fresh再解7件が永続化済みper-chunk記録とnode数・判定・terminal範囲まで
  完全一致（kill (36,8)=341,994・(0,40)=81,839・(11,3)=42,463・(44,104)=75,723・
  witness pass (45,48)=7,528・(45,50)=25,984・(45,36)=50,890）。
  per-chunk log永続化により第13セッションで不可だった記録値照合が今回可能
 （プロトコル改善の実効性を実証）。
- root mob 56 直接列挙で再確認（56初手・21 kill + witness 1 = 22検討・34未走査）。

### 解釈上の注意（変更なし）

- bit34 の REFUTED は「深さ10以内のWIN7の否定」のみ（より深い勝ちはあり得る）。
  class 4・S2 {59,60}・二石 root {49,60}・**11×11 空盤はいずれも UNKNOWN**。
- bit7 の 400 node 集計差の留保は未解決のまま。

### 反映（全て push 後読み戻し確認・1コミット1ファイル・並走なし）

- campaign record output/class4-batch1-bit34-campaign.json
- ledger JSON（bit34 エントリ追記・next更新: heavy-pending空・未走査候補へ）
- audit JSON session14_bit34_chunk_campaign 追記（pending_incomplete 34 完了化）
- 本コミット: log 第14セッション

### 次回

1. 未走査候補（54, 88, 102, ...・mob 56-63帯）の chunk キャンペーン
 （同一プロトコル・per-chunk log永続化・per-candidate予算見積り必須・
  cap超過chunkは単体大cap再実行）。
2. WIN7 発見時は bit7/bit25 と同一の証明書プロトコル
 （kill-first抽出 → 50部分木分解検証 → union等価 → 1コミット1ファイルpush）。
3. 外部計算資源が使える場合は scripts/class4_child1_runner.ts で cap 5M-50M を投入。

## 第15セッション（2026-11-14、長期レーン）: 残全候補の一括chunk走査 — S6 child #1 の7石目sweep全66候補完了・新WIN7候補5件（bit18/67/82/117/120）・repo反映

### レジューム実行（第14セッション next 1）

bit34完了後、native Node実行の速度（~500k nodes/s・実行毎fresh engine）が
残候補の一括消化に十分であることを確認し、未走査30件 + プローブ/pending 23件
（bit3含む）の計53候補を同一プロトコル（chunk深さ8・応手はroot+m合法手から・
per-chunk logを候補毎stateに永続化・chunk cap 50M〔native〕・batch予算5-8M）で連続走査した。

### 結果: 全66候補の分類完了

- **48 REFUTED-D10 / 5 WIN7-D10（このrecord）**。WIN7-D10新候補:
  **bit18**（root 000000000200000038000000800c0000・mob 52・全52初手kill）・
  **bit67**（00000000020000083800000080080000・mob 59）・
  **bit82**（00000000020400003800000080080000・mob 53）・
  **bit117**（00200000020000003800000080080000・mob 59）・
  **bit120**（01000000020000003800000080080000・mob 62）。
- **S6 child #1 の7石目sweepは全66非退化候補で完了**:
  WIN7-D10が7件（bit7〔証明書済〕・bit25〔証明書済〕+ 新5件〔証明書未〕）・
  REFUTED-D10が59件。第4セッション以来未解決だったbit3もREFUTED確定。
- 54候補（bit34含む）合計 **455,601,226 nodes / 115実行 / 11,007 chunks**。
  最重はbit2（34.08M・mob 63）。capped chunk 0（chunk cap 50M・native）。
- 反証コストはmob 44-63帯で1.7M-34Mと20倍分散 — per-candidate見積りの教訓再確認。

### 検証（全て PASS）

- pilot d6 制御 5,949（公表v15制御）。
- **構造検査（54状態すべて）**: logにcapped行0・全killのr≠m（応手はroot+m）・
  REFUTEDはwitness chunk数==done数・WIN7はkill数==root mob。
- **決定制御**: WIN7候補5件のkill chunk 10件のfresh再解が全て永続化記録と
  node数・判定・terminal範囲まで完全一致
 （(18,0,40)=28,157・(18,2,70)=64,249・(67,0,48)=18,473・(67,2,117)=129,796・
  (82,0,92)=29,215・(82,2,50)=111,394・(117,0,25)=119,716・(117,2,40)=21,043・
  (120,2,40)=193,200・(120,3,80)=36,559）。pass chunkサンプル2件も完全一致
 （(67,21,40)=118,787・(82,33,50)=16,383）。

### 解釈上の注意（変更なし）

- WIN7-D10は「深さ10以内のWIN7」であって証明書化（抽出→独立検証）までは確定扱いにしない。
  REFUTEDは「深さ10以内のWIN7の否定」のみ。
- class 4・S2 {59,60}・二石 root {49,60}・**11×11 空盤はいずれも UNKNOWN**。
- bit7 の 400 node 集計差の留保は未解決のまま。

### 反映（全て push 後読み戻し確認・1コミット1ファイル）

- output/class4-batch1-unprobed-sweep.json（53候補の統合record・WIN7候補のkill表込み）
- ledger JSON（unprobed_sweep_session15 + WIN7候補5件のエントリ・next更新）
- audit JSON（session15_unprobed_sweep・sweep_status完了化・not_yet_searched空化）
- 本コミット: log 第15セッション

### 次回

1. **新WIN7候補5件 {18, 67, 82, 117, 120} の証明書プロトコル**
 （kill-first抽出 → 部分木分解検証 → union等価 → 1コミット1ファイルpush。
  verifierは --root <hex> で再利用可。kill表は ledger/unprobed-sweep record 参照）。
2. 全66候補分類確定を起点に、class-4 frontierの実効ワークリスト再計算
 （audit_class_frontier.py bookkeeping・S6 child #1の証明書が閉じるblocker辺の整理）。
3. 11×11 空盤は UNKNOWN のまま。

## 第16セッション（2026-11-14）: 新WIN7候補5件の証明書抽出・独立検証・main反映

### 作業

- **抽出**: repoの class4_child1_cert_extractor.ts extractBatch をkill表
 （session-15のstate.jsonの st.kill）指定で1候補1プロセス（native・CAP=1e9・
 実行毎fresh engine）で実行。5候補合計 34,496,301 nodes / 5 runs
 （bit18: 5,750,652 / bit67: 6,994,702 / bit82: 5,736,905 / bit117: 7,719,053 /
 bit120: 8,294,989）。rowsはin-processのsort-u mergeで確定。
- **独立検証**: repoの verify_bit7_win7_cert.ts（engine-free・cache-free・Bareiss det4）を
 使用。ローカルのnode CLI実行には先頭に `import * as fs from 'node:fs'` を追加したのみ
 （`require('fs')` が同ファイル内の require(cond, reason) assert helperと衝突するため。
 検証ロジックは無改変。upstream修正は推奨のみ記録）。
 全候補で root checks PASS（石数7・敵mobility一致・4点共円なし）＋
 全sub-root（loserの全初期応手）分解検証 PASS。
- **union等価**: 抽出rowsと消費winner状態集合の双方向diff 0。

### 成果物（全てmain反映・push後rawでmd5再確認）

| bit | root hex | rows | bytes | md5 |
|-----|----------|------|-------|-----|
| 18 | 000000000200000038000000800c0000 | 43,550 | 1,571,258 | 11a0f14f761f71c4d77fd6e618dee336 |
| 67 | 00000000020000083800000080080000 | 57,896 | 2,088,010 | d3aa2871e08afdf48d82b94ad3c0abb5 |
| 82 | 00000000020400003800000080080000 | 48,352 | 1,743,255 | ac5200a83c0342d284b5d026d7ebbf62 |
| 117 | 00200000020000003800000080080000 | 61,952 | 2,230,811 | 3119ae37fd843267a81c78cde40a4446 |
| 120 | 01000000020000003800000080080000 | 62,336 | 2,244,853 | bb2b8da776ca4d8b16dc5121a072d0cf |

- 証明書5件: `output/class4-batch1-certificates/n11_s7_<root_hex>.cert`
 （bit7/bit25の命名規約・ヘッダー2行＋sort済みrows）
- 検証記録: `output/class4-batch1-win7-certificates-20261114.json`
- ledger JSON（5件のcertificate完了化 + win7_certificates_session16 + next更新）
- audit JSON（session16_win7_certificates追記）
- 本コミット: log 第16セッション

### 反映時の技術的事実（備忘）

- 証明書2件（bit117: 2.23MB・bit120: 2.24MB）はpushツールの16MiB記録制限を超えるため、
 pack-delta（hex行前方一致差分をnibble境界でbyte packing）+base64化した転送表
 （~0.61/0.66MB）からsandbox内でblock単位に復号してpushする方式で反映。
 復号後の内容はfnv-1a checksum・行数・バイト数で検証し、push後はrawでmd5一致を確認。
- この制限事象は一時的な作業環境の問題であり、repo側の証明書・検証内容には影響しない。

### 結果

- S6 child #1 の7石目sweepは**深さ10以内で全66候補確定**:
 証明書付きWIN7 7件（bit7, 25, 18, 67, 82, 117, 120）+ REFUTED 59件。

### 解釈上の注意（変更なし）

- WIN7証明書は「7石rootから深さ10以内の勝ち」の証明。それ以上深い構造は決定していない。
 REFUTEDは「深さ10以内のWIN7の否定」のみ。
- class 4・S2 {59,60}・二石root {49,60}・**11×11 空盤はいずれも UNKNOWN**。
- bit7 の 400 node 集計差の留保は未解決のまま。

### 次回

1. **class-4 frontierの再計算**（7証明書が閉じるblocker辺の整理・
 audit_class_frontier.py bookkeeping）。
2. frontier結果をS2 {59,60}のblocker構造へ接続。より深いオブジェクトは UNKNOWN 維持。
3. 11×11 空盤は UNKNOWN のまま。

## 第17セッション（2026-11-14）: class-4 frontier再計算 — 7証明書がmanifest内S6軌道19件を解決・レーン目標S5の残り43→35軌道

### 作業

- repoの `audit_class_frontier.py` を、新規の検証receiptsファイル
 `output/class4-batch1-certificates-verified.json`（bit7/25/18/67/82/117/120の7root・
  session 7/9/16のverify結果）を追加して再実行。スナップショットassertは
 事前batch1基準に固定されているため設計通り無効化（ローカル実行のみ
 `if False: assert` 化・repoファイルは無変更）。
- 入力は全てmain公開ファイル（win7-reuse-hits・class2系verified JSON 12件・
  ms5 S6 manifest・remaining/incidences CSV）。

### 結果（全数値はbookkeeping・新たな探索判定ではない）

- **7証明書のcovers和集合は43 S6軌道**（基準比で40件が新規）。うち**manifest内19件が新規解決**:
 solved&manifest 638 → **657**。unique remaining S6 7208 → 7189・
 残コスト 565,500 → 564,070。open class必要S6 5425 → 5406（424,077）。
- **class-4レーン目標S5 `00000000020000003800000080000000` の残りが43 → 35 S6軌道**
 （コスト3391 → 2756）。自身のS6 child #1 sweepが全証明済みで、
 covers経由で自S5の残8軌道を閉じた。
- class-2最良blockerは不変（`...3802000008000000`・32軌道・2206）。

### 反映（push後読み戻し確認・1コミット1ファイル・並走なし）

- `output/class4-batch1-certificates-verified.json`（7root receipts）
- `output/class4-batch1-frontier-update-20261114.json`（再計算record・covers分析・frontier差分）
- `output/class-frontier-s5-ranking-after-batch1.csv`
- `output/class-frontier-top-candidates-s6-after-batch1.csv`
- ledger JSON（frontier_session17 + next更新）
- audit JSON（session17_frontier_update追記）
- 本コミット: log 第17セッション

### 解釈上の注意（変更なし）

- 本セッションは既存receiptsのbookkeepingのみで、新たな探索判定は無い。
- class 4・S2 {59,60}・二石root {49,60}・**11×11 空盤はいずれも UNKNOWN**。
- bit7 の 400 node 集計差の留保は未解決のまま。

### 次回

1. **class-4レーン継続**: 目標S5（残35 S6軌道・2756）の次の子を
 `class-frontier-top-candidates-s6-after-batch1.csv` の順でsweep・証明書化。
2. frontierの更新は証明書push毎に再計算（assert基準の更新方法は要検討）。
3. 11×11 空盤は UNKNOWN のまま。


## 第18セッション（2026-11-14、長期レーン）: S6 child #2 sweep完結 — WIN7証明書3件（bit50/77/91）抽出・独立検証・main反映

### レジューム実行（第17セッション next 1）

class-4レーン目標S5 `00000000020000003800000080000000` の次の S6 child として
最安軌道 **child #2 `000000000200000038000000a0000000`（コスト67）** を選び、
67個の非退化7石目候補を chunk 法（深さ8 chunk・応手は root+m 合法手から・
fresh engine per batch・native Node ~470k nodes/s・chunk cap 50M）で全走査した。

### 結果: child #2 は全67候補で判定確定 — WIN7-D10 3件 + REFUTED-D10 64件

- **WIN7-D10**: bit50（root `000000000200000038040000a0000000`, mob 50, 2,107,194 nodes）・
  bit77（`000000000200200038000000a0000000`, mob 58, 11,058,432 nodes）・
