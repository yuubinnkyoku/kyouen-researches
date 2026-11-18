# 2026-11-18 N11 全174 open S5 parentの最小証明coverコスト表（head-1476状態）

## 成果

head-1410 worklist（6,438行）のfold-chain適用後（head-1476・閉鎖66行・STERILE 91 incidence/35行除外）のopen非STERILE 6,337行を対象に、**全174 open S5 parent それぞれについて「自前行の候補rootで残り行全体を被覆する最小本数」を厳密決定**し、witness coverつきで出版した。coordinatorがparent選定するときの直接的な指標（何本の証明書があればそのparentの残行を全部被覆できるか）。

- script phase 1: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/enumerate_global_candidate_roots_20261118.py`（全行D4候補列挙・各行候補数は出版cost列とassert一致・約40秒・中間JSONL 20.5MBは出版せずscriptで再生成可能）
- script phase 2: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/parent_cover_cost_table_20261118.py`
- output: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json`
- **531 checks all PASS**。二重実行 byte-identical。

## 方法

各parent P: 対象行 = Pを5-subset D4正準親に持つopen非STERILE行。候補root = 対象行のD4正準7石拡張（1石追加・det4全triple非退化、出版own_candidates cost列と全行一致）。下界 = ceil(r/maxspan)（被覆発生数の初等的な計数）。**witnessが下界サイズで提示できれば最小値は厳密確定**。maxspan ≤ 2の場合、witnessはpair rootのマッチング+高々1本のsingletonに帰着し、決定的greedy matching（60 restart・seed固定）で全parent発見できた。witnessは機械検証（対象行を過不足なく被覆・root重複なし・各生成対でcanon(row|1<<bit)==rootを確認済み。出版JSONにはroot hexのみ同梱し、全詳細はpublished script再実行（約45秒）で再現）。

## 主要な新所見

1. **全174 parentの最小coverコストが厳密確定**（exact 174/174・cost分布 6〜45）。170 parentがmaxspan=2、4 parentはr=0（残行なし）。**どのparentでも1個のrootが3行以上を被覆することはない**（全parentでヒストグラムがspan 1と2のみ）。
2. **コスト最小は既知のclass-2 top parent `00000000000000403800000008000000`（11行・cost 6）**で全174中唯一の6。2番目は **`00000000000000821082000000000000`（18行・cost 9・no_sterile/class1）**、3番目が **`00000000000000003800000008002000`（23行・cost 12・partial_sterile/class2）** で、class-2 runner-up `00000000000000003800000009000000`（29行・cost 15）より安い。**最小coverコスト順位は行数順位・class-2 ranking順位と一致しない**（coordinator選定に使える新しい測度）。
3. **r=0 parentが4つ**: censusのall_remaining_sterile 3 parentに加え、**partial_sterile `00000000000000801202000040000000`（K0865 effective worklist第1位）はfold chain（76c/76d/77e fold）で非STERILE 3行がすべて閉鎖済みとなり、head-1476時点で残行はSTERILE 2行のみ**。K0863によりこの2行はD10 receiptで永久に被覆不能なので、このparentの自前行証明作業は残余ゼロ（parent閉鎖の主張ではなく簿記的事実）。
4. parent別witness coverは全174 parent分を同梱（計6,070 root・hexのみ、生成対はscript再実行で再現）。witnessは「このparentを閉じる最安の証明書セット」の具体候補（各rootが実際にWIN7-D10等のreceiptとして妥当になることを前提とした計画上の計数）。

## クロスチェック

- census（`9c251da3`）の174 parent全てで remaining_s6_orbits == |join(P)|・remaining_s7_edge_cost == Σ cost（STERILE行込みの全remaining行で一致・remaining_row_refs総計12,274一致）。注: censusのremainingはSTERILE行を含む（rank-1 parent 5 = 非STERILE 3 + STERILE 2）。
- top parent: 11行/806候補/757 root/ヒストグラム708+49/最小6（出版censusと全一致）。runner-up: 29行/2,203/1,854/1,505+349/最小15（29−14マッチング+1 singleton、下界ceil(29/2)=15と一致）。
- 全parentの対象行の和集合 == open非STERILE全6,337行（12,052 parent-incidence）。

## 解釈上の注意

最小coverコストは「選んだrootすべてが証明書として成立するなら、parentの残行をすべて被覆するのに必要な最小本数」。rootの妥当性（WIN/REFUTED）は一切主張しない。被覆できないroot（REFUTED等）が出れば必要本数は増える（top parentのelimination分析がその場合の構造を与える）。REFUTED-D10・STERILE は LOSS 証明ではない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて UNKNOWN。
