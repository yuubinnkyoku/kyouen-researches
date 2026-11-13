
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
