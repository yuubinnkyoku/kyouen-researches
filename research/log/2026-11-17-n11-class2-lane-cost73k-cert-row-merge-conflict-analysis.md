# 2026-11-17：cost73k証明書行集合のmerge衝突解析（conflict 0の直接実証・共有構造の定量・優先事項(3)への基盤）

## 開始時点

開始時のmainは `8e1fdd6f`（並走のK0903 z=6 y=15）を起点に確認し、cost73k関連のknowledge・experiments・logを読んだ。前項でcost73kメモ容量測定のcross-lane合意照合（`6e5c341e`）を出版済み。レジュームの(iii)「worker間メモmergeの実測」に着手するにあたり、その前提となる「position-keyed mergeの衝突安全性」を、**出版済み証明書bytesだけから直接計算できる**ことに着目した。探索を実行せず、行集合の集合演算だけで完結する軽い解析であり、優先事項(3)「workerごとのcacheを安全にmergeし、WIN/LOSS conflictを即検出する」の第一歩にあたる。

## 解析手順

入力はすべて公開pinから取得した（manifest `class2-lane-cost73k-win7-certificates-20261117.json` blob `0892aed07d187ae2fb3b4b90a21c7adbc1002b62`・pin commit `a3c27e9f`、証明書41ファイル〔19 split pair + 3 whole〕、結合md5をmanifestと22/22照合）。各行は `position_hex value` 形式で、valueはその局面の決定的な勝ち手witnessである。

22 rootの行集合をbit昇順に1つずつmergeし、(1) 同一positionが既出のときのvalue不一致をconflictとして即検出、(2) positionの共有次数分布、(3) 231 bitペアの共有行数、(4) band-wide逐次順（bit昇順）での各rootの先行被覆率、を計算した。

## 結果

| 項目 | 値 |
|---|---:|
| 総行数（22証明書合計） | 966,535 |
| distinct positions | 682,861（=出版済みunion測定と一致） |
| merge hits（既出positionの再訪問行） | 283,674（29.4%） |
| **conflict（同一position・value不一致）** | **0** |

- **conflict 0の直接実証**: 283,674行の共有positionすべてで、異なるrootの証明書が同じvalue（witness）を記録している。抽出器のwitness選択はpositionのみに依存して決定的（root非依存）であることを22 root横断で実証しており、**worker間のposition-keyed cacheをmergeしてもWIN/LOSS conflictは生じない**という共有cache設計の前提が、出版bytesから直接確定した。即時conflict検出付きmerge（`pos_val[pos] != val` の即assert）は何も検出するものがなかった。
- **共有次数分布**: 1 root専用 463,259（67.8%）/ 2 root 168,739 / 3 root 39,870 / 4 root 9,001 / 5 root 1,782 / 6 root 197 / 7 root 12 / **8 root 1**。最大で8つの証明書に現れるpositionが存在する。
- **ペア共有**: 231ペア中180ペアが少なくとも1行を共有。上位は (15,39)=5,970・(41,73)=5,907・(58,73)=5,900・(0,58)=5,645。bit 73は複数の上位ペアに現れるハブroot。
- **逐次被覆率（band-wide順）**: bit 0/7は先行共有0%。bit 11から11.4%で始まり、bit 58で41.1%、後半bitは39〜47%に達する（bit 112=47.55%、bit 117=46.75%）。この数列は、(a) band-wide共有にcross-root再利用の利得がある理由、(b) 出版済みms23/ms24 band実行で後半bit（89/94/112/117）が汚染比トップだった理由（ルックアップの多くが先行root挿入のpositionに当たる）、を定量的に説明する。

## 解釈

本解析は**出版済み証明書bytesの行集合解析**であり、探索を1ノードも実行していない。新しいverdictはなく、manifestの行は1行も閉じておらず、証明書bytesは1バイトも変わっていない。得られたのは、共有cache/merge設計（優先事項(3)）に対する3つの定量的基盤: (1) merge衝突安全性の実証（conflict 0）、(2) 共有構造の次数・ペア分布（cache hit率の予測材料・coordinatorのroot順序設計に直結するハブroot bit 73等の特定）、(3) 逐次被覆率（band-wide実行の利得・汚染の定量的説明）。

次のステップとして、実worker 2分割のmerge実行（mergeテーブルをseedとした再抽出コストと、merge時のload factor実測）が挙げられるが、本解析で「merge後テーブルは682,861エントリ」が確定したため、MS>=1<<20（load 65%以下）で段階的にseedする設計判断の材料は揃った。

## 出版物

- `scripts/analyze_cost73k_cert_row_merge_conflicts_20261117.py`: 解析スクリプト。manifest blob pin検証・41ファイルmd5照合・merge衝突即検出・次数分布・ペア共有・逐次被覆を計算しJSON出力。デフォルトでraw CDN pinから取得、ローカル証明書ディレクトリ指定も可（ネットワーク不要）。conflict検出時はexit 1。
- `output/class2-lane-cost73k-cert-row-merge-conflict-analysis-20261117.json`: 解析結果（conflicts 0・全数値入り）。

## 解釈と次の作業

WIN7-D10は個別7石rootの深さ10以内の先手勝ちであり、REFUTED-D10はLOSS証明ではない。73k receipt foldは76c/66i/66j/69j/71e/72d/73i folds完了まで並走管理のまま着手禁止。73i証明書は並走がclaim（`batches_run: 0`）のままsweep中であり、出版後に72d/73jパターンのBigInt bytes再検証が本レーンの次候補のまま変わらない。標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4は引き続きUNKNOWN。
