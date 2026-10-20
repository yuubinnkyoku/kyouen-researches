# 2026-10-20 添付成果の統合監査

基準main: `2535cf99c9d7ea2322279e0d862e895468a9d91a`。
元の作業フォルダに未コミット変更があるため、別のdetached checkoutで統合した。

## 取込と証拠境界

2つの原ZIPを `research/archive/bundles-20261020/` に保存しCRCとSHA-256を確認した。非衝突候補・n11代表証明・競合の片方等、578ファイルを新規配置した。`__pycache__` と `.pyc` は展開先の正本へ取り込まない。さらに、repo相対配置になっていなかった幾何Grundy5の証明・検証器を専用experimentへ取り出した。

既存パスは無条件に上書きしない。3つの既存候補差分および原資料との相違はmain版を維持し、取込元はZIPに保持した。競合では三行q5のhistogram拡張版、三列初出のmultiplicity拡張版、残余三辺の初期版を専用パスに配置し、別版もZIPへ保持した。これらの計算全体の再監査は未完了である。全件の処置は `import-manifest.json` に記録した。`kept-main` は、先に新規採用した別版を維持する場合も含む。

同一命題の草案は証拠を一項目に統合した。二辺公式、sunflower、傾きの篩上界、四辺上界、幾何Grundy5、座標交換で一致する3×4 q6の別版は新しい別命題に数えない。仮番号は再採番し、既存mainの番号は変更しない。元資料中の仮番号は歴史的記述であり、現在のK番号の解釈にはmanifestの対応を用いる。

新規の一般命題48件は `needs-review` として受け入れた。元資料のproved/computedやsolution metadataは報告内容であって、この統合で監査完了を意味しない。本文でも明示した。既存K0350の21候補十分という定理は維持し、19・17候補への改善資料は未採用の監査候補として同じKに追加した。

## 今回実行した検証

- n11四つのS7 WIN: `bash research/experiments/n11-s7-four-win-terminal-20261020/reproduce.sh` が終了コード0。C++証明書再生成、収録証明書とのバイト比較、独立Pythonの全合法子・2,670終局葉・569,993状態、改変負例4種類を確認。K0485に採用した。実行記録は `n11-four-win-validation.txt`。
- n11圧縮証明: `bash research/experiments/n11-s8-compact385-pruned1946-20261020/reproduce.sh` が終了コード0。1,946局面のC++直接判定、Pythonの1,561 WIN証人と385 LOSS葉、二成分のPython/C++完全整数gap検査、215個の個別必要性検査を確認。K0486に採用した。実行記録は `n11-compact-validation.txt`。counterfactual coverは実ゲーム証明書ではなく、215個の必要性を任意の代替排除集合に対する最小性へ拡張しない。
- n11逆向き伝播: `verify_and_lift.py --archive <保存ZIP内の1946版> --terminal-only` が終了コード0。385終局LOSS、35 S8 LOSS、246 S7 LOSSでPASS。旧cacheとの差分比較は省略し、新規238件という値を独立再確認したとは扱わない。実行記録は `n11-lift-validation.txt`。
- 幾何Grundy5の `verify.py`: 330四点組、1,635安全局面、空盤値5の検算PASS。
- `game-structure/scripts/verify_two_edges.py`: 14頂点以下1,105型の占有subset mex検算PASS。
- `fixed-width/scripts/verify_capacity_parity_counts_20261016.py`: 75組の独立全subset検算PASS。
- 新規Python 171ファイルのAST構文検査PASS（上記の追加幾何資料は別途収録）。構文検査は意味的な正しさの保証ではない。

その他の添付検証器・全称証明・過去の大規模列挙は今回再実行していない。未知盤の長時間探索やworkflowの自動化は追加していない。

## 規約検査

`uv sync --locked`、knowledge check（480項目・エラー0・警告0）、33単体テスト、build、再生成差分検査（差分0）を実行し、すべて成功した。単体テストの最終実行は248.933秒でOK（`knowledge-unit-tests.txt`）。旧移行試験の「全項目にneeds-reviewがない」という前提は、監査済みB系列の移行保証に限定した。新規未監査項目をschemaの正式statusで受け入れつつ、旧項目の保証を保持するためである。

同一命題のK草案を統合した後、root READMEの生成領域に残る古いリンクがbuildの事前検査を止める不具合を確認した。`include_generated=False` ではREADMEの生成領域だけを事前リンク検査から除き、生成後は通常検査で全リンクを確認するよう修正した。人が書いたREADMEリンクの欠落を引き続き拒否することも既存のlayout回帰に追加した。

11×11空盤は引き続きUNKNOWN。既知S6の訂正はK0485、圧縮終局証明はK0486を現在の知識とし、古いREADMEやlogのUNKNOWN記述を現在の判定として使わない。
