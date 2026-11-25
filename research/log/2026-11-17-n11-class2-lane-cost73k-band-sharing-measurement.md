# 2026-11-17：cost73k bandの状態共有・クロスband対称cache価値・confirmation再走査コスト・WIN転送certificate再利用の測定

## 開始時点

開始時のmainは `63f5287e0d0958c9ad6633d625d90af8d49c042a`。`AGENTS.md`、`research/knowledge/README.md`、K0023、K0863、K0865、および並走レーンの最新刊（cost73k証明書22本・claim v3・BigInt再検証22/22 PASS、cost76c bit61証明書とhead1473へのfold、cost66i bit19 BigInt再検証）を確認した。fold chain（76c→66i→66j→69j→71e→72d→73i→73j）と73i証明書抽出は並走レーン管轄のまま本レーンは着手しない。前回の本レーン測定（v1: commit `9f2422d3`、D4 addendum: commit `2700ed3c`）は3 band（73j/72d/71e）までだったため、出版済みのcost73k band（22 WIN7-D10証明書・966,535行・公開bytes 34,933,538）を加えた4 band測定を本レーンの作業とした。

## 測定内容（script `measure_cost73k_band_sharing_and_reuse_20261117.py`・入力128ファイルすべてgit blob sha + bytes pin・pin commit `63f5287e`）

1. **band内状態共有（exact + D4正準形）**: 4 bandそれぞれについて、証明書行状態の重複を測定。v1互換（行出現ベース）と厳密な証明書単位の両方で計数し、73j/72d/71eの再計算はv1/addendum出版値と全フィールド一致をassert（回帰ゲート）。
2. **band間共有**: 4 bandの全6対（exact・canon両方）+ 3-way/4-way交差 + 石数ヒストグラム。旧3対は出版値と一致をassert。
3. **73k sweepのconfirmation再走査コスト**: 出版concurrent-record（並走の第3独立実行とper-bit 73/73一致）のper-bit nodesから、confirmation 7 bit [14,23,26,34,53,55,107] の再走査コストを集計。WIN転送3 bitとREFUTED転送4 bitに分解。record総nodes 128,861,941・WIN 25/REFUTED 48/capped 0はraw sweep audit（並走出版）と突合assert。
4. **WIN転送rootのcanon等価の独立再導出**: 73k bit14 ↔ 73j bit110、73k bit55 ↔ 69j bit110はpublished manifestのd4_canon_rootと照合、73k bit26 ↔ 73i bit110は両側計算で等価を確認（73i証明書bandはまだmainに無く、bit26の証明書被覆は73i抽出待ち）。73k bit53 ↔ 66i bit10のraw同一性も再確認。D4 canon関数は5 manifest（73k 22 + 73j 16 + 72d 11 + 71e 13 + 69j 6 = 68件）のpublished d4_canon_rootを全件再現してから測定。

## 測定結果（すべて有限測定・2回実行で出力byte同一・md5 `a4e70e6659c802e0965433f74348b896`）

- **73k band内**: 22証明書・966,535行・distinct状態 682,861・**band内共有32.159%**（4 band最高・73j 26.00%・72d 20.15%・71e 22.52%を上回る）・重複行29.350%・1状態の最大共有証明書数8（histogram 1:463,259 / 2:168,739 / 3:39,870 / 4:9,001 / 5:1,782 / 6:197 / 7:12 / 8:1）。行出現ベースと証明書単位の計数は73kでは完全一致。band内canonマージは0.00%（他3 bandと同様、回転コピーのband内共存なし）。
- **band間exact**: 73kは71e/72d/73jのいずれとも**exact共有0**（71eと同様。「同一parentの構造近接childでもexactキーでは共有しない」ことを3例目として確定）。
- **band間canon**: **73j∩73k = 27,009**（73jの4.929%・73kの3.955%・計測史上最大のband間canon共有）・71e∩73k = 15,869・72d∩73k = 11,765・3-way (71e,72d,73k) = 135・4-way = 9。**73kのcanon状態の7.786%（53,165状態）が旧3 bandのunionで事前被覆**されていた（石数は12-16に集中）。
- **confirmation再走査コスト（73k sweep）**: 13,619,457 nodes = **sweepの10.569%**（WIN転送bits 14/26/55: 9,086,455 nodes = 7.051%、REFUTED転送bits 23/34/53/107: 4,533,002 nodes = 3.518%）。系統の累積とともに単調増加（73i 2.13% → 73j 6.97% → 73k 10.57%）。転送信頼型verdict cacheの直接削減ポテンシャルとして読める。
- **WIN転送certificate再利用**: 25 WIN bitのうち22本が新規抽出、bit14（73j bit110）とbit55（69j bit110）は出版済みbyte検証済み証明書でcanon等価被覆（**再利用により回避された抽出97,460行・23,788,624 nodes**）、bit26（73i bit110）はsweep verdictのみで証明書被覆は73i band抽出待ち（claim v3の「covered by the published cost73i bit 110 certificates」は2026-11-17時点のmainでは証明書としては未着地であることを記録）。

## 解釈上の制限

出版済み証明書bytesとsweep記録のみの効率・簿記測定であり、新しい探索verdictは1つも作っていない。WIN7-D10証明書は個別7石rootのdepth-10内先手勝ちのみを証明し、REFUTED-D10はLOSS証明ではない。本測定はmanifest行もS5 parentも1つも閉じない。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべて引き続きUNKNOWN。

## 出版物

- script: `scripts/measure_cost73k_band_sharing_and_reuse_20261117.py`（入力pin表埋込・自己完結・stdlibのみ）
- output: `output/class2-lane-cost73k-band-sharing-and-reuse-measurement-20261117.json`（33,646 bytes・md5 `a4e70e6659c802e0965433f74348b896`・2回実行byte同一）
- 本log

## 次の作業候補

1. 73k band内の**cross-root共有memo抽出**のnode削減実測（band内共有32.16%・最大8証明書共有に対し、published抽出はrootごとに別プロセスでmemo非共有。63dのper-process memo 33%削減先例。測定専用の実験として実装・実行し、証明書出版はしない）。
2. 73i証明書bandが出版された時点での同band測定の追走と、73k bit26の証明書被覆の確定。
3. fold chain完了後（head再基準化後）のcensus v8再選定における、本測定のcanon cache被覆率の反映検討。
