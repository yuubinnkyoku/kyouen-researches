# 2026-11-16 — REMO 3枝: cap≤12サイズ境界（K0875）とK0874状態行列の独立検証

## Context

K0862定理H（cap≤10・r=3・非坍縮22キー完全境界）が「枝サイズ≥11は未走査」を限界として残していた。並走レーンがK0874（52キー×r=2..8状態行列）を出版した直後でもあり、(a) cap≤12へのサイズ境界拡張、(b) K0874の独立検証、を両方このセッションで実行した。r=9フルスイープは並走レーン担当（着手せず）。

## What was done

- 08:15に実行環境リセットが発生し作業ファイル・実行中プロセスが消滅。全成果物（engineスライス・出版定数抽出・両ドライバ）をmainから再取得・再構築して続行した。教訓: 長いsleepを含むbash呼び出しを避け短いpoll呼び出しに分ける。ドラフトはcurrent-chat以下にも二重保存。
- cap≤12境界検証器 `verify_remo_k_branch_cap12_boundary.py` を作成（K0862エンジンverbatim・stdlibのみ・決定的・main二重実行バイト同一・出版定数の機械抽出埋込み・コミット済みJSONとのバイト一致検証を組み込み）。
- K0874独立検証器 `verify_remo_failure_family_matrix_independent.py` を作成（同じエンジン・独立に書いたドライバ・K0874のaudit JSONから機械抽出した期待定数: 44キーmixedリスト・K0866出版r=7分割6キー・K0869出版r=8分割10キー・K0867出版4/10計数8キー・K0864出版r=3分割・15族活動窓）。
- 並走レーンが「52キー×r=2..8状態行列」をK0874として出版済みだったため、行列側は新規K項を作らず独立検証experimentとして出版する方針に変更（重複出版の回避）。cap≤12境界は新規のままK0875とする。

## Results

- **定理H12（K0875・新規）**: cap≤12（47,595プロファイル・1,365キー・予算スキップ0）でも非坍縮キーは定理Hの22個ちょうどで新規0。サイズ11枝363キー・12枝364キー（和650）は全て坍縮。2剰余キー890個のうち非坍縮は同じ22個。22キーの分割・witness・決定生存者P_1・非決定集合⊆{{1,2},{0,1,2}}はcap≤10と完全不変。補題FL違反0・Δ=0全定理D値・F′閉形式1,155対完全一致・定理D表84エントリ一致・E′セルアンカー44組一致。
- **K0874独立検証**: 52キー×r=2..8=364セル（9,744判定）を独立ドライバで完全再計算し、全18機械チェックが出版アンカーと一致（W4 mixedリスト・W5定理I r=2・W6定理G′・W7出版分割・W8剰余レンズ・W9活動窓15族・W10 4/10族全行）。K0874の結論に修正は不要。

## Consequences

- 「r=3でサイズ8が非坍縮に必要」がサイズ≤12域で確定し、K0862の未走査限界が1つ閉じた。残る未走査: 枝サイズ≥13、**r≥4×サイズ11,12の組合せセル**、r≥9。
- K0874は第二の独立したドライバによる全セル再計算で検証済みとなった（同じエンジンだが定数は出版JSONから機械抽出）。
- 次の候補: (i) r=4×cap≤12スイープ（r=4でサイズ11,12を含むキーのmixed有無。r=4はcap≤10では12キーmixed）、(ii) 枝サイズ≥13の剰余レンジ順序付け探索（2剰余キーの見積り）、(iii) K0872剰余署名の一般必要条件の証明の試み。

## Artifacts

- research/experiments/remo-k-branch-cap12-boundary-20261116/{verify_remo_k_branch_cap12_boundary.py, report.md, output/remo_k_branch_cap12_boundary_audit.json}
- research/experiments/remo-failure-family-matrix-independent-20261116/{verify_remo_failure_family_matrix_independent.py, report.md, output/remo_failure_family_matrix_independent_audit.json}
- research/knowledge/items/K0875-remo-k-branch-cap12-boundary.md
- research/knowledge/README.md（K0875行を追加）
- .github/workflows/refresh-knowledge-generated.yml（監査step 2件・trigger comment 2行を追加）

## Interpretation guard

定理H12はr=3・サイズ≤12の有限完全計算であり、r≥4・サイズ≥13への外挿でもない特徴づけでもない。行列の独立検証は新規の数学的主張を含まない。「一様非決定」は決定性レベルの話で、可能生存者集合はr・atom配分に依存してよい。本項の有限観察を全称定理へ昇格させない。
