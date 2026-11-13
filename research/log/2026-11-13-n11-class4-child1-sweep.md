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
