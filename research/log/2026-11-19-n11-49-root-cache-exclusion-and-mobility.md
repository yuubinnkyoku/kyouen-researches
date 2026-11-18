# 2026-11-19 n11: 49-root cache nonmembership and exact next-move census

## 基準

49-root監査の開始時mainは `317f6af8c9810941bda38b5cf355a8f27ce3aa65`。その後、並行するn11 cost-16 laneがrank-30生存曲線を追加した（main `69b4e02966d9cf6b9bd07fc7680b2eb165557247`）。これは別の31行親局面のcover-plan計数で、今回固定した49-root witness/K0863 indexを変更しない。root `AGENTS.md`、knowledge README、K0863/K0865/K0868、5親97行の49-root witnessと直近logを確認した。

## 1. 8,964 verdict indexへの完全な非所属監査

K0863 theorem-applicability scanは、109 claim・77 sweep・29 auditから133個の6石childを構成し、1,064 raw batch filesをすべてchildへ解決（unresolved 0）。このchild universe上のengine indexは8,964 verdict（REFUTED-D10 8,305・WIN7-D10 659・capped 0）、同位置衝突0。さらに未判定候補へのD4転送は115件すべてREFUTED-D10で、WIN転送0。

7石root Xがこのindexのどれかに現れるなら、必ずある6石child Cとbit bについて X ≡D4 C∪{b} である。従ってCはXから石を1個取り除いた7通りのいずれかのD4 orbitに属する。49本すべてについて全7削除子を133 childの全D4 orbitと照合した。

- 48本: 7削除子のD4 orbitが133 child universeに一つもない。
- 残る1本 `00000000000000909002200080000000`: child `00000000000000801222000000800000` とbit 74で一致するが、このchildはengine verdict 0件、transferはREFUTED bits 55/65/109のみ、legal 69 = open 66 + transfer 3。bit 74はopen。
- 結果: 49本すべて、公開済み8,964 engine verdictと115 transferのどちらにも既知判定なし。

これは1,064 rawファイルをこの回に再走査した結果ではない。K0863 scanが全raw/aggregateをchild単位に集約した133 child universeと、scan生成器のchild構成を固定blobで確認し、候補側の全削除子から非所属を証明したもの。候補rootの完全なcache hit joinを避ける構造的な方法である。indexの外にある未公開ローカルcacheまでは主張しない。

## 2. 49 rootの合法次手数

K0868の規約と同じ一般化円判定（共線退化も含む）を7石rootの次手へ適用した。各候補点pについて、既存7石の全3つ組との `det4(a,b,c,p) != 0` を検査。det4は行 `[x²+y²,x,y,1]` の4×4整数行列式。

BigInt Bareiss消去とBigInt Leibniz展開の独立2方式で、root安全性の35四点組×49本と、候補次手の153,988四点判定を照合し、全て一致した。

- 合法な次手数: **47〜77**
- 平均: **60.918367**
- 中央値: **62**
- 最小: 47（root `00000000000000821082000010800000`、2行を被覆）
- 次点: 49（root `00000000000000805212000001000000`）
- 49本すべてD4 orbit size 8（非自明な対称性なし）。合法な次局面も全て相異なるD4類。

この数は初手の構造的分岐数であって、DFPN node数・実行時間・証明費用ではない。47手rootを最初の小規模probe候補に置く根拠にはなるが、探索順を確定するには実測が必要。

## 3. 再現資料

- 再現スクリプト: `../experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/scripts/audit_49_root_cache_exclusion_and_mobility_20261119.mjs`（blob `9b5b255f4702315f0d7d1db12fec79aafd4b2bdc`）
- 結果JSON: `../experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-cache-exclusion-mobility-20261119.json`（blob `466fb0ff04cd5241945e06eefa255c75a4609372`）
- 入力はK0863 scan、49-root witness、scan生成器、K0868をGit blob SHAで固定。

この回は固定入力をV8上で独立再計算した。公開Nodeスクリプトはrepo checkout上では起動していない。push後のknowledge integrity workflowによる検査結果は別途確認する。

## 4. 次の判断

49本に既存cache hitはないため、全本を無差別に起動しない。47手rootを先行probe候補とし、coordinatorが実測node/timeと共有cache効率を比較して選んだ少数だけを探索する。WIN7-D10が得られた場合のみ独立検証してreceiptへ進める。

新しいWIN/LOSS verdict・certificate・receiptは今回作っていない。REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root `{49,60}`/`{59,60}`、S2 `{59,60}`、class 1/2/4は **UNKNOWN** のまま。
