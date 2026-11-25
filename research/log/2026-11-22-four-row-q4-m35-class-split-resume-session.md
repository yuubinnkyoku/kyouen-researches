# (4,4) m=35 class-split — 2026-11-22 resume セッションログ (単一オーナー宣言)

[four-row-q4-m35-class-split-20261115](../experiments/four-row-q4-m35-class-split-20261115/)
レーンの 2026-11-22 単一オーナー resume セッションの実行記録。
宣言: [2026-11-22-four-row-q4-m35-class-split-resume-single-owner-note](2026-11-22-four-row-q4-m35-class-split-resume-single-owner-note.md)
(宣言時 HEAD `d73bb0b8`・宣言コミット `4fcee8eb`)。
**判定は不推移 (UNSAT 0・SAT 0)。不在/存在の主張は一切ない** (`M_{4,4} ∈ [35,237]` 不変)。

## まとめ

- 対照込み 15 piece を cap 200-240s で実行し全て INDET (honest negative)。
- pipeline 較正: 対照 CNF 再生成が出版対照ログの DIMACS header と完全一致
  (vars=392,614 / clauses=1,300,317, cnf_md5 `c26434a356033a5a7dd4884da4c92208`)。
  親キー CNF の md5 はリセット越しに 3 回同一 (決定性)。
- `sat4.js` (second-stone 位置分割 `--x2`) を m23 レーンから導入
  (repo fetch で文字列一致確認) し、k=2 バケット `c1k2p0` の最初の 2 sub-key を実行。
- 運用較正: 2 コア・RAM ~2GB・bash 300s 呼び出し上限の環境では親 piece は
  収束しない可能性が高い (下記観察)。成果は較正データ・ツール群・honest negative
  として本コミットで出版し、決着は次回以降へ移送する。

## タイムライン (2026-11-22 UTC)

- 05:02 kit から work へ復元 (md5 全一致確認)・single-owner note push (4fcee8eb)。
- 05:03-05:05 noexec 事故の発見と除去 (rc=126 擬似 INDET 24 行)。CNF md5 は較正に流用。
- 05:07 対照 CNF 再生成較正 (上記 header 完全一致)。
- 05:08 対照 cap 220s 実行: INDET・872,303 conflicts (records 1 行目 05:08:57Z)。
- 05:14-05:34 親 `c1k2p0..p7` を cap 240s で 2 並列 2 wave で実行、全 INDET
  (conflicts 18,272〜438,368)。
- 05:46 x2 サブ `c1k2p0x21`/`x22` cap 200s: INDET (788,535 / 919,077 conflicts)。
- 05:55-05:59 category sampling `c01`/`c1k0`/`c0123`/`c1k1p0` cap 200s: 全 INDET。
- 06:0x 本コミットで出版 (README addendum・records 15 行・sat4.js・sweep35x2.sh・
  sample35.sh・本ログ)。

## records (output/records.jsonl・15 行)

| # | key | class | extra | cap(s) | conflicts | result |
|---|-----|-------|-------|--------|-----------|--------|
| 1 | `ctrl_4x34_c1k2p7` | 1 | `--krow=1:2 --minpos=7` | 220 | 872,303 | INDET |
| 2 | `c1k2p0` | 1 | `--krow=1:2 --minpos=0` | 240 | 438,368 | INDET |
| 3 | `c1k2p2` | 1 | `--krow=1:2 --minpos=2` | 240 | 294,654 | INDET |
| 4 | `c1k2p1` | 1 | `--krow=1:2 --minpos=1` | 240 | 83,542 | INDET |
| 5 | `c1k2p3` | 1 | `--krow=1:2 --minpos=3` | 240 | 18,418 | INDET |
| 6 | `c1k2p5` | 1 | `--krow=1:2 --minpos=5` | 240 | 18,345 | INDET |
| 7 | `c1k2p4` | 1 | `--krow=1:2 --minpos=4` | 240 | 60,341 | INDET |
| 8 | `c1k2p6` | 1 | `--krow=1:2 --minpos=6` | 240 | 18,310 | INDET |
| 9 | `c1k2p7` | 1 | `--krow=1:2 --minpos=7` | 240 | 18,272 | INDET |
| 10 | `c1k2p0x21` | 1 | `--krow=1:2 --minpos=0` | 200 | 788,535 | INDET |
| 11 | `c1k2p0x22` | 1 | `--krow=1:2 --minpos=0` | 200 | 919,077 | INDET |
| 12 | `c01` | 0,1 | `` | 200 | 82,234 | INDET |
| 13 | `c1k0` | 1 | `--krow=1:0` | 200 | 868,532 | INDET |
| 14 | `c0123` | 0,1,2,3 | `` | 200 | 33,861 | INDET |
| 15 | `c1k1p0` | 1 | `--krow=1:1 --minpos=0` | 200 | 843,903 | INDET |

(cf: `c1k0` 868,532 / 200s = 4,343/s、`c1k2p3` 18,418 / 240s = 76.7/s、
`c0123` 33,861 / 200s = 169/s、ctrl 872,303 / 220s = 3,965/s)

## 観察・分析 (ヒューリスティック運用較正・全称主張なし)

1. 同一 cap でも conflicts は 18k〜438k と約 24 倍差。`c1k2p3/p5/p6/p7` は
   240s で 18k-19k conflicts 台で停滞 (conflict production が skeletons/hunting に
   入らず burn するタイプ)。cap 到達 piece の conflicts は壁時計打ち切りで
   bit-exact ではない (README 既記事項)。
2. second stone をピンした x2 サブでも ~800-900k conflicts/200s で未収束。
   (4,5) m23 レーンの同種 sub-piece はこの環境の cap で UNSAT 収束させており、
   対比から (4,4) m=35 の piece は 1-2 桁難しいと読める。
3. 帰結: 実行環境の制約 (300s/呼び出し・2 コア・~2GB) では親 piece の決着は
   期待できない。決着には (a) 呼び出しあたり 800s+ の budget が取れる環境、
   (b) x3 以降の分割や multi クラス向け row-split によるさらなる分解が必要。
   ただし (b) の妥当性評価 (sub-piece が 200-240s 級で収束するか) は
   まず x2 の残り B=3..34 で確かめるのが最短と判断する。

## 次回レジュームgets

- INDET 行 15 のうち親 12 キーは done_key で skip される。retry 時は該当行を
  records.jsonl から除去してから (2026-11-15 truncation 除去と同規約)。
- `c1k2p0` の x2 展開は B ∈ {1..34} の 34 sub-key のうち B=1,2 のみ記録済み。
  B=3..34 (32 sub-key) が次の最短確定経路候補。
- multi クラス (`c01`, `c0123`) 向け row-split 分割は未実装 (`sat4.js` は
  単一 deficient row・k>=2 のみ)。
- 実行規約: work は /home/user/work (exec 可) で、knowledge マウントは退避専用。
  bash 1 呼び出しの合計ソルブ < 270s。CNF gen は逐次。
- K 番号不使用 (実験 1 回 1 K 規約: 判定不推移の中間進行は item 化しない)。
