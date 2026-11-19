# n11 残余72行候補供給 K1075 独立第二検証（2026-11-20）

K1075の「残余72行・fresh-safe 36-root witness」について、候補供給生成器をimportせず、公開済み正本だけを入力とする独立幾何検証を実施した。**44/44 gate PASS**。検証器はD4座標作用を再実装し、安全性は4×4行列のBareiss法で厳密整数判定した。

## 入力正本のSHA-256 pin

| 入力 | SHA-256 |
|---|---|
| K1075候補供給正本 | `49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa` |
| resolve7正本 | `207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f` |
| fold9正本 | `24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2` |
| fold10正本 | `bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a` |
| 第17証明書38-gate検証正本 | `c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc` |
| 39-live掃引正本 | `22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc` |

## 独立に再導出した結果

- fold9後74行・fold10後72行・resolve7の72行・K1075の72行リストが完全一致。fold9の4行、fold10のtarget 2行とtarget外extra 1行の区別も一致。
- 72行から各空点を1つ加えD4正準化して、add-one-stone universe **7,448 root**を独立再構築。
- 7,448 rootすべての35個の4点部分集合を4×4 Bareiss determinantで検査。safe **4,577**・unsafe **2,871**。被覆数の分布は1行被覆6,616 root・2行被覆832 rootで、3行以上被覆するrootは0。
- K1075のphase-2集計（fresh-safe 4,109・fresh-unsafe 2,871・judged REFUTED 468・judged WIN 0）と独立safe/unsafe総数は算術的に完全一致。すなわち、この72-root universe内の468 judged rootは個数上すべてsafe側に属する。
- K1075の36 fresh witness rootを全件再検査。全rootが7石・D4正準形・Bareiss安全、各rootの削除被覆は記録された2行と完全一致。36本は72行を重複なくちょうど1回被覆する。
- よってpair matchingの上界36（72頂点を2行ずつ覆う）に対し36本の完全matchingが存在し、**matching size 36は最適**。witness被覆の重複所属は0。
- resolve7のretire後38 root assignmentも再検査。**34 root×2行 + 4 root×1行 = 72行**で、全rootのD4削除被覆が記録と一致し、重複・欠落0。
- 72行のfresh-safe demandは正本記録上すべて正で、最少52・最多76、合計4,678 incidence。K1075のpair edges 536・singleton 72行・multi-cover 0・stranded 0・greedy 40本などの主要欄も整合を確認した。

## 実行・決定論

- 実行環境: Proxmox `pve-hp-aio:204`、Debian 13、1 vCPU / 2 GiB、Python 3.13.5。
- K1075生成器はimportせず、stdlibのみの独立検証器。
- 44/44 gate PASS。2回の別プロセス実行で出力byte-identical。3回目の計測実行は37.313秒、出力は同一。
- 検証器SHA-256: `74fd3275baffb576dee2959678b85a655136dd4595fa2d39bf980c7b3a515972`
- 結果JSON SHA-256: `5511222b5385a2e57845b944e3607d2ac406203e4da827fb4e62b8e362b5a46d`（10,233 bytes）。

## 検証境界

これは**公開記録に対する幾何・個数の独立検証**である。K0863の1,279-file corpusを再読してphase-2 verdict joinを再構築したものではない。したがって、fresh-safe 4,109のroot identity集合とpair edges 536の全辺集合を独立に列挙したわけではなく、これらはK1075正本の集計値としてpinし、独立再導出したsafe/unsafe universe総数・witness geometry・row demandとの整合を確認した。WIN/REFUTEDの判定そのものも再実行していない。

36-root depth-10 sweepは別のsingle-owner宣言（`2026-11-20-n11-residual72-36witness-sweep-single-owner-note.md`）に属するため、本検証では探索を起動していない。新しいWIN/LOSS verdict、certificate、receipt、foldは発生していない。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はUNKNOWNのまま。** REFUTED-D10はLOSS証明ではなく、matching・被覆は行の簿記であり、ゲームの勝敗を示さない。
