# 2026-11-19 N11 cost-16 rank-38 preread の独立bit-mask検証

## 開始時点

開始時の最新mainは 48c109440e1d0bebe1b621a84fd7080be5657a46。AGENTS.md、research/knowledge/README.md、K0863/K0865/K0868、直近の49-root frontier記録、cost-16 rank-36〜38 preread記録、docs/NORMAL_DFPN.md、DFPN coordinator/S5 cacheの既存報告を確認した。

K0865の49候補rootは、公開済み8,964 engine verdictと115件のD4 verdict転送に未該当で、WIN7-D10証明書ではない。最小候補 00000000000000821082000010800000 は合法次手47だが、これは分岐数であってDFPN費用ではない。49-rootの10石frontier共有も幾何学的なD4重複であり、実探索の表参照率ではない。

## 実施内容

公開済みrank-38 prereadを、元のpreread実装をimportしない第二系統で検証した。

- 新規検証器: research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/verify_cost16_k38_preread_independent_20261119.py
- 検証器Git blob SHA-1: 585147f0b973fafa819cb83ab1c04e0fd7811fa8
- 固定入力:
  - phase-B aggregate: 31bdefdb2e2cc90b706cbb8090e98eb5eece4d87
  - k36 preread: 760aa396361cc7d2ea8bc371f4dd673d962f07fe
  - k37 preread: b98ed685e772eacbd28dc3100e9813e81c27040a
  - k38 preread: 3fa8297990d8e9880f386a0cfa075e3a95f226fd
- 全入力をGit blob SHA-1で固定し、Python標準JSONの任意精度整数でmembership/A/Bを保持した。
- 主分類器は各rootの被覆行をbit mask化し、全pairwise intersectionとtriplewise intersectionから disjoint / b_only / zero を再分類する。prereadのdict累積・Counter系とは異なる経路である。
- 別の行数カウンタ実装との照合は、rank36〜38の全triple、三rankの新quint・新tripleを合わせた **202,547組**。不一致0。

## 結果

**48 / 48 checks PASS**

rank36・rank37の元出版prereadと、k38 prereadに埋め込まれた両回帰欄、rank38新規欄を照合した。root、行、prior hit、正確なmembership/A/B、新pair/triple/quad/quint census、二重行histogram、quintの5つの4-subset profile、disjoint quadのunion sizeと累積数、full triple/quint censusを再導出して一致した。

rank38の主要値:

- root: 00000008800000003800000008100000
- rows: [19, 29]
- membership: **119,940,649,042,609,991**
- A/B: **91,876,760,891,572,775 / 28,063,888,151,037,216**
- new pair: 13 shared / 24 disjoint
- new triple: 420 / 113 / 133
- new quad: 2,519 / 5,094 / 157
- new quint: 2,868 / 63,177 / 0
- full C(38,3): 5,178 / 1,533 / 1,725
- full C(38,5): 23,024 / 478,918 / 0
- cumulative disjoint quads: 1,677

行29はrank37までの単一sharer（index 19）から新たに参加し、triple層8件・quad層11件で二重行化するが、quint層には現れないことも再確認した。

C(38,6)=2,760,681件はbit-mask分類器で全件再分類し、すべてzeroだった。rank36・rank37の6-subsetはこのrank38集合の部分集合なので、両rankのsextet全zeroも含意される。元のrank36/rank37出版欄とk38内の回帰欄の双方について、件数と分類を照合した。

k38 prereadのrank36/rank37回帰欄は、元のrank36/rank37 prereadより一部のdisjoint quad詳細（新規件数・union size・累積値）を省いたcompact schemaである。初回の検証器は元欄と同じ詳細があると仮定して失敗したため、検証器を修正した。最終版では、詳細値は元の出版prereadに対して再導出・照合し、compact回帰欄では収録されているcensus/histogramを照合する。これはデータ不一致ではなくschema差である。

## 再現環境

Proxmox pve:199 の専用runnerで実行した。

- Debian 13 / Python 3.13.5
- 1 vCPU / 4 GiB RAM
- root filesystemは3.9 GiB中3.7 GiB使用・空き37 MiB、100%
- /dev/shm は5.8 GiB。入力取得・検証器・出力をtmpfs上に置き、root filesystemへの大きな書き込みを避けた。
- py_compile PASS
- 48 checks / 0 failures
- fresh process 2回の出力はbyte-identical
- 実行時間は12.85秒と12.91秒
- 出力23,834 bytes、SHA-256 e21d5b19eef4745b1bc8c79fe4c2704ddb2733a4daf88ce276f1185303a930f4

検証器・結果JSONはmainへ直接反映した。branch/PRは作成していない。全体のknowledge unittest/buildは実行していない。runnerのroot filesystemは満杯で、既存 /opt/kyouen-checkout はmainより古い 46f7f73f18d0b673f513c5e4a263e4dad24e596c かつ未コミット変更があるため、そのcheckoutを現行mainの検査環境として使うことは避けた。knowledge item自体は変更していない。

## 証拠の境界と次の判断

この検証は、固定aggregateに記録された50 rootの rows_covered から組合せ分類を独立再導出したもの。円・共線の幾何判定をもう一度独立実装したものではなく、DFPN探索でもない。rank38の組合せ数・分類が再現されたことだけを確定する。

49候補rootの実探索はまだ開始していない。専用runnerにC++ compilerがなく、root filesystemも満杯のため、今回DFPNを起動しなかった。次の実作業は、ビルド可能な専用環境を確保して、最小47手rootの小規模probeを行い、実測node/timeと共有表のhit率を取ること。起動しただけの長時間探索は成果に数えない。

**標準11×11空盤、二石root {49,60} / {59,60}、S2 {59,60}、class 1/2/4はすべてUNKNOWNのまま。** この検証は勝敗verdict、WIN7-D10証明書、receipt、manifest閉鎖を一つも生成していない。
